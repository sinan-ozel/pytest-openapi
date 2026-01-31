# Pytest timeout example

Example command demonstrating the `--pytest-timeout` option:

```bash
pytest --pytest-timeout=60 -v
```

- `--pytest-timeout`: set the global pytest timeout (in seconds) for tests.

Use this option when you want to limit how long tests may run, for example
when running against slow or flaky test servers.
