"""Posts & Queue endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== POSTS TESTS ===")
results.append(test("TC-POST-001", "/api/post_status", OW, {"post_id": "valid_post_id=="}, 200, "post status valid"))
results.append(test("TC-POST-002", "/api/post_status", OW, {"post_id": "invalid=="}, 404, "post status invalid id"))
results.append(test("TC-POST-003", "/api/post_details", OW, {"post_id": "valid_post_id=="}, 200, "post details valid"))
results.append(test("TC-POST-006", "/api/draft_list", OW, {}, 200, "draft list"))
results.append(test("TC-POST-010", "/api/queue_list", OW, {}, 200, "queue list"))
results.append(test("TC-POST-021", "/api/calendar", OW, {"month": "2026-11"}, 200, "calendar valid month"))
results.append(test("TC-POST-026", "/api/history_list", OW, {}, 200, "history list"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== POSTS SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)