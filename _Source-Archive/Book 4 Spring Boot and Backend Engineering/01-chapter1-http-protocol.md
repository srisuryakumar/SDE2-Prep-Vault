# Chapter 1: The HTTP Protocol

Before any Spring annotation makes sense, you need to understand the protocol it's secretly managing for you. Every `@GetMapping`, every `ResponseEntity`, every `@RequestHeader` is Spring giving you a friendlier face on top of plain-text rules that have barely changed since the 1990s. This chapter has no Spring code in it on purpose — everything here is what's actually flowing over the wire, regardless of what framework or language is on either end of it.

## 1.1 The anatomy of a request

An HTTP request is genuinely just text. If you opened a raw TCP socket to a server and typed the right characters by hand, you'd get a real response back. Here's what a request to our (eventual) Order Management API looks like at the wire level, when a client asks to place an order:

```
POST /v1/orders HTTP/1.1
Host: api.ordermanagement.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqYW5lIn0.s1gn4tur3
Accept: application/json
Content-Length: 87

{
  "items": [
    { "productId": 42, "quantity": 2 },
    { "productId": 7,  "quantity": 1 }
  ]
}
```

Four parts, always in this order:

**The request line** — `POST /v1/orders HTTP/1.1`. This is the method, the path (never the full URL — the host is a separate header, which is what lets one server handle multiple domains), and the protocol version.

**Headers** — key-value metadata about the request, one per line, terminated by an empty line. Headers tell the server things it needs to know *before* it reads the body: what format the body is in, who's making the request, how long the body is, what response formats are acceptable.

**An empty line** — this is what separates headers from the body. It's not optional and it's not cosmetic; it's how the receiving end knows where metadata stops and payload starts.

**The body** (optional) — the actual payload. `GET` and `DELETE` requests conventionally don't have one; `POST`, `PUT`, and `PATCH` usually do.

A response has the identical shape, just with a status line instead of a request line:

```
HTTP/1.1 201 Created
Content-Type: application/json
Location: /v1/orders/9001

{
  "id": 9001,
  "status": "PENDING",
  "totalAmount": 145.50,
  "items": [
    { "productId": 42, "quantity": 2, "unitPrice": 50.00 },
    { "productId": 7,  "quantity": 1, "unitPrice": 45.50 }
  ]
}
```

Everything Spring does — deserializing `@RequestBody`, populating `@RequestHeader`, setting a status code via `ResponseEntity` — is just programmatic construction or parsing of this exact text format. Keep that picture in your head; it demystifies a lot of "magic" later.

## 1.2 HTTP methods

HTTP methods aren't just convention — two specific properties, **safety** and **idempotency**, are part of the actual specification and have real consequences for how browsers, proxies, load balancers, and retry logic are allowed to treat a request.

A method is **safe** if it's not supposed to change server state at all — the client is only asking for information. A method is **idempotent** if making the same request N times produces the same server state as making it once (the *response* can still differ — e.g., a `DELETE` might return `200` the first time and `404` the second — but the underlying resource ends up in the same place).

| Method | Safe? | Idempotent? | Typical use in our API |
|---|---|---|---|
| `GET` | Yes | Yes | `GET /v1/orders/9001` — fetch an order |
| `POST` | No | **No** | `POST /v1/orders` — create a new order |
| `PUT` | No | Yes | `PUT /v1/products/42` — replace a product entirely |
| `PATCH` | No | Not guaranteed | `PATCH /v1/orders/9001` — change just the status |
| `DELETE` | No | Yes | `DELETE /v1/products/42` — remove a product |

A few of these deserve unpacking, because the "why" is more useful than the "what":

**`GET` is safe and idempotent.** A client, a corporate proxy, or a browser's "back" button can re-issue a `GET` freely, cache it, or prefetch it, because by definition it can't change anything. This is why putting side effects behind a `GET` endpoint (a classic mistake: `GET /v1/orders/9001/cancel`) is a real bug, not just a style nitpick — a crawler, a browser prefetch, or an automatic retry could cancel orders nobody asked to cancel.

