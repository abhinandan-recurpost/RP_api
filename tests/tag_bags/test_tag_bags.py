"""Tag Bags endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== TAG BAG TESTS ===")
results.append(test("TC-TB-001", "/api/tag_bags_list", OW, {}, 200, "tag bags list"))
results.append(test("TC-TB-002", "/api/tag_bags_add", OW, {"bag_name": "Test Bag"}, 200, "tag bag add"))
results.append(test("TC-TB-004", "/api/tag_bags_delete", OW, {"bag_id": "valid_id=="}, 200, "tag bag delete"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== TAG BAG SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)