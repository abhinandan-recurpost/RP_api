"""DM Automations endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== DM TESTS ===")
results.append(test("TC-DM-001", "/api/dm_automation_accounts", OW, {}, 200, "dm automation accounts"))
results.append(test("TC-DM-003", "/api/dm_automation_list", OW, {}, 200, "dm automation list"))
results.append(test("TC-DM-005", "/api/dm_automation_stats", OW, {}, 200, "dm automation stats"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== DM SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)