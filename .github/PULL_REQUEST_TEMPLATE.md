# 🧪 Pull Request Checklist

- [ ] **Tests:** Run all containerized tests before submitting the PR
  - VS Code task: `test`
  - CLI:
    ```bash
    docker compose -f ./tests/docker-compose.yaml --project-directory ./tests up --build --abort-on-container-exit --exit-code-from test
    ```

- [ ] **Development Environment (Optional):**
  - VS Code task: `run-mock-server`
  - Run one of the mock servers in `tests/test_servers`
  - Add your own mock server if needed, then add integration tests using:
    ```python
    subprocess.run(['pytest', '--openapi=http://your-server:8000'])
    ```

- [ ] **Lint / Reformat:** Ensure code is properly formatted before PR
  - VS Code task: `lint`
  - CLI:
    ```bash
    docker compose -f ./lint/docker-compose.yaml --project-directory ./lint up --build --abort-on-container-exit --exit-code-from linter
    ```

- [ ] **Documentation:** Add or update documentation for any new functionality

- [ ] **Submit Bugs / Features:** Open an issue or PR for any bugs or feature requests

- [ ] **Dev Release:** After merge, verify the dev release and update version numbers as needed
