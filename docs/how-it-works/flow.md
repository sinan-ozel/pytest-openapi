## Execution Flow

1. **Plugin Configuration** (`pytest_configure`)
   - Load OpenAPI specification from the provided URL
   - Validate spec completeness and quality
   - Store configuration for test generation

2. **Test Collection** (`pytest_generate_tests`)
   - Iterate over all paths and HTTP methods
   - Generate test cases from examples and schemas
   - Parametrize test function with individual test cases
   - Each test case becomes a separate pytest item

3. **Test Execution** (pytest's normal flow)
   - pytest collects and runs each parametrized test item
   - For each test: generate request payload, execute HTTP request
   - Compare response to contract (example or schema)
   - pytest reports pass/fail for each test item

4. **Report Generation** (`pytest_sessionfinish`)
   - Compile all test results
   - Write detailed markdown report to file
   - Display report location message

This integration with pytest's standard flow means OpenAPI tests appear alongside your regular tests in the pytest output and benefit from pytest's features (parallel execution, reporting, etc.).