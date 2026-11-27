"""Labels endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== LABEL TESTS ===")
results.append(test("TC-LBL-001", "/api/label_list", OW, {}, 200, "label list"))
results.append(test("TC-LBL-002", "/api/label_create", OW, {"name": "Test Label"}, 200, "label create"))
results.append(test("TC-LBL-004", "/api/label_delete", OW, {"label_id": "valid_id=="}, 200, "label delete"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== LABEL SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)