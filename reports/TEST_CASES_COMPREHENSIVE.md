# RecurPost Comprehensive Test Cases

**Total endpoints:** 199 (from recurpost_api.json v2.0.0)
**Base URL:** https://apptest.recurpost.com
**Generated:** 2026-11-27

Each test case follows: ID, Endpoint, Method, Role, Input, Expected, Notes

---

## 1. Authentication (3 endpoints)

### TC-AUTH-001: user_login valid credentials
- Endpoint: POST /api/user_login
- Role: any
- Input: {"emailid":"abhinandan@recurrpost.com","api_key":"0088b..."}
- Expected: 200, token, expires_at, user_info
- Notes: all 4 accounts tested PASS

### TC-AUTH-002: user_login invalid password
- Input: wrong api_key
- Expected: 401 invalid_credentials

### TC-AUTH-003: user_login missing emailid
- Input: {"api_key":"..."}
- Expected: 400 missing_param

### TC-AUTH-004: user_login missing api_key
- Input: {"emailid":"..."}
- Expected: 400 missing_param

### TC-AUTH-005: user_login locked account
- Input: 5+ failed attempts
- Expected: 429 login_locked

### TC-AUTH-006: user_login expired token reuse
- Input: Bearer expired_token
- Expected: 401 token_expired

### TC-AUTH-007: user_login Basic auth (legacy Zapier)
- Input: Authorization: Basic base64(email:api_key)
- Expected: 200 token

### TC-AUTH-008: user_login with pass_key alias
- Input: {"emailid":"...","pass_key":"..."}
- Expected: 200 token

### TC-AUTH-009: user_login with zapier_key alias
- Input: {"emailid":"...","zapier_key":"..."}
- Expected: 200 token

---

## 2. Workspaces (12 endpoints)

### TC-WS-001: workspace_list owner
- Expected: 3 workspaces (My Workspace default, API Caller test, Faces)

### TC-WS-002: workspace_list member
- Expected: own + shared workspaces

### TC-WS-003: workspace_details valid id
- Expected: workspace metadata + members + social accounts

### TC-WS-004: workspace_details invalid id
- Expected: 404 workspace_not_found

### TC-WS-005: workspace_details cross-user id
- Expected: 404 workspace_not_found (not 403)

### TC-WS-006: workspace_create valid
- Input: name, invite list
- Expected: 200 workspace created

### TC-WS-007: workspace_create duplicate name
- Expected: 409 conflict

### TC-WS-008: workspace_create missing name
- Expected: 400 missing_param

### TC-WS-009: workspace_update owner
- Expected: 200 updated

### TC-WS-010: workspace_update non-owner
- Expected: 403 permission_denied

### TC-WS-011: workspace_update rename to existing name
- Expected: 409 conflict

### TC-WS-012: workspace_clone owner
- Expected: 200 cloned with new id

### TC-WS-013: workspace_clone non-owner
- Expected: 403 only owner can do this

### TC-WS-014: workspace_delete owner with confirm
- Expected: 200 deleted

### TC-WS-015: workspace_delete without confirm
- Expected: 400 confirm required

### TC-WS-016: workspace_delete non-owner
- Expected: 403 permission_denied

### TC-WS-017: workspace_members owner
- Expected: member list + pending invites + approvers

### TC-WS-018: workspace_members non-member
- Expected: 404 workspace_not_found

### TC-WS-019: workspace_invite valid email
- Expected: 200 invite sent

### TC-WS-020: workspace_invite duplicate email
- Expected: 409 already member

### TC-WS-021: workspace_invite invalid email format
- Expected: 400 invalid_param

### TC-WS-022: workspace_invite_resend
- Expected: 200 resent

### TC-WS-023: workspace_member_update change role
- Expected: 200 updated

### TC-WS-024: workspace_member_update non-owner
- Expected: 403 permission_denied

### TC-WS-025: workspace_member_remove owner
- Expected: 200 removed

### TC-WS-026: workspace_member_remove self
- Expected: 400 cannot remove self

### TC-WS-027: workspace_member_remove last owner
- Expected: 400 cannot remove last owner

### TC-WS-028: workspace_social_accounts_add
- Expected: 200 added

### TC-WS-029: workspace_social_accounts_remove
- Expected: 200 removed

