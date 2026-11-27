"""Shared test helpers for RecurPost API tests."""
import json, urllib.request, urllib.error, os, sys

BASE = "https://apptest.recurpost.com"

ACCOUNTS = {
    "owner": ("abhinandan@recurrpost.com", "0088b47df3f75830bd85edc1c485d562"),
    "writer": ("abhinandan+steeve@recurrpost.com", "5c875c1974fda9224980c47e6cafe6410ddc97e1"),
    "publisher": ("abhinandan+00@recurrpost.com", "c5cee9866ec5fa35587e83c789e0fe4688313104"),
    "editor": ("abhinandan+abhi@recurrpost.com", "aef6226889309122040559a9455a4495e2a822a8"),
}

def login(email, key):
    req = urllib.request.Request(f"{BASE}/api/user_login",
        data=json.dumps({"emailid": email, "api_key": key}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["token"]

def call(endpoint, token=None, body=None, content_type="application/json"):
    url = f"{BASE}{endpoint}"
    if body == "not json":
        data = b"not json"
    elif body is None:
        data = b"{}"
    else:
        data = json.dumps(body).encode()
    headers = {"Content-Type": content_type}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            resp = json.loads(r.read())
            # API returns HTTP 200 but status in JSON body
            api_status = resp.get("status", r.status) if isinstance(resp, dict) else r.status
            return api_status, resp
    except urllib.error.HTTPError as e:
        try:
            resp = json.loads(e.read())
            api_status = resp.get("status", e.code) if isinstance(resp, dict) else e.code
            return api_status, resp
        except:
            raw = e.read().decode()[:200]
            return e.code, {"raw": raw}

def test(tc_id, endpoint, token, body, expected_status, note=""):
    status, resp = call(endpoint, token, body)
    ok = status == expected_status
    icon = "PASS" if ok else "FAIL"
    print(f"[{icon}] {tc_id}: {endpoint} -> {status} (expected {expected_status}) {note}")
    if not ok:
        print(f"   Response: {json.dumps(resp)[:500]}")
    return {"id": tc_id, "endpoint": endpoint, "status": status, "expected": expected_status, "pass": ok, "note": note, "response": resp}