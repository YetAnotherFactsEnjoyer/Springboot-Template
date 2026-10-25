# Spring Boot Backend Starter

A **reusable Java 21 / Spring Boot 4 backend template** extracted and cleaned from GhostPay's identity and JWT foundation. Start new projects with registration, login, JWT verification, PostgreSQL, Flyway, Docker, and tests already wired up.

> This is a starter for projects such as StockFlow, not a production-certified authentication service. Security review and deployment hardening are still required for each application.

## Included

- Spring Boot 4.1.1, Gradle wrapper 9.8.1, Java 21
- `POST /api/v1/auth/register` and `POST /api/v1/auth/login`
- `GET /api/v1/account/me` (Bearer JWT required)
- `GET /actuator/health` (public, without sensitive details)
- BCrypt password hashes, email normalization, UUID users
- HS256 JWT signing with externally supplied 32+ byte secret, issuer and expiry validation
- Stateless Spring Security, error JSON, request validation, explicit CORS origins
- PostgreSQL + **single clean V1 Flyway migration** (no GhostPay upgrade migrations)
- Dockerfile, Compose, isolated Testcontainers integration tests and GitHub Actions CI

## Create a new project (one-time per clone)

```bash
# Clone / Use this repository as a GitHub template first.
python3 scripts/new_project.py --name stockflow --package com.stockflow
python3 scripts/init_env.py  # generates random local secrets in ignored .env
```

The rename script adjusts Java package paths, project name, database name/user, and JWT issuer. Run it **before** creating `.env` or any database. Do not run it against an already-deployed project.

## Run locally: DB in Docker, backend on host

Prerequisites: Java 21, Python 3, Docker, and a free local port 5432.

```bash
python3 scripts/init_env.py        # only if you have not already generated .env
# Alternatively: copy .env.example and provide strong independent secrets yourself.
docker compose up -d db
./gradlew bootRun
```

Open `http://localhost:8080/actuator/health`. PostgreSQL is localhost-only. The backend reads its secrets from `.env` (ignored by Git).

## Run everything in Docker

```bash
docker compose up -d --build
# API: http://localhost:8080
# Logs: docker compose logs -f backend
```

Do not run both the local backend and Docker backend simultaneously on port 8080. Never use `docker compose down -v` on databases containing data.

## Try it

```bash
curl -i -X POST http://localhost:8080/api/v1/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"demo@example.com","password":"a-long-test-password"}'

curl -s -X POST http://localhost:8080/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"demo@example.com","password":"a-long-test-password"}'
```

Copy the `accessToken` from the login response:

```bash
curl -i http://localhost:8080/api/v1/account/me \
  -H 'Authorization: Bearer PASTE_ACCESS_TOKEN_HERE'
```

## Tests

```bash
# No Docker needed: quick local checks
./gradlew test --tests '*JwtConfigTest' --tests '*GlobalExceptionHandlerTest'

# Docker required: Testcontainers spins up a **disposable** PostgreSQL container
./gradlew clean test build
```

Tests must never target existing databases. In CI, Testcontainers requires an available Docker daemon. The included workflow expects a standard Ubuntu runner with Docker.

## Project structure

```text
src/main/java/com/example/starter/
  identity/
    api/          # register, login, account/me + request/response DTOs
    application/  # registration, login, user lookup
    domain/       # User + business exceptions
    persistence/  # UserRepository
  shared/
    security/     # SecurityFilterChain, JWT, BCrypt and CORS
    exception/    # consistent API errors
src/main/resources/db/migration/V1__create_users.sql
scripts/new_project.py
scripts/init_env.py
```

## Extending it for StockFlow (or another backend)

1. Create feature packages: e.g. `inventory/{api,application,domain,persistence}`.
2. Add **new** migrations (`V2__...`, `V3__...`). Do not edit migrations already applied in deployed databases.
3. Use `@AuthenticationPrincipal Jwt jwt` and `CurrentUserService` to resolve the current persisted user.
4. Enforce object ownership / roles **in each business feature**; JWT authentication alone is not authorization.
5. Add integration tests for every protected workflow and cross-user access.
6. Revisit `/api/v1/auth/register` public access, CORS origins, rate limiting, HTTPS and token storage for the intended product.

## What is deliberately *not* included

- GhostPay's merchants, terminals, payments, synchronization and repair utilities
- StockFlow-specific inventory entities or roles/permissions
- Refresh tokens, server-side logout/revocation, OAuth social login, email verification, password reset
- Automated rate limiting, account lockout, MFA, email delivery or production monitoring
- A frontend or deployment infrastructure for public TLS / backups

For real users, add auth abuse prevention (login throttling), secret rotation plan, secure client token storage, auditable permissions, data retention/deletion, monitoring, backups and operational procedures. Current logout is **client-side token deletion only**; issued JWTs remain valid until expiry. Use a secret manager outside local development.

## Useful docs

- [Spring Boot](https://docs.spring.io/spring-boot/index.html)
- [Spring Security](https://docs.spring.io/spring-security/reference/index.html)
- [Spring OAuth2 Resource Server](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html)
- [Spring Data JPA](https://docs.spring.io/spring-data/jpa/reference/index.html)
- [Flyway](https://documentation.red-gate.com/fd/)

See [`docs/SECURITY.md`](docs/SECURITY.md), [`docs/USING_AS_TEMPLATE.md`](docs/USING_AS_TEMPLATE.md), [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), and [`docs/VERIFICATION.md`](docs/VERIFICATION.md).
