# Environment Setup and Safe Lab Conventions

## Baseline

- macOS Apple Silicon development host; Ubuntu VM available for Linux-only exercises.
- Todo repository cloned and checked out to an explicit branch.
- Python, Node/npm, Git installed; Docker, Terraform, kubectl, and Helm are installed **only when their modules begin**.

## Verify tools without changing state

```bash
pwd
git branch --show-current
git status --short
python3 --version
node --version
npm --version
```

## Start Todo locally

Terminal A (repo root):

```bash
cd backend
uvicorn todo_api.main:app --reload --host 127.0.0.1 --port 8000
```

Terminal B (repo root):

```bash
cd frontend
npm run dev
```

Terminal C:

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
lsof -nP -iTCP:5173 -sTCP:LISTEN
curl -i http://127.0.0.1:8000/api/v1/todos
curl -i http://127.0.0.1:5173/api/v1/todos
```

Unauthenticated Todo GET commonly returns 401 **when the API is healthy**. Use browser DevTools for authenticated GET; do not disclose tokens.

## Safe failure labs

1. Announce which disposable component will be stopped or altered.
2. Save a healthy baseline.
3. Set a time limit and know the exact rollback.
4. Do not modify production systems or the real SQLite file.
5. Verify restoration end to end, not only that a process exists.

## Code changes

Keep tutorials separate from application source. For any real feature use Spec Kit/specification artifacts, tests, code review, and a small PR.
