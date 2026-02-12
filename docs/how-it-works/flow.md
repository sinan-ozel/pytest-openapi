## Execution Flow

1. **Plugin Configuration** (`pytest_configure`)
   - Load OpenAPI specification from the provided URL
   - Validate spec completeness and quality
   - Store configuration for dynamic test generation

2. **Test Collection** (`pytest_collection_modifyitems`)
   - Dynamically inject OpenAPI test items into pytest's collection
   - Iterate over all paths and HTTP methods in the OpenAPI spec
   - Generate test cases from examples and schemas
   - Create individual `pytest.Function` items for each test case
   - Each test appears as `.::test_openapi[METHOD /path [origin-N]]`
   - Add items to pytest's test collection

3. **Collection Finish** (`pytest_collection_finish`)
   - Print summary of created test items:
     - Number of items from OpenAPI examples
     - Number of items generated from schemas

4. **Test Execution** (pytest's normal flow)
   - pytest runs each dynamically created test item
   - For each test: generate request payload, execute HTTP request
   - Compare response to contract (example or schema)
   - pytest reports pass/fail for each test item
   - In verbose modes (`-vv`, `-vvv`), print request/response details

5. **Report Generation** (`pytest_sessionfinish`)
   - Compile all test results
   - Write detailed markdown report to file (if configured)
   - Display report location message

This integration with pytest's standard flow means OpenAPI tests appear alongside your regular tests in the pytest output and benefit from pytest's features (parallel execution, reporting, etc.).