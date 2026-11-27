# TEST-001 — Authentication: all 4 test accounts

**Test ID:** TEST-001  
**Title:** Login (user_login) with emailid + api_key returns a Bearer token for every account  
**Endpoint:** `POST https://apptest.recurpost.com/api/user_login`  
**Auth base:** `https://apptest.recurpost.com` (NOT social.recurpost.com)

---

## Account / User
| Account | Display name | User id |
|---|---|---|
| `abhinandan@recurrpost.com` | Abhinandan Tiwari (Owner) | `yFwdgp/x4CeZtH1oue1CLw==` |
| `abhinandan+steeve@recurrpost.com` | steeve vanz (Member A / Writer) | `l+T81bFEu76Usgt05cLD1Q==` |
| `abhinandan+00@recurrpost.com` | abhinandan+00 (Member B / Publisher) | `dGODSaojqRC1C/1oY/ZZsg==` |
| `abhinandan+abhi@recurrpost.com` | abhi chan (shared in all ws) | `JgUK0KNiADvqHtYCKo+glw==` |

---

## Steps
1. For each account, call `POST /api/user_login` with JSON body `{"emailid": "<account>", "api_key": "<key>"}`.
2. Capture the `token`, `expires_at`, and `expires_in` from a 200 response.
3. Record the user_info (id, name, email).

### Keys used
| Account | API key |
|---|---|
| abhinandan@recurrpost.com | `0088b47df3f75830bd85edc1c485d562` |
| abhinandan+steeve@recurrpost.com | `5c875c1974fda9224980c47e6cafe6410ddc97e1` |
| abhinandan+00@recurrpost.com | `c5cee9866ec5fa35587e83c789e0fe4688313104` |
| abhinandan+abhi@recurrpost.com | `aef6226889309122040559a9455a4495e2a822a8` |

---

## Expected behaviour
- Each account returns HTTP 200 with `"status":200`, `"message":"Success"`.
- Response body contains a non-empty `token` (3600s lifetime), `expires_at` (ISO 8601 UTC), and `user_info`.
- Token is usable as `Authorization: Bearer <token>` on all other endpoints.

## Actual behaviour
| Account | Status | Token issued | Expires at | Error |
|---|---|---|---|---|
| abhinandan@recurrpost.com | 200 | `dd6102a80e135e9b847d50623ae05b3f0bf30421ce6360e16acd199437a3287f` | 2026-11-27T06:07:15Z | — |
| abhinandan+steeve@recurrpost.com | 200 | `88cacd696b0887460360cd11619247237ccefdb07ad6367b34cccbffc6037272` | 2026-11-27T06:07:20Z | — |
| abhinandan+00@recurrpost.com | 200 | `0b60c9b935396417451902c42ea86eb01f3c7d04f16f6255a973d67d1cacfb70` | 2026-11-27T06:07:17Z | — |
| abhinandan+abhi@recurrpost.com | 200 | `f6b3fef3559f013c56eb0b98f58a6690cd4569492958442a1e6558c3093c2d3b` | 2026-11-27T06:07:13Z | — |

Example raw response (owner):
```json
{"status":200,"message":"Success","user_info":{"id":"yFwdgp\/x4CeZtH1oue1CLw==","name":"Abhinandan Tiwari","email":"abhinandan@recurrpost.com"},"token":"dd6102a80e135e9b847d50623ae05b3f0bf30421ce6360e16acd199437a3287f","expires_at":"2026-11-27T06:07:15Z","expires_in":3600}
```

**Status:** PASS  
**Evidence:** All four accounts authenticated successfully; tokens captured and used for subsequent tests.

---