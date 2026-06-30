# Chapter 2: REST API Design Principles

REST isn't a protocol, a library, or something you "turn on." It's a set of architectural constraints Roy Fielding described in his year-2000 dissertation, and in practice it's mostly a design discipline for how you organize URLs, methods, and payloads so that an API is predictable to anyone who's used a different REST API before. None of what's in this chapter is enforced by Spring Boot — you *can* build a Spring Boot application that violates every principle here, and it'll run fine. The principles exist because violating them makes an API harder to use, harder to evolve, and harder to reason about, not because the framework will stop you.

## 2.1 Resource naming: nouns, not verbs

The core idea of REST is that a URL identifies a **resource** — a thing, a noun — and the HTTP method describes the **action** on it. The method is where the verb lives; the URL should never need one of its own.

```
Bad:   POST /createOrder
Bad:   POST /v1/orders/cancelOrder
Good:  POST /v1/orders                  (the verb is POST itself: "create")
Good:  PATCH /v1/orders/9001            (the verb is PATCH: "partially update")
```

A `PATCH` with a body of `{ "status": "CANCELLED" }` is the RESTful way to express "cancel this order" — the resource (`/v1/orders/9001`) doesn't change meaning based on what you're doing to it; only the method and body do. Once you start putting verbs in URLs, you're forced to invent a new endpoint for every new action (`/cancelOrder`, `/shipOrder`, `/refundOrder`...) instead of reusing the same resource with different methods or different states.

**Plural, not singular**, by convention: `/v1/orders`, not `/v1/order`. The collection endpoint (`GET /v1/orders`) and the single-item endpoint (`GET /v1/orders/9001`) share the same plural noun; only the path shape differs. This is a convention, not a hard rule of REST itself, but it's close to universal in real APIs, and an interviewer will notice if you reach for the singular.

**Hierarchy reflects ownership.** When one resource only meaningfully exists in the context of another — an `OrderItem` doesn't exist independently of its `Order` — nest it: `/v1/orders/9001/items`. When a resource can stand alone and is just *associated* with another (a `Product` exists independently of any order that references it), don't force a nesting that implies ownership that isn't real; keep it flat (`/v1/products/42`) and let the relationship live in the data, not the URL.

## 2.2 URL design: `/users/123/orders` vs. `/getUserOrders?userId=123`

These two URLs return the same data. Only one of them is RESTful, and the difference is worth being able to articulate precisely, because it's a question interviewers ask almost verbatim:

```
RESTful:      GET /v1/users/123/orders
Not RESTful:  GET /v1/getUserOrders?userId=123
```

The second form has two separate problems, not one. First, `getUserOrders` is a verb-shaped *action name* masquerading as a path — it's RPC (remote procedure call) style dressed up to look like REST. Second, and more subtly, it puts what is structurally a *path parameter* — which user's orders — into the query string, where it reads more like an optional filter than a required piece of the resource's identity. The first form encodes the hierarchy directly: "the orders belonging to user 123" is a sentence you can read straight off the URL, nested exactly the way the relationship is nested in your data model (`User (1) → Order (N)`, the same relationship you'll see mapped with `@OneToMany` in Chapter 4).

The general rule for path vs. query string: **if a value identifies *which* resource (or sub-collection of a resource) you mean, it's a path segment. If a value filters, sorts, or paginates *within* an already-identified resource, it's a query parameter.** `123` in `/users/123/orders` identifies whose orders; `?status=SHIPPED` in `/users/123/orders?status=SHIPPED` filters within that already-identified collection. Conflating the two — `/getUserOrders?userId=123&status=SHIPPED` — works, technically, but it stops communicating structure, and structure is the entire value REST is offering you over a flat list of RPC-style function names.

We build exactly this endpoint — `GET /v1/users/{userId}/orders` — in Chapter 4, specifically so this isn't just a slide-deck example.

## 2.3 Consistent response shapes

