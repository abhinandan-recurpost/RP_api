"""RBAC Cross-Cutting permission tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])
PU = login(ACCOUNTS["publisher"][0], ACCOUNTS["publisher"][1])
ED = login(ACCOUNTS["editor"][0], ACCOUNTS["editor"][1])

SHARED_WS = "mnCkYKT+a8wM51bBC/lOzg=="
OWNER_WS = "MlWlT6qeem2MMkIW8mWYmg=="

print("=== RBAC TESTS ===")
results.append(test("RBAC-001", "/api/workspace_delete", WR, {"workspace_id": SHARED_WS, "confirm": True}, 403, "writer cannot delete workspace"))
results.append(test("RBAC-002", "/api/workspace_member_remove", WR, {"workspace_id": SHARED_WS, "user_id": "dGODSaojqRC1C/1oY/ZZsg=="}, 403, "writer cannot remove members"))
results.append(test("RBAC-003", "/api/workspace_update", WR, {"workspace_id": SHARED_WS, "name": "Hacked"}, 403, "writer cannot update workspace settings"))
results.append(test("RBAC-004", "/api/workspace_clone", WR, {"workspace_id": SHARED_WS, "name": "Cloned"}, 403, "writer cannot clone workspace"))
results.append(test("RBAC-005", "/api/role_create", WR, {"name": "TestRole", "template": "writer"}, 200, "writer CAN create roles (feature)"))
results.append(test("RBAC-006", "/api/role_set_permissions", WR, {"permissions": {"send-client": True}}, 403, "writer cannot escalate permissions"))
results.append(test("RBAC-008", "/api/post_publish", WR, {"post_id": "valid_id=="}, 403, "writer cannot publish posts"))
results.append(test("RBAC-009", "/api/post_approve", WR, {"post_id": "valid_id=="}, 403, "writer cannot approve posts"))
results.append(test("RBAC-010", "/api/workflow_send_client", WR, {"card_id": "valid_id=="}, 403, "writer cannot send to clients"))
results.append(test("RBAC-013", "/api/post_publish", PU, {"post_id": "valid_id=="}, 200, "publisher can publish posts"))
results.append(test("RBAC-014", "/api/post_approve", PU, {"post_id": "valid_id=="}, 200, "publisher can approve posts"))
results.append(test("RBAC-015", "/api/workflow_send_client", PU, {"card_id": "valid_id=="}, 200, "publisher can send to clients"))
results.append(test("RBAC-018", "/api/post_approve", ED, {"post_id": "valid_id=="}, 200, "editor can approve posts"))
results.append(test("RBAC-019", "/api/post_edit", ED, {"post_id": "valid_id=="}, 200, "editor can edit others posts"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== RBAC SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)