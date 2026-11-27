"""Watermark endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== WATERMARK TESTS ===")
results.append(test("TC-WM-001", "/api/watermark_get", OW, {}, 200, "watermark get"))
results.append(test("TC-WM-002", "/api/watermark_set", OW, {"image_url": "https://example.com/img.png"}, 200, "watermark set"))
results.append(test("TC-WM-003", "/api/watermark_delete", OW, {}, 200, "watermark delete"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== WATERMARK SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)