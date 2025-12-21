![Tests & Lint](https://github.com/<ORGANIZATION>/<MODULE_NAME>/actions/workflows/ci.yaml/badge.svg?branch=main)
![PyPI](https://img.shields.io/pypi/v/<MODULE_NAME>.svg)
![Downloads](https://static.pepy.tech/badge/<MODULE_NAME>)
![Monthly Downloads](https://static.pepy.tech/badge/<MODULE_NAME>/month)
![License](https://img.shields.io/github/license/sinan-ozel/pypi-publish-with-cicd.svg)

# Introduction

# ✨ Introduction

This repository serves as a polished, production-ready template for creating PyPI modules.

It includes:

- 🧪 **Automated Unit Testing** — Comprehensive test execution via CI.
- 🧹 **Linting & Code Quality** — Ensures clean, consistent standards.
- 🔢 **SemVer-Compatible Versioning** — Predictable, automated release management.

Additional features:

- 🛠️ **.devcontainer Environment** — Enables seamless collaboration with zero local setup beyond VS Code and Docker.
- ▶️ **Ready-Made VS Code Tasks** (`.vscode/tasks.json`) — Developers can run tests instantly, even without installing dependencies.

# Examples
(https://github.com/sinan-ozel/pytest-repeated)[https://github.com/sinan-ozel/pytest-repeated]
(https://github.com/sinan-ozel/redis-memory)[https://github.com/sinan-ozel/redis-memory]

# Usage

1. Base a repo on this template.

2. Find all instances of <MODULE_NAME>, <MODULE-NAME> and <ORGANIZATION> in muiiltiple files and replace with your module. (Take care with `_` and `-`, use `-` in docker-compose.yaml, `_` in `pyproject.toml`, and in the shields.
Python requires module names to use `_`, but the URLs tend to use `-`.

3. Create the folders `src/` and `src/<MODULE_NAME>`. `touch src/<MODULE_NAME>/__init__.py`

3. Add name and email under author in `pyproject.toml`.

3. Set up PyPI repo with the <MODULE_NAME>. Set up publisher as the github repo that you created in step 1. (See below for more details.) # TODO: Add a link to a good set of instructions.

4. Update the readme: Delete the top part, Introduction and Usage, and replace with your content.

## PyPI Setup

1. Clock on your username on PyPI to get a scroll-down menu, then go to "Your Projects" -> "Publishing".
2. Scroll down. Stay on the GitHub tab.
3. Enter the <MODULE_NAME> from the repo as ``PyPI Project Name''. (Actually, you can have a different name, but few do that.)
4. Enter the <ORGANIZATION> from the repo as ``Organization Name''.
5. Enter the <MODULE_NAME> from the repo as ``Repository Name''. (Actually, you can have a different name, but few do that.)
6. Workflow name is `ci.yaml` - it's the file in the `.github/workflows/` folder. Just enter the filename, not the full path.
7. You do not need to enter anything in the environment, keep the default.

This is it. Pro Tip: Make sure that the PyPI project name is available before creating the repo.


```
--- WHEN UPDATING README.md: YOU CAN KEEP EVERYTHING BELOW THIS LINE ---
```

# 🛠️ Development

The only requirement is 🐳 Docker.
(The `.devcontainer` and `tasks.json` are prepared assuming a *nix system, but if you know the commands, this will work on Windows, too.)

1. Clone the repo.
2. Branch out.
3. Open in "devcontainer" on VS Code and start developing. Run `pytest` under `tests` to test.
4. Akternatively, if you are a fan of Test-Driven Development like me, you can run the tests without getting on a container. `.vscode/tasks.json` has the command to do so, but it's also listed here:
```
docker compose -f tests/docker-compose.yaml up --build --abort-on-container-exit --exit-code-from test
```
