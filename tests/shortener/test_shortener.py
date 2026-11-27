"""Shortener endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== SHORTENER TESTS ===")
results.append(test("TC-SH-001", "/api/shortener_accounts_list", OW, {}, 200, "shortener accounts list"))
results.append(test("TC-SH-002", "/api/shortener_accounts_attach", OW, {"account_id": "valid_id=="}, 200, "shortener attach"))
results.append(test("TC-SH-003", "/api/shortener_accounts_detach", OW, {"account_id": "valid_id=="}, 200, "shortener detach"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== SHORTENER SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)