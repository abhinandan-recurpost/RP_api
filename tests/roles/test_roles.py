"""Team Roles endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== ROLE TESTS ===")
results.append(test("TC-ROLE-001", "/api/roles", OW, {}, 200, "owner lists roles"))
results.append(test("TC-ROLE-002", "/api/roles", WR, {}, 200, "member lists roles"))
results.append(test("TC-ROLE-003", "/api/role_permissions", OW, {}, 200, "role permissions valid"))
results.append(test("TC-ROLE-005", "/api/role_create", WR, {"name": "TestRole", "template": "writer"}, 200, "non-owner creates role"))
results.append(test("TC-ROLE-012", "/api/role_set_permissions", WR, {"permissions": ["send-client"]}, 400, "invalid format array"))
results.append(test("TC-ROLE-013", "/api/role_set_permissions", WR, {"permissions": {"send-client": True}}, 403, "non-owner escalates permissions"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== ROLE SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)