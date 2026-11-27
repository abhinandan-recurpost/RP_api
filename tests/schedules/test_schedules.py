"""Schedules endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== SCHEDULE TESTS ===")
results.append(test("TC-SCH-001", "/api/schedule_list", OW, {}, 200, "schedule list"))
results.append(test("TC-SCH-002", "/api/schedule_create", OW, {"name": "Test Schedule", "frequency": "daily"}, 200, "schedule create valid"))
results.append(test("TC-SCH-006", "/api/schedule_calendar", OW, {}, 200, "schedule calendar"))
results.append(test("TC-SCH-008", "/api/schedule_remaining", OW, {}, 200, "schedule remaining"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== SCHEDULE SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)