### TC-WS-030: workspace_libraries_add
- Expected: 200 added

### TC-WS-031: workspace_libraries_remove
- Expected: 200 removed

### TC-WS-032: workspace_report_emails_list
- Expected: list of report emails

### TC-WS-033: workspace_report_emails_add
- Expected: 200 added

### TC-WS-034: workspace_report_emails_update
- Expected: 200 updated

### TC-WS-035: workspace_report_emails_delete
- Expected: 200 deleted

---

## 3. Team Roles (7 endpoints)

### TC-ROLE-001: roles list (owner)
- Expected: Editor, Publisher, Writer with permission_keys

### TC-ROLE-002: roles list (member)
- Expected: Contributor, Editor, Publisher, Writer (own workspace roles)

### TC-ROLE-003: role_permissions valid role_id
- Expected: permission map

### TC-ROLE-004: role_permissions invalid id
- Expected: 400 invalid_id

### TC-ROLE-005: role_create valid
- Expected: 200 role created

### TC-ROLE-006: role_create duplicate name
- Expected: 409 conflict

### TC-ROLE-007: role_create non-owner
- Expected: 403 permission_denied (POTENTIAL BYPASS: currently 200!)

### TC-ROLE-008: role_rename owner
- Expected: 200 renamed

### TC-ROLE-009: role_rename non-owner
- Expected: 403

### TC-ROLE-010: role_duplicate
- Expected: 200 duplicated

### TC-ROLE-011: role_set_permissions valid format
- Input: {"permissions":{"key":true/false}}
- Expected: 200 saved

### TC-ROLE-012: role_set_permissions invalid format (array)
- Input: {"permissions":["key"]}
- Expected: 400 invalid_param

### TC-ROLE-013: role_set_permissions escalate to send-client (non-owner)
- Input: {"permissions":{"send-client":true}}
- Expected: 403 (CURRENTLY 200 — BUG)

### TC-ROLE-014: role_set_notification
- Expected: 200 saved

### TC-ROLE-015: role_delete owner
- Expected: 200 deleted

### TC-ROLE-016: role_delete with members assigned
- Expected: 400 cannot delete role with members

### TC-ROLE-017: role_delete non-owner
- Expected: 403

---

## 4. Social Accounts (8 endpoints)

### TC-SA-001: social_account_list
- Expected: 12 connected accounts

### TC-SA-002: social_account_details valid id
- Expected: account details + status

### TC-SA-003: social_account_details invalid id
- Expected: 404 not_found

### TC-SA-004: social_account_status
- Expected: connected/disconnected

### TC-SA-005: social_account_rename
- Expected: 200 renamed

### TC-SA-006: social_account_remove
- Expected: 200 removed

### TC-SA-007: social_account_remove non-owner
- Expected: 403

### TC-SA-008: connect_social_account_urls
- Expected: OAuth URLs

### TC-SA-009: tiktok_options
- Expected: tiktok-specific options

### TC-SA-010: youtube_options
- Expected: youtube-specific options

### TC-SA-011: facebook_backgrounds
- Expected: background list

### TC-SA-012: mention_search
- Expected: mention results

### TC-SA-013: instagram_products
- Expected: product list

### TC-SA-014: instagram_audio_search
- Expected: audio list

---

## 5. Account & Settings (10 endpoints)

### TC-ACC-001: account_details
- Expected: name, email, timezone, plan, default_workspace

### TC-ACC-002: account_timezone
- Expected: timezone string

### TC-ACC-003: account_update valid
- Expected: 200 updated

### TC-ACC-004: account_update invalid timezone
- Expected: 400 invalid_param

### TC-ACC-005: account_limits
- Expected: plan limits

### TC-ACC-006: plan_details
- Expected: plan info

### TC-ACC-007: billing_invoices
- Expected: invoice list

### TC-ACC-008: queue_pause
- Expected: 200 paused

### TC-ACC-009: queue_resume
- Expected: 200 resumed

### TC-ACC-010: x_wallet
- Expected: wallet balance

### TC-ACC-011: custom_fields_list
- Expected: field list

### TC-ACC-012: custom_fields_create
- Expected: 200 created

### TC-ACC-013: custom_fields_rename
- Expected: 200 renamed

### TC-ACC-014: custom_fields_set_value
- Expected: 200 set

