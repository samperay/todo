---
name: pull-request
description: >-
  Draft and publish a GitHub pull request title and description for this
  repository, including local Ruff, Mypy, Pytest, and coverage results. Use
  when the user asks to open a pull request, update a pull request description,
  fill a PR title or body, or include test results on a pull request.
---

# Pull request

Write the title and description, then publish them with `gh`. Run the checks in `backend/` before writing the description. Do not invent results.

## Checks

From `backend/`, with the virtual environment active:

```bash
ruff check .
ruff format --check .
mypy src
python -m pytest --cov=todo_api --cov-report=term-missing --cov-fail-under=90
```

Record each command as Passed or Failed, plus the coverage percentage pytest prints. If a command fails, include the relevant failure output in the description and still publish when the user asked to open the pull request.

## Title

Use one line, at most 72 characters, that states the change. Prefer the commit style already on `main` (`feat:`, `fix:`, `docs:`, `ci:`, `test:`, `chore:`).

Leave an existing title unchanged when it is not the branch name.

## Description

Keep any description the author already wrote. Add or replace only the block between `<!-- ci-status:start -->` and `<!-- ci-status:end -->`.

When the description is empty, start with a short summary of the commits and the diff, then the results block:

```markdown
## Summary
- <what changed and why>

<!-- ci-status:start -->
## CI results

| Check | Result |
| --- | --- |
| Ruff Lint | Passed |
| Ruff Format | Passed |
| Mypy | Passed |
| Pytest | Passed |
| Coverage | 98.0% |

Checked locally before this pull request was published.
<!-- ci-status:end -->
```

Use the real result and coverage values. Keep the results inside the markers so a later run of this skill can refresh them.

## Publish

Push the current branch, then create the pull request against `main`:

```bash
git push -u origin HEAD
gh pr create --base main --title "<title>" --body-file pr-body.md
```

When a pull request for this branch already exists, edit it instead:

```bash
gh pr edit --title "<title>" --body-file pr-body.md
```

Omit `--title` when the existing title should stay. Delete `pr-body.md` after `gh` succeeds. Return the pull request URL.
