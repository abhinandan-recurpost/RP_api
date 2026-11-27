"""Shared test helpers for RecurPost LIVE API tests (social.recurpost.com)."""
import json, urllib.request, urllib.error, os, sys

BASE = "https://social.recurpost.com"

# API keys to be retrieved from account settings on live server
# Update these after retrieving from https://social.recurpost.com account settings
ACCOUNTS = {
    "owner": ("abhinandan@recurrpost.com", "0301352d52bd6e8d4783c32a7af2b6ca09102393"),
    "writer": ("abhinandan+steeve@recurrpost.com", "3154ad461ffd65953c028bd3d4fb822dfe8b5b7b"),
    "publisher": ("abhinandan+00@recurrpost.com", "383021ffb356d7787d3a216434a6d810"),
    "editor": ("abhinandan+abhi@recurrpost.com", "c493bcfc0ee6c4f54b1ffdb738ac9672"),
}

def login(email, key):
    req = urllib.request.Request(f"{BASE}/api/user_login",
        data=json.dumps({"emailid": email, "api_key": key}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["token"]

def call(endpoint, token=None, body=None):
    url = f"{BASE}{endpoint}"
    data = json.dumps(body or {}).encode()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            resp = json.loads(r.read())
            api_status = resp.get("status", r.status) if isinstance(resp, dict) else r.status
            return api_status, resp
    except urllib.error.HTTPError as e:
        try:
            resp = json.loads(e.read())
            api_status = resp.get("status", e.code) if isinstance(resp, dict) else e.code
            return api_status, resp
        except:
            return e.code, {"raw": e.read().decode()[:200]}

def test(tc_id, endpoint, token, body, expected_status, note=""):
    status, resp = call(endpoint, token, body)
    ok = status == expected_status
    icon = "PASS" if ok else "FAIL"
    print(f"[{icon}] {tc_id}: {endpoint} -> {status} (expected {expected_status}) {note}")
    if not ok:
        print(f"   Response: {json.dumps(resp)[:500]}")
    return {"id": tc_id, "endpoint": endpoint, "status": status, "expected": expected_status, "pass": ok, "note": note, "response": resp}