# Chapter 10: Swagger UI — Making Your API Public

## 10.1 Why a live, clickable API matters for a portfolio

An interviewer who opens your GitHub repository sees a README. Whether they actually *read* it and understand what your project does — or close the tab in three seconds — often comes down to whether there's something they can click and immediately interact with. A live Swagger UI is the most effective thing you can put in a backend project's README because it lets a reader *try your API in their browser, right now*, without cloning anything or setting up a local environment. It demonstrates that your application actually works, that it's actually deployed, and that you understand production-readiness well enough to have made it publicly accessible.

The link in your README should look like this:

```
## 🚀 Live Demo

**API:** https://order-management-api.up.railway.app
**Swagger UI:** https://order-management-api.up.railway.app/swagger-ui.html

Try it live — register an account at POST /v1/auth/register, copy the
returned token, click "Authorize" in the Swagger UI, paste it in, and
you can create and manage orders directly from your browser.
```

This chapter covers Dockerizing the application and deploying it to Railway — a hosting platform whose free tier works well for portfolio projects as of mid-2026, with notes on where to look if its free availability changes.

## 10.2 Dockerizing the application

A `Dockerfile` is a recipe for producing a container image — a self-contained, portable snapshot of your application and everything it needs to run. The image is what you ship to the hosting platform; the platform runs it.

For a Spring Boot application, the best-practice Dockerfile uses a multi-stage build: a builder stage that compiles the application, and a runtime stage that contains only the compiled artifact — not the JDK, Maven, source code, or any other build-time artifact. The resulting image is smaller (faster to upload, faster to pull, smaller attack surface) and more appropriate for production.

Spring Boot 2.3+ has built-in support for **layered JARs** — the JAR's contents are organized so that the parts that change least (library dependencies) are in separate layers from the parts that change most (your own compiled classes). Docker caches image layers; if your dependencies didn't change between builds, Docker reuses the cached dependency layer and only rebuilds the layers containing your code. For a typical Spring Boot application this turns a 60-second build into a 5-second one after the first push.

**`Dockerfile`** (place at the project root alongside `pom.xml`):
```dockerfile
# ── Stage 1: Build ──────────────────────────────────────────────────────────
FROM eclipse-temurin:21-jdk-jammy AS builder

WORKDIR /app

# Copy Maven wrapper and pom.xml first — Docker caches this layer separately.
# If only source files changed (not pom.xml), this layer is reused from cache.
COPY .mvn/ .mvn/
COPY mvnw pom.xml ./

# Download all dependencies in a separate layer — changes rarely.
RUN ./mvnw dependency:go-offline -B

# Now copy source and build the JAR.
COPY src ./src
RUN ./mvnw package -DskipTests -B

# Extract the layered JAR — creates separate directories for dependencies,
# Spring Boot loader, snapshot dependencies, and application classes.
RUN java -Djarmode=tools -jar target/*.jar extract --layers --launcher --destination target/extracted

# ── Stage 2: Runtime ─────────────────────────────────────────────────────────
FROM eclipse-temurin:21-jre-jammy AS runtime

# Run as a non-root user — never run a production container as root.
RUN groupadd --system appgroup && useradd --system --gid appgroup appuser

WORKDIR /app

# Copy the extracted layers in ascending order of change frequency.
# Docker caches each COPY layer; unchanged layers are reused on next build.
COPY --from=builder --chown=appuser:appgroup /app/target/extracted/dependencies/ ./
COPY --from=builder --chown=appuser:appgroup /app/target/extracted/spring-boot-loader/ ./
COPY --from=builder --chown=appuser:appgroup /app/target/extracted/snapshot-dependencies/ ./
COPY --from=builder --chown=appuser:appgroup /app/target/extracted/application/ ./

USER appuser

# Expose the port Spring Boot listens on (must match server.port in application.yml)
EXPOSE 8080

# Use the exec form (JSON array) — avoids a shell wrapper process and ensures
# signals (SIGTERM for graceful shutdown) are sent directly to the JVM.
ENTRYPOINT ["java", "-XX:+UseContainerSupport", "-XX:MaxRAMPercentage=75.0", "org.springframework.boot.loader.launch.JarLauncher"]
```

