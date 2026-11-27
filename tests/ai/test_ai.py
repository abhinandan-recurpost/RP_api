"""AI endpoint tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from conftest import *
import json

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== AI TESTS ===")
results.append(test("TC-AI-001", "/api/ai_credits", OW, {}, 200, "ai credits"))
results.append(test("TC-AI-002", "/api/generate_content_with_ai", OW, {"prompt": "test"}, 200, "generate content AI"))
results.append(test("TC-AI-004", "/api/ai_hashtags", OW, {"text": "test"}, 200, "ai hashtags"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== AI SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(results, f, indent=2)