A client integrating against your API (your own frontend, a third-party, your future self six months from now) benefits enormously from every endpoint *looking* like it was designed by the same person, even on a team where it wasn't. Two places this matters most: errors, and pagination.

### A consistent error format

Every error response across the entire API — regardless of which controller, which exception, which status code — should have the same shape. This book uses:

```json
{
  "timestamp": "2026-06-18T09:15:30Z",
  "status": 404,
  "error": "Not Found",
  "message": "Order with id 9001 not found",
  "path": "/v1/orders/9001"
}
```

Five fields, always present, always in this shape: when (`timestamp`), the numeric code (`status`), the standard HTTP reason phrase (`error`), a human-readable explanation specific to this failure (`message`), and where it happened (`path`). A client can write *one* error-handling code path that reads `status` and `message` and have it work for every single endpoint in the API, instead of writing bespoke parsing logic per endpoint because one controller returns `{"err": "..."}` and another returns `{"errors": [{"detail": "..."}]}`. We implement this exact shape with a single `@RestControllerAdvice` in Chapter 4 — one class, applied globally, is what makes "consistent across every endpoint" actually achievable instead of aspirational.

### Pagination metadata

A list endpoint that can return thousands of rows needs to tell the client more than just the rows on the current page — it needs to communicate where the client is in the overall collection:

```json
{
  "content": [ { "id": 1, "...": "..." }, { "id": 2, "...": "..." } ],
  "page": 0,
  "size": 20,
  "totalElements": 487,
  "totalPages": 25,
  "last": false
}
```

This is, not coincidentally, almost exactly what Spring Data's `Page<T>` serializes to by default, which is one of the reasons this book leans on `Pageable`/`Page<T>` in Chapter 4 rather than hand-rolling pagination — you get a response shape that already matches this convention, for free, from the framework.

## 2.4 Filtering, sorting, and pagination: offset vs. cursor

There are two fundamentally different strategies for paginating a large collection, and the trade-off between them is a genuinely common system-design interview topic, not just API trivia.

**Offset-based pagination** (`?page=2&size=20`, which translates to `LIMIT 20 OFFSET 40` in SQL) is simple to implement, lets a client jump directly to "page 7," and is what Spring Data's `Pageable` gives you out of the box. Its weaknesses show up at scale and under concurrent writes: `OFFSET 40` means the database still has to scan and discard the first 40 matching rows before it can return the next 20, so deep pages on a huge table get progressively slower. Worse, it's not stable under concurrent modification — if a row is inserted into the result set while a client is paging through it, every subsequent page shifts by one, and the client can see a duplicate row or skip one entirely. This is sometimes called "page drift."

**Cursor-based pagination** (`?after=9001&size=20`, which translates to `WHERE id > 9001 ORDER BY id LIMIT 20`) uses the last-seen item's own sortable key as the starting point for the next page, instead of a numeric offset. This is stable under concurrent writes (new rows inserted "behind" the cursor don't shift anything ahead of it), and it stays fast at any depth because the database can use an index to jump straight to `id > 9001` rather than scanning and discarding. The costs are real, though: a client can no longer jump to "page 7" — only "the next page after the one I'm holding" — and the implementation needs a sortable, stable, ideally unique column to cursor on (an auto-increment ID or a timestamp with enough precision to break ties).

The practical guidance: offset pagination is the right default for admin dashboards, internal tools, and anything where the collection is bounded and "jump to page N" is a real user need. Cursor pagination is the right call for public, high-volume, or infinite-scroll-style APIs (think a social media feed) where stability and consistent performance at scale matter more than arbitrary page-jumping. This book's Order Management API uses offset pagination via `Pageable` throughout Chapter 4, because it's an internal/admin-style API where that trade-off is the right one — but Chapter 4 also shows what a cursor-based query would look like, specifically so you've seen both shapes of code, not just read about the difference.

