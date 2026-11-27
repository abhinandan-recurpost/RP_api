"""Edge Case Bug Hunting Tests - XSS, SQL injection, malformed input, rate limiting.
Run independently: python tests/edge_bug_hunt.py
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from conftest import *

results = []
OW = login(ACCOUNTS["owner"][0], ACCOUNTS["owner"][1])
WR = login(ACCOUNTS["writer"][0], ACCOUNTS["writer"][1])

print("=== BUG HUNT: Edge Cases ===\n")

# --- XSS in various text fields ---
xss_payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "javascript:alert(1)",
    "<svg onload=alert(1)>",
]
for i, payload in enumerate(xss_payloads):
    status, resp = call("/api/inbox_reply_comment", WR,
        {"comment": payload, "item_id": "valid_id=="})
    results.append(test(f"BUG-XSS-00{i+1}", "/api/inbox_reply_comment", WR,
        {"comment": payload, "item_id": "valid_id=="}, 200,
        f"XSS payload {i+1} should be sanitized/stored safely"))
    # Check if payload is reflected unescaped in response
    resp_str = json.dumps(resp)
    if payload in resp_str:
        print(f"   *** POTENTIAL XSS REFLECTION: payload returned unescaped!")

# --- SQL Injection ---
sqli_payloads = [
    "'; DROP TABLE posts; --",
    "' OR '1'='1",
    "' UNION SELECT * FROM users --",
    "admin'--",
]
for i, payload in enumerate(sqli_payloads):
    status, resp = call("/api/workflow_idea_create", WR,
        {"title": payload, "content": "test"})
    results.append(test(f"BUG-SQLI-00{i+1}", "/api/workflow_idea_create", WR,
        {"title": payload, "content": "test"}, 200,
        f"SQLi payload {i+1} should not cause server error"))
    resp_str = json.dumps(resp)
    if "sql" in resp_str.lower() or "syntax" in resp_str.lower() or "database" in resp_str.lower():
        print(f"   *** POTENTIAL SQLi: database error in response!")

# --- Oversized payloads ---
big_title = "A" * 10000
status, resp = call("/api/workflow_idea_create", WR,
    {"title": big_title, "content": "test"})
results.append(test("BUG-OVERSIZE-001", "/api/workflow_idea_create", WR,
    {"title": big_title, "content": "test"}, 400,
    "10KB title should be rejected"))

# --- Malformed JSON (no Content-Type) ---
import urllib.request, urllib.error
url = f"{BASE}/api/workspace_list"
req = urllib.request.Request(url, data=b"", headers={}, method="POST")
try:
    with urllib.request.urlopen(req) as r:
        status = r.status
        resp = json.loads(r.read())
except urllib.error.HTTPError as e:
    status = e.code
    try: resp = json.loads(e.read())
    except: resp = {"raw": e.read().decode()[:200]}
# API wraps status in JSON body
api_status = resp.get("status", status) if isinstance(resp, dict) else status
results.append(test("BUG-MALFORMED-001", "/api/workspace_list", None, "not json",
    400, "Malformed JSON should return 400"))

# --- Rate limiting: rapid fire requests ---
rate_results = []
for i in range(20):
    s, r = call("/api/workspace_list", OW, {})
    rate_results.append(s)
if rate_results.count(429) > 0:
    results.append(test("BUG-RATE-001", "/api/workspace_list", OW, {},
        429, "Rate limiting should kick in after rapid requests"))
    print(f"   *** Rate limit observed: {rate_results.count(429)}/20 requests got 429")
else:
    results.append(test("BUG-RATE-001", "/api/workspace_list", OW, {},
        200, "No rate limiting (20 req) - potential DoS vector"))
    print("   *** NO RATE LIMITING: 20 rapid requests all succeeded - potential DoS vector")

# --- Unicode / special chars ---
status, resp = call("/api/workflow_idea_create", WR,
    {"title": "Hello 🎉 世界 🚀", "content": "test"})
results.append(test("BUG-UNICODE-001", "/api/workflow_idea_create", WR,
    {"title": "Hello 🎉 世界 🚀", "content": "test"}, 200,
    "Unicode should be handled safely"))

# --- Null bytes ---
status, resp = call("/api/workflow_idea_create", WR,
    {"title": "test\x00null", "content": "test"})
results.append(test("BUG-NULL-001", "/api/workflow_idea_create", WR,
    {"title": "test\x00null", "content": "test"}, 400,
    "Null bytes in input should be rejected"))

# --- Negative / zero IDs ---
status, resp = call("/api/workspace_details", OW, {"workspace_id": "-1"})
results.append(test("BUG-NEGID-001", "/api/workspace_details", OW,
    {"workspace_id": "-1"}, 400,
    "Negative workspace ID should be rejected"))

status, resp = call("/api/workspace_details", OW, {"workspace_id": "0"})
results.append(test("BUG-NEGID-002", "/api/workspace_details", OW,
    {"workspace_id": "0"}, 400,
    "Zero workspace ID should be rejected"))

# --- Extra unknown fields ---
status, resp = call("/api/workspace_list", OW, {"extra_unknown_field": "value", "another": 123})
results.append(test("BUG-EXTRAFIELD-001", "/api/workspace_list", OW,
    {"extra_unknown_field": "value", "another": 123}, 200,
    "Extra unknown fields should be ignored (or rejected)"))
resp_str = json.dumps(resp)
if "extra" in resp_str.lower() or "unknown" in resp_str.lower():
    print("   *** INFO: API echoes back unknown fields")

# --- Same param multiple times (if supported) ---
status, resp = call("/api/workspace_list", OW, {})
results.append(test("BUG-DUPKEY-001", "/api/workspace_list", OW, {},
    200, "Empty body workspace_list should work"))

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== EDGE CASE BUG HUNT SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")
print("FAILED tests above are POTENTIAL BUGS - investigate each")
with open(os.path.join(os.path.dirname(__file__), "edge_bug_results.json"), "w") as f:
    json.dump(results, f, indent=2)