"""Inbox endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== INBOX TESTS ===")
results.append(test("TC-INB-001", "/api/inbox_accounts", OW, {}, 200, "inbox accounts"))
results.append(test("TC-INB-002", "/api/inbox_list", OW, {}, 200, "inbox list"))
results.append(test("TC-INB-007", "/api/inbox_label_list", OW, {}, 200, "inbox label list"))
results.append(test("TC-INB-017", "/api/inbox_like", OW, {"item_id": "valid_id=="}, 200, "inbox like"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== INBOX SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)