# How this starter is organized

The design follows GhostPay's identity module and shared-security layering; domain-specific GhostPay features were removed.

| File / directory | Responsibility |
| --- | --- |
| `identity/domain/User.java` | Persisted UUID user, email and password hash; no password exposed through API |
| `identity/persistence/UserRepository.java` | Query users by UUID and normalized email |
| `identity/application/RegisterUserService.java` | Normalize email, validate BCrypt byte limit, hash password, save user |
| `identity/application/LoginUserService.java` | Check credentials with constant-work BCrypt password verification for existing users |
| `identity/application/CurrentUserService.java` | Look up authenticated user from JWT subject rather than trusting client-supplied user IDs |
| `identity/api/AuthController.java` | Map HTTP registration/login to services, return safe DTOs |
| `identity/api/account/AccountController.java` | Protected `GET /api/v1/account/me` |
| `shared/security/SecurityConfig.java` | Stateless authentication, JWT resource server, HTTP 401/403, CORS |
| `shared/security/jwt/JwtConfig.java` | HS256 secret strength, issuer/expiry/UUID verification |
| `shared/security/JwtService.java` | Issue short-lived access tokens |
| `shared/security/PasswordConfig.java` | BCrypt password encoder bean |
| `shared/exception/GlobalExceptionHandler.java` | Map application/framework errors to sanitized JSON and HTTP statuses |
| `db/migration/V1__create_users.sql` | Fresh users table (UUID ID) |

## Authentication flows

**Register:** `POST /api/v1/auth/register` -> DTO validation -> `RegisterUserService` -> BCrypt -> `UserRepository` -> safe 201 DTO.

**Login:** `POST /api/v1/auth/login` -> `LoginUserService` -> password check -> `JwtService` -> signed HS256 Bearer token.

**Authenticated API:** Bearer token -> `JwtDecoder` validates signature, issuer and expiry -> controller obtains `Jwt` via `@AuthenticationPrincipal` -> `CurrentUserService` loads the user from PostgreSQL.

No role system or domain-specific ownership model is included. Add roles and per-resource authorization to each new project's application services. For public internet traffic, protect auth routes against brute-force attempts and abuse.
