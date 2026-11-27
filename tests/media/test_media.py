"""Media endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== MEDIA TESTS ===")
results.append(test("TC-MED-001", "/api/media_list", OW, {}, 200, "media list"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== MEDIA SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)