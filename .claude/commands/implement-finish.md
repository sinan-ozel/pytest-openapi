---
allowed-tools: Bash(docker compose *), Bash(git *), Edit(!tests/**), Write(!tests/**), Read
---

The tests have been reviewed and approved. Complete the implementation.

## Step 1 — Write Implementation
Implement the feature. Infer code style and conventions from the existing codebase.

STRICT RULE: Do NOT modify any files under `tests/`. Do not add, edit, or delete any test files under any circumstances.

## Step 2 — Update Docs
Update documentation under `docs/` to reflect the new feature.

## Step 3 — Test Loop
Run and repeat until exit code is 0. Fix only implementation files — never test files:
```
docker compose -f tests/docker-compose.yaml --project-directory tests up --build --abort-on-container-exit --exit-code-from test 2>&1
```

## Step 4 — Reformat
```
docker compose -f reformat/docker-compose.yaml up --build --abort-on-container-exit --exit-code-from reformat 2>&1
```

## Step 5 — Lint Loop
Run and repeat until exit code is 0. Fix only implementation files — never test files:
```
docker compose -f lint/docker-compose.yaml up --build --abort-on-container-exit --exit-code-from linter 2>&1
```

## Step 6 — Validate Docs Loop
Run and repeat until exit code is 0:
```
docker compose -f docs-validate/docker-compose.yaml --project-directory docs-validate up --build --abort-on-container-exit --exit-code-from docs-validator 2>&1
```

## Step 7 — Update CHANGELOG
1. Run `git tag --sort=-v:refname | head -5` to find the most recent tag
2. If `CHANGELOG.md` does not exist, create it with a standard header
3. Add a new entry at the top for the current change, using the next logical version after the most recent tag
4. Summarize what was implemented, what tests were added, and what docs were updated

## Step 8 — Commit & Push
1. Run `git status` to see all modified files
2. Stage and commit only the files that were changed by this implementation (excluding test files if they were somehow touched — they should not have been)
3. Stage them file-by-file, do not use asterisk (*)
4. Analyze all of it, git commit with a good message.
We are looking for a 50-character summary on top, detailed information below.

Separate subject from body with a blank line
Limit the subject line to 50 characters
Capitalize the subject line
Do not end the subject line with a period
Use the imperative mood in the subject line
Wrap the body at 72 characters
Use the body to explain what and why vs. how

Do not ask for permission, just write the commit.
5. git push

## Step 9 — Open a PR

Find the PR template:
- Look for a file matching `.github/*PULL_REQUEST_TEMPLATE*`

Get the current branch with `git branch --show-current`.
If it equals the default branch, stop and tell the user to switch branches first.

Run `git diff <default_branch>...<current_branch> --stat` and show the summary.

Get the full diff and commit log, then write a PR with:
- A title at Grade 5 reading level: short, plain, action-oriented
- A body that fills out the PR template based on the diff

Create the PR using: `gh pr create --title "..." --body "..."`

## Step 10 — Report Token Usage
Run:
```
/cost
```
Report the token usage and cost for this session so far.