### TC-ACC-015: custom_fields_delete_value
- Expected: 200 deleted

### TC-ACC-016: custom_fields_delete
- Expected: 200 deleted

### TC-ACC-017: email_preferences
- Expected: preferences

### TC-ACC-018: working_hours
- Expected: working hours

### TC-ACC-019: notifications
- Expected: notification list

### TC-ACC-020: white_label_get
- Expected: white label config

### TC-ACC-021: white_label_set
- Expected: 200 set

### TC-ACC-022: white_label_delete
- Expected: 200 deleted

---

## 6. Posts & Queue (15 endpoints)

### TC-POST-001: post_status valid id
- Expected: status

### TC-POST-002: post_status invalid id
- Expected: 404

### TC-POST-003: post_details valid id
- Expected: message, image_url, accounts with status

### TC-POST-004: post_details cross-user id
- Expected: 404 not_found

### TC-POST-005: post_content valid url
- Expected: preview

### TC-POST-006: draft_list
- Expected: draft list

### TC-POST-007: draft_save valid
- Expected: 200 saved

### TC-POST-008: draft_schedule valid
- Expected: 200 scheduled

### TC-POST-009: draft_delete
- Expected: 200 deleted

### TC-POST-010: queue_list
- Expected: paginated items

### TC-POST-011: queue_list with date range
- Expected: filtered items

### TC-POST-012: queue_post valid
- Expected: 200 queued

### TC-POST-013: queue_post missing account
- Expected: 400 missing_param

### TC-POST-014: queue_post_update
- Expected: 200 updated

### TC-POST-015: queue_post_delete
- Expected: 200 deleted

### TC-POST-016: queue_reschedule
- Expected: 200 rescheduled

### TC-POST-017: queue_post_now
- Expected: 200 published

### TC-POST-018: queue_post_now already published
- Expected: 400 already published

### TC-POST-019: post_retry failed post
- Expected: 200 retried

### TC-POST-020: post_retry non-failed post
- Expected: 400 not eligible

### TC-POST-021: calendar valid month
- Expected: days with items

### TC-POST-022: calendar invalid month
- Expected: 400 invalid_param

### TC-POST-023: queue_post_add_accounts
- Expected: 200 added

### TC-POST-024: post_unpublish published post
- Expected: 200 unpublished

### TC-POST-025: post_unpublish non-published
- Expected: 400 not published

### TC-POST-026: history_list
- Expected: history items

### TC-POST-027: history_data valid id
- Expected: history details

### TC-POST-028: history_to_library
- Expected: 200 moved

---

## 7. Libraries (18 endpoints)

### TC-LIB-001: library_list
- Expected: library list

### TC-LIB-002: library_details valid id
- Expected: library metadata

### TC-LIB-003: library_create valid
- Expected: 200 created

### TC-LIB-004: library_create duplicate name
- Expected: 409 conflict

### TC-LIB-005: library_update
- Expected: 200 updated

### TC-LIB-006: library_pause
- Expected: 200 paused

### TC-LIB-007: library_resume
- Expected: 200 resumed

### TC-LIB-008: library_content_list
- Expected: content items

### TC-LIB-009: library_content valid id
- Expected: content details

### TC-LIB-010: add_content_in_library valid
- Expected: 200 added

### TC-LIB-011: library_content_update
- Expected: 200 updated

### TC-LIB-012: library_content_search
- Expected: search results

### TC-LIB-013: library_content_move
- Expected: 200 moved

### TC-LIB-014: library_content_copy
- Expected: 200 copied

### TC-LIB-015: library_content_delete
- Expected: 200 deleted

### TC-LIB-016: library_content_order_move
- Expected: 200 reordered

### TC-LIB-017: library_content_order_shuffle
- Expected: 200 shuffled

### TC-LIB-018: library_delete
- Expected: 200 deleted

### TC-LIB-019: library_delete with content
- Expected: 400 has content, confirm required

### TC-LIB-020: library_duplicate
- Expected: 200 duplicated

### TC-LIB-021: expired_content_list
- Expected: expired items

### TC-LIB-022: expired_content_restore
- Expected: 200 restored

### TC-LIB-023: expired_content_delete
- Expected: 200 deleted

### TC-LIB-024: expired_content_expire
- Expected: 200 expired

### TC-LIB-025: library_drafts_list
- Expected: draft list

