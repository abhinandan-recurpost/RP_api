"""RSS Feeds endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== FEED TESTS ===")
results.append(test("TC-FEED-001", "/api/feed_list", OW, {}, 200, "feed list"))
results.append(test("TC-FEED-002", "/api/feed_create", OW, {"url": "https://example.com/feed"}, 200, "feed create"))
results.append(test("TC-FEED-005", "/api/feed_delete", OW, {"feed_id": "valid_id=="}, 200, "feed delete"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== FEED SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)