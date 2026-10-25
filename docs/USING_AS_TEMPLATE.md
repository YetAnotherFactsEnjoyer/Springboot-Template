# Creating and using the GitHub template

1. Create a GitHub repo named `java-backend-starter` from this folder and push the committed files. **Never** commit `.env`.
2. GitHub → repository **Settings** → enable **Template repository**.
3. For each new project: click **Use this template**, clone the newly created repo.
4. Before first run: `python3 scripts/new_project.py --name stockflow --package com.stockflow`.
5. `python3 scripts/init_env.py` generates unique local development passwords and JWT secret.
6. `docker compose up -d db && ./gradlew bootRun`, or `docker compose up -d --build`.
7. Create your first feature (for StockFlow, start with inventory entities, business invariants, migrations and tests).

The rename tool updates Java package directories and package declarations in the main and test sources, Gradle project name, JWT issuer, DB name/username and Compose volume name. It intentionally does **not** rewrite an already deployed DB, existing `.env`, or Git remote.

## Release hardening

This starter is a **development foundation** and must not be treated as a complete ready-to-deploy authentication product. Apply the checklist in `SECURITY.md`. Never ship test credentials, hardcoded production secrets, or unchecked permission models.