### TC-LIB-026: library_drafts_get
- Expected: draft details

### TC-LIB-027: library_drafts_update
- Expected: 200 updated

### TC-LIB-028: library_drafts_publish
- Expected: 200 published

### TC-LIB-029: library_drafts_delete
- Expected: 200 deleted

### TC-LIB-030: library_bulk_edit_count
- Expected: count

### TC-LIB-031: library_bulk_edit_replace
- Expected: 200 replaced

### TC-LIB-032: library_bulk_edit_append
- Expected: 200 appended

### TC-LIB-033: library_pointers_list
- Expected: pointers

### TC-LIB-034: library_pointers_set
- Expected: 200 set

### TC-LIB-035: library_pointers_reset
- Expected: 200 reset

### TC-LIB-036: library_share_get
- Expected: share config

### TC-LIB-037: library_share_create
- Expected: 200 created

### TC-LIB-038: library_share_reset
- Expected: 200 reset

### TC-LIB-039: library_share_invite
- Expected: 200 invited

### TC-LIB-040: library_comments_list
- Expected: comments

### TC-LIB-041: library_comments_add
- Expected: 200 added

### TC-LIB-042: library_comments_mark
- Expected: 200 marked

### TC-LIB-043: content_variation_list
- Expected: variations

### TC-LIB-044: content_variation_add
- Expected: 200 added

### TC-LIB-045: content_variation_update
- Expected: 200 updated

### TC-LIB-046: content_variation_delete
- Expected: 200 deleted

---

## 8. Schedules (7 endpoints)

### TC-SCH-001: schedule_list
- Expected: schedules list

### TC-SCH-002: schedule_create valid
- Expected: 200 created

### TC-SCH-003: schedule_create invalid frequency
- Expected: 400 invalid_param

### TC-SCH-004: schedule_update
- Expected: 200 updated

### TC-SCH-005: schedule_delete
- Expected: 200 deleted

### TC-SCH-006: schedule_calendar
- Expected: calendar view

### TC-SCH-007: schedule_copy
- Expected: 200 copied

### TC-SCH-008: schedule_remaining
- Expected: remaining count

### TC-SCH-009: schedule_move_slot
- Expected: 200 moved

---

## 9. Approvals (6 endpoints)

### TC-APR-001: approval_list
- Expected: approval items

### TC-APR-002: approval_approve
- Expected: 200 approved

### TC-APR-003: approval_reject
- Expected: 200 rejected

### TC-APR-004: approval_comment
- Expected: 200 commented

### TC-APR-005: approval_edit
- Expected: 200 edited

### TC-APR-006: approval_resend
- Expected: 200 resent

### TC-APR-007: approval_delete
- Expected: 200 deleted

---

## 10. Workflow (23 endpoints) — ALREADY TESTED
See WORKFLOW_TEST_REPORT.md (36 tests)

---

## 11. Shared Calendars (10 endpoints)

### TC-SC-001: shared_calendar_get
- Expected: calendar details

### TC-SC-002: shared_calendar_create
- Expected: 200 created

### TC-SC-003: shared_calendar_update
- Expected: 200 updated

### TC-SC-004: shared_calendar_link
- Expected: share link

### TC-SC-005: shared_calendar_delete
- Expected: 200 deleted

### TC-SC-006: shared_calendar_clients
- Expected: client list

### TC-SC-007: shared_calendar_invite_client
- Expected: 200 invited

### TC-SC-008: shared_calendar_remove_client
- Expected: 200 removed

### TC-SC-009: shared_calendar_comments_list
- Expected: comments

### TC-SC-010: shared_calendar_comments_add
- Expected: 200 added

### TC-SC-011: shared_calendar_comments_mark
- Expected: 200 marked

---

## 12. Inbox (20 endpoints)

### TC-INB-001: inbox_accounts
- Expected: inbox accounts

### TC-INB-002: inbox_list
- Expected: conversation list

### TC-INB-003: inbox_item
- Expected: item details

### TC-INB-004: inbox_conversation
- Expected: conversation thread

### TC-INB-005: inbox_comments
- Expected: comments

### TC-INB-006: inbox_team_members
- Expected: team members

### TC-INB-007: inbox_label_list
- Expected: labels

### TC-INB-008: inbox_label_create
- Expected: 200 created

