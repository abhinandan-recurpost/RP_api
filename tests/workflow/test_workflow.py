"""Workflow endpoint tests (23 endpoints)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])
PU = login(ACCOUNTS["publisher"][0], ACCOUNTS["publisher"][1])
ED = login(ACCOUNTS["editor"][0], ACCOUNTS["editor"][1])

print("=== WORKFLOW TESTS ===")
results.append(test("TC-WF-001", "/api/workflow_board", OW, {}, 200, "owner lists workflow board"))
results.append(test("TC-WF-002", "/api/workflow_board", WR, {}, 200, "writer lists workflow board"))
results.append(test("TC-WF-003", "/api/workflow_idea_create", WR, {"title": "Test Idea", "content": "Test content"}, 200, "writer creates idea"))
results.append(test("TC-WF-004", "/api/workflow_card_advance", WR, {"card_id": "valid_card_id==", "stage": "review"}, 200, "advance card"))
results.append(test("TC-WF-005", "/api/workflow_urgent", WR, {"card_id": "valid_card_id=="}, 403, "writer urgent blocked"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== WORKFLOW SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)