"""Account Groups endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== ACCOUNT GROUP TESTS ===")
results.append(test("TC-AG-001", "/api/account_groups", OW, {}, 200, "account groups list"))
results.append(test("TC-AG-002", "/api/account_group_create", OW, {"group_name": "Test Group"}, 200, "account group create"))
results.append(test("TC-AG-004", "/api/account_group_delete", OW, {"group_id": "valid_id=="}, 200, "account group delete"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== ACCOUNT GROUP SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)