### TC-INB-009: inbox_label_update
- Expected: 200 updated

### TC-INB-010: inbox_label_delete
- Expected: 200 deleted

### TC-INB-011: inbox_item_labels_add
- Expected: 200 added

### TC-INB-012: inbox_item_labels_remove
- Expected: 200 removed

### TC-INB-013: inbox_item_labels_set
- Expected: 200 set

### TC-INB-014: inbox_reply_comment
- Expected: 200 replied

### TC-INB-015: inbox_reply_message
- Expected: 200 replied

### TC-INB-016: inbox_delete_comment
- Expected: 200 deleted

### TC-INB-017: inbox_like
- Expected: 200 liked

### TC-INB-018: inbox_unlike
- Expected: 200 unliked

### TC-INB-019: inbox_mark_reviewed
- Expected: 200 marked

### TC-INB-020: inbox_mark_unreviewed
- Expected: 200 unmarked

### TC-INB-021: inbox_bookmark_add
- Expected: 200 bookmarked

### TC-INB-022: inbox_bookmark_remove
- Expected: 200 removed

### TC-INB-023: inbox_assign
- Expected: 200 assigned

### TC-INB-024: inbox_unassign
- Expected: 200 unassigned

### TC-INB-025: inbox_ai_reply
- Expected: 200 AI reply

### TC-INB-026: inbox_sync
- Expected: 200 synced

### TC-INB-027: inbox_ai_review_summary
- Expected: summary

### TC-INB-028: inbox_to_library
- Expected: 200 moved

---

## 13. DM Automations (8 endpoints)

### TC-DM-001: dm_automation_accounts
- Expected: accounts

### TC-DM-002: dm_automation_posts
- Expected: posts

### TC-DM-003: dm_automation_list
- Expected: automation list

### TC-DM-004: dm_automation (get)
- Expected: automation details

### TC-DM-005: dm_automation_stats
- Expected: stats

### TC-DM-006: dm_automation_create
- Expected: 200 created

### TC-DM-007: dm_automation_update
- Expected: 200 updated

### TC-DM-008: dm_automation_delete
- Expected: 200 deleted

### TC-DM-009: dm_automation_status
- Expected: 200 toggled

---

## 14. Reports (7 endpoints)

### TC-REP-001: report_account
- Expected: account report

### TC-REP-002: report_posts
- Expected: post report

### TC-REP-003: report_pdf
- Expected: PDF

### TC-REP-004: report_pins
- Expected: pins

### TC-REP-005: report_ads
- Expected: ads

### TC-REP-006: report_x_quote
- Expected: x quote

### TC-REP-007: report_x_fetch
- Expected: fetch

### TC-REP-008: report_labels
- Expected: labels

### TC-REP-009: report_ai_chat
- Expected: AI chat

### TC-REP-010: custom_reports_list
- Expected: custom reports

### TC-REP-011: custom_reports_get
- Expected: report details

### TC-REP-012: custom_reports_data
- Expected: data

### TC-REP-013: custom_report_metrics
- Expected: metrics

### TC-REP-014: custom_report_templates
- Expected: templates

### TC-REP-015: custom_reports_save
- Expected: 200 saved

### TC-REP-016: custom_reports_duplicate
- Expected: 200 duplicated

### TC-REP-017: custom_reports_delete
- Expected: 200 deleted

### TC-REP-018: custom_report_pdf
- Expected: PDF

---

## 15. AI (12 endpoints)

### TC-AI-001: ai_credits
- Expected: credit balance

### TC-AI-002: generate_content_with_ai
- Expected: generated content

### TC-AI-003: generate_image_with_ai
- Expected: generated image

### TC-AI-004: ai_hashtags
- Expected: hashtags

### TC-AI-005: ai_variations
- Expected: variations

### TC-AI-006: ai_templates_list
- Expected: templates

### TC-AI-007: ai_templates_questions
- Expected: questions

### TC-AI-008: ai_templates_formats
- Expected: formats

### TC-AI-009: ai_templates_generate
- Expected: generated

### TC-AI-010: ai_week_plan
- Expected: week plan

### TC-AI-011: ai_special_days_list
- Expected: special days

### TC-AI-012: ai_special_days_generate
- Expected: generated

### TC-AI-013: ai_to_library
- Expected: 200 moved

