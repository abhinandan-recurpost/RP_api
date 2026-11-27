"""Content Tools endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== CONTENT TOOLS TESTS ===")
results.append(test("TC-CT-001", "/api/click_tracking", OW, {}, 200, "click tracking"))
results.append(test("TC-CT-002", "/api/shorten_url", OW, {"url": "https://example.com"}, 200, "shorten url"))
results.append(test("TC-CT-003", "/api/url_preview", OW, {"url": "https://example.com"}, 200, "url preview"))
results.append(test("TC-CT-004", "/api/instagram_locations", OW, {"query": "nyc"}, 200, "instagram locations"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== CONTENT TOOLS SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)