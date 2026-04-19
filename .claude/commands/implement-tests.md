---
allowed-tools: Bash(git *), Edit(tests/**), Write(tests/**), Read
---

Implement tests for the following feature: $ARGUMENTS

## Step 1 — Understand the Repo
Read `README.md` carefully. Understand:
- The purpose and scope of the project
- Key concepts, terminology, and architecture
- Any conventions or constraints mentioned

## Step 2 — Branch
Make sure you are on the main branch.
```
git checkout main
```
Make sure that `main` is up-to-date, `git pull`.

If something is not as expected, stop and report.
If the pull errors out, do not try to fix it, just stop.

Create a new branch with a reasonable name based on the feature description:
```
git checkout -b <branch-name>
```

## Step 3 — Study Tests
Read ALL files under `tests/` carefully. Understand:
- The exact testing patterns and conventions used
- How tests are structured, named, and organized
- What utilities, fixtures, or helpers are used
- The import style and assertion style

## Step 4 — Write Tests
Write new tests for the feature. Rules:
- Follow the exact same patterns observed in `tests/` — no exceptions
- Use the same file naming convention
- Use the same assertion style
- Use the same fixtures and utilities already present
- Do NOT introduce new testing patterns, libraries, or styles not already in use
- Do NOT create or modify any files under `.github/`

## Step 5 — Pause for Review
List all test files written and what each test covers.
Ask the user: "Tests are written. Please review and confirm to proceed with implementation by running /implement-finish."

## Step 6 — Report Token Usage
Run:
```
/cost
```
Report the token usage and cost for this session so far.