### TC-AI-014: ai_settings_get
- Expected: settings

### TC-AI-015: ai_settings_set
- Expected: 200 set

---

## 16. RSS Feeds (7 endpoints)

### TC-FEED-001: feed_list
- Expected: feeds

### TC-FEED-002: feed_create
- Expected: 200 created

### TC-FEED-003: feed_pause
- Expected: 200 paused

### TC-FEED-004: feed_resume
- Expected: 200 resumed

### TC-FEED-005: feed_delete
- Expected: 200 deleted

### TC-FEED-006: feed_update
- Expected: 200 updated

### TC-FEED-007: feed_refresh
- Expected: 200 refreshed

### TC-FEED-008: feed_items
- Expected: items

### TC-FEED-009: feed_item_approve
- Expected: 200 approved

### TC-FEED-010: feed_item_reject
- Expected: 200 rejected

### TC-FEED-011: feed_item_approve_all
- Expected: 200 all approved

### TC-FEED-012: feed_item_reject_all
- Expected: 200 all rejected

---

## 17. Import (4 endpoints)

### TC-IMP-001: import_accounts
- Expected: accounts

### TC-IMP-002: import_posts
- Expected: posts

### TC-IMP-003: import_to_library
- Expected: 200 imported

### TC-IMP-004: import_posts_more
- Expected: more posts

### TC-IMP-005: import_refresh
- Expected: 200 refreshed

---

## 18. Labels (5 endpoints)

### TC-LBL-001: label_list
- Expected: labels

### TC-LBL-002: label_create
- Expected: 200 created

### TC-LBL-003: label_update
- Expected: 200 updated

### TC-LBL-004: label_delete
- Expected: 200 deleted

### TC-LBL-005: label_assign_set
- Expected: 200 set

### TC-LBL-006: label_assign_add
- Expected: 200 added

### TC-LBL-007: label_assign_remove
- Expected: 200 removed

---

## 19. Hashtag Groups (5 endpoints)

### TC-HG-001: hashtag_groups_list
- Expected: groups

### TC-HG-002: hashtag_groups_add
- Expected: 200 added

### TC-HG-003: hashtag_groups_update
- Expected: 200 updated

### TC-HG-004: hashtag_groups_delete
- Expected: 200 deleted

### TC-HG-005: hashtag_groups_copy
- Expected: 200 copied

---

## 20. Tag Bags (4 endpoints)

### TC-TB-001: tag_bags_list
- Expected: bags

### TC-TB-002: tag_bags_add
- Expected: 200 added

### TC-TB-003: tag_bags_update
- Expected: 200 updated

### TC-TB-004: tag_bags_delete
- Expected: 200 deleted

---

## 21. Watermark (4 endpoints)

### TC-WM-001: watermark_get
- Expected: watermark

### TC-WM-002: watermark_set
- Expected: 200 set

### TC-WM-003: watermark_delete
- Expected: 200 deleted

### TC-WM-004: watermark_copy
- Expected: 200 copied

---

## 22. Testimonial Templates (3 endpoints)

### TC-TT-001: testimonial_templates_list
- Expected: templates

### TC-TT-002: testimonial_templates_add
- Expected: 200 added

### TC-TT-003: testimonial_templates_delete
- Expected: 200 deleted

---

## 23. Shortener (3 endpoints)

### TC-SH-001: shortener_accounts_list
- Expected: accounts

### TC-SH-002: shortener_accounts_attach
- Expected: 200 attached

### TC-SH-003: shortener_accounts_detach
- Expected: 200 detached

---

## 24. Catalog (3 endpoints)

### TC-CAT-001: catalog_businesses
- Expected: businesses

### TC-CAT-002: catalog_product_save
- Expected: 200 saved

### TC-CAT-003: catalog_product_delete
- Expected: 200 deleted

---

## 25. Account Groups (4 endpoints)

### TC-AG-001: account_groups
- Expected: groups

### TC-AG-002: account_group_create
- Expected: 200 created

### TC-AG-003: account_group_update
- Expected: 200 updated

### TC-AG-004: account_group_delete
- Expected: 200 deleted

---

## 26. Content Tools (4 endpoints)

### TC-CT-001: click_tracking
- Expected: tracking data

### TC-CT-002: shorten_url
- Expected: shortened url

