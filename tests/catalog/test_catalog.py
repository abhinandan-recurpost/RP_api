"""Catalog endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== CATALOG TESTS ===")
results.append(test("TC-CAT-001", "/api/catalog_businesses", OW, {}, 200, "catalog businesses"))
results.append(test("TC-CAT-002", "/api/catalog_product_save", OW, {"product": {"name": "Test"}}, 200, "catalog product save"))
results.append(test("TC-CAT-003", "/api/catalog_product_delete", OW, {"product_id": "valid_id=="}, 200, "catalog product delete"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== CATALOG SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)