**`PUT` is idempotent by definition, and that definition is "replace."** `PUT /v1/products/42` with a full product body means "this is now the entire state of product 42" — sending it once or five times in a row leaves product 42 in the same final state. That's *why* it's idempotent: it's not "increment this," it's "set this." Contrast that with `POST /v1/orders` — sending the same order payload twice creates two separate orders with two different IDs, which is precisely why `POST` is **not** idempotent, and precisely why Chapter 2 introduces idempotency keys to fix that for cases where it matters.

**`PATCH` is idempotency-agnostic.** `PATCH` means "apply this partial change," and whether that's idempotent depends entirely on what the change *is*. `PATCH { "status": "CANCELLED" }` is idempotent — setting status to `CANCELLED` twice is the same as once. `PATCH { "quantityAvailable": "+5" }` (a relative delta) is not — applying it twice doubles the effect. Spring doesn't enforce either behavior for you; idempotency under `PATCH` is something you design into your endpoint, not something the method gives you for free.

**`DELETE` is idempotent even though the second call usually 404s.** The HTTP spec is talking about the *resource's state*, not the response code. After the first `DELETE /v1/products/42`, the product is gone. After the second, it's still gone — same end state, even though the second response is a `404` instead of a `204`. Many engineers get tripped up by this distinction in interviews, so it's worth saying explicitly: idempotent doesn't mean "returns the same status code every time."

### Why idempotency matters for distributed systems

This isn't academic. In a distributed system, networks fail in the worst possible place: *after* the server processed the request but *before* the client got the response. From the client's point of view, a timed-out request is indistinguishable from a request that never arrived. The only safe move is often to retry — and whether that retry is safe depends entirely on idempotency.

Picture a payment service calling `POST /v1/orders` to charge a customer, the request succeeds, the order is created, but the response is lost to a network blip. The client's retry logic, seeing no response, retries the exact same `POST`. If the endpoint isn't designed with this in mind, the customer is now charged twice and has two orders. This single failure mode — "the request succeeded but I don't know it" — is one of the most common sources of duplicate-charge and duplicate-order bugs in real systems, and it's *why* idempotency keys exist (Chapter 2) and why load balancers and HTTP clients will automatically retry `GET`/`PUT`/`DELETE` on connection failure but are deliberately conservative about auto-retrying `POST`.

> **Interview Question — SDE-2:** "Why is `POST` not idempotent, and how would you make an endpoint that creates a resource safe to retry?"
>
> **Answer:** `POST` creates a new resource on every call by design — there's no natural key in the request that the server can use to recognize "I've already done this." The fix isn't to change the method; it's to give the client a way to supply that natural key. The client generates a UUID once per logical operation, sends it as a header (commonly `X-Idempotency-Key` or `Idempotency-Key`), and the server persists a record of "this key produced this result" the first time it sees it. If the same key arrives again — because of a client retry after a timeout — the server returns the cached result instead of creating a second resource. This turns a non-idempotent method into a practically idempotent operation from the caller's perspective, without violating what `POST` means semantically. We implement exactly this pattern for order creation in Chapter 4.

## 1.3 Status codes: what each one is actually for

Status codes are grouped by their first digit — 2xx is success, 3xx is redirection, 4xx is "you (the client) did something the server won't honor," 5xx is "the server failed, and it wasn't your fault." Picking the right one is a design decision, not decoration — clients (including your own frontend, and any SDK generated from your OpenAPI spec) branch their logic on these codes.