### TC-CT-003: url_preview
- Expected: preview

### TC-CT-004: instagram_locations
- Expected: locations

---

## 27. Media (1 endpoint)

### TC-MED-001: media_list
- Expected: media items

---

## RBAC Cross-Cutting Test Cases (50+)

### RBAC-001: Writer cannot delete workspace
### RBAC-002: Writer cannot remove members
### RBAC-003: Writer cannot update workspace settings
### RBAC-004: Writer cannot clone workspace
### RBAC-005: Writer cannot create roles (CURRENTLY CAN — BUG)
### RBAC-006: Writer cannot set permissions on roles (CURRENTLY CAN — BUG)
### RBAC-007: Writer cannot assign self to elevated role
### RBAC-008: Writer cannot publish posts (no publish permission)
### RBAC-009: Writer cannot approve posts
### RBAC-010: Writer cannot send to clients (send-client)
### RBAC-011: Writer cannot manage social accounts
### RBAC-012: Writer cannot delete others' posts
### RBAC-013: Publisher can publish posts
### RBAC-014: Publisher can approve posts
### RBAC-015: Publisher can send to clients
### RBAC-016: Publisher cannot delete workspace
### RBAC-017: Publisher cannot manage roles
### RBAC-018: Editor can approve posts
### RBAC-019: Editor can edit others' posts
### RBAC-020: Editor cannot publish
### RBAC-021: Editor cannot send to clients
### RBAC-022: Editor cannot manage social accounts
### RBAC-023: Non-member cannot access workspace
### RBAC-024: Non-member cannot access cards
### RBAC-025: Non-member cannot access posts
### RBAC-026: Non-member cannot access libraries
### RBAC-027: Cross-workspace card access returns 404
### RBAC-028: Cross-workspace post access returns 404
### RBAC-029: Cross-workspace library access returns 404
### RBAC-030: Cross-user token cannot access other user's data

---

## Edge Cases (100+)

### EDGE-001: Empty string title in workflow_idea_create
### EDGE-002: Null title
### EDGE-003: Very long title (>255 chars)
### EDGE-004: SQL injection in title
### EDGE-005: XSS in comment text
### EDGE-006: Unicode/emoji in post message
### EDGE-007: Schedule date in past
### EDGE-008: Schedule date far future (>1 year)
### EDGE-009: Invalid account_id in schedule
### EDGE-010: Duplicate account_id in schedule
### EDGE-011: Media URL with invalid format
### EDGE-012: Media URL with XSS
### EDGE-013: Empty media array
### EDGE-014: Media type mismatch (image url as video)
### EDGE-015: Concurrent card advance (race condition)
### EDGE-016: Card deleted while being edited
### EDGE-017: Workspace deleted while board open
### EDGE-018: Token expired mid-session
### EDGE-019: Rate limiting (100 req/min)
### EDGE-020: Large payload (>1MB)
### EDGE-021: Malformed JSON
### EDGE-022: Missing Content-Type header
### EDGE-023: Wrong HTTP method (GET instead of POST)
### EDGE-024: Extra unknown fields in body
### EDGE-025: Null values in required fields
### EDGE-026: Boolean where string expected
### EDGE-027: Number where string expected
### EDGE-028: Array where object expected
### EDGE-029: Object where array expected
### EDGE-030: Nested injection in JSON

---

## Validation Matrix (per endpoint)

For each of 199 endpoints, test:
1. Missing required fields → 400
2. Invalid field types → 400
3. Invalid IDs → 404
4. Cross-user access → 404
5. Insufficient permissions → 403
6. Valid input → 200
7. Duplicate/conflict → 409
8. Rate limit → 429

= 199 × 8 = 1592 validation test cases minimum

---

## RBAC Matrix (role × action)

Roles: Owner, Publisher, Editor, Writer, Contributor, Member, Non-member
Actions: 199 endpoints × 7 roles = 1393 permission test cases

---

## Total Estimated Test Cases

- Per-endpoint happy path: 199
- Per-endpoint validation: 199 × 8 = 1592
- RBAC matrix: 199 × 7 = 1393
- Edge cases: 200+
- Integration/E2E flows: 50+
- **Total: ~3,500+ test cases**

This document provides the framework. Each test case needs to be executed and results recorded in per-run report files in the /reports/ folder.