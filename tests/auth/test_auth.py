"""Authentication endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== AUTH TESTS ===")
results.append(test("TC-AUTH-001", "/api/user_login", None,
    {"emailid": ACCOUNTS["owner"][0], "api_key": ACCOUNTS["owner"][1]}, 200, "valid credentials"))
results.append(test("TC-AUTH-002", "/api/user_login", None,
    {"emailid": ACCOUNTS["owner"][0], "api_key": "wrongkey"}, 401, "wrong api key"))
results.append(test("TC-AUTH-003", "/api/user_login", None,
    {"api_key": ACCOUNTS["owner"][1]}, 401, "missing emailid"))
results.append(test("TC-AUTH-004", "/api/user_login", None,
    {"emailid": ACCOUNTS["owner"][0]}, 401, "missing api_key"))
results.append(test("TC-AUTH-007", "/api/user_login", None,
    {"emailid": ACCOUNTS["owner"][0], "pass_key": ACCOUNTS["owner"][1]}, 200, "pass_key alias"))
results.append(test("TC-AUTH-008", "/api/user_login", None,
    {"emailid": ACCOUNTS["owner"][0], "zapier_key": ACCOUNTS["owner"][1]}, 200, "zapier_key alias"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== AUTH SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)