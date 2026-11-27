"""Shared Calendars endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== SHARED CALENDAR TESTS ===")
results.append(test("TC-SC-001", "/api/shared_calendar_get", OW, {}, 200, "shared calendar get"))
results.append(test("TC-SC-002", "/api/shared_calendar_create", OW, {"name": "Shared Cal"}, 200, "shared calendar create"))
results.append(test("TC-SC-005", "/api/shared_calendar_delete", OW, {"calendar_id": "valid_id=="}, 200, "shared calendar delete"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== SHARED CALENDAR SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)