"""Hashtag Groups endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== HASHTAG GROUP TESTS ===")
results.append(test("TC-HG-001", "/api/hashtag_groups_list", OW, {}, 200, "hashtag groups list"))
results.append(test("TC-HG-002", "/api/hashtag_groups_add", OW, {"group_name": "Test Group"}, 200, "hashtag group add"))
results.append(test("TC-HG-004", "/api/hashtag_groups_delete", OW, {"group_id": "valid_id=="}, 200, "hashtag group delete"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== HASHTAG GROUP SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)