`-XX:+UseContainerSupport` tells the JVM to respect the container's memory limit (set by Docker/Kubernetes) instead of defaulting to a fraction of the *host* machine's RAM, which could be enormous — leading to the JVM allocating far more heap than the container actually has available and getting OOM-killed. `-XX:MaxRAMPercentage=75.0` lets the JVM use up to 75% of the container's memory for the heap, leaving 25% for off-heap use (thread stacks, Metaspace, native memory).

## 10.3 Testing the Docker build locally

```bash
# Build the image
docker build -t order-management:local .

# Run it — connecting to the same docker-compose postgres from Chapter 4
# The postgres container and this container need to be on the same docker network,
# or you can use host.docker.internal to reach the host machine's localhost.
docker run -p 8080:8080 \
  -e SPRING_PROFILES_ACTIVE=local \
  -e SPRING_DATASOURCE_URL=jdbc:postgresql://host.docker.internal:5432/orderdb \
  -e SPRING_DATASOURCE_USERNAME=orderapp \
  -e SPRING_DATASOURCE_PASSWORD=orderapp_dev_password \
  order-management:local

# Verify it's up
curl http://localhost:8080/actuator/health
# Expected: {"status":"UP",...}

# Verify Swagger UI is accessible
open http://localhost:8080/swagger-ui.html
```

## 10.4 Deploying to Railway

Railway (railway.app) is a PaaS (platform-as-a-service) that deploys from a GitHub repository or a pre-built Docker image, adds a managed PostgreSQL database, and handles SSL termination, giving you a public HTTPS URL with minimal configuration. As of mid-2026, it has a paid starter tier that covers small portfolio projects; check railway.app/pricing for current terms, as pricing tiers for cloud platforms change frequently.

### Step-by-step deployment

**1. Push your project to GitHub.** Your repository should contain the `Dockerfile`, the Spring Boot source, and a `docker-compose.yml` for local development — but *not* any file containing secrets (`application-prod.yml` with real credentials should never be committed; credentials go in environment variables).

