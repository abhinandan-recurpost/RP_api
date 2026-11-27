import json, urllib.request, urllib.error

BASE = "https://apptest.recurpost.com"
ACCOUNTS = {
    "owner": ("abhinandan@recurrpost.com", "0088b47df3f75830bd85edc1c485d562"),
    "writer": ("abhinandan+steeve@recurrpost.com", "5c875c1974fda9224980c47e6cafe6410ddc97e1"),
    "publisher": ("abhinandan+00@recurrpost.com", "c5cee9866ec5fa35587e83c789e0fe4688313104"),
    "editor": ("abhinandan+abhi@recurrpost.com", "aef6226889309122040559a9455a4495e2a822a8"),
}

def login(email, key):
    req = urllib.request.Request(f"{BASE}/api/user_login", data=json.dumps({"emailid": email, "api_key": key}).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())["token"]

tokens = {role: login(e, k) for role, (e, k) in ACCOUNTS.items()}
print("Tokens acquired")

def call(endpoint, token=None, body=None):
    url = f"{BASE}{endpoint}"
    data = json.dumps(body or {}).encode()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except:
            return e.code, {"raw": e.read().decode()[:200]}

results = []

def test(tc_id, endpoint, token, body, expected_status, note=""):
    status, resp = call(endpoint, token, body)
    ok = status == expected_status
    results.append({"id": tc_id, "endpoint": endpoint, "status": status, "expected": expected_status, "pass": ok, "note": note})
    icon = "PASS" if ok else "FAIL"
    print(f"[{icon}] {tc_id}: {endpoint} -> {status} (expected {expected_status}) {note}")

OW = tokens["owner"]; WR = tokens["writer"]; PU = tokens["publisher"]; ED = tokens["editor"]

print("=== AUTH TESTS ===")
test("TC-AUTH-001", "/api/user_login", None, {"emailid": "abhinandan@recurrpost.com", "api_key": "0088b47df3f75830bd85edc1c485d562"}, 200)
test("TC-AUTH-002", "/api/user_login", None, {"emailid": "abhinandan@recurrpost.com", "api_key": "wrongkey"}, 401)
test("TC-AUTH-003", "/api/user_login", None, {"api_key": "0088b47df3f75830bd85edc1c485d562"}, 400)
test("TC-AUTH-004", "/api/user_login", None, {"emailid": "abhinandan@recurrpost.com"}, 400)

print("=== WORKSPACE TESTS ===")
test("TC-WS-001", "/api/workspace_list", OW, {}, 200)
test("TC-WS-002", "/api/workspace_list", WR, {}, 200)
test("TC-WS-003", "/api/workspace_details", OW, {"workspace_id": "MlWlT6qeem2MMkIW8mWYmg=="}, 200)
test("TC-WS-004", "/api/workspace_details", OW, {"workspace_id": "nonexistent=="}, 404)
test("TC-WS-005", "/api/workspace_details", WR, {"workspace_id": "MlWlT6qeem2MMkIW8mWYmg=="}, 404)
test("TC-WS-009", "/api/workspace_update", OW, {"workspace_id": "MlWlT6qeem2MMkIW8mWYmg==", "name": "My Workspace"}, 200)
test("TC-WS-010", "/api/workspace_update", WR, {"workspace_id": "mnCkYKT+a8wM51bBC/lOzg==", "name": "Hacked"}, 403)
test("TC-WS-013", "/api/workspace_clone", WR, {"workspace_id": "mnCkYKT+a8wM51bBC/lOzg==", "name": "Cloned"}, 403)
test("TC-WS-015", "/api/workspace_delete", OW, {"workspace_id": "mnCkYKT+a8wM51bBC/lOzg=="}, 400)
test("TC-WS-016", "/api/workspace_delete", WR, {"workspace_id": "mnCkYKT+a8wM51bBC/lOzg==", "confirm": True}, 403)
test("TC-WS-017", "/api/workspace_members", OW, {"workspace_id": "mnCkYKT+a8wM51bBC/lOzg=="}, 200)
test("TC-WS-018", "/api/workspace_members", WR, {"workspace_id": "MlWlT6qeem2MMkIW8mWYmg=="}, 404)
test("TC-WS-023", "/api/workspace_member_update", WR, {"workspace_id": "mnCkYKT+a8wM51bBC/lOzg==", "user_id": "l+T81bFEu76Usgt05cLD1Q==", "role_id": "XqdhbL1XGr5uMzLIu+zBLA=="}, 403)
test("TC-WS-025", "/api/workspace_member_remove", WR, {"workspace_id": "mnCkYKT+a8wM51bBC/lOzg==", "user_id": "dGODSaojqRC1C/1oY/ZZsg=="}, 403)

print("=== ROLE TESTS ===")
test("TC-ROLE-001", "/api/roles", OW, {}, 200)
test("TC-ROLE-002", "/api/roles", WR, {}, 200)
test("TC-ROLE-004", "/api/role_permissions", OW, {"role_id": "invalid=="}, 400)
test("TC-ROLE-005", "/api/role_create", WR, {"name": "Escalation Role3", "template": "writer"}, 200)
test("TC-ROLE-012", "/api/role_set_permissions", WR, {"role_id": "QN23Pn4nqCfjo9hhtBD8ow==", "permissions": ["send-client"]}, 400)
test("TC-ROLE-013", "/api/role_set_permissions", WR, {"role_id": "QN23Pn4nqCfjo9hhtBD8ow==", "permissions": {"send-client": True}}, 403)

with open("reports/test_run_4.json", "w") as f:
    json.dump(results, f, indent=2)

passed = sum(1 for r in results if r["pass"])
failed = sum(1 for r in results if not r["pass"])
print(f"\n=== SUMMARY: {passed} passed, {failed} failed out of {len(results)} ===")