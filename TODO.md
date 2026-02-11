- [ ] Add a test to see if it follows declared data types.
- [ ] Add a test with a regexp
- [ ] Go over the messages, make them useful.
- [ ] (Requires LiteLLM) Check if descriptions make sense
- [ ] (Requires LiteLLM) Check if error messages make sense with 400, and responses are clear with 201.
- [ ] (Requires LiteLLM) Check if the responses match descriptions.
- [ ] Check the new output with -vv
- [ ] Check the new output with -vvv
- [ ] Check the new output with -vvvv
- [ ] Check report.md
- [ ] Removed check for "enum_field" in verbose output - put this back
- [ ] Remove "test case created from schema" in the output - put this back.
- [ ] Removed assertion looking for "Expected" and status codes in same line (old verbose format) Put this back
- [x] Add the test "module" name in the output with no verbosity.
- [ ] Add something like "pytest-openapi added 10 tests" under "collected 3 items" and add an integration test to check.


==================================================

✅ OpenAPI spec validated successfully from http://mock-server:8000/openapi.json
   Found 1 path(s)

✅ OpenAPI spec validated and loaded from http://mock-server:8000/openapi.json

✅ OpenAPI spec validated and loaded from http://mock-server:8000/openapi.json
====================================================================================== test session starts =======================================================================================
platform linux -- Python 3.11.14, pytest-9.0.2, pluggy-1.6.0
rootdir: /workspace
plugins: openapi-0.2.1, depends-1.0.1, mock-3.15.1
collected 3 items

tests/test_samples/test_sample_math.py ..                                                                                                                                                  [ 15%]
. ..........                                                                                                                                                                               [ 92%]
tests/test_samples/test_sample_math.py .                                                                                                                                                   [100%]
📝 Full test report saved to: /workspace/tests/report.md
   (Configure output file with: --openapi-markdown-output=<filename>)


======================================================================================= 13 passed in 0.11s =======================================================================================
==================================================