**2. Create a Railway project.**
- Go to [railway.app](https://railway.app) and sign in with GitHub.
- Click **New Project → Deploy from GitHub Repo**.
- Select your repository. Railway detects the `Dockerfile` automatically.

**3. Add a PostgreSQL service.**
- In your Railway project dashboard, click **New Service → Database → PostgreSQL**.
- Railway provisions a managed PostgreSQL instance and makes the connection URL available as a `${{Postgres.DATABASE_URL}}` variable within the project.

**4. Configure environment variables.**
In the service settings, add these variables (Railway's UI has an "Add Variable" interface, or you can use the `railway` CLI):

```
SPRING_PROFILES_ACTIVE=prod
DATABASE_URL=${{Postgres.DATABASE_URL}}
DATABASE_USERNAME=${{Postgres.PGUSER}}
DATABASE_PASSWORD=${{Postgres.PGPASSWORD}}
ORDERMANAGEMENT_SECURITY_JWT_SECRET=<generate a 64-char random hex string here>
```

For the JWT secret, generate one securely:
```bash
openssl rand -hex 32
```

**5. Configure the application to read Railway's connection URL.**

Railway's `${{Postgres.DATABASE_URL}}` provides a full JDBC URL in the format `postgresql://user:password@host:port/dbname`. The `application-prod.yml` already uses `${DATABASE_URL}`, matching the environment variable name above.

Verify that `application-prod.yml` disables `ddl-auto: update` (should be `validate`) — Flyway manages the schema, and the migrations in `classpath:db/migration` will run automatically on startup.

**6. Set the deploy trigger and deploy.**
Railway redeploys automatically on every push to your main branch. Trigger the first deploy by pushing a commit, or click **Deploy** in the dashboard.

**7. Get your public URL.**
Railway assigns a URL in the format `https://your-project-name.up.railway.app`. You can also add a custom domain in the Settings tab.

**8. Verify:**
```bash
# Health check
curl https://your-project-name.up.railway.app/actuator/health

# Register a test user
curl -X POST https://your-project-name.up.railway.app/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

# Open Swagger UI
open https://your-project-name.up.railway.app/swagger-ui.html
```

### Railway deployment — quick reference

The step-by-step above uses the full layered Dockerfile from section 10.2. Railway also supports two simpler deployment paths worth knowing about, plus configuration details that matter for a production-ready portfolio project:

```bash
# ─── Deploying to Railway.app — Step by Step ─────────────────────────────────
# Railway gives $5/month free credit — no credit card needed for most projects

# PREREQUISITE: Your Spring Boot app must:
# 1. Have a Dockerfile (or Railway auto-detects Maven and builds itself)
# 2. Read PORT from environment: server.port=${PORT:8080}
# 3. Database connection uses environment variables (not hardcoded)

# ─── Option A: Railway Auto-Detection (Nixpacks, no Dockerfile needed) ───────

# Step 1: Push your project to GitHub

# Step 2: Go to railway.app → New Project → Deploy from GitHub
# Select your repository → Railway auto-detects Java/Maven

# Step 3: Add environment variables in Railway Dashboard:
# DATABASE_URL    = postgresql://user:pass@host:5432/dbname
# SPRING_PROFILES_ACTIVE = prod

# Step 4: Add a PostgreSQL plugin:
# Railway Dashboard → New → Database → PostgreSQL
# Railway auto-sets DATABASE_URL in your app's environment

# Step 5: Railway deploys automatically on every push to main

# ─── Option B: With Dockerfile ───────────────────────────────────────────────

# Dockerfile (multi-stage — smaller final image):
FROM maven:3.9-eclipse-temurin-21 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -q          # cache dependencies layer
COPY src ./src
RUN mvn package -DskipTests -q            # build the JAR

FROM eclipse-temurin:21-jre-alpine        # JRE only — 180MB vs 500MB for JDK
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", \
    "-XX:+UseContainerSupport", \
    "-XX:MaxRAMPercentage=75.0", \
    "-jar", "app.jar"]

# railway.json (place in project root):
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "java -jar app.jar",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}

# ─── application-prod.yml ────────────────────────────────────────────────────

spring:
  datasource:
    url: ${DATABASE_URL}                  # Railway sets this automatically
    hikari:
      connection-timeout: 30000
      maximum-pool-size: 5               # Railway free tier: small pool
  jpa:
    hibernate:
      ddl-auto: validate                  # Flyway owns schema in production
    show-sql: false                       # don't log SQL in production
  flyway:
    enabled: true

server:
  port: ${PORT:8080}                      # Railway sets PORT at runtime

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    health:
      show-details: when-authorized

# ─── README Format with Live Links ───────────────────────────────────────────

# Every portfolio repository README must have this section:

## 🚀 Live Demo

| Resource | URL |
|----------|-----|
| **API Documentation (Swagger UI)** | https://your-app.up.railway.app/swagger-ui.html |
| **Health Check** | https://your-app.up.railway.app/actuator/health |
| **API Base URL** | https://your-app.up.railway.app/api/v1 |

> Try the API directly from Swagger — no setup required. Click "Authorize"
> to enter a JWT token from the `/api/v1/auth/login` endpoint.

## ⚙️ Run Locally

\`\`\`bash
# Prerequisites: Docker Desktop
docker-compose up -d          # starts PostgreSQL + Redis
./mvnw spring-boot:run        # starts the application on :8080
\`\`\`

# ─── Why this matters ─────────────────────────────────────────────────────────
# "Can I try it right now?" is the question every interviewer asks
# when they look at a portfolio project at 11pm before your interview.
# A live Swagger URL answers that question in one click.
# A "clone and run locally" setup requires 20 minutes and Docker.
# The live URL wins every time.
```

## 10.5 The Swagger UI authentication flow for a viewer

When an interviewer opens your Swagger UI, here's exactly what they should be able to do, end-to-end, without reading any code:

1. Navigate to `/swagger-ui.html`.
2. Find the **POST /v1/auth/register** endpoint under the "Authentication" section.
3. Click "Try it out", fill in a username, email, and password, and click Execute.
4. Copy the `accessToken` value from the response body.
5. Click the **Authorize** button (the padlock icon at the top of the Swagger UI).
6. In the dialog, paste the token into the **bearerAuth** field and click Authorize.
7. Now every subsequent "Try it out" execution automatically sends `Authorization: Bearer <token>`.
8. Try **GET /v1/products** — should return an empty list (or sample data if you've seeded some).
9. Try **POST /v1/products** with ADMIN credentials (they'd need to register as ADMIN — you can add a seed endpoint or seed script for demo data).
10. Try **POST /v1/orders** to create an order.

This is a complete, end-to-end, browser-based demonstration of your API — register, authenticate, and exercise every major endpoint — with nothing installed and nothing cloned. For a portfolio project, that's the difference between an interviewer who reads the README and moves on, and one who actually tries your API and has a real question to ask you about it.

## 10.6 Adding the README section

```markdown
## Live Demo

**Base URL:** `https://your-project-name.up.railway.app`  
**Swagger UI:** [`https://your-project-name.up.railway.app/swagger-ui.html`](https://your-project-name.up.railway.app/swagger-ui.html)

### Quick start (no setup required)

1. Open the Swagger UI link above.
2. Use `POST /v1/auth/register` to create an account.
3. Copy the `accessToken` from the response.
4. Click **Authorize** (padlock icon), paste the token, and click **Authorize**.
5. Try `POST /v1/products` (requires ADMIN role — use the admin seed endpoint below)
   or `GET /v1/products` to browse the product catalog.
6. Try `POST /v1/orders` to place an order.

### Running locally

```bash
# Prerequisites: Java 21, Maven, Docker

git clone https://github.com/yourname/order-management.git
cd order-management

# Start PostgreSQL
docker compose up -d

# Run the application
./mvnw spring-boot:run -Dspring-boot.run.profiles=local

# Swagger UI: http://localhost:8080/swagger-ui.html
```

### Tech stack

- **Java 21 + Spring Boot 3.5**
- **PostgreSQL** (Flyway-managed schema migrations)
- **Spring Security + JWT** (stateless authentication, BCrypt password hashing)
- **Hibernate / Spring Data JPA** (with optimistic locking via `@Version`)
- **Spring AOP** (performance logging, cross-cutting concerns)
- **springdoc-openapi** (Swagger UI)
- **Testcontainers** (integration tests against real PostgreSQL)
- **Docker** (multi-stage layered build, deployed on Railway)
```

## 10.7 If Railway's free tier is unavailable

Cloud platforms change their pricing regularly. If Railway's free tier is no longer available when you read this, here are direct alternatives that were available as of mid-2026, all capable of hosting a containerized Spring Boot application with a managed PostgreSQL database for a portfolio project at low or no cost:

**Render** (render.com) — free tier for web services (750 hours/month) and a free PostgreSQL instance (90-day retention on free tier, then $7/month). Deploys from GitHub similar to Railway, auto-detects `Dockerfile`.

**Fly.io** (fly.io) — free tier of 3 small VMs. Excellent for containerized applications, has managed PostgreSQL via their extension system, CLI-driven deployment. Slightly more configuration than Railway but more control.

**Google Cloud Run** (cloud.google.com/run) — free tier of 2 million requests/month and 180,000 vCPU-seconds. Stateless containers only — the database needs to be external (Cloud SQL, which is paid, or a free PostgreSQL instance from Render/Supabase). More setup, but genuinely production-grade infrastructure.

**Supabase** (supabase.com) — primarily a hosted PostgreSQL platform with a generous free tier for the database. Pair it with any of the above for the compute layer.

The specific platform matters less than the principle: a public URL exists, the Swagger UI is accessible, and it actually works. Check the current free tiers for each option at time of deployment.

> **Interview Question — SDE-2:** "Why use a multi-stage Docker build instead of a single-stage build that just runs `mvn package` and copies the JAR?"
>
> **Answer:** Two separate reasons. First, image size: a single-stage build that starts from a full JDK image and retains Maven, the Maven local repository cache, and the uncompiled source code produces an image that's several hundred megabytes larger than necessary. The runtime image only needs the JRE (not the full JDK) and the JAR — nothing else. A multi-stage build discards the builder stage entirely, keeping only what the runtime needs. Smaller images take less time to push to a container registry, less time to pull during deployment, and have a smaller attack surface (fewer binaries that could be exploited if the container is compromised). Second, caching efficiency: layering the Dockerfile to copy `pom.xml` and download dependencies before copying source code means that on a rebuild where only source changed (not dependencies), Docker reuses the dependency-download layer from cache and rebuilds only the compilation layer — typically 5–10 seconds instead of 60. This matters for CI/CD pipelines where you're rebuilding and pushing on every commit.

---

## Epilogue: what you've built and where to go next

The Order Management API is complete. What started as an empty `pom.xml` and a single `@SpringBootApplication` class is now:

- A fully-mapped relational data model with five JPA entities, all relationships correctly mapped, all fetch types explicitly declared, optimistic locking via `@Version` on two entities, and an idempotency record pattern for safe retries
- A query layer using derived methods, JPQL, native SQL, JOIN FETCH, and `@EntityGraph` — with a full understanding of the N+1 problem and three different tools for solving it
- A service layer with correct transaction management, proper propagation, the self-invocation trap identified and avoided, and business logic cleanly separated from both persistence and HTTP concerns
- A controller layer returning correct HTTP status codes, `Location` headers on 201 responses, and `ResponseEntity` for full response control
- Bean Validation on every incoming DTO, with a unified error envelope from a single `@RestControllerAdvice` that every endpoint benefits from
- JWT-based stateless authentication, a custom filter that populates the `SecurityContext`, method-level security with `@PreAuthorize`, and a correctly reasoned CORS/CSRF configuration
- A test suite with `@WebMvcTest` controller tests, `@DataJpaTest` repository tests, `@SpringBootTest` integration tests, and Testcontainers for real PostgreSQL fidelity
- OpenAPI documentation with JWT authentication in Swagger UI, Spring Actuator health and metrics endpoints, separate profiles for local and production configuration, and graceful shutdown
- A performance-logging AOP aspect that applies uniformly to the entire service layer without modifying any service class
- Flyway-managed schema migrations, with initial schema and zero-downtime migration strategies
- A layered Dockerfile with container-aware JVM settings, deployed to a public URL with a live Swagger UI

Each of these systems has an interview question in this book explaining not just *what* it does but *how it works internally* — because "I know the annotation" and "I know what happens when the proxy intercepts the method" are very different answers, and interviewers asking at the SDE-2 level have heard the first answer many times.

**What to build next:** the logical extensions to this system are the ones that introduce the remaining major backend engineering concepts not covered here — a message queue integration (Kafka or SQS) for event-driven order state changes; Redis caching with `@Cacheable` for product catalog reads; a distributed rate limiter; Spring Batch for the "cancel all PENDING orders older than 7 days" scheduled job that currently only exists as a `@Query` method in the repository; and extracting `InventoryService` into a separate microservice to see how the transactional guarantees you've built here need to change (or be replaced with eventual consistency) when the inventory database is no longer the same one the order database is in.

All of those topics are worth a book of their own. The foundation this book built — understanding the IoC container, the proxy mechanism, how transactions actually work, what a distributed system needs from idempotency — is what makes every subsequent concept learnable, instead of just copyable from a tutorial.
