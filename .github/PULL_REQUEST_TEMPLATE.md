# 🧪 Pull Request Checklist

**Development Environment:** There is a devcontainer if you are using VS Code, you can just run that and you will not need to install anything. Otherwise, rely on `pyprojext.toml`

- [ ] **Existing Tests:** Run all containerized tests before submitting the PR
  - VS Code task: `test`
  - CLI:
    ```bash
    docker compose -f ./tests/docker-compose.yaml --project-directory ./tests up --build --abort-on-container-exit --exit-code-from test
    ```

- [ ] **New Tests:**
  - Add your own mock server if needed, then add integration tests using:
    ```python
    subprocess.run(['pytest', '--openapi=http://your-server:8000'])
    ```
    See the current test implementation under [tests/test_integration.py](tests/test_integration.py)

- [ ] **Lint / Reformat:** Ensure code is properly formatted before PR
  - VS Code task: `lint`
  - CLI:
    ```bash
    docker compose -f ./lint/docker-compose.yaml --project-directory ./lint up --build --abort-on-container-exit --exit-code-from linter
    ```

- [ ] **Documentation:** Add or update documentation for any new functionality

**Dev Release:** After merge, verify the dev release and update version numbers as needed
