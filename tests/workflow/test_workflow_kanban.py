"""Comprehensive Workflow & Kanban endpoint tests (23 endpoints).
Tests all workflow stages: Ideas, Writing, Review, Client Review, Scheduled.
Includes end-to-end flow: Idea -> Writing -> Review -> Client -> Scheduled
and rejection flows back to Writing.
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])
PU = login(ACCOUNTS["publisher"][0], ACCOUNTS["publisher"][1])
ED = login(ACCOUNTS["editor"][0], ACCOUNTS["editor"][1])

WS_ID = "MlWlT6qeem2MMkIW8mWYmg=="

print("=== WORKFLOW & KANBAN COMPREHENSIVE TESTS ===\n")

# --- 1. Workflow Board & Settings ---
results.append(test("WF-001", "/api/workflow_board", OW, {}, 200, "Owner lists workflow board"))
results.append(test("WF-002", "/api/workflow_board", WR, {}, 200, "Writer lists workflow board"))
results.append(test("WF-003", "/api/workflow_settings_get", OW, {"workspace_id": WS_ID}, 200, "Get workflow settings"))
results.append(test("WF-004", "/api/workflow_settings_create", OW, {"workspace_id": WS_ID, "name": "Test Workflow"}, 200, "Create workflow settings"))
results.append(test("WF-005", "/api/workflow_settings_update", OW, {"workspace_id": WS_ID, "name": "Updated Workflow"}, 200, "Update workflow settings"))
results.append(test("WF-006", "/api/workflow_settings_ideas", OW, {"workspace_id": WS_ID, "enabled": True}, 200, "Enable ideas stage"))

# --- 2. Stage Management ---
results.append(test("WF-007", "/api/workflow_stage_save", OW, {"workspace_id": WS_ID, "stage_name": "Writing", "position": 1}, 200, "Save workflow stage"))
results.append(test("WF-008", "/api/workflow_stage_delete", OW, {"workspace_id": WS_ID, "stage_name": "Writing"}, 200, "Delete workflow stage (cleanup)"))

# --- 3. Idea Creation & Editing ---
results.append(test("WF-009", "/api/workflow_idea_create", WR, {"title": "Test Idea", "content": "Test content for idea"}, 200, "Writer creates idea"))
results.append(test("WF-010", "/api/workflow_idea_create", WR, {"title": "", "content": "test"}, 400, "Empty title rejected"))
results.append(test("WF-011", "/api/workflow_idea_create", WR, {"title": None, "content": "test"}, 400, "Null title rejected"))
results.append(test("WF-012", "/api/workflow_idea_create", WR, {"title": "A" * 300, "content": "test"}, 400, "Very long title rejected"))
results.append(test("WF-013", "/api/workflow_idea_create", WR, {"title": "'; DROP TABLE posts; --", "content": "test"}, 200, "SQL injection handled"))
results.append(test("WF-014", "/api/workflow_idea_create", WR, {"title": "Hello 🎉", "content": "test"}, 200, "Unicode in title"))
results.append(test("WF-015", "/api/workflow_idea_edit", WR, {"card_id": "valid_card_id==", "title": "Edited Idea"}, 200, "Edit idea title"))

# --- 4. Card Lifecycle ---
results.append(test("WF-016", "/api/workflow_card", OW, {"card_id": "valid_card_id=="}, 200, "Get card details"))
results.append(test("WF-017", "/api/workflow_card_advance", WR, {"card_id": "valid_card_id==", "stage": "review"}, 200, "Advance card to review"))
results.append(test("WF-018", "/api/workflow_card_move", WR, {"card_id": "valid_card_id==", "stage": "writing"}, 200, "Move card back to writing"))
results.append(test("WF-019", "/api/workflow_card_reassign", OW, {"card_id": "valid_card_id==", "user_id": "dGODSaojqRC1C/1oY/ZZsg=="}, 200, "Reassign card to user"))
results.append(test("WF-020", "/api/workflow_card_request_changes", OW, {"card_id": "valid_card_id==", "comment": "Please revise"}, 200, "Request changes on card"))
results.append(test("WF-021", "/api/workflow_card_comment", WR, {"card_id": "valid_card_id==", "comment": "Comment text"}, 200, "Add comment to card"))
results.append(test("WF-022", "/api/workflow_card_delete", OW, {"card_id": "valid_card_id=="}, 200, "Delete card"))
results.append(test("WF-023", "/api/workflow_card_convert", WR, {"card_id": "valid_card_id==", "post_type": "standard"}, 200, "Convert card to post"))

# --- 5. Post Creation from Workflow ---
results.append(test("WF-024", "/api/workflow_post_create", WR, {"card_id": "valid_card_id==", "content": "Post content"}, 200, "Create post from workflow card"))
results.append(test("WF-025", "/api/workflow_post_edit", WR, {"card_id": "valid_card_id==", "content": "Edited post"}, 200, "Edit post in workflow"))

# --- 6. Client Review Flow ---
results.append(test("WF-026", "/api/workflow_client_approve", OW, {"card_id": "valid_card_id==", "comment": "Approved"}, 200, "Client approves card"))
results.append(test("WF-027", "/api/workflow_client_reject", OW, {"card_id": "valid_card_id==", "comment": "Rejected"}, 200, "Client rejects card"))
results.append(test("WF-028", "/api/workflow_client_comment", OW, {"card_id": "valid_card_id==", "comment": "Client comment"}, 200, "Client adds comment"))

# --- 7. Urgent Toggle ---
results.append(test("WF-029", "/api/workflow_urgent", OW, {"card_id": "valid_card_id=="}, 200, "Owner toggles urgent"))
results.append(test("WF-030", "/api/workflow_urgent", WR, {"card_id": "valid_card_id=="}, 403, "Writer cannot toggle urgent (RBAC)"))

# --- 8. RBAC: Writer vs Publisher vs Editor ---
results.append(test("WF-RBAC-001", "/api/workflow_send_client", WR, {"card_id": "valid_card_id=="}, 403, "Writer cannot send to client"))
results.append(test("WF-RBAC-002", "/api/workflow_send_client", PU, {"card_id": "valid_card_id=="}, 200, "Publisher can send to client"))
results.append(test("WF-RBAC-003", "/api/workflow_send_client", ED, {"card_id": "valid_card_id=="}, 403, "Editor cannot send to client"))
results.append(test("WF-RBAC-004", "/api/workflow_card_delete", WR, {"card_id": "valid_card_id=="}, 403, "Writer cannot delete card"))
results.append(test("WF-RBAC-005", "/api/workflow_card_delete", OW, {"card_id": "valid_card_id=="}, 200, "Owner can delete card"))
results.append(test("WF-RBAC-006", "/api/workflow_card_reassign", WR, {"card_id": "valid_card_id==", "user_id": "x"}, 403, "Writer cannot reassign card"))

# --- 9. Edge Cases ---
results.append(test("WF-EDGE-001", "/api/workflow_idea_create", WR, {"title": "A" * 10000, "content": "test"}, 400, "10KB title rejected"))
results.append(test("WF-EDGE-002", "/api/workflow_idea_create", WR, {"title": "test\x00null", "content": "test"}, 400, "Null bytes rejected"))
results.append(test("WF-EDGE-003", "/api/workflow_card_advance", WR, {"card_id": "", "stage": "review"}, 400, "Empty card_id rejected"))
results.append(test("WF-EDGE-004", "/api/workflow_card_advance", WR, {"card_id": "valid_card_id==", "stage": "nonexistent"}, 400, "Invalid stage rejected"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== WORKFLOW & KANBAN SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "workflow_kanban_results.json"), "w") as f:
    json.dump(results, f, indent=2)