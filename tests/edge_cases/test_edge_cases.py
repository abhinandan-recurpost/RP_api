"""Edge case tests: XSS, SQL injection, malformed JSON, rate limiting, etc."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== EDGE CASE TESTS ===")
results.append(test("EDGE-001", "/api/workflow_idea_create", WR, {"title": "", "content": "test"}, 200, "empty string title"))
results.append(test("EDGE-002", "/api/workflow_idea_create", WR, {"title": None, "content": "test"}, 400, "null title"))
results.append(test("EDGE-003", "/api/workflow_idea_create", WR, {"title": "A" * 300, "content": "test"}, 400, "very long title >255 chars"))
results.append(test("EDGE-004", "/api/workflow_idea_create", WR, {"title": "'; DROP TABLE posts; --", "content": "test"}, 200, "SQL injection in title"))
results.append(test("EDGE-005", "/api/inbox_reply_comment", WR, {"comment": "<script>alert(1)</script>", "item_id": "valid_id=="}, 200, "XSS in comment text"))
results.append(test("EDGE-006", "/api/workflow_idea_create", WR, {"title": "Hello 🎉", "content": "test"}, 200, "unicode emoji in message"))
results.append(test("EDGE-007", "/api/schedule_create", OW, {"name": "Test", "frequency": "daily", "schedule_date": "2020-01-01"}, 400, "schedule date in past"))
results.append(test("EDGE-008", "/api/schedule_create", OW, {"name": "Test", "frequency": "daily", "schedule_date": "2030-01-01"}, 400, "schedule date far future >1 year"))
results.append(test("EDGE-019", "/api/workspace_list", OW, {}, 429, "rate limiting 100 req/min"))
results.append(test("EDGE-021", "/api/user_login", None, "not json", 400, "malformed JSON"))
results.append(test("EDGE-022", "/api/workspace_list", OW, {}, 400, "missing Content-Type header"))
results.append(test("EDGE-024", "/api/workspace_list", OW, {"extra_unknown_field": "value"}, 200, "extra unknown fields in body"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== EDGE CASE SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)