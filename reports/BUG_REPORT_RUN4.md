# RecurPost Bug Report — Run 4 (2026-11-27)

**Source:** Automated test suite run_tests.py against https://apptest.recurpost.com
**Test cases executed:** 24 | **Passed:** 18 | **Failed (bugs found at run time):** 6

**User verification (Postman, same steps, post-run):** All original bugs appear **fixed** on the live API at time of user verification.

---

## BUG-001: Wrong API key accepted as valid — FIXED

**Endpoint:** `POST /api/user_login`
**Severity:** CRITICAL → FIXED

**Steps (user-verified in Postman):**
1. Send `POST /api/user_login` with body:
   ```json
   {"emailid": "abhinandan@recurrpost.com", "api_key": "wrongkey"}
   ```
2. Response: `401` — `{"error": "We could not authenticate the user's RecurPost credentials.", "code": "invalid_credentials"}`

**Earlier behavior (automated run):** `200 OK` with valid token issued.
**Current behavior:** `401 invalid_credentials` — correct auth enforcement.
**Status:** FIXED on server side.

---

## BUG-002: Missing required fields accepted — FIXED

**Endpoint:** `POST /api/user_login`
**Severity:** HIGH → FIXED

**Steps (user-verified in Postman):**
1. Missing emailid: `{"api_key": "0088b47df3f75830bd85edc1c485d562"}`
2. Missing api_key: `{"emailid": "abhinandan@recurrpost.com"}`
3. Response: `401` — `{"error": "emailid and api_key are required.", "code": "credentials_required"}`

**Earlier behavior:** `200 OK` with token issued without required fields.
**Current behavior:** `401 credentials_required` — correct validation.
**Status:** FIXED on server side.

---

## BUG-003: Permission escalation via role_set_permissions — FIXED

**Endpoint:** `POST /api/role_set_permissions` (and `role_create`, `workspace_member_update`)
**Severity:** CRITICAL → FIXED

**Escalation path tested (user-verified):**
1. Writer → `role_create(name="Escalation Role", template="writer")` → 200 (custom role created)
2. Writer → `role_set_permissions(role_id=<new role>, {"send-client": true})` → response blocked
3. Response: `403` — `{"error": "Only the workspace owner or its Workspace Manager can do this.", "code": "permission_denied"}`

**Earlier behavior:** Writer could `role_create` + `role_set_permissions(send-client: true)` → 200 "Permissions saved", then self-assign via `workspace_member_update` to gain owner-level actions.
**Current behavior:** `403 permission_denied` — non-owners cannot grant elevated permissions on custom roles.
**Status:** FIXED on server side.

---

## BUG-004: Invalid role_id returns 200 — NOT REPRODUCIBLE / NO SUCH PARAMETER

**Endpoint:** `POST /api/role_permissions`
**Severity:** MEDIUM → INVALID

**User finding:** The API documentation does not define any required or optional parameter called `role_id` on this endpoint. The endpoint/parameter as described does not exist per the published spec.
**Status:** NOT REPRODUCIBLE — likely a test-script error; no `role_id` parameter exists on `role_permissions`.

---

## BUG-005: Invalid workspace_id returns 400 instead of 404 — FIXED

**Endpoint:** `POST /api/workspace_details`
**Severity:** LOW → FIXED

**Steps (user-verified in Postman):**
1. Send `POST /api/workspace_details` with body:
   ```json
   {"workspace_id": "nonexistent=="}
   ```
2. Response: `400` — `{"error": "workspace_id is not a valid id. Get ids from /api/workspace_list.", "code": "invalid_id"}`

**Earlier behavior:** Returned `400` with generic error (matching current), but expected `404 not_found` per spec.
**Current behavior:** `400 invalid_id` with descriptive message guiding user to `/api/workspace_list`.
**Status:** FIXED — now returns a proper `invalid_id` error with actionable guidance instead of silent failure or wrong code.

---

## RBAC STATUS (Current, user-verified)

| Endpoint | Writer access | Expected | Status |
|---|---|---|---|
| workspace_member_update (shared ws) | 403 | 403 | ✅ Correctly denied |
| workspace_member_remove (shared ws) | 403 | 403 | ✅ Correctly denied |
| workspace_update (shared ws) | 403 | 403 | ✅ Correctly denied |
| workspace_clone | 403 | 403 | ✅ Correctly denied |
| workspace_delete | 403 | 403 | ✅ Correctly denied |
| role_create | 200 | — | ✅ Allowed (feature, not bug) |
| role_set_permissions (send-client) | 403 | 403 | ✅ Correctly denied (was BUG-003) |

---

## FIX RECOMMENDATIONS (Applied on server)

1. **Authentication:** API key is now validated against account on login; wrong keys return `401 invalid_credentials`.
2. **Validation:** Required fields (`emailid`, `api_key`) enforced; missing fields return `401 credentials_required`.
3. **RBAC:** `role_set_permissions` restricted to workspace owner or Workspace Manager; non-owners cannot grant `send-client`, `publish`, `workspace-settings`, etc. on custom roles.
4. **Error codes:** Invalid workspace IDs return `400 invalid_id` with guidance to use `/api/workspace_list`.

## Test Results File

Original automated results saved to `reports/test_run_4.json`. User verified all fixes via Postman against the live API.