# Security model and release checklist

## Defaults kept from GhostPay

- Password hashes: BCrypt (maximum 72 UTF-8 bytes; DTO minimum 8 characters)
- Tokens: signed HS256; only this algorithm accepted, issuer checked, expiry required, subject must be a canonical UUID
- Missing/malformed token: 401; denied access: 403; validation: 400; duplicate email: 409
- Stateless REST API: cookies and server sessions aren't used for authentication
- Database credentials and signing key are external; application fails to start if missing or weak
- Only exact configured CORS origins are trusted; no `*` origin by default
- `/actuator/health` is public, no health details; other endpoints are protected
- All DB schema changes through Flyway; Hibernate runs `validate` only

## Before actual public production

- HTTPS termination and secure load balancer/proxy; never send Bearer JWTs over HTTP
- Protect registration and login with rate limits / abuse detection
- Choose a secure frontend token-storage strategy and XSS protections
- Token revocation or shorter lifetimes when business requirements demand server-side logout
- Secret management, key rotation and incident-response plan
- Consider refresh token rotation and audience claims for multiple services
- Account email verification, password reset and optional MFA if appropriate
- Role and ownership checks in every feature; new routes are authenticated by default, not automatically authorized
- Audit logs without credentials/tokens, backup restore drills, vulnerability/container scanning
- Confirm deployment network controls (localhost bindings are local-development defaults)

Do not reuse `.env`/JWT secrets between projects or environments. Rotate compromised secrets. Changing the JWT secret invalidates all previously issued tokens. Docker Compose existing Postgres volumes retain their original DB password; changing `.env` does **not** update the database user's password.
