"""Account & Settings endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== ACCOUNT TESTS ===")
results.append(test("TC-ACC-001", "/api/account_details", OW, {}, 200, "owner account details"))
results.append(test("TC-ACC-002", "/api/account_timezone", OW, {}, 200, "account timezone"))
results.append(test("TC-ACC-005", "/api/account_limits", OW, {}, 200, "account limits"))
results.append(test("TC-ACC-006", "/api/plan_details", OW, {}, 200, "plan details"))
results.append(test("TC-ACC-008", "/api/queue_pause", OW, {}, 200, "pause queue"))
results.append(test("TC-ACC-009", "/api/queue_resume", OW, {}, 200, "resume queue"))
results.append(test("TC-ACC-010", "/api/x_wallet", OW, {}, 200, "wallet balance"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== ACCOUNT SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)