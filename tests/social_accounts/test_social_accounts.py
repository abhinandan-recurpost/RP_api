"""Social Accounts endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== SOCIAL ACCOUNTS TESTS ===")
results.append(test("TC-SA-001", "/api/social_account_list", OW, {}, 200, "owner lists social accounts"))
results.append(test("TC-SA-002", "/api/social_account_details", OW, {"social_account_id": "sa_valid_id=="}, 200, "valid social account details"))
results.append(test("TC-SA-003", "/api/social_account_details", OW, {"social_account_id": "invalid=="}, 404, "invalid social account id"))
results.append(test("TC-SA-004", "/api/social_account_status", OW, {}, 200, "social account status"))
results.append(test("TC-SA-007", "/api/social_account_remove", WR, {}, 403, "non-owner removes social account"))
results.append(test("TC-SA-008", "/api/connect_social_account_urls", OW, {}, 200, "connect social account urls"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== SOCIAL ACCOUNTS SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)