> **Interview Question — SDE-2:** "Your `/v1/products` endpoint is getting slow specifically on high page numbers, but fast on early pages. Why, and how would you fix it without changing the database?"
>
> **Answer:** This is the textbook symptom of offset pagination on a large table: `OFFSET 10000` forces the database to walk through and discard 10,000 rows before it can start returning the requested 20, even though an index exists on the sort column — the index helps with ordering, not with skipping. Early pages are fast because the offset is small; the cost grows linearly with how deep into the collection you are. Without touching the schema, the fix is to switch the pagination strategy itself to cursor-based: instead of `page=500`, the client sends the last `id` (or sort key) it saw, and the query becomes `WHERE id > :lastSeenId ORDER BY id LIMIT 20`, which the existing index on `id` can satisfy directly regardless of how deep into the collection the client has paged — the database jumps straight there instead of counting through everything before it.

## 2.5 API versioning

APIs change. Fields get renamed, response shapes evolve, behavior shifts. Versioning is how you make those changes without breaking every client that's already integrated against you. Two dominant approaches:

**URL versioning** — `/v1/orders`, `/v2/orders`. The version is baked directly into the path. This is what this book uses throughout (`/v1/...` on every endpoint).
- *Pros:* Impossible to miss — it's visible in every log line, every browser address bar, every curl command, every API documentation link. Trivial to route at the infrastructure layer (a load balancer or gateway can route `/v1/*` and `/v2/*` to entirely different backend deployments without inspecting headers). Easiest to reason about and explain.
- *Cons:* Technically, a URL is supposed to identify a *resource*, and arguably `/v1/orders/9001` and `/v2/orders/9001` are "the same order," just represented differently — versioning the URL conflates the resource's identity with its representation. It also means every single endpoint needs to be touched (or at least namespaced) for every version bump, even ones that didn't change.

**Header versioning** — a single, version-agnostic URL (`/orders/9001`), with the version conveyed via a header, often through content negotiation: `Accept: application/vnd.ordermanagement.v2+json`, or a custom header like `X-API-Version: 2`.
- *Pros:* Keeps the URL "pure" — it always identifies the same resource regardless of version, which is more faithful to REST's original idea of what a URL means. Lets a single resource serve multiple representations without proliferating routes.
- *Cons:* Invisible. You cannot tell what version a request is targeting just by looking at the URL, which makes debugging, sharing links, and reading server logs meaningfully harder. It's also harder to route at the infrastructure layer, since a load balancer typically has to parse headers rather than match path prefixes, and it's easy for a client to simply forget to send the header and silently get a default version they didn't intend.

In practice, URL versioning wins in the majority of real-world APIs specifically *because* of its operational simplicity — Stripe, GitHub, and most public APIs you've used are URL- or simple-header-versioned, not pure HATEOAS-content-negotiated. This book uses URL versioning for that reason, but you should be able to argue both sides in an interview, because "it depends on your operational priorities" is the actually-correct answer, not "URL versioning is right and header versioning is wrong."

## 2.6 Idempotency keys: making `POST` safe to retry

Chapter 1 established *why* `POST` isn't idempotent and *why* that's a real problem under network failures and retries. The fix is a client-supplied idempotency key:

```
POST /v1/orders
Idempotency-Key: 7c9e6679-7425-40de-944b-e07fc1f90ae7
Content-Type: application/json

{ "items": [ { "productId": 42, "quantity": 2 } ] }
```

The contract: the client generates this key **once** per logical attempt to create an order (a UUID is the typical choice) and resends the *exact same key* if it has to retry — because it got a timeout, a `5xx`, or a dropped connection, none of which tell the client whether the original request actually succeeded server-side. The server, the first time it sees a given key, processes the request normally and stores the key alongside the result. If that same key arrives again, the server doesn't reprocess the request at all — it looks up the stored result and returns it, as if nothing happened twice.

