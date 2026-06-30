# Docker, Kubernetes and Cloud Infrastructure
### From Containers to Production Orchestration

*A practical guide for engineers who know Docker but not Kubernetes — or CI/CD.*

---

## Table of Contents

1. [The History That Explains Everything](#chapter-1-the-history-that-explains-everything)
2. [Docker Deep Dive](#chapter-2-docker-deep-dive)
3. [Kubernetes Architecture](#chapter-3-kubernetes-architecture)
4. [Kubernetes Objects](#chapter-4-kubernetes-objects)
5. [Networking](#chapter-5-networking)
6. [Resource Management and Autoscaling](#chapter-6-resource-management-and-autoscaling)
7. [CI/CD with GitHub Actions and Helm](#chapter-7-cicd-with-github-actions-and-helm)
8. [AWS Fundamentals](#chapter-8-aws-fundamentals)
9. [Observability](#chapter-9-observability)
10. [kubectl Mastery](#chapter-10-kubectl-mastery)

---

## How to read this book

Every chapter follows the same rule: **understand the problem before you look at the solution.**
Kubernetes has hundreds of fields, flags, and YAML keys. Memorizing them is a waste of time.
Understanding *why each one exists* means you can derive most of them yourself, and you'll
never be confused by a new one — you'll just ask "what problem does this solve?" and the
answer will usually be obvious from the history in Chapter 1.

---

# CHAPTER 1: The History That Explains Everything

Kubernetes looks like an enormous, arbitrary pile of YAML the first time you meet it.
It isn't arbitrary. Every object, every field, every controller exists because someone,
at some point, hit a real production problem and needed a real production fix. If you
understand the 30-year history that led here, the YAML stops looking arbitrary and starts
looking inevitable.

This chapter walks through four eras of running software. Each era solved the previous
era's biggest problem — and created a new one, which the next era then solved.

```
 Era 1            Era 2              Era 3              Era 4
 Bare Metal   →   Virtual Machines → Containers      →  Orchestration
 1990s–2005       2005–2013           2013–present       2014–present

 Problem:         Problem:           Problem:           Problem:
 1 app/server,    full OS per VM,    500+ containers
 huge waste       slow boot,         across 50 servers
                  config drift       — who manages them?
```

## Era 1: Bare Metal (1990s – 2005)

In this era, "deploying an application" meant buying a physical server, racking it in a
data center, installing an OS, installing the runtime, configuring networking, and only
then deploying your code onto it.

```
+------------------------------+
|        Physical Server        |
|  +--------------------------+ |
|  |   Operating System        | |
|  |  +---------------------+  | |
|  |  |   Application A      |  | |
|  |  +---------------------+  | |
|  +--------------------------+ |
|         (1 app per box)       |
+------------------------------+
```

**The defining rule of this era: one application per server.** Why? Because applications
fought over the machine. App A needs Python 2.6, App B needs Python 3. App A needs port
8080, App B also wants port 8080. App A leaks memory and crashes the box, taking App B
down with it. The only reliable way to isolate two applications was to put them on two
different physical machines.

This created two enormous, expensive problems:

- **Utilization was 5–15%.** Capacity planning meant guessing your application's peak
  load a year in advance and buying a server sized for it. The server then sat mostly idle
  the other 90% of the time, because you couldn't safely run anything else on it.
- **Provisioning took 4–6 weeks.** Ordering hardware, waiting for delivery, racking it,
  cabling it, installing the OS, patching it, configuring the network — every single new
  application or every scale-out event meant a multi-week lead time. You could not
  respond to a traffic spike that happened this afternoon.

There was also no real redundancy story by default: if the physical box died, the
application died with it, and recovery meant repeating the entire weeks-long provisioning
process on different hardware.

This is the problem the next 25 years of infrastructure engineering tried to solve:
**how do we run more applications, on less hardware, provisioned faster, without them
interfering with each other?**

## Era 2: Virtual Machines (2005 – 2013)

The hypervisor solved the isolation problem without requiring separate physical hardware.
A hypervisor is a thin layer of software that can carve one physical machine into several
*virtual* machines, each with its own virtual CPU, memory, disk, and — critically — **its
own full operating system kernel.** Because each VM has its own kernel, App A's VM can run
a completely different OS, library set, and configuration than App B's VM, with hardware-
level memory isolation between them.

```
+----------------------------------------------------+
|                  Physical Server                     |
|  +--------------------------------------------------+|
|  |              Hypervisor (e.g. ESXi)               ||
|  +--------------------------------------------------+|
|  +---------------+ +---------------+ +-------------+ |
|  |     VM 1        | |     VM 2        | |    VM 3     | |
|  |  +-----------+  | |  +-----------+  | | +---------+ | |
|  |  | Guest OS A |  | |  | Guest OS B |  | | Guest OS C| | |
|  |  +-----------+  | |  +-----------+  | | +---------+ | |
|  |  |  App A     |  | |  |  App B     |  | |  App C    | | |
|  |  +-----------+  | |  +-----------+  | | +---------+ | |
|  +---------------+ +---------------+ +-------------+ |
+----------------------------------------------------+
```

### Type 1 vs Type 2 hypervisors

| | Type 1 (bare-metal) | Type 2 (hosted) |
|---|---|---|
| Runs on | Physical hardware directly | On top of a host OS |
| Examples | VMware ESXi, Microsoft Hyper-V, Xen | VMware Workstation, VirtualBox, Parallels |
| Performance | Near-native — no host OS overhead | Slower — competes with host OS |
| Used for | Production data centers, cloud providers | Developer laptops, local testing |

Production infrastructure almost exclusively uses Type 1 hypervisors, because there's no
host OS stealing CPU cycles and memory between the hardware and the VMs.

### What got better

- **Utilization rose to 40–70%.** Several VMs could now safely share one physical box,
  because the hypervisor enforced hard isolation between them at the hardware level.
- **Provisioning dropped to minutes.** Instead of ordering and racking hardware, you cloned
  a pre-built VM template. This is also where "Infrastructure as Code" tooling (Puppet,
  Chef, Terraform's ancestors) began to matter — you could now describe a server's
  configuration in a file and provision it on demand.

### What was still broken

VMs solved isolation and provisioning speed, but they didn't solve the underlying
inefficiency of duplicating an entire operating system for every workload:

- **Every VM needs its own full OS** — typically 2–4 GB of disk and several hundred MB of
  RAM just for the kernel, init system, and base packages, *before your application has
  used a single byte.* Run 50 small microservices and you're paying that 2–4 GB tax 50
  times over.
- **Boot time was still measured in minutes**, because a VM has to boot an entire
  operating system — BIOS/UEFI, bootloader, kernel, init system — before your application
  process even starts.
- **Config drift was still a problem.** Even with VM templates, the VM that ran in staging
  and the VM that ran in production would slowly diverge — different patch levels,
  different manually-applied tweaks — leading to the infamous "works on my machine."
  A VM image bundles the OS and the app together, but doesn't guarantee the *running*
  environment matches what the developer tested locally.

The unsolved problem heading into the next era: **how do we get isolation without paying
for a full OS per workload, and how do we guarantee the artifact a developer tests is
*exactly* the artifact that runs in production?**

## Era 3: Containers (2013 – present)

Containers solve this by giving up something VMs gave you (a separate kernel per
workload) in exchange for something much lighter weight. A container does **not** virtualize
hardware and does **not** boot its own kernel. Instead, every container on a host shares
that host's single Linux kernel, and is isolated from other containers using two kernel
features that had existed for years but nobody had packaged well:

- **Namespaces** isolate *what a process can see*: its own process tree (PID namespace),
  its own network stack and IP address (NET namespace), its own filesystem mount points
  (MNT namespace), its own hostname (UTS namespace), its own inter-process communication
  (IPC namespace), and its own user/group ID mapping (USER namespace).
- **cgroups** (control groups) isolate *what a process can use*: hard limits on CPU,
  memory, disk I/O, and network bandwidth, so one container can't starve its neighbors.

```
+--------------------------------------------------------+
|                    Physical / Virtual Host                |
|  +--------------------------------------------------------+|
|  |              Single Shared Linux Kernel                  ||
|  +--------------------------------------------------------+|
|  +-------------+ +-------------+ +---------------------+  |
|  |  Container 1  | |  Container 2  | |   Container 3       |  |
|  | (namespaces +| | (namespaces +| |  (namespaces +      |  |
|  |   cgroups)    | |   cgroups)    | |    cgroups)         |  |
|  |  +---------+ | |  +---------+ | |   +-----------+     |  |
|  |  |  App A   | | |  |  App B   | | |   |  App C     |   |  |
|  |  +---------+ | |  +---------+ | |   +-----------+     |  |
|  +-------------+ +-------------+ +---------------------+  |
+--------------------------------------------------------+
       no per-container kernel -> fast start, low overhead
```

### Docker's actual innovation

Namespaces and cgroups existed in the Linux kernel since the mid-2000s. What Docker
contributed in 2013 wasn't the isolation primitive — it was making that primitive
*usable*, through three pieces that, together, solved the config-drift problem for good:

1. **The Dockerfile** — a declarative, version-controllable recipe for building an image,
   so "how this container is built" lives in source control next to the application code.
2. **Image layers** — each instruction in a Dockerfile produces an immutable, content-
   addressed layer that can be cached and reused, making builds fast and images shareable.
3. **Docker Hub** — a public registry so an image built once could be `docker push`ed and
   `docker pull`ed identically anywhere, guaranteeing the artifact a developer tested
   locally is bit-for-bit the same artifact that runs in staging and production.

That third point is the real config-drift killer: a container image is a single
immutable artifact. There's no "the package list slowly drifted" problem, because nothing
about the image can change after it's built — you build a new one and replace the old one.

### Containers vs VMs

| | Virtual Machine | Container |
|---|---|---|
| Isolation unit | Hardware (hypervisor) | OS (namespaces + cgroups) |
| Kernel | Own kernel per VM | Shared host kernel |
| Startup time | Minutes (boots full OS) | Milliseconds–seconds (starts a process) |
| Typical image size | GBs (full OS) | MBs–tens of MBs |
| Density per host | Tens of VMs | Hundreds–thousands of containers |
| Isolation strength | Very strong (hardware-enforced) | Strong, but shares kernel attack surface |
| Portability | OS-version sensitive | Runs identically anywhere the runtime exists |

Note the isolation row isn't a free lunch: because containers share a kernel, a kernel
exploit can in principle cross container boundaries in a way it can't cross VM
boundaries. This is *why* cloud providers often run containers *inside* VMs in production
(you'll see this again in Chapter 8 with EKS worker nodes) — you get container density
and speed, with a VM as a hard outer isolation boundary between *tenants*.

## Era 4: Orchestration (2014 – present)

Containers solved density, startup speed, and config drift for a *single* container on a
*single* host. But production systems aren't one container on one host — picture a
realistic deployment: **500 containers spread across 50 servers.** Now ask some very
ordinary operational questions:

- A new container needs to start. **Which of the 50 servers should run it?** (Scheduling)
- A container crashes at 3 AM. **Who notices, and who restarts it?** (Healing)
- Traffic triples during a flash sale. **Who adds more instances, and who removes them
  again once traffic drops?** (Scaling)
- Container A needs to talk to container B, but B's IP changes every time it restarts.
  **How does A find B?** (Discovery)
- You need to ship a new version of an API to all 30 of its running instances **without
  taking the API down.** (Updates)

`docker run` answers none of these questions — it starts one container, on the host you
ran it on, and does nothing else. At 500-containers-across-50-servers scale, doing any of
this by hand, or with ad-hoc shell scripts, doesn't survive contact with reality. This is
the gap orchestration fills.

**The five problems orchestration solves:**

1. **Scheduling** — given a new container's resource needs and constraints, automatically
   pick the best of the available servers to run it on.
2. **Self-healing** — continuously watch running containers; if one dies or a whole server
   goes down, automatically reschedule replacements elsewhere.
3. **Scaling** — automatically add or remove container instances in response to load,
   within limits you define.
4. **Service discovery** — give every group of containers a stable name/address that
   doesn't change even as the individual containers behind it come and go.
5. **Rolling updates** — replace old container versions with new ones gradually, checking
   health as you go, with an automatic, safe path to roll back if something's wrong.

Several orchestrators were built to solve this — Docker Swarm, Apache Mesos, and
Kubernetes among them. Kubernetes (open-sourced by Google in 2014, drawing on a decade of
internal experience running containers at Google scale via an internal system called
Borg) became the dominant standard, and is what the rest of this book covers in depth.

Every remaining chapter is really just a detailed answer to those same five questions:
*scheduling* is Chapter 3 (the Scheduler) and Chapter 6 (resource requests/limits);
*healing* is Chapter 3 (controllers) and Chapter 4 (probes); *scaling* is Chapter 6 (HPA);
*discovery* is Chapter 5 (Services and DNS); *updates* is Chapter 4 (Deployments) and
Chapter 7 (CI/CD pipelines that trigger those updates).

---

> ### 🎤 Interview Corner — Chapter 1
>
> **Q: "Why didn't the industry just keep using bigger, better VMs instead of adopting
> containers?"**
>
> **A:** VMs solved hardware-level isolation, but they never solved the *packaging* and
> *density* problems. Every VM still needs to boot a full OS kernel — minutes of boot
> time, and 2–4 GB of overhead, before your application has even started. At microservice
> scale (tens or hundreds of small services), that overhead is multiplied by every
> service, every replica. Containers share the host kernel, so they start in
> milliseconds and carry almost no overhead beyond the application itself, letting a
> single host run 10–50x more workloads than the same host running one-VM-per-app. VMs
> didn't disappear, though — they moved up a layer: cloud providers and Kubernetes
> clusters commonly run containers *inside* VMs, using the VM as a strong security
> boundary between tenants while getting container-level density and speed for the
> workloads inside each VM.
>
> **Q: "What's the actual difference between what Docker does and what Kubernetes does?"**
>
> **A:** Docker operates at the single-host, single-container level: it builds images,
> manages image layers, and runs/stops containers on one machine. Kubernetes operates at
> the fleet level, across many machines: given a desired state ("run 5 replicas of this
> image, expose them on this port, autoscale up to 20 under load"), Kubernetes decides
> which machines run which containers, restarts failed ones, reroutes traffic away from
> unhealthy ones, and rolls out new versions safely. Kubernetes doesn't replace Docker's
> job of building images — it consumes the images Docker (or another OCI-compatible
> builder) produces, and orchestrates many containers built from them across a cluster of
> machines.


---

# CHAPTER 2: Docker Deep Dive

## Docker architecture

When you type `docker run nginx`, four pieces of software cooperate to make that happen.
Understanding the split between them explains a lot of Docker's behavior — for instance,
why `docker` commands still work over SSH to a remote machine, and why an image has to be
"pulled" before it can run.

```
   YOUR TERMINAL                      DOCKER HOST
  +-------------+   REST API    +--------------------------+
  | Docker CLI    |------------->|     Docker Daemon          |
  | (docker run,  |  (over a     |     (dockerd)               |
  |  docker build)|   Unix socket|                              |
  +-------------+   or TCP)     |  +----------------------+    |
                                  |  |  Images (local cache) |    |
                                  |  +----------------------+    |
                                  |  +----------------------+    |
                                  |  |  Running Containers    |    |
                                  |  +----------------------+    |
                                  |  +----------------------+    |
                                  |  |  Networks, Volumes      |    |
                                  |  +----------------------+    |
                                  +--------------------------+
                                              |
                                              | docker pull / push
                                              v
                                  +--------------------------+
                                  |   Registry (Docker Hub,     |
                                  |   GHCR, ECR, private...)    |
                                  +--------------------------+
```

- **Docker Client** — the `docker` CLI binary you type commands into. It doesn't do any
  work itself; it translates your command into a REST API call.
- **Docker Daemon (`dockerd`)** — the long-running background process that does the actual
  work: pulling images, building images, creating and running containers, managing
  networks and volumes. The client and daemon can be on the same machine (the common
  case) or different machines (the client just points `DOCKER_HOST` at a remote daemon).
- **Images** — read-only templates stored on the daemon's host, made up of stacked layers.
- **Containers** — a running (or stopped) instance of an image, with a thin writable layer
  on top.
- **Registry** — a server that stores and distributes images by name and tag (e.g.
  `myorg/order-api:1.4.0`). Docker Hub is the public default; most companies also run a
  private registry (GHCR, ECR, GCR, Harbor) for proprietary images.

## Image layers, and why instruction order matters

Every instruction in a Dockerfile (`FROM`, `RUN`, `COPY`, etc.) produces a new,
immutable, content-addressed **layer**. Layers stack on top of each other to form the
final image, and — critically — **Docker caches each layer.** If you rebuild an image and
a given instruction hasn't changed (and none of the instructions before it have changed),
Docker reuses the cached layer instead of re-executing it.

This is why instruction *order* in a Dockerfile is a performance decision, not just a
style preference. Consider a Node.js app:

```dockerfile
# BAD: source code copied before dependencies are installed
COPY . .
RUN npm install
```

Here, *any* change to *any* file in your repo — including a one-line README edit —
invalidates the `COPY . .` layer, which invalidates every layer after it, including
`npm install`. Every single build re-downloads and reinstalls every dependency, even
though `package.json` didn't change.

```dockerfile
# GOOD: dependency manifests copied (and installed) first
COPY package.json package-lock.json ./
RUN npm install
COPY . .
```

Now `npm install` only re-runs when `package.json` or `package-lock.json` actually
change. Editing application source code invalidates only the final `COPY . .` layer —
the expensive dependency-install layer stays cached. On a real CI pipeline this is
the difference between a 90-second build and a 4-second one.

**Rule of thumb: order Dockerfile instructions from least-frequently-changed to
most-frequently-changed.** OS packages change rarely → install those first. Application
dependencies change occasionally → install those next. Source code changes constantly →
copy that last.

## Multi-stage builds

A naive Dockerfile for a compiled or transpiled application bakes the entire build
toolchain — compilers, dev dependencies, source maps, package caches — into the final
image. That image is then needlessly large, slower to pull, and carries a bigger attack
surface (a compiler in your production image is a gift to an attacker who gets a shell).

**Multi-stage builds** fix this by using two (or more) `FROM` statements in one
Dockerfile: a **builder stage**, which has the full toolchain and produces compiled
artifacts, and a **runtime stage**, which starts from a minimal base image and copies
*only the finished artifacts* out of the builder stage. The builder stage, and
everything in it, is discarded — it never becomes part of the final image.

### Full Dockerfile: Order Management API

This is a complete, production-grade Dockerfile for a Node.js/TypeScript "Order
Management API," with every line explained.

```dockerfile
# ---------- Stage 1: builder ----------
# Full Node image (has npm, build tools) — only exists during the build,
# never shipped in the final image.
FROM node:20-bookworm AS builder

WORKDIR /app

# Copy ONLY the dependency manifests first, so the npm install layer is
# cached and skipped unless package.json/package-lock.json actually change.
COPY package.json package-lock.json ./

# npm ci (not npm install) installs EXACTLY what's in package-lock.json —
# reproducible, and faster, because it skips dependency resolution.
RUN npm ci

# Now copy the rest of the source code. This invalidates the cache only
# for this layer and below — npm ci above stays cached.
COPY . .

# Compile TypeScript -> JavaScript into /app/dist
RUN npm run build

# Drop dev dependencies (jest, eslint, typescript, etc.) now that the
# build is done — we only need production dependencies going forward.
RUN npm prune --production

# ---------- Stage 2: runtime ----------
# Minimal base image. "slim" strips out compilers, docs, and other build
# tooling that a runtime container never needs — smaller image, smaller
# attack surface.
FROM node:20-bookworm-slim AS runtime

# Create a dedicated, unprivileged user. Never run application processes
# as root inside a container — see "Docker security" below.
RUN groupadd --gid 1001 nodejs && \
    useradd --uid 1001 --gid nodejs --shell /bin/bash --create-home appuser

WORKDIR /app

# Copy ONLY what's needed to run: compiled JS, production node_modules,
# and package.json (needed for "npm start" / version metadata).
# --chown sets ownership at copy time, avoiding an extra RUN chown layer.
COPY --from=builder --chown=appuser:nodejs /app/dist ./dist
COPY --from=builder --chown=appuser:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:nodejs /app/package.json ./package.json

# Switch to the unprivileged user for everything from here on, including
# the container's main process.
USER appuser

# Documentation only — does NOT actually publish the port. The real
# port mapping happens at `docker run -p` or in Kubernetes Service specs.
EXPOSE 3000

# Let Docker (and Docker Compose / Swarm) know if the container is
# actually healthy, not just running. Kubernetes ignores this and uses
# its own probes instead (Chapter 4).
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD node ./dist/healthcheck.js || exit 1

# Exec form (JSON array), NOT shell form ("node dist/main.js"). Exec
# form runs node as PID 1 directly, so it receives SIGTERM correctly for
# graceful shutdown. Shell form wraps it in `/bin/sh -c`, which swallows
# signals and breaks graceful shutdown.
CMD ["node", "dist/main.js"]
```

**Why this matters in numbers:** the `builder` stage, with the full Node toolchain, dev
dependencies, and source maps, is typically 900MB–1.2GB. The final `runtime` image,
containing only compiled output and production dependencies, is typically 150–200MB.
That's a 4–6x reduction in image size, pull time, and attack surface, for free, just by
splitting the Dockerfile into two stages.

## Docker Compose: multi-container applications

A real application is rarely just one container — it's an API, talking to a database,
talking to a cache, talking to a message broker. Running each with separate `docker run`
commands (remembering every flag, every network, every restart) doesn't scale past a
toy example. **Docker Compose** lets you describe an entire multi-container application
in one declarative YAML file, then bring the whole thing up or down with one command.

### Complete docker-compose.yml: API + PostgreSQL + Redis + Kafka

```yaml
version: "3.9"

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    image: order-management-api:local
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgres://orders_user:orders_pass@postgres:5432/orders_db
      REDIS_URL: redis://redis:6379
      KAFKA_BROKERS: kafka:9092
      NODE_ENV: development
    # depends_on with "condition" waits for dependencies to actually be
    # READY (per their healthcheck), not just STARTED. Without the
    # condition, Compose only waits for the container process to begin,
    # which is almost always too early for a database connection to work.
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      kafka:
        condition: service_healthy
    networks:
      - backend
    restart: unless-stopped

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: orders_user
      POSTGRES_PASSWORD: orders_pass
      POSTGRES_DB: orders_db
    volumes:
      # Named volume: PostgreSQL's data directory persists across
      # `docker compose down` / `up`, unlike the container's writable
      # layer, which is destroyed when the container is removed.
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U orders_user -d orders_db"]
      interval: 5s
      timeout: 5s
      retries: 10
    networks:
      - backend

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 10
    networks:
      - backend

  zookeeper:
    image: confluentinc/cp-zookeeper:7.6.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    networks:
      - backend

  kafka:
    image: confluentinc/cp-kafka:7.6.0
    depends_on:
      - zookeeper
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      # Two listener names: one for connections from OTHER containers on
      # the "backend" network (using the service name "kafka"), one for
      # connections from the host machine (using "localhost"). Without
      # this split, host tools like a local Kafka UI can't connect.
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:29092
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,PLAINTEXT_HOST://0.0.0.0:29092
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    ports:
      - "29092:29092"
    healthcheck:
      test: ["CMD-SHELL", "kafka-broker-api-versions --bootstrap-server localhost:9092"]
      interval: 10s
      timeout: 5s
      retries: 10
    networks:
      - backend

volumes:
  postgres_data:

networks:
  backend:
    driver: bridge
```

Bring it all up with `docker compose up -d`. A few things worth calling out:

- **`depends_on` with `condition: service_healthy`** is the difference between "started"
  and "actually ready." Without it, `api` might start and try to connect to `postgres`
  before Postgres has finished initializing — a classic source of flaky local dev
  environments and CI runs.
- **Named volumes** (`postgres_data`) persist data across `docker compose down` /
  `docker compose up`. The container's own writable layer does not — `docker compose down`
  removes the containers, and anything written outside a mounted volume goes with them.
- **`networks: backend`** puts every service on the same user-defined bridge network,
  which is what makes the next section possible.

## Docker networking

Docker ships three built-in network drivers, each suited to a different scenario:

| Driver | Scope | Typical use |
|---|---|---|
| `bridge` (default) | Single host | Default for standalone containers; an isolated virtual network on one host |
| `host` | Single host | Container shares the host's network stack directly — no isolation, max performance |
| `overlay` | Multiple hosts | Multi-host networking for Docker Swarm clusters |

**Container-to-container communication by name.** Any user-defined bridge network (like
`backend` above) comes with a built-in embedded DNS server. Every container on that
network can resolve every *other* container on that network by its **service name** —
no hardcoded IPs required. That's why the Compose file above could simply write
`postgres://...@postgres:5432/...` — `postgres` resolves to the right container's IP
automatically, even though that IP isn't known until the container actually starts.
This pattern — "talk to your dependency by name, let the platform resolve the IP" — is
exactly the model Kubernetes Services formalize at cluster scale in Chapter 5.

The **default** bridge network (the one that exists automatically, not a user-defined
one) does *not* provide this DNS resolution by name — only user-defined bridge networks
do. This is one reason `docker-compose.yml` and explicit `docker network create` are
preferred over relying on Docker's default network for anything beyond a single
container.

## Docker security

Two defaults are worth overriding in every production Dockerfile:

**1. Never run as root.** By default, a process inside a container runs as root (UID 0)
*inside the container's namespace* — and if an attacker breaks out of that namespace
(via a kernel exploit or container-runtime bug), root inside the container becomes root
on the host. Create and switch to an unprivileged user, as the Order Management API
Dockerfile does above:

```dockerfile
RUN groupadd --gid 1001 nodejs && \
    useradd --uid 1001 --gid nodejs --create-home appuser
USER appuser
```

**2. Run with a read-only root filesystem where possible.** This isn't set in the
Dockerfile — it's a runtime flag (`docker run --read-only`, or Kubernetes'
`readOnlyRootFilesystem: true`, covered in Chapter 4) that prevents *any* process inside
the container from writing to the container's filesystem at all, even if it's
compromised. If your app genuinely needs to write somewhere (temp files, a cache
directory), mount a small, explicit writable volume for exactly that path rather than
leaving the whole filesystem writable:

```bash
docker run --read-only --tmpfs /tmp --tmpfs /app/cache order-management-api:local
```

## Common Dockerfile anti-patterns and fixes

| Anti-pattern | Why it's a problem | Fix |
|---|---|---|
| `COPY . .` before installing dependencies | Busts the dependency-install cache on every source change | Copy manifest files first, install, *then* copy source |
| `FROM ubuntu:latest` | `latest` is a moving target — your build isn't reproducible, and a base image update can silently break prod | Pin a specific tag (and ideally a digest): `FROM ubuntu:22.04` |
| One giant `RUN` per dependency (`RUN apt install a` / `RUN apt install b` / ...) | Each `RUN` is its own layer — many tiny layers bloat the image and slow pulls | Combine into one `RUN apt-get update && apt-get install -y a b && rm -rf /var/lib/apt/lists/*` |
| No `.dockerignore` | `node_modules/`, `.git/`, local `.env` files get copied into the build context, bloating it and risking secret leakage | Add a `.dockerignore` excluding `node_modules`, `.git`, `*.env`, build output |
| Running as root | Container compromise = easier host compromise | Create and `USER` an unprivileged account |
| Shell-form `CMD`/`ENTRYPOINT` (`CMD node dist/main.js`) | Runs under `/bin/sh -c`, which doesn't forward SIGTERM to your app — containers hang on shutdown until they're force-killed | Use exec form: `CMD ["node", "dist/main.js"]` |
| Single-stage build with full toolchain shipped to prod | Bloated image, larger attack surface (compilers, dev deps in production) | Multi-stage build — builder stage + minimal runtime stage |
| Hardcoded secrets (`ENV DB_PASSWORD=hunter2`) baked into the image | Secrets become part of the image's permanent layer history, extractable by anyone who can pull the image | Inject secrets at runtime via env vars / mounted files / orchestrator secrets — never bake them into a layer |

---

> ### 🎤 Interview Corner — Chapter 2
>
> **Q: "Your Docker build takes 6 minutes even when you only changed one line of
> application code. What's wrong, and how do you fix it?"**
>
> **A:** Almost always this means the Dockerfile copies the entire source tree before
> installing dependencies (`COPY . .` followed by `RUN npm install` / `pip install` /
> etc.). Because Docker's layer cache invalidates a layer — and every layer after it — as
> soon as any input to that layer changes, copying *all* source code before the install
> step means *any* code change, even a comment, invalidates the dependency-install layer,
> forcing a full reinstall every build. The fix is to copy only the dependency manifest
> files (`package.json`/`package-lock.json`, `requirements.txt`, `go.mod`, etc.) first,
> run the install step, and only then copy the rest of the source code — so the
> expensive install step stays cached unless dependencies actually changed.
>
> **Q: "Why use a multi-stage build instead of just deleting build tools at the end of a
> single-stage Dockerfile with `RUN rm -rf ...`?"**
>
> **A:** Because Docker layers are immutable and additive — deleting a file in a later
> `RUN` instruction doesn't remove it from the image, it just hides it in the final
> filesystem view. The earlier layer still contains the file, and that layer is still
> part of the image, still gets pulled, and is still extractable by anyone with access to
> the image (`docker save` + inspect, or a malicious actor with registry access). A
> multi-stage build genuinely never includes the builder stage's layers in the final
> image at all — the final image is built from a fresh `FROM`, with only explicit
> `COPY --from=builder` artifacts brought in. There's no way to recover the discarded
> stage's contents from the final image, because they were never layered into it.


---

# CHAPTER 3: Kubernetes Architecture

A Kubernetes **cluster** is a set of machines (**nodes**) split into two roles: a small
number of **control plane** nodes that make decisions about the cluster, and a larger
number of **worker** nodes that actually run your application containers. Nothing in this
chapter is arbitrary — every component exists to answer one of the five orchestration
questions from Chapter 1 (scheduling, healing, scaling, discovery, updates).

## Full cluster architecture

```
                              CONTROL PLANE
   +-------------------------------------------------------------------+
   |                                                                     |
   |   +-------------+        +-----------+        +-----------------+ |
   |   |  kubectl /    |------->|  API Server |<------>|     etcd          | |
   |   |  any client    |  REST  | (kube-     |  reads/|  (distributed     | |
   |   +-------------+  /JSON   |  apiserver) |  writes|   key-value store, | |
   |                            +-----------+        |   Raft consensus)  | |
   |                                  ^  ^             +-----------------+ |
   |                                  |  |                                  |
   |                      watches     |  |     watches                     |
   |                  +---------------+  +----------------+                |
   |                  |                                     |                |
   |        +-------------------+               +----------------------+   |
   |        |  Controller Manager |               |      Scheduler          |   |
   |        |  (reconciliation    |               |  (filter + score        |   |
   |        |   loops: ReplicaSet,|               |   unscheduled pods,     |   |
   |        |   Node, Endpoints..)|               |   bind to a node)       |   |
   |        +-------------------+               +----------------------+   |
   +-------------------------------------------------------------------+
                                  ^
                                  |  API Server is the ONLY component every
                                  |  other piece talks to. Nothing talks to
                                  |  etcd directly except the API Server.
                                  v
   +-------------------------------------------------------------------+
   |                          WORKER NODE  (x N)                          |
   |                                                                       |
   |   +-----------+      +---------------+      +---------------------+|
   |   |  kubelet    |<---->| Container       |      |   kube-proxy           ||
   |   |  (node agent,|      | Runtime         |      |   (iptables/IPVS rules,||
   |   |   talks to   |      | (containerd,    |      |    implements           ||
   |   |   API Server)|      |  via CRI)       |      |    Service routing)    ||
   |   +-----------+      +---------------+      +---------------------+|
   |          |                     |                                      |
   |          v                     v                                      |
   |   +-------------------------------------------------------------+   |
   |   |    Pod A          Pod B          Pod C        Pod D            |   |
   |   |  [container]   [container]   [container]   [container]        |   |
   |   +-------------------------------------------------------------+   |
   +-------------------------------------------------------------------+
```

## CONTROL PLANE

### API Server (`kube-apiserver`)

The API Server is the **single entry point** to the entire cluster. Every interaction —
`kubectl apply`, the Scheduler placing a pod, a kubelet reporting node status, a
Controller creating a new ReplicaSet — happens by calling the API Server's REST API.
Nothing in Kubernetes, including Kubernetes' own internal components, talks directly to
etcd. They all go through the API Server, which:

1. **Authenticates** the request (who are you? — client certs, bearer tokens, OIDC...).
2. **Authorizes** the request (are you allowed to do this? — typically RBAC: can this
   identity `create` a `pod` in this `namespace`?).
3. Runs it through **admission controllers** — plugins that **validate** (reject
   non-conforming objects, e.g. "no privileged containers allowed") and **mutate**
   (auto-inject defaults, e.g. a sidecar proxy or a default resource limit) the object
   *before* it is persisted.
4. Persists the (now validated/mutated) object to **etcd**.

Because every read and write funnels through one component, the API Server is also the
natural place to enforce consistent security policy across the entire cluster, regardless
of which client or controller is making the request.

### etcd

etcd is a distributed key-value store, and it is **the single source of truth for the
entire cluster's state** — every Deployment, Pod, Service, Secret, ConfigMap, and Node
status that exists, exists because it's a key in etcd. The API Server is etcd's only
client; nothing else talks to it.

etcd uses the **Raft consensus algorithm** to keep multiple etcd nodes in agreement. This
is why production etcd clusters run with **3 or 5 nodes, never an even number**: Raft
requires a strict **majority (quorum)** of nodes to agree before any write is committed.
With 3 nodes, the cluster tolerates 1 node failure (2 remaining nodes are still a
majority of 3). With 5 nodes, it tolerates 2 failures. An even number like 4 doesn't buy
you anything over 3 — you'd still only tolerate 1 failure (a 4-node cluster needs 3 for
quorum, same fault tolerance as a 3-node cluster needing 2), while paying for an extra
node and extra write latency.

> **The single most important operational fact in this entire book: losing etcd without a
> backup means losing the entire cluster's state** — every Deployment spec, every Secret,
> every record of what *should* be running, gone. The running containers may keep running
> for a while, but nothing can be updated, healed, or rescheduled, and a control-plane
> restart with no etcd data recovers to an empty cluster. **Back up etcd regularly, and
> verify the restore procedure before you need it.**

### Scheduler (`kube-scheduler`)

When a new Pod is created without a node already assigned, the Scheduler's job is to pick
which node it should run on. It does this in two phases:

**Phase 1 — Filter ("which nodes *can* run this pod?").** Eliminate every node that
cannot satisfy the pod's requirements:
- Does the node have enough *unallocated* CPU and memory to satisfy the pod's resource
  `requests` (Chapter 6)?
- Does the node satisfy the pod's `nodeAffinity` rules (e.g. "must be on a node labeled
  `disktype=ssd`")?
- Does the node have any `taints` the pod doesn't `tolerate` (e.g. a node tainted
  `dedicated=gpu:NoSchedule` is skipped unless the pod explicitly tolerates it)?
- Are there port conflicts, volume zone mismatches, or other hard constraints?

**Phase 2 — Score ("of the nodes that *can*, which is *best*?").** Every node that
survives filtering gets a score from several scoring plugins, and the highest-scoring
node wins:
- `LeastAllocated` — prefers nodes with *more* free resources, spreading load evenly
  across the cluster rather than packing nodes tightly.
- `ImageLocality` — prefers a node that has *already pulled* the pod's container image,
  since that avoids an image-pull delay.
- Several others (pod (anti-)affinity preferences, topology spread) contribute too.

The Scheduler then *binds* the pod to the winning node by writing that decision back to
the API Server — it does not start the container itself; that's the kubelet's job, next.

### Controller Manager (`kube-controller-manager`)

This runs dozens of **reconciliation loops** bundled into one process, each loop
responsible for one resource type. Two examples that come up constantly:

- **ReplicaSet controller**: continuously compares "how many pods does this ReplicaSet's
  spec say should exist?" against "how many actually exist right now?" If actual < desired
  (a pod crashed, a node died), it creates new pods to close the gap. If actual > desired
  (you scaled down), it deletes the excess.
- **Node controller**: watches for nodes that stop reporting heartbeats. After a
  configurable timeout, it marks the node `NotReady`, and after a further grace period,
  evicts (reschedules) the pods that were running on it elsewhere in the cluster.

## WORKER NODES

### kubelet

The kubelet is the **node agent** — one runs on every worker (and typically control
plane) node. It is the bridge between "what the API Server says should run on this node"
and "what's actually running on this node." Concretely, the kubelet:

- Watches the API Server for Pods assigned to its node.
- Tells the container runtime to pull images and start/stop containers accordingly.
- Continuously runs the liveness/readiness/startup **probes** defined on each pod
  (Chapter 4), and acts on the results (restart on liveness failure, mark not-ready and
  remove from Service endpoints on readiness failure).
- Reports the node's and its pods' status back to the API Server, which is what
  `kubectl get nodes` / `kubectl get pods` ultimately display.

### kube-proxy

kube-proxy runs on every node and is responsible for making **Services** (Chapter 5)
actually work at the network level. A Service has a stable virtual IP, but that IP isn't
attached to any real network interface — kube-proxy watches the API Server for
Services and their backing Pod IPs, and programs **iptables (or IPVS) rules** on the node
so that traffic sent to a Service's IP gets transparently load-balanced across the
Service's actual backing pod IPs.

### Container Runtime

The component that actually creates and runs containers, via the **Container Runtime
Interface (CRI)** — a standard interface that lets Kubernetes support multiple runtimes
interchangeably. **containerd** is the default and most common choice in modern clusters
(Docker Engine itself is no longer used as the runtime since Kubernetes 1.24 — though
images you build *with* `docker build` run on containerd identically, since both speak
the same OCI image format).

## The reconciliation loop — the single most important concept in Kubernetes

Every controller in Kubernetes, without exception, follows the exact same pattern:

```
        +------------------------------------------------+
        |                                                    |
        v                                                    |
  +------------+      compare       +-------------+         |
  |  Desired     |------------------->|  Actual       |         |
  |  State        |                    |  State        |         |
  |  (in etcd,    |                    |  (observed     |         |
  |   what you    |                    |   from the     |         |
  |   declared)   |                    |   real world)  |         |
  +------------+                    +-------------+         |
        ^                                   |                    |
        |            if different,          |                    |
        |            take action to         v                    |
        +------------ converge -----  [ Reconcile ] --------------+
                                       (create / delete /
                                        update something)
```

You declare **desired state** ("I want 3 replicas of this pod"). A controller observes
**actual state** ("2 are currently running"). It compares the two, and if they differ, it
takes the smallest action needed to converge them (create 1 more pod), then goes back to
watching. This loop runs continuously and indefinitely — it never "finishes."

This is *the* mental model for understanding anything new you encounter in Kubernetes.
A Deployment doesn't "deploy your app" in some imperative, one-time sense — it
continuously enforces "this many pods, running this image, should exist" forever, and
self-heals any deviation, whether that deviation was a crash, a manual `kubectl delete
pod`, or a node failure. Once this clicks, ReplicaSets, HPAs, Node controllers, and even
external tools like Helm and ArgoCD all become recognizable instances of the exact same
pattern, just reconciling different kinds of desired state.

---

> ### 🎤 Interview Corner — Chapter 3
>
> **Q: "What happens, step by step, when you run `kubectl apply -f deployment.yaml`?"**
>
> **A:**
> 1. `kubectl` reads the YAML, converts it to JSON, and sends an HTTPS request to the API
>    Server.
> 2. The API Server authenticates the request (who is this?) and authorizes it (is this
>    identity allowed to create/update Deployments in this namespace?).
> 3. The request passes through admission controllers, which may validate it (reject if
>    malformed or against policy) or mutate it (inject defaults).
> 4. The API Server writes the Deployment object to **etcd**.
> 5. The **Deployment controller** (in Controller Manager) notices a new/changed
>    Deployment and creates a matching **ReplicaSet** object.
> 6. The **ReplicaSet controller** notices the ReplicaSet wants N pods but 0 exist, and
>    creates N **Pod** objects (still unscheduled — no node assigned).
> 7. The **Scheduler** notices unscheduled pods, runs filter + score against all nodes,
>    and binds each pod to a chosen node.
> 8. The **kubelet** on each chosen node notices a pod has been assigned to it, pulls the
>    container image via the container runtime, and starts the container(s).
> 9. The kubelet begins running the pod's probes and reports status back to the API
>    Server, which is what `kubectl get pods` then shows you.
>
> **Q: "Why does Kubernetes route literally everything through the API Server instead of
> letting components like the Scheduler write to etcd directly?"**
>
> **A:** Centralizing all reads and writes through one component gives you one place to
> enforce authentication, authorization, validation, and mutation consistently for
> *every* actor in the system — kubectl users, controllers, kubelets, and third-party
> operators alike. It also means etcd's data model and consistency guarantees are fully
> owned by one component, which can manage things like optimistic concurrency (resource
> versions), watch streams, and admission logic in one place rather than every component
> needing to reimplement etcd-safe access patterns independently. It's a deliberate
> single point of (well-guarded) entry, not a single point of failure — multiple API
> Server replicas can run behind a load balancer for high availability.


---

# CHAPTER 4: Kubernetes Objects

## POD

The **Pod** is the smallest deployable unit in Kubernetes — notably, it is *not* a
container. A Pod is a wrapper around one or more containers that are guaranteed to be
co-located on the same node and share:

- **A single IP address** — every container in a pod shares one network namespace, so
  they reach each other over `localhost`, and the outside world sees one IP for the
  whole pod.
- **Volumes** — a volume defined at the pod level can be mounted into multiple containers
  within that pod.
- **Lifecycle** — containers in a pod start and stop together; the pod as a whole has one
  lifecycle, even though individual containers within it can restart independently.

```
                    Pod (one shared network namespace + IP: 10.244.1.7)
   +-----------------------------------------------------------------+
   |                                                                     |
   |   +----------------------+        +-------------------------+   |
   |   |  Container: app         |        |  Container: log-shipper    |   |
   |   |  (main application,     |<------>|  (sidecar — tails app's    |   |
   |   |   listens on :8080)     | shared |   log files, ships them    |   |
   |   |                          | volume |   to a log backend)        |   |
   |   +----------------------+        +-------------------------+   |
   |                                                                     |
   +-----------------------------------------------------------------+
```

**The sidecar pattern.** Most production pods run more than one container by design —
not because the app needs multiple processes, but because a *helper* container needs to
share the app's network and/or filesystem. Common sidecars: a log-collection agent
tailing the app's log files from a shared volume; a service-mesh proxy (e.g. Envoy in
Istio) transparently intercepting all inbound/outbound traffic for mTLS and observability;
a config-reloader watching a mounted ConfigMap volume for changes.

### Pod lifecycle

A pod moves through a small set of phases:

```
  Pending  --->  Running  --->  Succeeded   (ran to completion, e.g. a Job)
                     |
                     +------->  Failed       (a container exited non-zero and
                     |                        won't be restarted, per restartPolicy)
                     |
                     +------->  Unknown      (node unreachable — kubelet stopped
                                              reporting status)
```

- **Pending** — the pod has been accepted by the cluster, but one or more containers
  aren't running yet (commonly: not yet scheduled to a node, or its image is still being
  pulled).
- **Running** — the pod has been scheduled, and at least one container is running (or
  starting/restarting).
- **Succeeded / Failed** — terminal states, typically only relevant to run-to-completion
  workloads like Jobs; long-running services (web servers, APIs) aren't expected to reach
  these states under normal operation.
- **Unknown** — the kubelet has stopped reporting the pod's status, usually because its
  node is unreachable.

Within "Running," each individual **container** also has its own state, visible via
`kubectl describe pod`:

- **Waiting** — not running yet, most often because its image is still being pulled, or
  it's waiting on an init container to finish.
- **Running** — the container's process is executing.
- **Terminated** — the container has stopped, either by exiting (with an exit code) or by
  being killed.

## PROBES

Probes are how the kubelet answers "is this container actually working?" — the
foundation of self-healing and zero-downtime traffic routing.

| Probe | Question it answers | What happens if it fails |
|---|---|---|
| `livenessProbe` | Is the container alive (not deadlocked/hung)? | kubelet **kills and restarts** the container |
| `readinessProbe` | Is the container ready to receive traffic right now? | The pod is **removed from the Service's endpoints** (no traffic sent, container is NOT restarted) |
| `startupProbe` | Has a slow-starting container finished its startup sequence yet? | Liveness/readiness probes are **held off** until this succeeds; if it never succeeds within its threshold, the container is killed and restarted |

The liveness/readiness distinction matters a great deal: a container that's temporarily
overloaded and slow to respond should usually fail its **readiness** probe (stop new
traffic, but don't restart — it'll recover and traffic will resume) rather than its
**liveness** probe (which would kill and restart it, potentially compounding the
problem under load with a thundering herd of restarts).

`startupProbe` exists for applications with a long, variable startup time (e.g. a JVM
app loading a large cache on boot). Without it, you'd be forced to set a very generous
`initialDelaySeconds` on the liveness probe to avoid killing the container mid-startup —
but that same generous delay then means a genuinely hung container, post-startup, takes
much longer to be detected and restarted. `startupProbe` lets you have a long grace
period for startup *and* a tight, fast-reacting liveness probe once the app is actually
running.

### Probe types

```yaml
# HTTP probe — kubelet sends a GET request; any 200-399 response = success
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 10   # wait this long after container start before first probe
  periodSeconds: 10         # how often to probe
  timeoutSeconds: 2         # how long to wait for a response before counting as failed
  failureThreshold: 3       # consecutive failures before taking action

# TCP probe — kubelet just checks whether it can open the port. Useful for
# non-HTTP services (databases, raw TCP servers) with no health endpoint.
readinessProbe:
  tcpSocket:
    port: 5432
  periodSeconds: 5
  failureThreshold: 2

# exec probe — kubelet runs a command inside the container; exit code 0 = success
livenessProbe:
  exec:
    command: ["sh", "-c", "pg_isready -U postgres"]
  periodSeconds: 15
```

## DEPLOYMENT

A Deployment is the standard way to run a stateless, replicated, long-lived workload. It
doesn't manage Pods directly — it manages a **ReplicaSet**, which in turn manages the
Pods. The Deployment's job specifically is to manage *change over time*: rolling updates,
and rollback if something goes wrong.

```
   Deployment "order-api"  (spec.replicas: 3, image: order-api:1.4.0)
        |
        |  creates/owns
        v
   ReplicaSet "order-api-7f8d9c"  (desired: 3, image: order-api:1.4.0)
        |
        |  creates/owns
        v
   Pod        Pod        Pod
```

When you update the Deployment's pod template (e.g. a new image tag), it doesn't edit
the existing ReplicaSet's pods — it creates a **new** ReplicaSet for the new template,
and gradually shifts replica counts from the old ReplicaSet to the new one. This is what
gives you a clean rollback target: the old ReplicaSet (and its template) still exists,
scaled to 0, ready to be scaled back up if you `kubectl rollout undo`.

### Rolling updates: maxSurge and maxUnavailable

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1          # how many EXTRA pods (above desired count) are allowed
                            # during the rollout
      maxUnavailable: 0    # how many pods are allowed to be UNAVAILABLE during
                            # the rollout (0 = never drop below desired capacity)
```

### Step-by-step rolling update trace (3 replicas, maxSurge=1, maxUnavailable=0)

```
Start:    [v1] [v1] [v1]                          3 running, all v1

Step 1:   [v1] [v1] [v1] [v2-starting]             surge to 4 (maxSurge=1 allows it)
                              ^ new pod created, waiting on readiness probe

Step 2:   [v1] [v1] [v1] [v2-ready]                v2 pod passes readiness,
                                                    joins Service endpoints

Step 3:   [v1] [v1] [terminating] [v2-ready]       1 old pod terminated
                                                    (maxUnavailable=0 means this only
                                                     happens AFTER a new pod is ready,
                                                     keeping capacity at >= 3 throughout)

Step 4:   [v1] [v1] [v2-ready] [v2-starting]        repeat: surge again, start next v2

  ... pattern repeats until all 3 pods are v2 ...

End:      [v2] [v2] [v2]                           3 running, all v2, old
                                                    ReplicaSet scaled to 0 (not deleted)
```

At no point does available capacity drop below 3 (the desired count), and at no point
does it exceed 4 (3 desired + maxSurge of 1) — that's the contract `maxSurge`/
`maxUnavailable` enforce, and it's why a properly configured readiness probe is *not
optional* for safe rolling updates: the rollout uses readiness, not just "container
started," to decide when it's safe to terminate the next old pod.

### kubectl commands for rollouts

```bash
kubectl rollout status deployment/order-api          # watch a rollout in progress
kubectl rollout history deployment/order-api          # list revision history
kubectl rollout history deployment/order-api --revision=3   # detail on one revision
kubectl rollout undo deployment/order-api              # roll back to the previous revision
kubectl rollout undo deployment/order-api --to-revision=2   # roll back to a specific revision
kubectl rollout pause deployment/order-api              # pause a rollout mid-flight
kubectl rollout resume deployment/order-api             # resume a paused rollout
kubectl rollout restart deployment/order-api            # force a fresh rollout of the SAME image
                                                          # (e.g. to pick up a changed ConfigMap)
```

### Full production Deployment YAML — Order Management API

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-api
  namespace: production
  labels:
    app: order-api
spec:
  replicas: 3
  revisionHistoryLimit: 5        # how many old ReplicaSets to keep around for rollback
  selector:
    matchLabels:
      app: order-api
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: order-api
    spec:
      # Spread the 3 replicas across different nodes where possible, so a
      # single node failure can't take down every replica at once.
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values: ["order-api"]
                topologyKey: "kubernetes.io/hostname"
      terminationGracePeriodSeconds: 30
      containers:
        - name: order-api
          image: ghcr.io/example-org/order-api:1.4.0
          ports:
            - containerPort: 3000
              name: http
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: order-api-secrets
                  key: database-url
            - name: LOG_LEVEL
              valueFrom:
                configMapKeyRef:
                  name: order-api-config
                  key: log-level
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          startupProbe:
            httpGet:
              path: /healthz
              port: 3000
            failureThreshold: 30    # 30 x 2s = up to 60s to finish starting
            periodSeconds: 2
          livenessProbe:
            httpGet:
              path: /healthz
              port: 3000
            initialDelaySeconds: 0  # startupProbe already covers startup time
            periodSeconds: 10
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            periodSeconds: 5
            failureThreshold: 2
          lifecycle:
            preStop:
              # Gives load balancers/kube-proxy time to stop sending new
              # traffic BEFORE the app actually starts shutting down,
              # avoiding a race where requests land on a pod that's
              # already terminating. Runs concurrently with the SIGTERM
              # the kubelet sends at the start of termination.
              exec:
                command: ["sh", "-c", "sleep 5"]
          securityContext:
            runAsNonRoot: true
            runAsUser: 1001
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
            capabilities:
              drop: ["ALL"]
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
```

A quick note on `terminationGracePeriodSeconds` + `preStop` together: when a pod is
deleted, Kubernetes (1) immediately removes it from Service endpoints and (2) sends
SIGTERM to the container, then waits up to `terminationGracePeriodSeconds` before
sending SIGKILL. The `preStop` hook (here, a 5-second sleep) runs *before* SIGTERM is
delivered to the main process, buying time for in-flight requests and propagation delay
across the cluster's networking layer, so the app's actual shutdown logic (closing DB
connections, finishing in-flight requests) has the *remaining* grace period to complete
cleanly.

## STATEFULSET

A Deployment's pods are interchangeable — `order-api-7f8d9c-x7k2p` could be killed and
replaced with `order-api-7f8d9c-m4j1q` and nothing downstream would notice or care. That
model breaks for stateful systems like databases, where each replica has its own data and
its own role (e.g. a primary and two read replicas) — replica identity matters.
**StatefulSet** exists for exactly this case, providing three guarantees Deployments
don't:

1. **Stable, predictable pod identity** — pods are named `<statefulset-name>-0`,
   `<statefulset-name>-1`, `<statefulset-name>-2`, ... not random suffixes, and a
   replaced pod gets *the same* name and ordinal back.
2. **Stable network identity** — each pod gets its own stable DNS name
   (`postgres-0.postgres.default.svc.cluster.local`), so other systems can address a
   *specific* replica, not just "any replica behind a Service."
3. **Stable storage** — each pod gets its **own** PersistentVolumeClaim, created from a
   `volumeClaimTemplate`, and that exact PVC is **reattached** to the same-named pod if it
   restarts or is rescheduled — the data persists, it isn't shared or recreated.

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres        # headless Service providing per-pod DNS (see Chapter 5)
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:16-alpine
          ports:
            - containerPort: 5432
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 20Gi
```

StatefulSets also start and stop **in order** by default: `postgres-0` must be Running
and Ready before `postgres-1` is created, and on scale-down, the highest ordinal is
terminated first. This ordering matters for systems with bootstrapping dependencies
(e.g. a cluster's first node initializing before others join it).

**When to use a StatefulSet:** databases (PostgreSQL, MySQL, MongoDB), and distributed
systems where node identity matters (Kafka brokers, ZooKeeper ensembles, Elasticsearch
data nodes). If your workload is stateless and replicas are truly interchangeable, use a
Deployment — it's simpler and rolls out faster.

## DAEMONSET

A DaemonSet guarantees that exactly **one** copy of a pod runs on every node in the
cluster (or every node matching a selector) — and automatically adds a pod when a new
node joins, and removes it when a node leaves. This is the right tool whenever "one per
node" is the actual requirement, rather than "N total, anywhere."

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd-log-collector
  namespace: kube-system
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      containers:
        - name: fluentd
          image: fluent/fluentd:v1.16
          resources:
            requests:
              cpu: "100m"
              memory: "200Mi"
          volumeMounts:
            - name: varlog
              mountPath: /var/log
      volumes:
        - name: varlog
          hostPath:
            path: /var/log
```

**Common DaemonSet use cases:** log collection agents (Fluentd, Filebeat) that need to
read every node's log directory; monitoring/metrics agents (node-exporter) that report
per-node hardware metrics; and CNI network plugins, which by their nature must run on
every node to provide that node's networking.

## CONFIGMAP AND SECRET

Both objects exist to separate configuration from the container image, so the *same*
image can run unmodified across dev, staging, and production, each with different
configuration injected at deploy time. The split between them is about sensitivity, not
mechanism:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: order-api-config
data:
  log-level: "info"
  feature-flags.json: |
    {"newCheckoutFlow": true, "betaDiscounts": false}
```

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: order-api-secrets
type: Opaque
data:
  # NOTE: values here are base64-ENCODED, not encrypted. Anyone with read
  # access to this Secret object (e.g. via the API, or a backup of etcd)
  # can trivially decode it: `echo <value> | base64 -d`
  database-url: cG9zdGdyZXM6Ly91c2VyOnBhc3NAaG9zdDo1NDMyL2Ri
```

Both can be consumed the same two ways — as **environment variables** or as **mounted
volume files**:

```yaml
# As an environment variable
env:
  - name: LOG_LEVEL
    valueFrom:
      configMapKeyRef:
        name: order-api-config
        key: log-level

# As a mounted file (useful for larger config, or files an app re-reads on change)
volumeMounts:
  - name: feature-flags
    mountPath: /etc/config
volumes:
  - name: feature-flags
    configMap:
      name: order-api-config
```

### Secret is NOT encrypted by default — and what to actually do about it

This is one of the most common Kubernetes misconceptions: a `Secret` object's `data`
field is **base64-encoded, not encrypted.** Base64 is an encoding, not a cipher — it
provides zero confidentiality. Anyone who can `kubectl get secret -o yaml`, or who has
read access to an etcd backup, can decode it instantly. (Kubernetes *does* support
**encryption at rest** for etcd itself via an `EncryptionConfiguration`, which is a
separate, cluster-admin-level control most managed Kubernetes offerings enable by
default — but the Secret *object*, as returned by the API, is still base64, not cipher
text, to any client authorized to read it.)

**The production solution is to never let plaintext secrets sit in YAML files (especially
ones checked into git) in the first place.** Two common patterns:

- **Sealed Secrets** (Bitnami) — you encrypt a Secret client-side with a public key
  before committing it to git; only the in-cluster Sealed Secrets controller, holding the
  matching private key, can decrypt it back into a real Secret object. Safe to commit the
  *sealed* version to source control.
- **External Secrets Operator** — the Secret's actual value lives in an external secrets
  manager (AWS Secrets Manager, HashiCorp Vault, GCP Secret Manager), and an in-cluster
  controller syncs it into a native Kubernetes Secret automatically. Nothing
  secret-shaped is ever stored in git at all.

For ad-hoc or smaller setups, even just creating Secrets imperatively via `kubectl`
(rather than writing base64 by hand into a YAML file that then gets committed) avoids the
most common leak vector — a plaintext-adjacent Secret manifest sitting in version
control history forever, even if it's later deleted from the latest commit:

```bash
kubectl create secret generic order-api-secrets \
  --from-literal=database-url='postgres://user:pass@host:5432/db' \
  --namespace=production

# Or from a file, without ever putting the value on your shell history / a YAML file:
kubectl create secret generic tls-cert \
  --from-file=tls.crt=./server.crt \
  --from-file=tls.key=./server.key
```

---

> ### 🎤 Interview Corner — Chapter 4
>
> **Q: "Your Deployment's rollout is stuck — new pods are `Running` but the rollout never
> finishes. What's the most likely cause?"**
>
> **A:** Almost always a failing **readiness probe** on the new pods. The rollout
> mechanism doesn't consider a new pod "available" just because its container process is
> `Running` — it specifically waits for the pod to pass its readiness probe before it will
> terminate the next old pod (when `maxUnavailable: 0`). If the new pods are crash-free
> but never become Ready — wrong probe path, app listening on a different port than the
> probe checks, a missing dependency the readiness check verifies — the rollout will sit
> there indefinitely (or until `progressDeadlineSeconds` triggers a `ProgressDeadlineExceeded`
> condition). The fix is to `kubectl describe pod` on one of the new pods, check the probe
> configuration against what the app actually exposes, and check the app's logs for why
> the readiness endpoint itself might be failing.
>
> **Q: "Why can't you just use a Deployment for a PostgreSQL database instead of a
> StatefulSet?"**
>
> **A:** A Deployment's pods are interchangeable by design — if you scale a Deployment to
> 3 and one pod is deleted, its replacement gets a fresh random name, and (depending on
> the volume setup) could even end up reusing a *different* PersistentVolumeClaim than
> the pod it replaced, since Deployments don't guarantee a stable 1:1 mapping between a
> specific pod identity and a specific volume. For a database, that's catastrophic — you
> need the replica that thinks it's "the primary with this exact data on disk" to
> reliably come back as that same identity with that same disk attached after a restart,
> not a fresh, anonymous replica. StatefulSet provides exactly that: stable ordinal
> names, a dedicated PVC per ordinal that follows that ordinal across restarts and
> rescheduling, and ordered startup — which is also why some clustered databases use the
> ordinal itself (`postgres-0`, `postgres-1`) to determine bootstrap roles like
> "initialize as primary" vs "join as replica."


---

# CHAPTER 5: Networking

## SERVICE

### Why Services exist

Every pod gets its own IP address — but that IP is **not stable.** When a pod is deleted
and recreated (a crash, a rolling update, a rescheduled pod after a node failure), its
replacement gets a **brand new IP.** If `order-api`'s 3 pods are talking directly to
`payment-service`'s pods by IP, every single rollout or crash of `payment-service` would
silently break that connection for every caller that cached the old IPs.

A **Service** solves this by giving a *group* of pods (selected by label, exactly like
a Deployment selects its pods) one **stable virtual IP (ClusterIP)** that never changes,
for the lifetime of the Service object — regardless of how many times the underlying
pods are replaced.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: order-api
spec:
  selector:
    app: order-api          # routes traffic to any pod with this label
  ports:
    - port: 80               # the Service's own port
      targetPort: 3000        # the port the CONTAINER actually listens on
  type: ClusterIP
```

### The four Service types

| Type | Reachable from | Typical use |
|---|---|---|
| `ClusterIP` (default) | Inside the cluster only | Internal service-to-service traffic — the overwhelming majority of Services |
| `NodePort` | Any node's IP, on a fixed high port (30000–32767) | Quick local/dev access; rarely used directly in production |
| `LoadBalancer` | The public internet, via a cloud provider's load balancer | Production-facing entry points (often fronted by an Ingress instead — see below) |
| `ExternalName` | N/A — it's a DNS CNAME, not a proxy | Giving an in-cluster DNS name to an *external* resource, e.g. a managed RDS database, so in-cluster code can address it like any other Service |

```yaml
# NodePort — exposes the Service on every node's IP at a fixed port
apiVersion: v1
kind: Service
metadata:
  name: order-api-nodeport
spec:
  type: NodePort
  selector:
    app: order-api
  ports:
    - port: 80
      targetPort: 3000
      nodePort: 30080

---
# LoadBalancer — cloud provider provisions a real external load balancer
# (an AWS NLB/ELB, in an EKS cluster) and points it at this Service
apiVersion: v1
kind: Service
metadata:
  name: order-api-public
spec:
  type: LoadBalancer
  selector:
    app: order-api
  ports:
    - port: 443
      targetPort: 3000

---
# ExternalName — gives a managed external database an in-cluster DNS name
apiVersion: v1
kind: Service
metadata:
  name: legacy-database
spec:
  type: ExternalName
  externalName: legacy-db.abc123xyz.us-east-1.rds.amazonaws.com
```

### Service discovery: CoreDNS

Every Service automatically gets a predictable DNS name, served by the cluster's internal
DNS server, **CoreDNS**:

```
<service-name>.<namespace>.svc.cluster.local
```

So `order-api` in the `production` namespace is reachable cluster-wide as
`order-api.production.svc.cluster.local` — or, from *within* the same namespace, simply
as `order-api` (Kubernetes' DNS search-domain configuration resolves the short name).
This is the cluster-scale version of the same name-based discovery pattern Docker Compose
gave you for a single host in Chapter 2 — "talk to your dependency by its name, let the
platform handle the IP."

### How kube-proxy actually implements Service routing

A Service's ClusterIP is **virtual** — it's not bound to any real network interface
anywhere in the cluster. What makes traffic to that IP actually reach a real pod is
**kube-proxy**, running on every node, which watches the API Server for every Service and
its current set of healthy backing pod IPs (called **Endpoints**), and programs the
node's **iptables** (or, in higher-throughput setups, **IPVS**) rules accordingly:

```
  Client pod sends packet to:  order-api ClusterIP (10.96.45.12:80)
                |
                v
  Node's iptables rules (programmed by kube-proxy) intercept it:
       "packets to 10.96.45.12:80 -> DNAT to one of:
            10.244.1.7:3000  (pod 1)
            10.244.2.9:3000  (pod 2)
            10.244.3.4:3000  (pod 3)
        (chosen pseudo-randomly, roughly even distribution)"
                |
                v
  Packet is rewritten and delivered directly to the chosen pod's real IP
```

Because this happens at the kernel networking layer (iptables/IPVS), it's invisible to
the application — the app just sees a normal TCP connection to the Service's ClusterIP,
and the kernel handles getting it to a real, currently-healthy pod. (Only pods currently
passing their readiness probe are included in a Service's Endpoints — this is the
mechanical link between readiness probes in Chapter 4 and "Services never route traffic
to a pod that isn't ready," mentioned there.)

## INGRESS

### Why Ingress exists

A `LoadBalancer` Service provisions one real, billed cloud load balancer **per Service.**
A realistic application with 15 internal APIs, each needing external HTTPS access, would
mean 15 separate cloud load balancers — expensive, and a management headache (15 sets of
DNS records, 15 TLS certificates to provision and rotate).

**Ingress** solves this by putting **one** load balancer (and one **Ingress
controller** — typically an nginx, Traefik, or cloud-native proxy running as pods inside
the cluster) in front of *all* of them, and routing incoming requests to the right
internal Service based on the request's **hostname** and/or **URL path.**

```
                      Internet
                          |
                          v
              +---------------------+
              |  ONE LoadBalancer      |
              |  (cloud provider)       |
              +---------------------+
                          |
                          v
              +---------------------+
              |  Ingress Controller     |
              |  (nginx pods, reads     |
              |   Ingress resources)    |
              +---------------------+
                /        |         \
       host/path     host/path    host/path
       routing       routing      routing
              /            |            \
             v             v             v
   +---------------+ +---------------+ +---------------+
   | Service:         | | Service:         | | Service:         |
   | order-api          | | payment-api        | | inventory-api      |
   | (ClusterIP)        | | (ClusterIP)        | | (ClusterIP)        |
   +---------------+ +---------------+ +---------------+
```

The Ingress controller is itself just pods running inside the cluster — it watches the
API Server for `Ingress` objects (plain Kubernetes resources, like anything else) and
reconfigures its own routing rules (e.g. regenerating an nginx config and reloading)
whenever they change. Only the controller's own *entry point* — typically a single
`LoadBalancer` Service in front of the controller's pods — needs a real cloud load
balancer; everything after that is in-cluster routing.

### Full Ingress YAML — host-based and path-based routing, with TLS

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: production-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    # cert-manager watches for this annotation and automatically requests
    # (and renews) a TLS certificate from the named ClusterIssuer.
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.example.com
        - admin.example.com
      secretName: example-com-tls    # cert-manager writes the issued cert here
  rules:
    # Host-based routing: requests to api.example.com go here...
    - host: api.example.com
      http:
        paths:
          # ...and path-based routing further splits traffic within that host
          - path: /orders
            pathType: Prefix
            backend:
              service:
                name: order-api
                port:
                  number: 80
          - path: /payments
            pathType: Prefix
            backend:
              service:
                name: payment-api
                port:
                  number: 80
          - path: /inventory
            pathType: Prefix
            backend:
              service:
                name: inventory-api
                port:
                  number: 80
    # A completely different hostname, routed to a different backend entirely
    - host: admin.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: admin-dashboard
                port:
                  number: 80
```

**TLS termination with cert-manager and Let's Encrypt.** Provisioning and rotating TLS
certificates by hand doesn't scale past a handful of domains. `cert-manager` is a
cluster controller that watches for the `cert-manager.io/cluster-issuer` annotation
(or a dedicated `Certificate` object) on an Ingress, automatically performs the Let's
Encrypt domain-validation challenge (typically HTTP-01 or DNS-01), obtains a real
certificate, stores it in the named Secret (`example-com-tls` above), and **automatically
renews it** before expiry — so TLS for every domain on the Ingress is fully hands-off
after the initial `ClusterIssuer` setup.

## KUBERNETES NETWORKING DEEP DIVE

Three rules form the foundation of the entire Kubernetes networking model (formally, the
**Kubernetes Container Network Interface / "flat network" model**):

1. **Every pod gets its own unique IP**, drawn from the cluster's overall Pod CIDR range
   (e.g. `10.244.0.0/16`) — not shared with other pods, not the node's own IP.
2. **Pods can reach all other pods' IPs directly, across nodes, without NAT.** A pod on
   `node-1` can send a packet straight to a pod's real IP on `node-2`, and it arrives
   with the *originating pod's real IP* still intact as the source address — there's no
   address translation hiding who actually sent it.
3. **Nodes can reach all pods, and vice versa**, also without NAT.

Implementing rule 2 — routing pod-to-pod traffic *across different physical/virtual
nodes* — is the job of a **CNI (Container Network Interface) plugin**. Kubernetes itself
doesn't implement pod networking; it delegates to a pluggable CNI implementation,
commonly **Calico**, **Flannel**, or **Cilium**. These differ in mechanism (some use
simple overlay/VXLAN encapsulation, some do native L3 routing, some use eBPF for higher
performance) but all satisfy the same contract above.

```
   Node A (10.0.1.5)                         Node B (10.0.1.6)
   +------------------------+               +------------------------+
   |  Pod X: 10.244.1.7        |               |  Pod Y: 10.244.2.9        |
   |    sends packet to            |               |                              |
   |    10.244.2.9 directly     |  CNI plugin   |                              |
   |                              |--routes the-->|  receives packet,             |
   |                              |  packet       |  source IP is STILL          |
   |                              |  across nodes |  10.244.1.7 (no NAT)         |
   +------------------------+               +------------------------+
```

**Why "no NAT" matters in practice:** it dramatically simplifies security policy and
observability. Because the real source pod IP is preserved end-to-end, a NetworkPolicy
or an access log on Pod Y can identify *exactly which pod* sent a given packet, rather
than seeing a translated, ambiguous node-level IP. Compare this to typical Docker
single-host networking or classic NAT'd cloud VPCs, where you frequently lose the
original source identity a few hops in.

## NETWORKPOLICY

### The default is wide open

Out of the box, with no NetworkPolicy objects defined, **every pod in a Kubernetes
cluster can send traffic to every other pod**, across every namespace, with no
restriction. This is convenient for getting started, and a real liability in production
— a compromised pod in a low-stakes namespace can, by default, freely probe and connect
to your database pods in a "production" namespace right next to it.

### The standard pattern: deny-all baseline + explicit allows

```yaml
# Step 1: a deny-all baseline for a namespace — selects ALL pods, allows
# NOTHING in (no "ingress" rules listed = nothing is permitted)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}        # empty selector = applies to every pod in the namespace
  policyTypes:
    - Ingress

---
# Step 2: explicit allow — only order-api pods may receive traffic, and
# only from pods labeled "role: frontend", on port 3000
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-order-api
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: order-api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              role: frontend
      ports:
        - protocol: TCP
          port: 3000

---
# Step 3: an egress example — postgres pods may only be CONNECTED TO BY
# order-api, and may only themselves call out to DNS (required for any
# pod to resolve names at all) and nowhere else
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: postgres-egress-lockdown
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: postgres
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: UDP
          port: 53     # allow DNS resolution
        - protocol: TCP
          port: 53
```

A `NetworkPolicy`'s `podSelector` defines *which pods this policy applies to*; its
`ingress`/`egress` rules then define what's allowed *in addition to* the default-deny.
Rules can select by `podSelector` (specific pods, as above), `namespaceSelector` (entire
namespaces — useful for "allow anything in the `monitoring` namespace to scrape metrics
from anywhere"), or raw IP blocks (`ipBlock`, for external traffic).

One operational note: **NetworkPolicy enforcement depends entirely on the CNI plugin** —
Flannel, in its basic configuration, does not enforce NetworkPolicy at all (the objects
would apply with no effect), while Calico and Cilium do. Always confirm your chosen CNI
plugin actually enforces the policies before relying on them as a security boundary.

---

> ### 🎤 Interview Corner — Chapter 5
>
> **Q: "What happens, end to end, when one pod calls another pod through a Service's
> DNS name?"**
>
> **A:**
> 1. The calling pod resolves `order-api.production.svc.cluster.local` (or just
>    `order-api` from within the same namespace) via **CoreDNS**, which returns the
>    Service's stable **ClusterIP**.
> 2. The pod opens a TCP connection to that ClusterIP. The ClusterIP isn't bound to any
>    real interface — it's virtual.
> 3. On the way out, the local node's **kube-proxy**-programmed **iptables/IPVS** rules
>    intercept the packet and **DNAT** it to one of the Service's currently-Ready backing
>    pod IPs, chosen by the configured load-balancing algorithm.
> 4. If the destination pod is on a different node, the **CNI plugin** routes the packet
>    across nodes to the destination pod's real IP, preserving the original source IP
>    (no NAT at this layer).
> 5. The destination pod receives the connection on its real pod IP and port, completely
>    unaware any of the Service indirection happened — from its perspective, it's just a
>    normal inbound TCP connection.
>
> **Q: "You created a NetworkPolicy that should block traffic between two namespaces, but
> the traffic is still getting through. What's the first thing to check?"**
>
> **A:** Whether the cluster's CNI plugin actually **enforces** NetworkPolicy at all.
> NetworkPolicy is a Kubernetes API object, but Kubernetes itself doesn't implement the
> packet-filtering — that's delegated to the CNI plugin, exactly like pod networking
> itself. Some CNI plugins (basic Flannel configurations, in particular) accept and store
> NetworkPolicy objects via the API but never actually enforce them, silently leaving the
> cluster fully open despite policies that look correct on paper. The fix is either to
> switch to a CNI plugin that enforces NetworkPolicy (Calico, Cilium, and others), or, if
> already on one of those, to check the policy's `podSelector` and namespace labels
> carefully — a namespace missing an expected label, or a typo in a `matchLabels` value,
> is the next most common cause.


---

# CHAPTER 6: Resource Management and Autoscaling

## RESOURCES: requests and limits

Every container *should* declare two numbers for both CPU and memory: **requests** and
**limits.** They answer two different questions, and conflating them is one of the most
common sources of production incidents in Kubernetes.

```yaml
resources:
  requests:
    cpu: "250m"      # 250 millicores = 0.25 of one CPU core
    memory: "256Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

- **`requests` — "what this container is guaranteed to get, and what the Scheduler uses
  to decide placement."** When the Scheduler is choosing a node for a pod, it sums up the
  `requests` of everything already running on a node and only considers nodes with enough
  *unallocated* capacity left to satisfy the new pod's requests. Requests are a
  *reservation*, not a cap — a container can use more than its request if the node
  happens to have spare capacity at that moment.
- **`limits` — "the hard ceiling this container can never exceed."** Exceeding the
  **CPU** limit doesn't kill the container — the kernel's CFS scheduler simply
  **throttles** it, slowing it down to stay under the limit (which can look like
  mysterious latency spikes if you're not watching for throttling metrics). Exceeding the
  **memory** limit, by contrast, gets the container **OOMKilled** immediately by the
  kernel — memory isn't compressible the way CPU time is, so there's no "throttle"
  option; the container is simply killed and (per its restart policy) restarted.

### QoS classes

Kubernetes derives a **Quality of Service (QoS) class** for every pod automatically, from
how its requests/limits are set, and uses that class to decide **which pods get evicted
first** when a node runs out of resources:

| QoS Class | How it's assigned | Eviction priority | 
|---|---|---|
| **Guaranteed** | Every container has `requests == limits`, for both CPU and memory | Evicted **last** — most protected |
| **Burstable** | At least one container has a `requests`/`limits` set, but they aren't all equal | Evicted before Guaranteed, after BestEffort |
| **BestEffort** | **No** `requests` or `limits` set on any container at all | Evicted **first** — least protected. **Never use in production.** |

A `BestEffort` pod has made *no* claim on resources at all — the Scheduler can pack it
onto any node regardless of actual headroom, and the kubelet will kill it first,
without warning, the moment the node comes under memory pressure. There's no scenario
in a real production system where this tradeoff is worth it; every production
container should set at least `requests`, and most should set `limits` too.

### LimitRange

Relying on every engineer to remember to set requests/limits on every container doesn't
scale. A **LimitRange** lets a namespace enforce sane defaults and bounds automatically:

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: default-resource-limits
  namespace: production
spec:
  limits:
    - type: Container
      default:                 # applied if a container doesn't set its own limits
        cpu: "500m"
        memory: "512Mi"
      defaultRequest:          # applied if a container doesn't set its own requests
        cpu: "100m"
        memory: "128Mi"
      max:                     # hard ceiling — no container in this namespace may
        cpu: "2"               # request/limit more than this, even explicitly
        memory: "2Gi"
      min:                     # hard floor
        cpu: "50m"
        memory: "64Mi"
```

## HORIZONTAL POD AUTOSCALER (HPA)

### The algorithm

The HPA continuously evaluates one formula and adjusts replica count to match:

```
desiredReplicas = ceil( currentReplicas × ( currentMetricValue / targetMetricValue ) )
```

Concretely: if a Deployment has 4 replicas, targets 50% average CPU utilization, and is
currently averaging 80% CPU utilization across those 4 pods:

```
desiredReplicas = ceil( 4 × (80 / 50) ) = ceil( 6.4 ) = 7
```

The HPA scales the Deployment to 7 replicas, which (assuming load stays roughly constant)
should bring the *per-pod* average back down toward the 50% target, since the same total
load is now spread across more pods.

### Metric sources

- **CPU-based** (most common) — average CPU utilization across the target's pods,
  relative to their `requests.cpu` (which is why every autoscaled Deployment *must* set
  CPU requests — the percentage is meaningless without a baseline to measure against).
- **Memory-based** — same idea, for memory. Less commonly used for scaling decisions
  alone, since memory usage in many apps doesn't drop simply because you added more
  replicas (e.g. a memory leak scales linearly with replica count, it doesn't shrink).
- **Custom metrics** — anything else you can expose via a metrics adapter, most commonly
  **Prometheus** metrics surfaced through the `prometheus-adapter`, letting you scale on
  application-specific signals like queue depth, requests-per-second, or active
  connections — frequently a better leading indicator of needed capacity than CPU.

### stabilizationWindowSeconds — preventing flapping

Without damping, an HPA can "flap": scale up in response to a brief spike, then
immediately scale back down once the spike passes, then back up again — churning pods
constantly, with each new pod paying a cold-start cost that just makes the next spike
worse. `stabilizationWindowSeconds` fixes this by looking back over a recent window and
picking the **highest** desired-replica value seen in that window (for scale-*down*
decisions), rather than reacting instantly to the most recent single data point.

### Full HPA YAML with behavior section

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-api-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-api
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 70
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0       # react to scale-up needs immediately
      policies:
        - type: Percent
          value: 100                       # can at most DOUBLE replica count...
          periodSeconds: 60                # ...within any 60-second window
        - type: Pods
          value: 4                         # OR add at most 4 pods at once,
          periodSeconds: 60                # whichever policy allows MORE (max of the two)
      selectPolicy: Max
    scaleDown:
      stabilizationWindowSeconds: 300      # wait 5 minutes of sustained low usage
                                            # before scaling down at all — prevents
                                            # flapping on a brief lull in traffic
      policies:
        - type: Percent
          value: 10                        # remove at most 10% of replicas...
          periodSeconds: 60                # ...per 60-second window — gentle scale-down
      selectPolicy: Min
```

The asymmetry here is deliberate and standard practice: **scale up fast, scale down
slow.** Under-provisioning during a real traffic spike directly costs you failed
requests and unhappy users; over-provisioning for a few extra minutes after a spike
just costs a little extra compute spend. The behavior block lets you encode that
asymmetric risk tolerance directly, rather than relying on one timing knob for both
directions.

## PODDISRUPTIONBUDGET (PDB)

### Why it exists

The HPA and the Deployment controller protect you from *unplanned* disruption (crashes,
node failures) by replacing lost pods. But **voluntary** disruptions — a cluster admin
draining a node for an OS patch, an autoscaler removing an underutilized node, a cluster
version upgrade rolling through every node one at a time — can, without a PDB, evict
*every* pod of a given app simultaneously if they all happen to land on the node(s) being
drained at once, causing a full outage even though nothing actually "failed."

A **PodDisruptionBudget** tells the cluster (specifically, anything performing a
voluntary eviction via the Eviction API — `kubectl drain` and cluster-autoscaler both
respect it) the *minimum* capacity that must be preserved during any voluntary
disruption, and the eviction is simply **refused** if honoring it would violate that
budget.

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: order-api-pdb
  namespace: production
spec:
  minAvailable: 2          # at least 2 order-api pods must remain Ready at all times
                            # during a voluntary disruption — node drains pause/wait
                            # rather than evict a pod that would drop below this
  selector:
    matchLabels:
      app: order-api
```

```yaml
# Equivalent alternative phrasing, sometimes more convenient for a Deployment
# you intentionally autoscale a lot (since "minAvailable: 2" out of a
# fluctuating 3-20 replicas means very different things at different scale)
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: order-api-pdb-percent
  namespace: production
spec:
  maxUnavailable: 1        # at most 1 pod may be voluntarily disrupted at a time,
                            # regardless of current total replica count
  selector:
    matchLabels:
      app: order-api
```

`minAvailable` and `maxUnavailable` are two ways of expressing the same kind of
constraint — choose `minAvailable` when you have a fixed floor in mind, and
`maxUnavailable` when the constraint should scale naturally with replica count (common
for HPA-managed Deployments). A node drain command (`kubectl drain`) that would violate
an active PDB simply **blocks** on that pod until it's safe to proceed (or until the
operator overrides it explicitly), rather than evicting it anyway.

---

> ### 🎤 Interview Corner — Chapter 6
>
> **Q: "A container's CPU usage is well under its limit, but the app feels slow under
> load. The pod isn't being OOMKilled, and there are no obvious errors. What's
> happening?"**
>
> **A:** This is the classic CPU throttling symptom, and it's invisible in the most
> commonly-watched metric (CPU utilization percentage looks fine, often well under 100%
> of the limit, because throttling happens within sub-second scheduling windows that an
> averaged utilization metric smooths over). The kernel's CFS scheduler enforces a CPU
> `limit` by allocating the container a fixed quota of CPU-time per fixed period (e.g.
> 50ms of CPU time per 100ms period for a 500m limit) — once that quota is used up
       *within that period*, the container is paused until the next period starts, even
> if the node has completely idle CPU cores sitting right there. A bursty workload can
> exhaust its quota in the first few milliseconds of every period and spend the rest of
> each period throttled, which shows up as added latency, not as a utilization spike.
> The fix is usually to either raise the CPU limit (or remove it, accepting Burstable
> QoS instead of Guaranteed) or, ideally, to look directly at the
> `container_cpu_cfs_throttled_periods_total` metric (from cAdvisor/kube-state-metrics)
> rather than inferring throttling indirectly from utilization.
>
> **Q: "Your team is about to patch every node's OS in a rolling fashion. What stops this
> from taking your API completely down if all its replicas happen to land on the nodes
> being patched first?"**
>
> **A:** A correctly configured **PodDisruptionBudget**. Node draining (whether manual
> via `kubectl drain` or automated by a managed node-upgrade process) evicts pods through
> the Eviction API rather than just killing them outright, and the Eviction API checks
> every relevant PDB before allowing an eviction to proceed. If evicting a pod would
> violate its PDB's `minAvailable`/`maxUnavailable` constraint, the eviction is refused
> and the drain operation waits (or fails over to the next node, depending on tooling)
> until enough replacement pods elsewhere are Ready to make the eviction safe. Without a
> PDB defined at all, there's no such protection — a node drain (or several drained in
> quick succession) can evict every replica of an application simultaneously if that's
> simply where they happened to be scheduled, even though every individual node drain
> looks like an entirely "planned, safe" operation in isolation.


---

# CHAPTER 7: CI/CD with GitHub Actions and Helm

Every prior chapter assumed someone, somehow, gets a built image into a registry and a
correct YAML manifest applied to the cluster. This chapter automates that — turning
"engineer pushes code" into "tested, built, and safely deployed" without anyone running
`docker build` or `kubectl apply` by hand.

## GITHUB ACTIONS COMPLETE

### Full pipeline: test → build → push to GHCR → deploy to Kubernetes

```yaml
# .github/workflows/deploy.yml
name: Build, Test, and Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ---------- Job 1: test ----------
  # Runs on EVERY push and pull request. Nothing builds or deploys unless
  # this passes — combined with branch protection (below), this is what
  # makes "tests must pass before merge" actually enforced, not just a
  # social convention.
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Run unit tests
        run: npm test -- --coverage

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/

  # ---------- Job 2: build and push ----------
  # Only runs on pushes to main (not on PRs — we don't want to publish an
  # image for every branch's PR, only what actually merges), and only
  # after "test" succeeds (the "needs:" key below enforces the order).
  build-and-push:
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write          # required to push to GHCR
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          # GITHUB_TOKEN is auto-provisioned per workflow run — no manual
          # secret needed for GHCR specifically. For pushing to Docker Hub
          # instead, you'd reference repository secrets here, e.g.:
          #   username: ${{ secrets.DOCKER_USERNAME }}
          #   password: ${{ secrets.DOCKER_PASSWORD }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata (tags, labels)
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=raw,value=latest

      - name: Build and push image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ---------- Job 3: deploy ----------
  # Gated behind the "production" GitHub Environment — see below for what
  # that buys you (manual approval before this job is allowed to run).
  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://api.example.com
    steps:
      - uses: actions/checkout@v4

      - name: Configure kubeconfig
        run: |
          mkdir -p ~/.kube
          echo "${{ secrets.KUBE_CONFIG_BASE64 }}" | base64 -d > ~/.kube/config

      - name: Deploy with Helm
        run: |
          helm upgrade --install order-api ./charts/order-api \
            --namespace production \
            --values ./charts/order-api/values-prod.yaml \
            --set image.tag=${{ needs.build-and-push.outputs.image-tag }} \
            --wait --timeout 5m

      - name: Verify rollout
        run: kubectl rollout status deployment/order-api --namespace production
```

### Secrets: repository secrets

`DOCKER_USERNAME` / `DOCKER_PASSWORD` (or, for GHCR as above, the auto-issued
`GITHUB_TOKEN`) are stored under **Settings → Secrets and variables → Actions** in the
repository, never in the workflow file itself. They're injected at runtime via
`${{ secrets.NAME }}`, masked in logs automatically, and inaccessible to workflow runs
triggered from forks by default — a deliberate protection against a malicious PR
exfiltrating your registry credentials through a modified workflow file.

### GitHub Environments: a manual approval gate before production

A GitHub **Environment** (`environment: { name: production }` in the `deploy` job above)
lets you attach **protection rules** to a deploy target — most commonly, **required
reviewers**: the `deploy` job will build and sit paused, waiting, until a designated
person manually clicks "Approve" in the GitHub UI, no matter how fast the `test` and
`build-and-push` jobs finished. This gives you fully automated CI with a deliberate,
human-in-the-loop checkpoint specifically before anything touches production — automation
everywhere except the one place a human judgment call (timing, awareness of an ongoing
incident, a last look at the diff) is genuinely valuable.

Environments can also scope secrets — a `KUBE_CONFIG_BASE64` secret attached to the
`production` Environment specifically is only readable by jobs that reference that
Environment, keeping production cluster credentials inaccessible to, say, a staging
deploy job even within the same repository.

### Branch protection: require CI to pass before merge

Configured under **Settings → Branches → Branch protection rules** for `main`:

- **Require status checks to pass before merging** — select the `test` job (and any
  others) as required; GitHub will not allow a merge button to be clickable until that
  check reports success on the PR's latest commit.
- **Require branches to be up to date before merging** — re-runs checks against the
  latest `main` if the PR branch is behind, preventing a "passed when I branched, but
  main has since changed in a way that breaks this" merge.
- **Require pull request reviews before merging** — at least one approving review,
  separate from CI status, before merge is allowed.

Together, branch protection + the `test` job + the Environment approval gate give you
three independent checkpoints: automated correctness (tests), human code review (PR
approval), and human deployment judgment (Environment approval) — each catching a
different class of problem, none of them optional or bypassable by a single person.

## HELM CHARTS

### Why Helm

A real application's full set of Kubernetes manifests — Deployment, Service, Ingress,
ConfigMap, HPA, PDB, ServiceAccount, NetworkPolicy — is a lot of YAML, and a meaningful
chunk of it is *identical* across dev/staging/production except for a handful of values
(replica count, image tag, resource limits, hostnames). Maintaining three near-duplicate
copies of every manifest, hand-edited per environment, is exactly the kind of config
drift problem Chapter 1 described — except now it's *your* drift, not the platform's.

**Helm** packages a full set of Kubernetes manifests as a **chart**: templated YAML, with
the differences between environments extracted into a separate, small `values.yaml` file.
One chart, multiple value files, zero duplicated YAML structure.

### Chart structure

```
order-api/
├── Chart.yaml              # chart metadata: name, version, description
├── values.yaml             # DEFAULT values, used if no override is given
├── values-dev.yaml         # overrides specific to the dev environment
├── values-prod.yaml        # overrides specific to the prod environment
└── templates/
    ├── deployment.yaml      # templated Deployment (uses {{ .Values.* }})
    ├── service.yaml
    ├── ingress.yaml
    ├── hpa.yaml
    ├── pdb.yaml
    └── _helpers.tpl         # reusable template snippets (e.g. label sets)
```

```yaml
# Chart.yaml
apiVersion: v2
name: order-api
description: Order Management API Helm chart
type: application
version: 1.2.0          # chart version — bump when the TEMPLATES change
appVersion: "1.4.0"     # application version — typically tracks the image tag
```

```yaml
# values.yaml — sensible defaults
replicaCount: 2

image:
  repository: ghcr.io/example-org/order-api
  tag: latest
  pullPolicy: IfNotPresent

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 50

ingress:
  enabled: false
  host: ""
```

```yaml
# templates/deployment.yaml — note the {{ .Values.* }} template syntax
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app: {{ .Release.Name }}
    spec:
      containers:
        - name: {{ .Release.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

### values.yaml override per environment

```yaml
# values-dev.yaml — only the keys that differ from values.yaml need to be listed
replicaCount: 1

resources:
  requests:
    cpu: 50m
    memory: 64Mi
  limits:
    cpu: 200m
    memory: 256Mi

autoscaling:
  enabled: false
```

```yaml
# values-prod.yaml
replicaCount: 3

resources:
  requests:
    cpu: 250m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilizationPercentage: 50

ingress:
  enabled: true
  host: api.example.com
```

### Core Helm commands

```bash
helm create order-api                          # scaffold a new chart from a starter template

helm install order-api ./charts/order-api \      # first-time install
  --namespace production \
  --values ./charts/order-api/values-prod.yaml

helm upgrade order-api ./charts/order-api \      # update an existing release
  --namespace production \
  --values ./charts/order-api/values-prod.yaml \
  --set image.tag=1.4.1

helm upgrade --install order-api ./charts/order-api \   # the idiomatic CI/CD form:
  --namespace production \                              # installs if it doesn't exist
  --values ./charts/order-api/values-prod.yaml \         # yet, upgrades if it does —
  --set image.tag=1.4.1 --wait --timeout 5m              # exactly the pattern used in
                                                            # the deploy job above

helm rollback order-api 3                        # roll back to revision 3
helm history order-api                            # list all revisions of this release
helm get values order-api                         # show the values currently in use
helm template ./charts/order-api \                # render templates locally WITHOUT
  --values values-prod.yaml                        # installing anything — invaluable
                                                     # for reviewing exactly what YAML
                                                     # a values change would produce
helm uninstall order-api --namespace production    # remove a release entirely
```

`--set image.tag=...` deserves a callout: this is exactly how the GitHub Actions deploy
job above injects the freshly-built image's tag at deploy time, without needing to
hand-edit `values-prod.yaml` (and commit that edit) on every single deploy — the chart
defines *what* a deployment looks like structurally, the CI pipeline supplies *which
specific image* for *this* deploy.

---

> ### 🎤 Interview Corner — Chapter 7
>
> **Q: "Your GitHub Actions pipeline passed tests and pushed a new image, but the
> deploy job is just sitting there, not running. What's going on?"**
>
> **A:** Most likely the `deploy` job is gated behind a GitHub **Environment** with a
> required-reviewers protection rule, and it's correctly paused waiting for manual
> approval — this is expected, intended behavior, not a failure. Check the workflow run
> in the GitHub UI; a job waiting on Environment approval shows a distinct "Waiting"
> status with an explicit "Review deployments" action for an authorized approver. If
> that's not it, the next things to check are whether `deploy`'s `needs:` job
> (`build-and-push`) actually completed successfully — a job won't start if any of its
> `needs` dependencies failed or were skipped — and whether the workflow's trigger
> condition (`if: github.ref == 'refs/heads/main'`, in this pipeline) actually matched
> the event that ran it.
>
> **Q: "Why use Helm instead of just maintaining separate folders of raw YAML for dev,
> staging, and prod?"**
>
> **A:** Three raw-YAML folders that are 90% identical inevitably drift apart over time —
> someone fixes a probe path in `prod/deployment.yaml` during an incident and forgets to
> mirror it into `staging/deployment.yaml`, and six months later staging and prod are
> running meaningfully different configurations without anyone deciding that on purpose.
> Helm's templating separates the *structure* that should be identical everywhere (in
> `templates/`) from the *values* that should legitimately differ (replica count,
> resource sizing, hostnames, feature flags), so a structural fix — like that probe path
> — is made exactly once, in the template, and automatically applies to every
> environment's next deploy. It also gives you a recorded, named release history per
> environment (`helm history`) and a one-command rollback (`helm rollback`) to any prior
> revision, neither of which raw `kubectl apply -f` against a folder of YAML provides on
> its own.


---

# CHAPTER 8: AWS Fundamentals

Kubernetes doesn't run in a vacuum — it runs on top of real compute, storage, and
networking, and in production that's most commonly a cloud provider. This chapter covers
the AWS primitives that show up constantly once you're running Kubernetes for real:
who's allowed to do what (IAM), where things live on the network (VPC), what they run on
(EC2), where files and backups live (S3), where the database lives (RDS), and how all of
this comes together as a managed Kubernetes cluster (EKS).

## IAM (Identity and Access Management)

IAM controls **who** (or *what* — services count too) can do **what** to **which** AWS
resources.

- **Users** — an identity for a person (or occasionally a long-lived application),
  typically with their own login credentials and/or access keys.
- **Roles** — an identity *without* permanent credentials, **assumed temporarily** by a
  user, an AWS service, or (critically, for Kubernetes) a pod. Assuming a role grants
  short-lived, automatically-rotating credentials for the duration of the assumption.
  Roles, not long-lived user access keys, are the standard way services authenticate to
  other AWS services.
- **Policies** — JSON documents that define *exactly* which actions are allowed (or
  explicitly denied) on which resources, attached to a user, role, or group.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::order-api-uploads/*"
    }
  ]
}
```

**Principle of least privilege.** Grant exactly the permissions a role needs to do its
job, and nothing more — never `"Action": "*", "Resource": "*"` for a service identity
just because it's convenient. The policy above, for instance, grants an application's
role permission to read and write objects in *one specific bucket*, not list every
bucket in the account, not delete objects, not touch any other AWS service. The blast
radius of a compromised credential is bounded by exactly what its policy allows — a
narrowly-scoped role limits real damage if it's ever leaked or misused; an
overly-broad one turns any single compromise into an account-wide incident.

## VPC (Virtual Private Cloud)

A VPC is your own logically isolated slice of the AWS network — your own private IP
address range, subdivided into **subnets**, with explicit control over what can reach
what.

```
                              VPC (10.0.0.0/16)
   +-------------------------------------------------------------------+
   |                                                                     |
   |   +----------------------+         +----------------------+        |
   |   |  Public Subnet          |         |  Public Subnet          |        |
   |   |  (10.0.1.0/24)          |         |  (10.0.2.0/24)          |        |
   |   |  AZ: us-east-1a          |         |  AZ: us-east-1b          |        |
   |   |                          |         |                          |        |
   |   |  [ Load Balancer ]      |         |  [ NAT Gateway ]         |        |
   |   +----------------------+         +----------------------+        |
   |          ^                                    |                      |
   |          | Internet Gateway                   | private subnets'    |
   |          | (routes 0.0.0.0/0)                 | outbound traffic    |
   |          |                                    v                      |
   |   +----------------------+         +----------------------+        |
   |   |  Private Subnet         |         |  Private Subnet         |        |
   |   |  (10.0.11.0/24)         |         |  (10.0.12.0/24)         |        |
   |   |  AZ: us-east-1a          |         |  AZ: us-east-1b          |        |
   |   |                          |         |                          |        |
   |   |  [ EC2 / EKS nodes ]    |         |  [ RDS database ]       |        |
   |   |  [ RDS database ]       |         |  [ EC2 / EKS nodes ]    |        |
   |   +----------------------+         +----------------------+        |
   |                                                                     |
   +-------------------------------------------------------------------+
                      ^
                      |
                  Internet
```

- **Public subnets** have a route to an **Internet Gateway**, meaning resources in them
  (with a public IP) are directly reachable from, and can directly reach, the public
  internet. Reserved for things that genuinely need to be internet-facing: load
  balancers, bastion hosts.
- **Private subnets** have **no** route to the Internet Gateway — nothing inside them is
  directly reachable from the internet, regardless of security group configuration.
  This is where databases, internal application servers, and Kubernetes worker nodes
  belong: defense in depth, where even a security group misconfiguration can't expose
  them directly, because there's no network path to begin with.
- **NAT Gateway** — private subnets still often need *outbound* internet access (pulling
  container images, hitting external APIs, OS package updates) without being inbound-
  reachable. A NAT Gateway, placed in a public subnet, lets private-subnet resources
  initiate outbound connections (their source IP translated to the NAT Gateway's public
  IP) while remaining completely unreachable for *inbound* connections initiated from the
  internet.

Spreading subnets across multiple **Availability Zones** (`us-east-1a`, `us-east-1b`
above — physically distinct data centers within a region) is what gives this layout real
fault tolerance: an entire AZ outage still leaves resources in the other AZ's subnets
running.

## EC2 (Elastic Compute Cloud)

EC2 is AWS's virtual machine service — the literal "Era 2: Virtual Machines" technology
from Chapter 1, offered as a managed, on-demand cloud product. A few concepts that matter
operationally:

- **Instance types** — a name like `t3.medium` or `m5.xlarge` encodes a family (general
  purpose, compute-optimized, memory-optimized, GPU, etc.), a generation, and a size
  (vCPU/RAM combination). Picking the right family matters: a memory-heavy cache
  workload on a compute-optimized type wastes money on idle CPU it doesn't need, and vice
  versa.
- **Security groups** — a **stateful**, instance-level virtual firewall: a set of allow
  rules (no explicit deny rules — anything not allowed is implicitly denied) controlling
  inbound and outbound traffic. "Stateful" means a response to an allowed inbound
  request is automatically allowed back out, without needing a matching outbound rule.
- **SSH access** — EC2 instances are typically provisioned with a key pair; the public
  key is injected into the instance at launch (via `~/.ssh/authorized_keys`), and only
  someone holding the matching private key can SSH in. In a properly segmented VPC
  (above), SSH access to private-subnet instances usually goes through a **bastion
  host** in the public subnet, or, increasingly, through **AWS Systems Manager Session
  Manager**, which avoids exposing port 22 to anything at all, even a bastion.

## S3 (Simple Storage Service)

S3 is object storage — files (objects) stored in **buckets**, addressed by key, with
effectively unlimited capacity and no filesystem hierarchy to manage (the "folders" you
see in the console are a UI convenience over key prefixes, e.g. `uploads/2026/06/file.pdf`
is one flat key, not a literal directory tree).

**Presigned URLs** solve a common application problem: letting a user upload or download
a specific file directly to/from S3, without routing the (potentially large) file
through your application server, and without making the bucket itself publicly
readable/writable. Your backend, which *does* hold IAM credentials, generates a
time-limited, cryptographically-signed URL granting permission for exactly one
operation (e.g. `PUT` to exactly this one object key) for a short window (e.g. 15
minutes); the client then uploads/downloads directly against that URL.

```javascript
// Backend: generate a presigned URL for a client to upload directly to S3
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const s3 = new S3Client({ region: "us-east-1" });

const command = new PutObjectCommand({
  Bucket: "order-api-uploads",
  Key: `invoices/${orderId}.pdf`,
  ContentType: "application/pdf",
});

const presignedUrl = await getSignedUrl(s3, command, { expiresIn: 900 }); // 15 minutes
// Send `presignedUrl` to the client; the client PUTs the file directly to it.
```

## RDS (Relational Database Service)

RDS is AWS's managed relational database offering — PostgreSQL, MySQL, and others —
where AWS handles patching, backups, and failover infrastructure, in exchange for less
low-level control than a self-managed database on EC2.

```
                  Region: us-east-1
   +----------------------------------------------------------+
   |                                                              |
   |   AZ: us-east-1a                    AZ: us-east-1b           |
   |   +---------------------+         +---------------------+   |
   |   |  RDS PRIMARY            |  sync   |  RDS STANDBY            |   |
   |   |  (read + write)         |-------->|  (replicates, NOT       |   |
   |   |                          | replic. |   directly readable —  |   |
   |   |                          |         |   automatic failover   |   |
   |   |                          |         |   target only)         |   |
   |   +---------------------+         +---------------------+   |
   |              |                                                  |
   |              | async replication (separate from Multi-AZ)       |
   |              v                                                  |
   |   +---------------------+                                     |
   |   |  Read Replica            |   <-- application routes        |
   |   |  (READABLE, used to      |       read-heavy queries here    |
   |   |   offload read traffic)  |       to reduce primary load     |
   |   +---------------------+                                     |
   +----------------------------------------------------------+
```

- **Multi-AZ** — a synchronously-replicated standby in a *different* Availability Zone,
  existing purely for **automatic failover**: if the primary fails (or during planned
  maintenance), RDS automatically promotes the standby and repoints the database's
  endpoint to it, typically within a minute or two, without requiring any application
  reconfiguration. The standby is **not** directly queryable — it exists solely as a
  failover target, not a scaling mechanism.
- **Read replicas** — separate, asynchronously-replicated, independently queryable
  database instances, used to **scale read traffic** by directing read-heavy queries
  (reporting, analytics, read-only API endpoints) away from the primary. Because
  replication is asynchronous, read replicas can lag slightly behind the primary —
  acceptable for most read-scaling use cases, but a real consideration for anything
  requiring strict read-your-writes consistency.

These two features solve different problems and are commonly used **together**:
Multi-AZ for availability (the database survives an AZ failure), read replicas for
horizontal read scaling (the database handles more total query volume than one
instance could alone).

## EKS (Elastic Kubernetes Service)

EKS is AWS's managed Kubernetes offering. AWS runs and operates the **control plane**
(API Server, etcd, Scheduler, Controller Manager from Chapter 3) as a managed service —
highly available, patched, and backed up by AWS — while you manage the **worker nodes**
that actually run your pods.

```
   AWS-managed                         Your account, your VPC
   +-----------------------+          +----------------------------------+
   |   EKS Control Plane      |          |   Node Group (EC2 instances, or    |
   |   - API Server (HA)      |<-------->|   Fargate for serverless pods)     |
   |   - etcd (HA, backed up) |  kubelet |                                      |
   |   - Scheduler             |  <-->     |   [worker node] [worker node]      |
   |   - Controller Manager   |  API     |   [worker node] [worker node]      |
   |                           |  Server  |                                      |
   |  (you never SSH into       |          |   Your pods run here, in YOUR      |
   |   or directly manage       |          |   private subnets, governed by     |
   |   these components)        |          |   YOUR security groups            |
   +-----------------------+          +----------------------------------+
```

- **Node groups** — a managed set of EC2 instances (or, for serverless pod execution
  without managing EC2 instances at all, **Fargate**) that register themselves as
  Kubernetes worker nodes, running the kubelet, container runtime, and kube-proxy from
  Chapter 3. EKS can manage node group scaling, patching, and rolling updates for you
  (a "managed node group"), or you can self-manage your own EC2 Auto Scaling Group
  registered to the cluster for more control.
- **IAM Roles for Service Accounts (IRSA)** — the bridge between Kubernetes' own RBAC
  identity model and AWS IAM. Without it, giving a pod AWS permissions (e.g. "read from
  this S3 bucket") meant attaching broad IAM permissions to the *entire node's* instance
  role — every pod on that node, regardless of which application it belonged to, could
  then access anything the node could. IRSA lets you associate a specific Kubernetes
  **ServiceAccount** with a specific, narrowly-scoped IAM role, so only pods using that
  ServiceAccount can assume those permissions — least privilege (from the IAM section
  above) applied at the level of an individual application's pods, not an entire shared
  node.

```yaml
# A ServiceAccount annotated to assume a specific IAM role via IRSA
apiVersion: v1
kind: ServiceAccount
metadata:
  name: order-api
  namespace: production
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/order-api-s3-access
---
# The order-api Deployment's pods reference this ServiceAccount...
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-api
spec:
  template:
    spec:
      serviceAccountName: order-api    # ...and ONLY these pods can assume the role above
      containers:
        - name: order-api
          image: ghcr.io/example-org/order-api:1.4.0
```

---

> ### 🎤 Interview Corner — Chapter 8
>
> **Q: "Your application's pods need to read from an S3 bucket. What's wrong with just
> attaching an S3-read IAM policy to the EKS node group's EC2 instance role, and how do
> you do it properly?"**
>
> **A:** An IAM role attached to the node's EC2 instance profile is available to
> **every pod scheduled onto that node**, not just the application that's actually
> supposed to have S3 access — any other workload sharing that node (which, by default,
> pods from many different teams or applications might) inherits the same permissions
> by virtue of co-location, violating least privilege and making the actual scope of
> "what can read this bucket" effectively unauditable. The correct approach is **IAM
> Roles for Service Accounts (IRSA)**: create a narrowly-scoped IAM role with exactly
> the S3 permissions needed, annotate a dedicated Kubernetes ServiceAccount with that
> role's ARN, and have only the specific Deployment that needs S3 access reference that
> ServiceAccount via `serviceAccountName`. Permissions then follow the *application's
> identity*, not the node it happens to land on.
>
> **Q: "Why put your database in a private subnet instead of a public one with a
> restrictive security group?"**
>
> **A:** Security groups are a real and important control, but they're one layer, and
> layers can be misconfigured — a single overly broad inbound rule (`0.0.0.0/0` on the
> database port, added during a late-night debugging session and never removed) directly
> exposes a publicly-routable database to the entire internet. A private subnet removes
> the *network path* to the internet entirely, at the routing table level — there's no
> route to an Internet Gateway, so even a maximally permissive security group can't make
> the database internet-reachable, because traffic from the public internet has no way
> to arrive at that subnet in the first place. This is defense in depth: security groups
> remain the first line of access control *within* the private network, but the subnet
> placement itself is a structural backstop that doesn't depend on every security group
> rule being correct forever.


---

# CHAPTER 9: Observability

A Kubernetes cluster running 50 microservices across 200 pods is, by default, a black
box once something goes wrong — "which of the 200 pods is slow, and why?" isn't a
question `kubectl get pods` can answer. Observability is the set of practices and tools
that make that question answerable, built on three complementary pillars: **metrics**
(aggregated numbers over time), **logs** (discrete event records), and **traces**
(the path a single request took across services).

```
   METRICS                    LOGS                       TRACES
   "is something wrong,       "what exactly               "where, across
    and roughly where?"        happened, in detail?"        services, did
                                                              THIS request
   request rate, error        structured JSON log           spend its time?"
   rate, latency P99,         lines, one per event,
   CPU/memory saturation      searchable by trace ID        span-by-span
                                                              breakdown of one
   Prometheus + Grafana       Loki / ELK + Grafana           request's path

                                       |
                                       v
                            OpenTelemetry — unifies all
                            three under one instrumentation
                            standard, one trace ID linking
                            a metric spike to the specific
                            logs and traces that explain it
```

## Prometheus

Prometheus is a **metrics** system built around a deliberately simple model: it
periodically **scrapes** (pulls, via HTTP GET) a `/metrics` endpoint that each
application exposes, parses out a set of numeric time series, and stores them.

```yaml
# A Prometheus scrape config telling it where to find metrics endpoints
scrape_configs:
  - job_name: 'order-api'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      # Only scrape pods explicitly annotated as wanting to be scraped —
      # avoids Prometheus trying (and failing) to scrape every pod in
      # the cluster, most of which don't expose a /metrics endpoint at all
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

```yaml
# The corresponding annotation on the Deployment's pod template
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "3000"
    prometheus.io/path: "/metrics"
```

### PromQL basics

PromQL is Prometheus's query language, built around time series identified by a metric
name plus key-value **labels** (e.g. `http_requests_total{method="GET", status="200"}`).

```promql
# Raw counter value right now (rarely useful alone — counters only go up)
http_requests_total

# Per-second rate of increase over the last 5 minutes — THIS is how you
# actually use a counter: as a rate, not a raw cumulative total
rate(http_requests_total[5m])

# Error rate as a percentage: errors / total requests, both as rates
sum(rate(http_requests_total{status=~"5.."}[5m]))
  /
sum(rate(http_requests_total[5m])) * 100

# 99th percentile request latency, from a histogram metric
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Average memory usage per pod over the last hour, grouped by pod name
avg_over_time(container_memory_working_set_bytes{namespace="production"}[1h])
```

### Alert rules

```yaml
groups:
  - name: order-api-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{job="order-api",status=~"5.."}[5m]))
            /
          sum(rate(http_requests_total{job="order-api"}[5m])) > 0.05
        for: 5m              # must stay true for 5 CONSECUTIVE minutes before
                              # firing — avoids alerting on a brief, self-resolving blip
        labels:
          severity: critical
        annotations:
          summary: "order-api error rate above 5% for 5 minutes"
          description: "Current error rate: {{ $value | humanizePercentage }}"

      - alert: PodMemoryNearLimit
        expr: |
          container_memory_working_set_bytes{namespace="production"}
            /
          container_spec_memory_limit_bytes{namespace="production"} > 0.9
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Pod {{ $labels.pod }} is using >90% of its memory limit"
```

## Grafana

Grafana is the visualization layer on top of metrics (and logs) backends. It connects to
one or more **data sources** — Prometheus for metrics, **Loki** for logs being the most
common pairing — and renders both as dashboards, ideally letting an engineer pivot
directly from "this metric panel shows a spike" to "show me the logs from exactly that
pod, in that time window" without leaving the UI.

**Loki integration** specifically matters because Loki indexes logs by the *same* label
set Prometheus uses for metrics (pod, namespace, app, etc.) rather than indexing full
log text — which keeps it cheap to run at scale, and means a Grafana dashboard can link a
metrics panel and a logs panel through identical label selectors, letting you click a
spike on a graph and jump straight to the matching log lines for that exact pod and time
range.

## OpenTelemetry

Before OpenTelemetry, metrics, logs, and traces were typically instrumented with three
separate, incompatible libraries and SDKs per language, each with its own configuration,
its own way of tagging context, and no shared way to correlate "this trace" with "these
logs" with "this metric spike." **OpenTelemetry (OTel)** is a single, vendor-neutral
standard — one SDK, one set of conventions — for emitting all three signal types, with a
shared **trace context** that ties them together. The same `trace_id` that identifies a
distributed trace can be automatically attached to every log line and metric exemplar
produced during that request, which is what makes cross-pillar correlation actually
work in practice rather than just in theory.

## Distributed tracing

A single user request to `order-api` might fan out to `payment-api`, `inventory-api`,
and a database — a **trace** captures that entire path as a tree of **spans**, each span
representing one unit of work (one HTTP call, one DB query) with its own start time,
duration, and metadata.

```
Trace ID: 7f3a9c2e1b8d4f6a

order-api: POST /checkout                              [=====================] 420ms
  ├── payment-api: POST /charge                            [========]            180ms
  │     └── stripe-api: POST /v1/charges                       [======]              120ms
  ├── inventory-api: POST /reserve                                    [=====]      90ms
  │     └── postgres: UPDATE inventory SET...                            [==]        30ms
  └── postgres: INSERT INTO orders...                                          [=]   25ms
```

**Trace ID propagation** is what stitches this tree together across process and network
boundaries: when `order-api` calls `payment-api`, it includes the current trace ID (and
its own span ID, as the new span's parent) in an HTTP header
(`traceparent`, per the W3C Trace Context standard OTel implements). `payment-api`
reads that header, creates its own span as a child of it, and propagates the same trace
ID onward to anything *it* calls — so every span across every service in the call graph
shares one trace ID, letting a tracing backend reconstruct the full tree after the fact.
**Jaeger** and **Tempo** are the two most common backends for storing and visualizing
these traces (Tempo is commonly paired with Grafana, given common ownership, for a
unified metrics+logs+traces UI).

## Structured logging

A log line like:

```
[2026-06-20 14:32:01] ERROR Failed to process order 48291 for user 9213: connection timeout
```

is readable by a human staring at one terminal, and nearly useless at scale — you can't
reliably filter, aggregate, or correlate free-text log lines across thousands of pods.
**Structured logging** (JSON) fixes this by emitting each log line as a machine-parseable
object with consistent field names:

```json
{
  "timestamp": "2026-06-20T14:32:01.402Z",
  "level": "error",
  "message": "Failed to process order",
  "order_id": 48291,
  "user_id": 9213,
  "error": "connection timeout",
  "trace_id": "7f3a9c2e1b8d4f6a",
  "service": "order-api"
}
```

**`trace_id` in every log line, via MDC.** MDC (Mapped Diagnostic Context — a pattern
from logging libraries like Logback/SLF4J, with equivalents in most other ecosystems) is
a per-request context map that, once you set `trace_id` on it at the start of a request,
gets automatically attached to *every subsequent log line* emitted during that request's
handling, without manually passing it to every individual log call. The payoff: given any
error log line, you can immediately query "show me every log line, from every service,
that shares this exact `trace_id`" and reconstruct the complete picture of one specific
request's journey across the whole system — the structured-logging equivalent of the
distributed trace tree above, queryable directly from a single log line you happened to
notice.

## Key dashboards: the four golden signals

Every service-level dashboard should answer the same four questions, regardless of what
the service does — these are Google's "four golden signals," and they're the right
default starting point before reaching for anything more bespoke:

| Signal | What it measures | Example PromQL |
|---|---|---|
| **Request rate** | Throughput — how much traffic is the service handling? | `rate(http_requests_total[5m])` |
| **Error rate** | What fraction of requests are failing? | `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])` |
| **Latency (P50/P95/P99)** | How long do requests take — typical AND tail? | `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))` |
| **Saturation** | How close is the service to its resource limits? | `container_memory_working_set_bytes / container_spec_memory_limit_bytes` |

**Why P50/P95/P99, not just average latency:** an average can look perfectly healthy
while a meaningful fraction of real users have a terrible experience — 99 requests at
50ms and 1 request at 5 seconds averages to ~99.5ms, hiding the one genuinely broken
request entirely. P50 (median) tells you the typical experience; P99 tells you what your
worst-affected 1% of users are actually experiencing, which is very often where the
real, customer-visible problems live.

## Alertmanager: routing to Slack/email

Prometheus evaluates alert rules and fires alerts; **Alertmanager** is the separate
component responsible for what happens *next* — deduplicating related alerts,
**grouping** them sensibly (one Slack message for "12 pods are unhealthy" instead of 12
separate pages), and **routing** each alert to the right destination based on its labels.

```yaml
route:
  receiver: default-slack
  group_by: ['alertname', 'namespace']
  group_wait: 30s          # wait briefly to batch related alerts together
  group_interval: 5m
  repeat_interval: 4h      # don't re-notify for the same firing alert more than this often
  routes:
    - match:
        severity: critical
      receiver: pagerduty-oncall   # critical alerts page someone, not just Slack
      continue: true                # ALSO continue evaluating further routes below
    - match:
        severity: warning
      receiver: default-slack

receivers:
  - name: default-slack
    slack_configs:
      - api_url: https://hooks.slack.com/services/XXX/YYY/ZZZ
        channel: '#platform-alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: pagerduty-oncall
    pagerduty_configs:
      - service_key: <pagerduty-integration-key>
```

The `severity` label set on each alert rule (back in the Prometheus alert rules above) is
what this routing tree keys off — `critical` alerts page the on-call engineer via
PagerDuty *and* post to Slack (`continue: true` lets evaluation fall through to a
second matching route), while `warning` alerts only post to Slack, avoiding paging
someone awake at 3 AM for something that can wait until morning.

---

> ### 🎤 Interview Corner — Chapter 9
>
> **Q: "A dashboard shows average latency is fine, but customers are filing complaints
> about a slow checkout flow. How do you investigate?"**
>
> **A:** Start by looking at **P99 latency**, not the average — a healthy-looking average
> very commonly hides a meaningful tail of slow requests affecting a real subset of
> users, exactly the symptom described here. Once the P99 spike is confirmed on the
> metrics dashboard, the next step is to pivot to **distributed tracing**: pull a handful
> of actual slow traces from that time window (most tracing UIs let you filter spans by
> duration directly) and look at the span breakdown to see *where*, across the call
> graph, the time is actually going — is it one specific downstream dependency
> (`payment-api`, an external API call, a slow DB query)? From there, the relevant
> `trace_id` lets you pull the **exact structured log lines**, across every service
> involved, for one specific slow request, turning a vague "checkout feels slow"
> complaint into a precise root cause.
>
> **Q: "Why separate Prometheus (the rule evaluator) from Alertmanager (the notifier)
> instead of having Prometheus send Slack/PagerDuty notifications directly?"**
>
> **A:** Splitting evaluation from notification lets each do its one job well, and lets
> notification logic be shared and reused across multiple Prometheus instances (common
> in larger setups with one Prometheus per cluster/team, all routing through a shared
> Alertmanager). More importantly, Alertmanager owns the notification-quality logic that
> has nothing to do with *evaluating* a PromQL expression: **deduplication** (the same
> underlying issue shouldn't trigger five separate alert rules into five separate
> notifications), **grouping** (12 pods crash-looping from the same root cause should be
> one Slack message, not 12 pages), **silencing** (suppress known, already-being-worked
> alerts during a maintenance window without touching the rules themselves), and
> **routing** (severity-based fan-out to different destinations, as shown above). Baking
> all of that directly into the rule-evaluation engine would make Prometheus both more
> complex and harder to reason about for its actual core job — efficiently evaluating
> queries against time series data.

## Loki: The Prometheus for Logs

```yaml
# ─── Loki: Log Aggregation Without the ELK Complexity ───────────────────────
#
# ELK Stack (Elasticsearch + Logstash + Kibana): full-text indexes every log line
# → expensive storage, complex operations, powerful querying
#
# Loki: indexes only LABELS (metadata), not log content
# → 10× cheaper storage, simple operations, Grafana-native (no extra UI)
# → Logs and metrics in one Grafana dashboard
# → Trade-off: less powerful ad-hoc search than Elasticsearch
#
# For this plan: choose Loki — your Grafana is already set up for Prometheus metrics.
# Adding Loki gives you logs in the same dashboards.

# ─── docker-compose.yml additions ───────────────────────────────────────────

services:
  # Your existing services...
  prometheus:
    image: prom/prometheus:v2.47.0
    # ... existing config

  grafana:
    image: grafana/grafana:10.0.0
    # ... existing config
    environment:
      - GF_PATHS_PROVISIONING=/etc/grafana/provisioning
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning

  # ADD THESE:
  loki:
    image: grafana/loki:2.9.0
    ports:
      - "3100:3100"
    command: -config.file=/etc/loki/local-config.yaml
    volumes:
      - ./loki-config.yaml:/etc/loki/local-config.yaml
      - loki_data:/loki
    networks:
      - monitoring

  promtail:
    image: grafana/promtail:2.9.0
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro    # Docker socket for log discovery
      - ./promtail-config.yaml:/etc/promtail/config.yaml
    command: -config.file=/etc/promtail/config.yaml
    networks:
      - monitoring
    depends_on:
      - loki

volumes:
  loki_data:
```

```yaml
# loki-config.yaml
auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9096

ingester:
  lifecycler:
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/boltdb-shipper-active
    cache_location: /loki/boltdb-shipper-cache
    shared_store: filesystem
  filesystem:
    directory: /loki/chunks

limits_config:
  reject_old_samples: true
  reject_old_samples_max_age: 168h   # 7 days

chunk_store_config:
  max_look_back_period: 0s

table_manager:
  retention_deletes_enabled: false
  retention_period: 0s
```

```yaml
# promtail-config.yaml — collects logs from Docker containers and sends to Loki
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml   # tracks which log positions have been sent

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  # Auto-discover all Docker containers
  - job_name: docker-containers
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      # Use Docker container name as the app label
      - source_labels: [__meta_docker_container_name]
        regex: /(.*)
        target_label: app
      # Use Docker compose service name
      - source_labels: [__meta_docker_container_label_com_docker_compose_service]
        target_label: service
      # Add environment label
      - source_labels: [__meta_docker_container_label_environment]
        target_label: env
        replacement: local
    pipeline_stages:
      # Parse JSON logs from Spring Boot (logstash-logback-encoder format)
      - json:
          expressions:
            timestamp: timestamp
            level: level
            traceId: traceId
            spanId: spanId
            message: message
            logger: logger_name
      # Promote JSON fields as Loki labels
      - labels:
          level:
          traceId:
      # Set the log timestamp from the log content (not ingestion time)
      - timestamp:
          source: timestamp
          format: RFC3339Nano
```

```java
// ─── Spring Boot: Structured JSON Logging for Loki ──────────────────────────

// pom.xml: add logstash-logback-encoder
/*
<dependency>
    <groupId>net.logstash.logback</groupId>
    <artifactId>logstash-logback-encoder</artifactId>
    <version>7.4</version>
</dependency>
*/

// src/main/resources/logback-spring.xml
/*
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <springProfile name="local,dev">
        <!-- Human-readable for local development -->
        <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
            <encoder>
                <pattern>%d{HH:mm:ss} %highlight(%-5level) [%cyan(%X{traceId})] %logger{36} - %msg%n</pattern>
            </encoder>
        </appender>
        <root level="INFO">
            <appender-ref ref="CONSOLE"/>
        </root>
    </springProfile>

    <springProfile name="prod,staging">
        <!-- JSON for Loki in production -->
        <appender name="JSON_CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
            <encoder class="net.logstash.logback.encoder.LogstashEncoder">
                <customFields>
                    {"app":"${spring.application.name}","env":"${spring.profiles.active}"}
                </customFields>
                <fieldNames>
                    <timestamp>timestamp</timestamp>
                    <version>[ignore]</version>
                </fieldNames>
            </encoder>
        </appender>
        <root level="INFO">
            <appender-ref ref="JSON_CONSOLE"/>
        </root>
    </springProfile>
</configuration>
*/

// Adding trace ID to every log line:
// application.yml:
/*
spring:
  application:
    name: order-service
logging:
  pattern:
    level: "%5p [${spring.application.name:},%X{traceId:-},%X{spanId:-}]"
*/

// Sample JSON log output that Loki and Promtail will parse:
/*
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "INFO",
  "message": "Processing payment for order 123",
  "logger_name": "dev.surya.service.PaymentService",
  "traceId": "4bf92f3577b34da6",
  "spanId": "00f067aa0ba902b7",
  "app": "order-service",
  "env": "prod"
}
*/
```

```
# ─── LogQL — Querying Logs in Grafana ────────────────────────────────────────

# 1. View all logs from order-service in the last 5 minutes:
{app="order-service"}

# 2. Filter to ERROR level only:
{app="order-service"} |= "ERROR"

# 3. JSON parsing — filter by structured field:
{app="order-service"} | json | level = "ERROR"

# 4. Find all logs for a specific trace (across ALL services):
{env="production"} |= "4bf92f3577b34da6"
# This is the killer feature: one trace ID, full request journey across services

# 5. Count error rate per minute:
sum(rate({app="order-service"} |= "ERROR" [1m])) by (service)

# 6. Extract and display specific fields:
{app="order-service"} | json | line_format "{{.level}} {{.message}} traceId={{.traceId}}"

# 7. Find slow requests (if you log request duration):
{app="order-service"} | json | duration > 500

# ─── Grafana: Adding Loki as a Data Source ────────────────────────────────────
# Grafana UI → Configuration → Data Sources → Add data source → Loki
# URL: http://loki:3100
# Save & Test → "Data source connected and labels found."

# ─── Creating a Logs Panel in Grafana ─────────────────────────────────────────
# Dashboard → Add panel → Panel type: Logs
# Data source: Loki
# Label filters: app = order-service
# Line filters: ERROR

# ─── Interview Answer ─────────────────────────────────────────────────────────
# "How do you debug a slow request in your microservices setup?"
#
# "I use distributed tracing. When a request enters the Gateway, it gets a
# trace ID that is propagated to every downstream service via HTTP headers.
# Every log line includes this trace ID. In Grafana, I have a Loki panel —
# I search for the trace ID and instantly see the complete request journey
# across all services: what each service did, in what order, with timestamps.
# For latency analysis, the Tempo trace shows exactly which service and
# which method added the most delay."
```

---

# CHAPTER 10: kubectl Mastery

This chapter is the cheat sheet — every command referenced earlier in the book, plus the
ones that didn't fit naturally anywhere else, organized the way you'll actually reach for
them: by task, and finally by "something is broken, where do I even start."

## Complete command reference

### Cluster and context

```bash
kubectl cluster-info                          # control plane endpoint info
kubectl config get-contexts                   # list available cluster contexts
kubectl config use-context <name>             # switch active cluster
kubectl config set-context --current --namespace=<ns>   # set default namespace for this context
kubectl version                               # client and server versions
```

### Viewing resources

```bash
kubectl get pods                              # list pods in current namespace
kubectl get pods -A                           # list pods in ALL namespaces
kubectl get pods -o wide                      # include node, IP columns
kubectl get pods -w                           # watch for changes in real time
kubectl get pods -l app=order-api             # filter by label
kubectl get all                               # pods, services, deployments, replicasets...
kubectl get pods --sort-by=.metadata.creationTimestamp   # oldest/newest first
kubectl get pod order-api-7f8d9c-x7k2p -o yaml           # full resource definition
kubectl get events --sort-by=.lastTimestamp   # recent cluster events, oldest last
```

### Describing and inspecting

```bash
kubectl describe pod <pod-name>               # full detail + recent events for one pod
kubectl describe node <node-name>             # node capacity, allocations, conditions
kubectl describe deployment order-api         # deployment status, rollout conditions
kubectl explain pod.spec.containers           # built-in field-level API documentation
```

### Logs

```bash
kubectl logs <pod-name>                       # logs from a single-container pod
kubectl logs <pod-name> -c <container-name>   # logs from a specific container in a multi-container pod
kubectl logs <pod-name> --previous            # logs from the PREVIOUS instance of a crashed/restarted container
kubectl logs <pod-name> -f                    # stream/follow logs live
kubectl logs <pod-name> --since=10m           # only the last 10 minutes
kubectl logs -l app=order-api --all-containers # logs from every pod matching a label
```

### Exec and debugging shells

```bash
kubectl exec -it <pod-name> -- /bin/sh        # interactive shell into a running container
kubectl exec <pod-name> -- env                 # run a one-off command, see output, exit
kubectl debug <pod-name> -it --image=busybox --target=<container-name>
                                                # attach an ephemeral debug container to a
                                                # running pod — invaluable for distroless/
                                                # minimal images that have no shell at all
kubectl port-forward pod/<pod-name> 8080:3000  # forward local:8080 to the pod's :3000
kubectl port-forward svc/order-api 8080:80     # same, but via a Service
```

### Creating and modifying

```bash
kubectl apply -f deployment.yaml               # create or update from a manifest (idempotent)
kubectl apply -f ./manifests/                  # apply every manifest in a directory
kubectl delete -f deployment.yaml               # delete resources defined in a manifest
kubectl delete pod <pod-name>                   # delete a single pod (a Deployment will
                                                  # recreate it immediately, per Chapter 3)
kubectl edit deployment order-api               # open a resource in $EDITOR, apply on save
kubectl scale deployment order-api --replicas=5 # imperative scale (bypasses HPA's own state
                                                  # briefly — HPA may override it on its
                                                  # next reconcile if autoscaling is enabled)
kubectl set image deployment/order-api order-api=ghcr.io/example-org/order-api:1.4.1
                                                  # update just the image, trigger a rollout
kubectl label pod <pod-name> tier=backend       # add/update a label
kubectl annotate pod <pod-name> note="debug-2026-06-20"  # add/update an annotation
kubectl cp <pod-name>:/app/logs/error.log ./error.log    # copy a file out of a pod
```

### Rollouts (see Chapter 4 for the full walkthrough)

```bash
kubectl rollout status deployment/order-api
kubectl rollout history deployment/order-api
kubectl rollout undo deployment/order-api
kubectl rollout restart deployment/order-api
```

### Namespaces, Secrets, ConfigMaps

```bash
kubectl create namespace staging
kubectl get namespaces
kubectl create secret generic db-creds --from-literal=password=hunter2
kubectl create configmap app-config --from-file=config.yaml
kubectl get secret db-creds -o jsonpath='{.data.password}' | base64 -d   # decode a secret value
```

### Resource usage

```bash
kubectl top nodes                              # CPU/memory usage per node (requires metrics-server)
kubectl top pods                                # CPU/memory usage per pod
kubectl top pods --containers                   # broken down per container within each pod
```

## Debugging workflow: a pod isn't running

This is the single most common real-world kubectl task, and it always follows the same
funnel — don't skip steps, even when you're confident you already know the answer:

```
         kubectl get pods
                |
                v
   What's the STATUS column showing?
   (Pending / ImagePullBackOff / CrashLoopBackOff / Running-but-not-Ready / ...)
                |
                v
         kubectl describe pod <name>
   Read the EVENTS section at the bottom — it almost always tells you
   exactly what's wrong, in plain English, before you need to guess
                |
                v
         kubectl logs <name>
   (add --previous if the container has already restarted —
    the CURRENT container's logs may just show "starting up...",
    while the crash reason is in the PREVIOUS instance's logs)
                |
                v
         kubectl exec -it <name> -- /bin/sh
   Get an interactive shell INSIDE the container to check things
   the logs didn't explain: can it resolve DNS? Can it reach the
   database on the expected port? Are expected env vars/files present?
```

## Common failure reasons and solutions

| Status / symptom | What it means | How to confirm | Typical fix |
|---|---|---|---|
| **ImagePullBackOff** | The kubelet can't pull the specified container image | `kubectl describe pod` → Events will show the exact registry error (auth failure, image/tag doesn't exist, network issue reaching the registry) | Check the image name/tag is correct and actually pushed; check `imagePullSecrets` are configured if the registry is private; check the node has network access to the registry |
| **CrashLoopBackOff** | The container starts, then exits (crashes), repeatedly — Kubernetes is backing off between restart attempts | `kubectl logs <pod> --previous` to see what the container printed right before it died | Almost always an application-level startup failure — a missing/incorrect env var, a failed DB connection on boot, an uncaught startup exception. Fix the underlying app issue; the restart loop itself is a symptom, not the cause |
| **OOMKilled** (visible via `kubectl describe pod` → `Last State: Terminated, Reason: OOMKilled`) | The container exceeded its memory `limit` and the kernel killed it | `kubectl describe pod` shows the OOMKilled reason and exit code 137 | Either the limit is genuinely too low for the app's real usage (raise it, based on actual observed `kubectl top` data), or there's a real memory leak in the app (raising the limit only delays the same crash) |
| **Pending** (pod never gets scheduled) | The Scheduler can't find any node that satisfies the pod's requirements | `kubectl describe pod` → Events will show something like "0/5 nodes are available: 5 Insufficient cpu" | Most often insufficient cluster capacity for the requested CPU/memory `requests` — either free up capacity, add nodes, or right-size the requests. Also check for unsatisfiable `nodeAffinity`/taints that no node actually matches |
| **Init:Error / Init:CrashLoopBackOff** | An **init container** (a container that must run to completion before the main containers start) is failing | `kubectl logs <pod> -c <init-container-name>` — note you must specify the init container's name explicitly | Fix whatever the init container is responsible for (commonly: waiting on a dependency, running a migration, fetching a config file) — the main application containers won't even attempt to start until every init container exits successfully |
| **Running, but 0/1 Ready** | The container process is running, but its `readinessProbe` is failing | `kubectl describe pod` → check the readiness probe's configured path/port against what the app actually exposes; `kubectl exec` in and curl the readiness endpoint directly | Usually a probe misconfiguration (wrong path/port) or a genuine dependency the readiness check correctly identifies as unavailable (e.g. can't reach the database yet) |
| **Pod stuck `Terminating`** | The pod has been deleted, but its container(s) haven't exited within `terminationGracePeriodSeconds` | `kubectl describe pod` to check for a stuck `preStop` hook or a process ignoring SIGTERM | Check the app actually handles SIGTERM gracefully (see the exec-form `CMD` note in Chapter 2); as a last resort, `kubectl delete pod <name> --grace-period=0 --force` (use sparingly — this skips graceful shutdown entirely) |

---

> ### 🎤 Interview Corner — Chapter 10
>
> **Q: "Walk me through your exact debugging process for a pod stuck in
> `CrashLoopBackOff`."**
>
> **A:** First, `kubectl get pods` to confirm the status and see the restart count —
> a high, climbing restart count confirms it's a genuine repeated crash, not a one-off.
> Next, `kubectl describe pod <name>` to read the Events section, which often already
> states the exit code and reason. Then, critically, `kubectl logs <name> --previous` —
> not `kubectl logs <name>` without `--previous`, because by the time you're looking,
> the container has likely already restarted again, and the *current* container's logs
> may just show a few seconds of fresh startup output, while the actual crash reason is
> in the logs from the *previous*, now-terminated instance. From there it's almost always
> an application-level issue visible right in those logs — a missing required
> environment variable, a database connection failure on startup, an unhandled exception
> during initialization. If the logs are unhelpful (e.g. the app dies before logging
> initializes), `kubectl describe pod` will at least show the container's exit code,
> which narrows things further (e.g. exit code 1 is a generic application error; exit
> code 137 specifically indicates the process was killed, commonly OOMKilled).
>
> **Q: "What's the difference between `kubectl delete pod` and `kubectl rollout restart
> deployment`, and when would you use each?"**
>
> **A:** `kubectl delete pod <name>` deletes one specific pod. If that pod is managed by
> a Deployment/ReplicaSet, the ReplicaSet controller's reconciliation loop (Chapter 3)
> notices actual replica count just dropped below desired and immediately creates a
> replacement — but it's a blunt, single-pod tool, and deleting several pods in quick
> succession risks momentarily dropping below the capacity a PodDisruptionBudget or your
> own SLOs require. `kubectl rollout restart deployment/<name>`, by contrast, triggers a
> full, *managed* rolling update of every pod in the Deployment — same `maxSurge`/
> `maxUnavailable`-respecting, readiness-gated process covered in Chapter 4 — without
> changing the image or any other spec field. It's the right tool specifically when you
> need every pod recreated (commonly: to pick up a changed ConfigMap/Secret that pods
> don't automatically reload, or to clear some accumulated in-memory state) but want that
> recreation to happen safely, with zero capacity loss, rather than via a manual,
> unmanaged sequence of individual pod deletions.

---

## Closing note

If you've worked through all ten chapters, you now have the full mental model this book
opened with: every piece of Kubernetes — every controller, every YAML field, every
`kubectl` subcommand — is reconciliation in service of one of five problems (scheduling,
healing, scaling, discovery, updates), problems that exist because of one historical
progression (bare metal → VMs → containers → orchestration). The YAML will keep growing
as you encounter new resource types and new cloud services, but the questions you ask of
it — "what problem does this solve, and what's the desired-vs-actual state being
reconciled here?" — don't change. That's the part worth actually memorizing.