| Code | Name | When to use it |
|---|---|---|
| `200` | OK | A successful `GET`, or a successful `PUT`/`PATCH` that returns the updated resource. |
| `201` | Created | A successful `POST` that created a new resource. Should be paired with a `Location` header pointing at the new resource. |
| `202` | Accepted | The request was valid and *will* be processed, but not synchronously — e.g., `POST /v1/orders/9001/cancel` if cancellation triggers an async workflow (notifying a warehouse, reversing a payment) rather than completing instantly. |
| `204` | No Content | The request succeeded and there is deliberately nothing to return — the canonical response for `DELETE`. |
| `301` | Moved Permanently | The resource now lives at a different URL, permanently — clients and search engines should update their bookmarks/links. Rare in JSON APIs; common for whole-domain migrations. |
| `302` | Found | A *temporary* redirect — don't update bookmarks, the original URL is still valid for next time. Common after a successful login form submission in browser-based flows. |
| `304` | Not Modified | Sent in response to a conditional `GET` (one with an `If-None-Match` or `If-Modified-Since` header) when the resource hasn't changed — tells the client "use the copy you already cached," saving the bandwidth of resending the body. |
| `400` | Bad Request | The request is malformed at the syntax level — invalid JSON, missing required structural pieces. In Chapter 4 we use this specifically for unparseable bodies. |
| `401` | Unauthorized | Confusingly named — it actually means **unauthenticated**. You haven't proven who you are (missing or invalid credentials), so the server doesn't know who's asking. |
| `403` | Forbidden | The server knows exactly who you are, and the answer is no. You're authenticated but not authorized for this specific action — e.g., a `CUSTOMER` trying to delete a product. |
| `404` | Not Found | The resource doesn't exist — or, in security-conscious APIs, the server is deliberately pretending it doesn't, to avoid confirming the existence of resources to unauthorized users. |
| `409` | Conflict | The request is well-formed and the client is authorized, but it can't be applied because of the *current state* of the resource — two requests racing for the last unit of inventory, both losing the optimistic-lock check, get a `409`. This is the code our `@Version` handling returns in Chapter 4. |
| `422` | Unprocessable Entity | The request is syntactically valid (parseable JSON) but semantically invalid — a quantity of `-5`, a missing required field, an email that fails the format check. This is the code Bean Validation failures return in our API. |
| `429` | Too Many Requests | Rate limiting. Should be paired with a `Retry-After` header telling the client how long to back off. |
| `500` | Internal Server Error | The server hit a bug or unhandled exception. This should never leak a stack trace to the client — see the global exception handler in Chapter 4. |
| `502` | Bad Gateway | A proxy or load balancer in front of your app got an invalid response from the upstream server — often means your app crashed or isn't listening at all. |
| `503` | Service Unavailable | The server is deliberately not handling requests right now — overloaded, or intentionally down for maintenance. Should be paired with `Retry-After` when possible. |
| `504` | Gateway Timeout | A proxy gave up waiting for the upstream server to respond — the app is up but too slow, as opposed to `502` where it's down or returning garbage. |

The distinction that trips people up most in interviews is **400 vs. 401 vs. 403 vs. 422**, and **400 vs. 422** specifically, so it's worth stating the dividing line plainly: *can the server even parse the request?* If no — garbled JSON, wrong `Content-Type` — that's `400`. If yes, but the values inside violate business or validation rules — quantity must be positive, email must be a valid format — that's `422`. Many APIs collapse this distinction and use `400` for everything; this book is deliberately precise about it because the distinction is genuinely useful for clients (a `400` usually means "fix your client code," a `422` usually means "fix the data you sent, your client code is fine") and because interviewers specifically probe for whether you understand the difference.

