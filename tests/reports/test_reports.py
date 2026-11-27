"""Reports endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== REPORTS TESTS ===")
results.append(test("TC-REP-001", "/api/report_account", OW, {}, 200, "report account"))
results.append(test("TC-REP-002", "/api/report_posts", OW, {}, 200, "report posts"))
results.append(test("TC-REP-004", "/api/report_pins", OW, {}, 200, "report pins"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== REPORTS SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)