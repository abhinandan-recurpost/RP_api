"""Testimonial Templates endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== TESTIMONIAL TESTS ===")
results.append(test("TC-TT-001", "/api/testimonial_templates_list", OW, {}, 200, "testimonial templates list"))
results.append(test("TC-TT-002", "/api/testimonial_templates_add", OW, {"template": "Test"}, 200, "testimonial template add"))
results.append(test("TC-TT-003", "/api/testimonial_templates_delete", OW, {"template_id": "valid_id=="}, 200, "testimonial template delete"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== TESTIMONIAL SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)