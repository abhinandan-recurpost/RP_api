"""Workflow endpoint tests (23 endpoints) — LIVE social.recurpost.com server."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])
PU = login(ACCOUNTS["publisher"][0], ACCOUNTS["publisher"][1])
ED = login(ACCOUNTS["editor"][0], ACCOUNTS["editor"][1])

# Create a test workspace
status, resp = call("/api/workspace_create", OW, {"name": "API_Test_Workspace_Live"})
WS_ID = resp.get("workspace", {}).get("id", "") or "Ygz0YeO9J3oQoIHgUG7xXQ=="
print(f"Created workspace: {WS_ID}")

print("=== LIVE WORKFLOW TESTS (social.recurpost.com) ===")
results.append(test("TC-WF-001", "/api/workflow_board", OW, {}, 200, "owner lists workflow board"))
results.append(test("TC-WF-002", "/api/workflow_board", WR, {}, 200, "writer lists workflow board"))
results.append(test("TC-WF-003", "/api/workflow_idea_create", WR, {"title": "Live Test Idea", "content": "Live test content"}, 200, "writer creates idea"))
results.append(test("TC-WF-004", "/api/workflow_idea_create", WR, {"title": "", "content": "test"}, 400, "empty title rejected"))
results.append(test("TC-WF-005", "/api/workflow_idea_create", WR, {"title": "A" * 300, "content": "test"}, 400, "very long title rejected"))
results.append(test("TC-WF-006", "/api/workflow_idea_create", WR, {"title": "'; DROP TABLE posts; --", "content": "test"}, 200, "SQL injection in title handled"))
results.append(test("TC-WF-007", "/api/workflow_idea_create", WR, {"title": "Hello 🎉", "content": "test"}, 200, "unicode emoji in title"))
results.append(test("TC-WF-008", "/api/workflow_idea_create", WR, {"title": None, "content": "test"}, 400, "null title rejected"))
results.append(test("TC-WF-009", "/api/workflow_idea_create", WR, {}, 400, "missing required fields"))
results.append(test("TC-WF-010", "/api/workflow_idea_create", WR, {"title": "Test", "content": "Test"}, 200, "valid idea creation"))

# RBAC tests
results.append(test("RBAC-WF-001", "/api/workflow_send_client", WR, {"card_id": "valid_id=="}, 403, "writer cannot send to clients"))
results.append(test("RBAC-WF-002", "/api/workflow_send_client", PU, {"card_id": "valid_id=="}, 200, "publisher can send to clients"))
results.append(test("RBAC-WF-003", "/api/workflow_urgent", WR, {"card_id": "valid_id=="}, 403, "writer cannot toggle urgent"))
results.append(test("RBAC-WF-004", "/api/workflow_urgent", OW, {"card_id": "valid_id=="}, 200, "owner can toggle urgent"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== LIVE WORKFLOW SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)
print(f"\nWorkspace ID for cleanup: {WS_ID}")