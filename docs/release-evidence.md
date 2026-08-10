# Release Evidence

## Baseline

- Branch: `final-project`
- Date: 2026-08-05
- Local app run command:

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8006
```

- `/health` result:

```text
HTTP/1.1 200 OK
{"status":"ok","timestamp":"2026-08-05T18:50:00.531871+00:00"}
```

- Frontend check: Opened with `cd frontend && python -m http.server 5173`, then `http://localhost:5173`. The Kanban board, New Task modal, create/edit fields, due date display, tag chips, and filters remain visible and inside the existing Task Tracker scope.
- Test command:

```bash
python -m pytest -q
```

- Test result:

```text
14 passed in 0.11s
```

## Scope control

No new product feature was added during the final project. The only `app/` change was a small security-supported correction recorded in `docs/final-ai-review.md`: CORS was narrowed to local frontend origins and an unused hidden test reset endpoint was removed.

## CI evidence

- Workflow file: `.github/workflows/ci.yml`
- Latest run link or note: After pushing the `final-project` branch, confirm the GitHub Actions `CI` workflow is green. Replace this note with the green run link before final submission if your LMS/instructor expects the link in the document.
- Test command used by CI:

```bash
python -m pytest -q
```

- Shortcut check: `.github/workflows/ci.yml` uses Python `3.11`, installs `requirements.txt`, and runs pytest directly. It does not use `continue-on-error`, `|| true`, skipped pytest commands, or a vague Python version.

## Docker evidence

- Dockerfile: `Dockerfile`
- Ignore file: `.dockerignore`
- Build command:

```bash
docker build -t task-tracker-final .
```

- Run command:

```bash
docker run --rm -p 8000:8000 task-tracker-final
```

- `/health` check:

```bash
curl -i http://localhost:8000/health
```

- Expected successful result:

```text
HTTP/1.1 200 OK
{"status":"ok", ...}
```

- Non-root check: `Dockerfile` creates `appuser` and runs the container with `USER appuser`.
- No-baked-secrets check: `Dockerfile` copies only `requirements.txt` and `app/`. `.dockerignore` excludes `.env`, `.env.*`, logs, virtual environments, caches, and `.git`.
- Environment note: Docker was run locally before submission. The image built successfully, the container started on port 8000, and `GET /health` returned HTTP 200 with `status` equal to `ok`.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| README says `python -m pytest -q` runs the test suite. | Ran `python -m pytest -q`. | Passed: `14 passed in 0.11s`. | README kept this exact command and result. |
| README says `/health` returns HTTP 200. | Started Uvicorn and ran `curl -i http://127.0.0.1:8006/health`. | Passed: HTTP 200 with `status` equal to `ok`. | README and evidence use the actual endpoint. |
| CI runs pytest without dangerous shortcuts. | Inspected `.github/workflows/ci.yml`. | Passed: explicit Python `3.11`, dependency installation, direct pytest command, no `continue-on-error` or `|| true`. | No change after inspection. |
| Docker image avoids copied secrets. | Inspected `Dockerfile` and `.dockerignore`. | Passed by file review: `.env` patterns are ignored and the image copies only runtime app files. | Kept Dockerfile minimal and used non-root `appuser`. |
