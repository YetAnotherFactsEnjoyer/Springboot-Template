# Verification in the generation environment

- Original base inspected: `GhostPay-repaired.zip`, with the identity, security, JWT and error-handler classes examined.
- Confirmed Spring Boot `4.1.1` and Spring Security `7` JWT encoder APIs from official documentation.
- Static Java parser: 29 Java source and test files parsed without Java syntax errors.
- Python project initialization: verified package and Gradle group replacement, renamed DB and JWT issuer, and moved Java source/test directories.
- Local secret setup: verified generated secrets and prevention of accidental overwrite.
- Docker Compose and application YAML parsed successfully.
- Full Java compilation and JUnit/Testcontainers tests: **NOT VERIFIED** in generation environment. Gradle wrapper could not download Gradle 9.8.1 because `services.gradle.org` was not resolvable. Docker was not installed in this environment.

## Run the required checks on your own machine

```bash
./gradlew clean test build
python3 scripts/init_env.py      # if .env does not already exist
docker compose up -d --build
docker compose ps
curl -i http://localhost:8080/actuator/health
```

Also run registration, login and account routes from the README. No application is considered production-verified solely on the basis of the checks listed above.
