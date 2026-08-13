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
16 passed, 1 warning in 0.17s
```

## Scope control

No new product feature was added during the final project. App changes stayed limited to release hardening and bug fixes: CORS was narrowed to local frontend origins, an unused hidden test reset endpoint was removed, and update validation now rejects explicit `null` for non-nullable PATCH fields before storage can be mutated.

## CI evidence

- Workflow file: `.github/workflows/ci.yml`
- CI run: `https://github.com/MhmdAssaf14/task-tracker-final-project/actions/runs/31641977746`
- CI branch: `final-project`
- CI commit: `6ce8411`
- CI status: successful/green
- CI duration: 17 seconds
- Trigger check: the workflow runs on pushes to `final-project`, `mid-course-project`, and `main`, and on pull requests.
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

- Observed Docker `/health` result from local verification:

```text
HTTP/1.1 200 OK
date: Wed, 12 Aug 2026 21:17:19 GMT
server: uvicorn
content-length: 62
content-type: application/json

{"status":"ok","timestamp":"2026-08-12T21:17:19.696311+00:00"}
```

- Non-root check: `Dockerfile` creates `appuser` and runs the container with `USER appuser`.
- No-baked-secrets check: `Dockerfile` copies only `requirements.txt` and `app/`. `.dockerignore` excludes `.env`, `.env.*`, logs, virtual environments, caches, and `.git`.
- Environment note: Docker was run locally before submission. The image built successfully, the container started on port 8000, `GET /health` returned HTTP 200 with `status` equal to `ok`, and the temporary `task-tracker-final-check` container was removed afterward.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| README says `python -m pytest -q` runs the test suite. | Ran `.venv\Scripts\python -m pytest -q`. | Passed: `16 passed, 1 warning in 0.17s`. | Evidence updated with the current regression-test result. |
| README says `/health` returns HTTP 200. | Started Uvicorn and ran `curl -i http://127.0.0.1:8006/health`. | Passed: HTTP 200 with `status` equal to `ok`. | README and evidence use the actual endpoint. |
| CI runs pytest without dangerous shortcuts. | Inspected `.github/workflows/ci.yml`. | Passed: explicit Python `3.11`, dependency installation, direct pytest command, no `continue-on-error` or `|| true`. | No change after inspection. |
| Docker image avoids copied secrets. | Inspected `Dockerfile` and `.dockerignore`. | Passed by file review: `.env` patterns are ignored and the image copies only runtime app files. | Kept Dockerfile minimal and used non-root `appuser`. |
