"""Approvals endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== APPROVAL TESTS ===")
results.append(test("TC-APR-001", "/api/approval_list", OW, {}, 200, "approval list"))
results.append(test("TC-APR-002", "/api/approval_approve", OW, {"approval_id": "valid_id=="}, 200, "approve valid"))
results.append(test("TC-APR-003", "/api/approval_reject", OW, {"approval_id": "valid_id=="}, 200, "reject valid"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== APPROVAL SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)