> **Interview Question — SDE-2:** "A client sends a request to update an order's status to `CANCELLED`, but the order was already `SHIPPED`. What status code do you return, and why not `400`?"
>
> **Answer:** `409 Conflict`. The request itself is perfectly valid — well-formed JSON, a real status value, sent by an authorized user. The problem is purely that the *current state* of the resource doesn't allow this transition. `400` would incorrectly suggest the client sent something malformed; `422` would suggest the data itself is invalid in isolation (it isn't — `CANCELLED` is a perfectly valid order status, just not a valid status *from here*). `409` is the code that specifically communicates "this is a state-transition problem, not a data problem" — and a well-built client can use that distinction to decide whether retrying makes sense (it doesn't, here) versus whether to surface a generic error.

## 1.4 Headers you'll actually use

Headers are how a request or response carries metadata that the body shouldn't have to. A handful show up constantly enough to be worth knowing cold:

**`Content-Type`** — describes the format of the *body that follows it*. `application/json` is what we use throughout this book; `application/x-www-form-urlencoded` and `multipart/form-data` show up for traditional HTML forms and file uploads, respectively. This is also the header Spring's `HttpMessageConverter` mechanism inspects to decide *how* to deserialize an incoming `@RequestBody` — a request claiming `Content-Type: application/json` but containing XML will fail to parse, by design.

**`Authorization`** — carries credentials. The format is `<scheme> <credentials>` — `Bearer <token>` for JWTs and OAuth access tokens (what we use from Chapter 5 onward), `Basic <base64-encoded-user:pass>` for HTTP Basic Auth. Note that `Basic` is base64-*encoded*, not encrypted — it's only safe over TLS.

**`Accept`** — the inverse of `Content-Type`: tells the server what format(s) the *client* is willing to receive in the response, in preference order, optionally with weights (`Accept: application/json;q=0.9, application/xml;q=0.5`). A server that can produce multiple formats uses this to decide what to send back — this is also the mechanism behind header-based API versioning, covered in Chapter 2.

**`Cache-Control`** — governs caching behavior for both directions. `Cache-Control: no-store` on a response means "don't cache this at all" (appropriate for anything containing a JWT or personal data); `Cache-Control: max-age=3600` means "this is good for an hour without revalidating." For a typical order or user-data endpoint in our API, the right value is almost always `no-store` — you don't want a shared proxy caching one user's order history and serving it to another.

**`X-Request-ID`** — not part of the official HTTP spec, but a near-universal convention. A unique ID generated for a single request, propagated through every service that touches it, and included in every log line that request produces. When something goes wrong in production and a user reports "my order failed at 3:14pm," this is the field that lets you find the *exact* log lines across potentially a dozen microservices, instead of grepping by timestamp and hoping. Worth generating server-side if the client doesn't supply one, and worth echoing back in the response so a client-side error report can include it.

**`Location`** — sent on a `201 Created` response, pointing at the URL of the resource that was just created. This is what lets a client immediately `GET` the new order without you having to return its entire representation in the creation response (though, as you'll see in Chapter 4, returning the full body *and* the `Location` header is the more common and more convenient pattern in practice).

> **Interview Question — SDE-2:** "What's the difference between `Content-Type` and `Accept`, and could a single request need both?"
>
> **Answer:** `Content-Type` describes the request's own body — what format you're sending. `Accept` describes what formats you're willing to receive back. They're independent and a request can absolutely need both: a client could send a `PATCH` with `Content-Type: application/json` (the patch document is JSON) while setting `Accept: application/xml` (but please respond in XML). They only happen to look similar because they reuse the same MIME-type vocabulary — they govern opposite directions of the same exchange.

## 1.5 HTTP/1.1 vs. HTTP/2

HTTP/1.1, standardized in 1997, has one structural limitation that shaped a decade of web-performance workarounds: on a single TCP connection, requests are processed strictly one-at-a-time — issue a request, wait for the full response, *then* issue the next one (technically "pipelining" exists in the spec but is barely supported in practice because of how it interacts with proxies). Browsers worked around this by opening multiple parallel TCP connections to the same host (historically 6 per origin) — which is *why* techniques like spriting images together or splitting assets across subdomains ("domain sharding") were ever considered good practice. They were performance hacks around a protocol limitation, not good engineering in isolation.

HTTP/2 (2015) fixes the root problem instead of working around it:

**Multiplexing** — many logical request/response exchanges share a *single* TCP connection simultaneously, interleaved as small frames, instead of queueing behind each other. One slow request no longer blocks others behind it on the same connection (a problem nicknamed "head-of-line blocking," which HTTP/2 solves at the HTTP layer — though it can still occur at the TCP layer, which is part of why HTTP/3 moves to UDP-based QUIC).

**Header compression (HPACK)** — HTTP/1.1 resends full, verbose headers (cookies, user-agent strings, auth tokens) on every single request, uncompressed. HPACK maintains a compression context between client and server so repeated header fields are encoded as small references instead of being retransmitted in full every time — a meaningful bandwidth saving when a client is making many small requests with large, mostly-unchanging header sets.

**Server push** — originally, HTTP/2 let a server proactively send resources to the client before they were even requested (e.g., push the CSS file along with the HTML that references it, anticipating the request). In practice, this turned out to interact badly with browser caching — servers would often push resources the client already had cached, wasting bandwidth — and the benefit rarely materialized in the real world. Major browsers have since removed support for it; it's worth knowing it existed and why it didn't survive, but you shouldn't expect to use it.

None of this is something you configure directly in a Spring Boot application most of the time — it's typically handled by the embedded server (Tomcat, by default) or, more commonly in production, by a reverse proxy or load balancer in front of your app (nginx, an AWS ALB, etc.) that terminates HTTP/2 from the internet and may speak plain HTTP/1.1 to your application internally. Knowing *why* it exists, though, is exactly the kind of "how does this work" depth that separates a surface-level answer from an SDE-2-level one.

> **Interview Question — SDE-2:** "If HTTP/2 multiplexes requests over one connection, why do people still talk about connection pooling on the server side?"
>
> **Answer:** Multiplexing solves the *client-to-edge* connection count problem — a browser no longer needs six TCP connections to fetch a page's assets. It does nothing for what happens *behind* your server. Your Spring Boot application still needs a pool of database connections (HikariCP, by default) because the database speaks its own wire protocol over its own TCP connections, entirely separate from however the HTTP request arrived. A single HTTP/2 connection carrying a thousand multiplexed requests can still exhaust your database connection pool if each request needs a DB round-trip and the pool is sized too small — the two are unrelated layers of the stack.

## 1.6 HTTPS and TLS, at the depth an interview actually probes

HTTPS is HTTP, unmodified, sent over a TLS-encrypted connection instead of a plain TCP one. The protocol you've spent this whole chapter on doesn't change at all — TLS just wraps it. Two things are worth understanding at a real level: how a client decides to trust a server, and what happens in the handshake before any HTTP bytes are exchanged.

**The certificate chain.** A server presents a certificate claiming "I am api.ordermanagement.com," signed by some Certificate Authority (CA). The client doesn't trust that signature blindly — it walks a chain: the server's certificate is signed by an *intermediate* CA's certificate, and that intermediate's certificate is signed by a *root* CA's certificate, and the root CA's certificate is one of a small, fixed set that ships pre-trusted in the client's OS or browser. If every link in that chain validates — each signature checks out against the next certificate up, and the root is one the client already trusts — the client trusts the server's identity. This is also why certificate expiry is a real operational hazard: if any certificate in that chain expires, the entire chain of trust breaks, and every client immediately starts rejecting the connection.

**The handshake (TLS 1.3, the modern default).** At a level worth being able to explain out loud: the client sends a `ClientHello` proposing supported cipher suites and a key share; the server responds with its certificate (for the chain above), its own key share, and a `Finished` message; both sides now independently derive the same symmetric session key using Diffie-Hellman key exchange (the actual math is out of scope for an SDE-2 interview, but the concept — both sides can compute the same shared secret without ever transmitting the secret itself — is worth being able to say); from that point, all traffic, including the rest of the HTTP request/response cycle, is encrypted with that symmetric key. TLS 1.3 specifically reduced this to effectively one round trip before encrypted application data can flow, down from two in TLS 1.2 — a meaningful latency win that's part of why TLS 1.3 adoption mattered for web performance, not just security.

The reason the underlying asymmetric (public/private key) cryptography from the certificate isn't used for the *whole* conversation is performance: asymmetric encryption is computationally expensive relative to symmetric encryption. So asymmetric crypto is used briefly, just to safely establish a shared symmetric key, and then the fast symmetric cipher does the heavy lifting for the actual data transfer. That handoff — asymmetric for the handshake, symmetric for the bulk transfer — is the single fact about TLS most worth retaining, because it explains *why* the protocol is shaped the way it is rather than just *what* it does.

> **Interview Question — SDE-2:** "Why does TLS use both asymmetric and symmetric encryption instead of just one?"
>
> **Answer:** Asymmetric (public-key) cryptography solves a problem symmetric encryption can't: establishing a shared secret between two parties who've never communicated before, over a channel an attacker can observe. But it's slow — orders of magnitude slower than symmetric ciphers for the same amount of data. So TLS uses asymmetric crypto for exactly one job, the handshake: safely agreeing on a symmetric session key. Once both sides have that key, the connection switches to a symmetric cipher (like AES) for the actual HTTP traffic, because symmetric encryption is fast enough to not bottleneck a high-throughput connection. It's a deliberate trade-off: pay the expensive operation once, per connection, to unlock cheap operations for everything after.

---

With the protocol itself covered, Chapter 2 moves up a level: given that you *can* send any method, any header, any status code — what conventions make an HTTP API actually pleasant and predictable to consume? That's REST, and it's a design discipline, not a protocol feature.
