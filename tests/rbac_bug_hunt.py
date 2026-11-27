"""RBAC Bug Hunting Tests - cross-role permission bypass attempts.
Uses real workspace/member IDs from the live API (not placeholders).
Run independently: python tests/rbac_bug_hunt.py
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from conftest import *

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])
PU = login(ACCOUNTS["publisher"][0], ACCOUNTS["publisher"][1])
ED = login(ACCOUNTS["editor"][0], ACCOUNTS["editor"][1])

print("=== BUG HUNT: RBAC Cross-Role Access ===\n")

# Get real workspace list
status, ws_list = call("/api/workspace_list", OW, {})
workspaces = ws_list.get("workspace_list", [])
if not workspaces:
    print("NO WORKSPACES FOUND - cannot run IDOR tests")
else:
    # Get first workspace ID
    first_ws = workspaces[0]["ws_id"]
    print(f"Using workspace: {first_ws}")

    # --- IDOR: Writer accessing Owner's workspace ---
    status, resp = call("/api/workspace_details", WR, {"workspace_id": first_ws})
    results.append(test("BUG-IDOR-001", "/api/workspace_details", WR,
        {"workspace_id": first_ws}, 403,
        "Writer should NOT access Owner workspace details"))
    # (if returns 200 = BUG)

    # --- IDOR: Editor accessing Owner's workspace ---
    status, resp = call("/api/workspace_details", ED, {"workspace_id": first_ws})
    results.append(test("BUG-IDOR-002", "/api/workspace_details", ED,
        {"workspace_id": first_ws}, 403,
        "Editor should NOT access Owner workspace details"))

    # --- IDOR: Publisher accessing Owner's workspace ---
    status, resp = call("/api/workspace_details", PU, {"workspace_id": first_ws})
    results.append(test("BUG-IDOR-003", "/api/workspace_details", PU,
        {"workspace_id": first_ws}, 403,
        "Publisher should NOT access Owner workspace details"))

    # --- Writer trying to delete Owner workspace ---
    status, resp = call("/api/workspace_delete", WR,
        {"workspace_id": first_ws, "confirm": True})
    results.append(test("BUG-IDOR-004", "/api/workspace_delete", WR,
        {"workspace_id": first_ws, "confirm": True}, 403,
        "Writer should NOT delete Owner workspace"))

    # --- Writer trying to update workspace settings ---
    status, resp = call("/api/workspace_update", WR,
        {"workspace_id": first_ws, "name": "Hacked Workspace"})
    results.append(test("BUG-IDOR-005", "/api/workspace_update", WR,
        {"workspace_id": first_ws, "name": "Hacked Workspace"}, 403,
        "Writer should NOT update workspace settings"))

    # --- Writer trying to clone workspace ---
    status, resp = call("/api/workspace_clone", WR,
        {"workspace_id": first_ws, "name": "Cloned"})
    results.append(test("BUG-IDOR-006", "/api/workspace_clone", WR,
        {"workspace_id": first_ws, "name": "Cloned"}, 403,
        "Writer should NOT clone workspace"))

    # --- Writer trying to remove members ---
    status, resp = call("/api/workspace_member_remove", WR,
        {"workspace_id": first_ws, "user_id": "dGODSaojqRC1C/1oY/ZZsg=="})
    results.append(test("BUG-IDOR-007", "/api/workspace_member_remove", WR,
        {"workspace_id": first_ws, "user_id": "dGODSaojqRC1C/1oY/ZZsg=="}, 403,
        "Writer should NOT remove members"))

    # --- Cross-user: different account accessing same workspace ---
    status, resp = call("/api/workspace_members", WR, {"workspace_id": first_ws})
    results.append(test("BUG-IDOR-008", "/api/workspace_members", WR,
        {"workspace_id": first_ws}, 403,
        "Writer should NOT list members of workspace they don't own"))

# --- Auth bypass: expired/invalid token ---
status, resp = call("/api/workspace_list", "invalid.token.here", {})
results.append(test("BUG-AUTH-001", "/api/workspace_list", "invalid.token.here", {},
    401, "Invalid token should return 401"))

status, resp = call("/api/workspace_list", "", {})
results.append(test("BUG-AUTH-002", "/api/workspace_list", "", {},
    401, "Empty token should return 401"))

# --- Writer creating role with escalated permissions ---
status, resp = call("/api/role_create", WR, {"name": "SuperWriter", "template": "writer"})
role_id = resp.get("role_id", "")
results.append(test("BUG-RBAC-001", "/api/role_create", WR,
    {"name": "SuperWriter", "template": "writer"}, 200,
    "Writer CAN create roles (feature)"))
if role_id:
    # Try to escalate the new role's permissions
    status, resp = call("/api/role_set_permissions", WR,
        {"role_id": role_id, "permissions": {"send-client": True, "publish": True, "approve": True}})
    results.append(test("BUG-RBAC-002", "/api/role_set_permissions", WR,
        {"role_id": role_id, "permissions": {"send-client": True, "publish": True, "approve": True}}, 403,
        "Writer should NOT escalate own role permissions"))

# --- Editor trying to publish posts (should need publisher role) ---
status, resp = call("/api/post_publish", ED, {"post_id": "valid_post_id=="})
results.append(test("BUG-RBAC-003", "/api/post_publish", ED,
    {"post_id": "valid_post_id=="}, 403,
    "Editor should NOT publish posts"))

# --- Writer trying to approve posts ---
status, resp = call("/api/post_approve", WR, {"post_id": "valid_post_id=="})
results.append(test("BUG-RBAC-004", "/api/post_approve", WR,
    {"post_id": "valid_post_id=="}, 403,
    "Writer should NOT approve posts"))

# --- Non-owner trying workspace_settings ---
status, resp = call("/api/workspace_settings", WR,
    {"workspace_id": first_ws if workspaces else "dummy=="})
results.append(test("BUG-RBAC-005", "/api/workspace_settings", WR,
    {"workspace_id": first_ws if workspaces else "dummy=="}, 403,
    "Writer should NOT access workspace settings"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== RBAC BUG HUNT SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
print("FAILED tests above are POTENTIAL BUGS - investigate each")
with open(os.path.join(os.path.dirname(__file__), "rbac_bug_results.json"), "w") as f:
    json.dump(results, f, indent=2)