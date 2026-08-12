# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: yes.
- Docs-first/read-first guardrail included: yes.
- Unexpected `app/` or `frontend/` edits rule included: yes.

`AGENTS.md` tells AI tools to read the README, backend files, tests, and final evidence files before suggesting edits. It also states that authentication, a production database, comments, notifications, real-time updates, and unrelated UI changes are out of scope.

## AI code review mini-log

Reviewed files: `.github/workflows/ci.yml`, `Dockerfile`, `.dockerignore`, `README.md`, `app/main.py`, `app/models.py`, and `tests/test_baseline_api.py`.

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| Use an explicit Python version in CI instead of a vague latest version. | Useful | The final brief asks graders to check for vague Python versions and dangerous shortcuts. | Implemented `python-version: "3.11"` in `.github/workflows/ci.yml`. |
| Add Docker runtime as a non-root user. | Useful | This is a reasonable hardening step and does not add a product feature. | Implemented `appuser` and `USER appuser` in `Dockerfile`. |
| Add authentication before final submission. | Wrong | Authentication is explicitly outside the course Task Tracker scope and the final project says not to add new product features. | Rejected. No auth files, login UI, or token logic were added. |
| Add a production database so Docker data persists. | Wrong | A production database would change the architecture and scope. The course baseline uses in-memory storage. | Rejected. Kept in-memory storage and documented runtime limitations. |

## AI security mini-review

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| CORS allowed all origins and credentials. | `app/main.py` previously used `allow_origins=["*"]` and `allow_credentials=True`. | Valid | Too broad even for a learning app and easy to narrow without changing product behavior. | Corrected to local frontend origins and `allow_credentials=False`. |
| Hidden `/test/reset` route could clear all tasks if the app were exposed. | `app/main.py` previously included `@app.post("/test/reset", include_in_schema=False)`. | Valid | Tests reset storage directly through the fixture, so this route was not needed. | Removed the route as a small security-supported correction. |
| Explicit `null` in PATCH could corrupt task records. | `app/models.py` allowed explicit `None` for non-nullable update fields and `app/storage.py` applied `exclude_unset=True` updates directly. | Valid | A rejected update should never write invalid values into storage or break later response validation. | Corrected `TaskUpdate` validation and added regression tests for `title: null` and other non-nullable fields. |
| No authentication on task endpoints. | `app/main.py` routes are public. | False Positive | The course scope intentionally excludes authentication, user accounts, and multi-tenancy. | No change. Documented as out of scope, not a final-project gap. |
| In-memory storage loses tasks on restart. | `app/storage.py` uses a module-level dictionary. | Noise | This is a known learning-project architecture choice, not a release security defect for this course. | No change. README describes the project as a learning Task Tracker. |

## Manual security check

I manually checked the repository for committed secrets and local-only files. `.gitignore` excludes `.env`, virtual environments, caches, and Python bytecode. `.dockerignore` excludes `.env`, `.env.*`, logs, caches, and `.git`. The repo keeps only `.env.example`, which contains non-secret sample configuration.

## One AI output I rejected or corrected

AI suggested adding authentication and a persistent database as part of “release hardening.” I rejected both suggestions because the final brief says not to add new product features and the original course scope excludes authentication and production database work. Instead, I limited final code changes to small release-readiness corrections: narrowing CORS, removing the unused test reset endpoint, and fixing the explicit-null PATCH validation bug reported during review.

## Three AI usage rules

1. Never paste: real secrets, `.env` values, access tokens, customer data, production logs, or private personal data into AI tools or the repo.
2. Always verify: run pytest, check `/health`, inspect the diff, and confirm Docker/CI behavior before accepting AI-generated release changes.
3. Record AI contributions by: naming the changed file, grading review comments as Useful/Noise/Wrong or Valid/False Positive/Noise, and writing down what I accepted, corrected, or rejected.

## Ownership statement

I am comfortable submitting this repository as my own work because I inspected the generated files, ran the backend checks, ran the pytest suite, and reviewed the release changes against the course scope. I did not accept AI suggestions blindly; I rejected scope-expanding ideas such as authentication and production database work. The final changes are small, explainable, and documented with evidence. I can explain the CI file, Dockerfile, security fixes, run commands, and the reason each final evidence document exists.
