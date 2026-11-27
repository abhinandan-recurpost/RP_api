# RecurPost Workflow API Endpoints

Source: https://developers.recurpost.com/recurpost_api.json (v2.0.0), base URL https://social.recurpost.com

Authentication: POST /api/user_login with emailid + api_key → Bearer token (1h). All endpoints are POST with JSON body.

## Endpoints (23)

See `workflow_endpoints.txt` for full request/response schemas.

1. POST /api/workflow_board
2. POST /api/workflow_card
3. POST /api/workflow_card_advance
4. POST /api/workflow_card_comment
5. POST /api/workflow_card_convert
6. POST /api/workflow_card_delete
7. POST /api/workflow_card_move
8. POST /api/workflow_card_reassign
9. POST /api/workflow_card_request_changes
10. POST /api/workflow_client_approve
11. POST /api/workflow_client_comment
12. POST /api/workflow_client_reject
13. POST /api/workflow_idea_create
14. POST /api/workflow_idea_edit
15. POST /api/workflow_post_create
16. POST /api/workflow_post_edit
17. POST /api/workflow_settings_create
18. POST /api/workflow_settings_get
19. POST /api/workflow_settings_ideas
20. POST /api/workflow_settings_update
21. POST /api/workflow_stage_delete
22. POST /api/workflow_stage_save
23. POST /api/workflow_urgent

## Testing status

Live testing was attempted against https://social.recurpost.com using the provided credentials. All login attempts returned 401 invalid_credentials, and the account abhinandan@recurrpost.com is now locked for ~6 minutes (login_locked, HTTP 429). The strings supplied in braces appear to be encrypted API-key values rather than the raw API key text; the RecurPost API requires the raw API key from Account Settings → API key. No browser tool is available in this environment to retrieve the key from https://apptest.recurpost.com.

To complete live testing, provide the raw API key (from Account Settings → API key) for abhinandan@recurrpost.com, or unblock the account and re-run. The full endpoint schemas are in `workflow_endpoints.txt`.