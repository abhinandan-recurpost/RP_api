"""Workspace endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

# Known workspace IDs from earlier runs
OWNER_WS = "MlWlT6qeem2MMkIW8mWYmg=="
SHARED_WS = "mnCkYKT+a8wM51bBC/lOzg=="

print("=== WORKSPACE TESTS ===")
results.append(test("TC-WS-001", "/api/workspace_list", OW, {}, 200, "owner lists workspaces"))
results.append(test("TC-WS-002", "/api/workspace_list", WR, {}, 200, "member lists workspaces"))
results.append(test("TC-WS-003", "/api/workspace_details", OW, {"workspace_id": OWNER_WS}, 200, "valid workspace details"))
results.append(test("TC-WS-004", "/api/workspace_details", OW, {"workspace_id": "nonexistent=="}, 400, "invalid workspace id"))
results.append(test("TC-WS-005", "/api/workspace_details", WR, {"workspace_id": OWNER_WS}, 404, "cross-user workspace details"))
results.append(test("TC-WS-009", "/api/workspace_update", OW, {"workspace_id": OWNER_WS, "name": "My Workspace"}, 200, "owner updates workspace"))
results.append(test("TC-WS-010", "/api/workspace_update", WR, {"workspace_id": SHARED_WS, "name": "Hacked"}, 403, "non-owner updates workspace"))
results.append(test("TC-WS-013", "/api/workspace_clone", WR, {"workspace_id": SHARED_WS, "name": "Cloned"}, 403, "non-owner clones workspace"))
results.append(test("TC-WS-015", "/api/workspace_delete", OW, {"workspace_id": SHARED_WS}, 400, "owner delete without confirm"))
results.append(test("TC-WS-016", "/api/workspace_delete", WR, {"workspace_id": SHARED_WS, "confirm": True}, 403, "non-owner deletes workspace"))
results.append(test("TC-WS-017", "/api/workspace_members", OW, {"workspace_id": SHARED_WS}, 200, "owner lists members"))
results.append(test("TC-WS-018", "/api/workspace_members", WR, {"workspace_id": OWNER_WS}, 404, "non-member lists members"))
results.append(test("TC-WS-023", "/api/workspace_member_update", WR, {"workspace_id": SHARED_WS, "user_id": "l+T81bFEu76Usgt05cLD1Q==", "role_id": "XqdhbL1XGr5uMzLIu+zBLA=="}, 403, "non-owner updates member role"))
results.append(test("TC-WS-025", "/api/workspace_member_remove", WR, {"workspace_id": SHARED_WS, "user_id": "dGODSaojqRC1C/1oY/ZZsg=="}, 403, "non-owner removes member"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== WORKSPACE SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)