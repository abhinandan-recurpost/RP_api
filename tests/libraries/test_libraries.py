"""Libraries endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== LIBRARY TESTS ===")
results.append(test("TC-LIB-001", "/api/library_list", OW, {}, 200, "library list"))
results.append(test("TC-LIB-003", "/api/library_create", OW, {"name": "Test Library"}, 200, "library create valid"))
results.append(test("TC-LIB-008", "/api/library_content_list", OW, {}, 200, "library content list"))
results.append(test("TC-LIB-018", "/api/library_delete", OW, {"library_id": "test_library_id=="}, 200, "library delete"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== LIBRARY SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)