This has to be implemented carefully under concurrency: two requests with the *same* idempotency key can genuinely arrive at almost the same instant (a client firing a request, timing out at the network layer, and immediately retrying while the original is still being processed). A naive "check if the key exists, then insert" has a race condition in exactly that window. The robust implementation relies on a database-level unique constraint on the key column and handles the constraint violation as the signal that a concurrent duplicate happened — we build this for real, including that race condition, when we implement `POST /v1/orders` in Chapter 4.

## 2.7 The Richardson Maturity Model

Leonard Richardson proposed a four-level scale (Level 0 through Level 3) for how "RESTful" an HTTP API actually is, and it's a useful mental model for placing any API you encounter — including, honestly, most production APIs, which rarely make it past Level 2.

**Level 0 — The Swamp of POX ("Plain Old XML," though it applies to JSON too).** One single URL, one single HTTP method (almost always `POST`), and the *actual* operation is described entirely inside the request body — essentially RPC over HTTP, ignoring everything HTTP itself offers. `POST /api` with `{ "action": "getOrder", "orderId": 9001 }` is Level 0. SOAP web services are the canonical historical example.

**Level 1 — Resources.** Multiple URLs now exist, one per resource (`/orders`, `/products`), but every operation on a resource still goes through one method, typically `POST`, with the specific action still named inside the body. Progress over Level 0 (at least the URL tells you *what* you're operating on), but HTTP methods still aren't doing any semantic work.

**Level 2 — HTTP verbs.** This is where the methods from section 2.1 actually get used as intended: `GET` to read, `POST` to create, `PUT`/`PATCH` to update, `DELETE` to remove, and status codes are used meaningfully instead of always returning `200` with an error description buried in the body. **This is where the overwhelming majority of real-world "RESTful" APIs live, including the one this book builds.** It's a perfectly legitimate, productive place to stop.

**Level 3 — HATEOAS** (Hypermedia as the Engine of Application State). Responses don't just return data — they include links describing what the client can legitimately do *next*, given the resource's current state:

```json
{
  "id": 9001,
  "status": "PENDING",
  "_links": {
    "self":   { "href": "/v1/orders/9001" },
    "cancel": { "href": "/v1/orders/9001/cancel" },
    "items":  { "href": "/v1/orders/9001/items" }
  }
}
```

The idea is that a client shouldn't need out-of-band documentation to know that a `PENDING` order can be cancelled — the API tells it so, in the response itself, the same way a website's HTML tells a browser what links are clickable from the current page. Notice the `_links` block would *not* include a `cancel` link if the order were already `SHIPPED` — the available actions are derived from the resource's actual state, which is the entire point.

In practice, full HATEOAS is rare outside of specific ecosystems (it's more common in enterprise/internal APIs than public ones) because it adds real implementation complexity and most client developers building against your API are reading documentation anyway, not programmatically discovering links at runtime. It's worth knowing the concept cold for an interview — and worth being honest that Level 2 is where the vast majority of production APIs, including the one in this book, deliberately stop, because the cost of full hypermedia rarely buys back its complexity for a typical CRUD-style backend.

> **Interview Question — SDE-2:** "Is our API RESTful?"
>
> **Answer:** It's Level 2 on the Richardson Maturity Model — proper resource-oriented URLs, correct and meaningful use of HTTP methods and status codes, no verbs in paths. It's not Level 3; there's no HATEOAS, no `_links` describing valid next actions from a response. That's a deliberate trade-off, not an oversight: Level 2 is what the overwhelming majority of production REST APIs actually implement, because hypermedia's main benefit — clients discovering valid actions at runtime instead of from documentation — rarely justifies its implementation cost for a typical internal or B2B API where client developers are reading docs anyway. If an interviewer is asking this, the strong answer isn't "yes" or "no," it's naming the level and explaining why stopping there was the right call for this kind of API.

---

Chapter 1 and 2 covered the *contract* — what flows over the wire and how to shape it well. Chapter 3 starts looking at the framework that's going to implement that contract for you: what Spring Boot is actually doing between `main()` and your first successful `curl` request.
