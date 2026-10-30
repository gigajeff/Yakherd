# Yakherd.dev Concierge Disposable Capability Evidence

Date: 2026-07-21

Status: FAIL

Attempt ID: `20260721T155833Z`

## Exact reviewed plan identity

This sole capability attempt is bound to the following composite, in precedence
order:

- v3: `e34aa007270ad6ea62789305e319c9d0a2e8b2455ec00bc9c4c2c10b858c37b7`;
- v5: `56bf787b927fd565789281c2fa9dac75a4e7cfa5b725100f19d98ed83838ea38`;
- v6: `b20af29ccb82a0910a99630bfed91f241648e14986847488b5b86681a7b64334`;
- v7: `5bd429444d569178e0bad02177ae82e39dd2bea30ae7498b2ec4d494c5a89893`;
- v8: `67a3346a601e9d98cac297432fe69fd4c89cf152c881c129f9fa6dcae35a3cd6`;
- v9: `5f95a7765d9bd3cf7941c449a7f6550ea80d0268ac8238b530cf4b3351e0f35d`;
- v10: `57d336416c4c823761470f3b6957bd8114150374b91cb1d48d7108ef1899b34b`;
- v11: `08736a3855137296bc89bdecc4039859b414b2800f3ec8b593503c8ecec755dc`;
- v12: `c2daaa03baf52390f40d07f9f640e074463f8025acfaf7b73258c2d4d2e1cdc2`;
- v13: `d9f2f008f0155e1e16b908c1939817363a2f94ec8aac587e34374f193158625f`.

Independent v13 plan PASS:
`docs/audits/yakherd/2026-07-21_yakherd_dev_concierge_plan_red_team_v13.md`,
SHA-256
`1e8813b0be1c238da50047e7387289ffa57842b6ee7d97392712359e17e6c6ea`.

Client schema ID: `yakherd-capability-client-v3`.

Failure schema ID: `yakherd-capability-failure-v5`.

Unchanged v8 PHP identity: 7,279 bytes; SHA-256
`34bed082512b91192d4b5e8b9cca5269fbbe1a2b53a45b7db392a48b6622a32c`.

## Result

Capability result: **FAIL**.

The single read-only certificate operation did not produce the required
`VALID` scalar. This record does not claim that the certificate is invalid; it
records the certificate fact as unobservable. The already available browser
binding was confirmed locally without repeating the certificate operation.
The one-attempt rule stopped the preflight before root or File Manager
inspection.

Attempt window: `20260721T155833Z` through `2026-07-21T16:02:30Z`.

## Mutation and action ledger

| Order | Action | Result |
| --- | --- | --- |
| 1 | Create and validate the sole local `IN_PROGRESS` evidence skeleton | completed |
| 2 | Invoke one read-only HTTPS certificate/origin check for the fixed staging hostname | required `VALID` scalar not obtained |
| 3 | Check only that the pre-existing local browser binding exists, without a browser request | binding present; certificate operation not retried |
| 4 | Stop before root/File Manager inspection or mutation | completed |

No DreamHost panel setting, remote file, remote directory, host-managed auth
file, credential, password-manager record, local download directory, probe,
log query, outbound provider request, cron job, SSH/SFTP state, Git state,
website byte, staging release, or production state was created, changed, read,
or deleted after the failed certificate check. No fixture or private work path
was inspected, so those states remain unobservable rather than guessed empty.

## Gate disposition

| Gate | Evidence result |
| --- | --- |
| Certificate | FAIL; expected scalar not obtained |
| Root inventory | unobservable; not attempted after certificate failure |
| File Manager observability | unobservable; not attempted after certificate failure |
| Final inventory | unobservable; no empty-state claim |
| Panel auth and credential lifecycle | not applicable; generator never invoked |
| Fixture, probe, OpenAI TLS, HTTP, and log checks | not attempted |
| Local download cleanup | `ABSENT`; no download directory was created |
| Cron, SSH/SFTP, Git, provider secret, live model, staging release, production | not authorized and not attempted |

Appendix A was not materialized. Its reviewed identity remains 7,279 bytes,
SHA-256
`34bed082512b91192d4b5e8b9cca5269fbbe1a2b53a45b7db392a48b6622a32c`.
No manifest preimage was created because no operator file was uploaded.

## Failure state (canonical JSON)

- Schema ID: `yakherd-capability-failure-v5`
- Client schema ID: `yakherd-capability-client-v3`
- Canonical byte length: `2558`
- SHA-256: `30687f4ede5638026b507d36b80b0c1aaba9b03f7e3295e6a90775511cc4e7b8`
- Base64 preimage (unwrapped padded RFC 4648):

```text
eyJjYXBhYmlsaXR5X3Jlc3VsdCI6IkZBSUwiLCJjbGVhbnVwX3V0YyI6IjIwMjYtMDctMjFUMTY6MDI6MzBaIiwiY2xpZW50X2NsZWFudXAiOnsiYnJvd3Nlcl9yZXN0YXJ0IjoiTk9UX0FQUExJQ0FCTEUiLCJoYW5kYmFja19jaGVjayI6Ik5PVF9BUFBMSUNBQkxFIiwicGFuZWxfZmllbGRzIjoiTk9UX0FQUExJQ0FCTEUiLCJwYW5lbF90YWIiOiJOT1RfQVBQTElDQUJMRSIsInBhc3N3b3JkX3JlY29yZCI6Ik5PVF9BUFBMSUNBQkxFIiwic2NoZW1hX3ZlcnNpb24iOjMsInN0YWdpbmdfdGFicyI6Ik5PVF9BUFBMSUNBQkxFIn0sImZhaWxlZF9jaGVja3MiOlsiQ0VSVElGSUNBVEUiLCJGSUxFX01BTkFHRVJfT0JTRVJWQUJJTElUWSIsIkZJTkFMX0lOVkVOVE9SWSIsIlJPT1RfSU5WRU5UT1JZIl0sImZhaWx1cmVfY2xhc3NlcyI6WyJGSVhUVVJFX1NUQVRFX1JFVEFJTkVEIiwiUEFORUxfU1RBVEVfUkVUQUlORUQiLCJXT1JLX1NUQVRFX1JFVEFJTkVEIl0sImZpeHR1cmVfaW52ZW50b3J5Ijp7ImVudHJpZXMiOlt7ImJ5dGVfbGVuZ3RoIjpudWxsLCJieXRlX2xlbmd0aF9zdGF0ZSI6IlVOT0JTRVJWQUJMRSIsIm1vZGUiOiJVTktOT1dOIiwib3duZXJfc3RhdGUiOiJVTk9CU0VSVkFCTEUiLCJwYXRoIjoiZml4dHVyZSIsInByZXNlbmNlIjoiVU5PQlNFUlZBQkxFIiwic2hhMjU2X3N0YXRlIjoiVU5PQlNFUlZBQkxFIiwidHlwZSI6IlVOS05PV04ifSx7ImJ5dGVfbGVuZ3RoIjpudWxsLCJieXRlX2xlbmd0aF9zdGF0ZSI6IlVOT0JTRVJWQUJMRSIsIm1vZGUiOiJVTktOT1dOIiwib3duZXJfc3RhdGUiOiJVTk9CU0VSVkFCTEUiLCJwYXRoIjoiZml4dHVyZS8uaHRhY2Nlc3MiLCJwcmVzZW5jZSI6IlVOT0JTRVJWQUJMRSIsInNoYTI1Nl9zdGF0ZSI6IlVOT0JTRVJWQUJMRSIsInR5cGUiOiJVTktOT1dOIn0seyJieXRlX2xlbmd0aCI6bnVsbCwiYnl0ZV9sZW5ndGhfc3RhdGUiOiJVTk9CU0VSVkFCTEUiLCJtb2RlIjoiVU5LTk9XTiIsIm93bmVyX3N0YXRlIjoiVU5PQlNFUlZBQkxFIiwicGF0aCI6ImZpeHR1cmUvNDA0Lmh0bWwiLCJwcmVzZW5jZSI6IlVOT0JTRVJWQUJMRSIsInNoYTI1Nl9zdGF0ZSI6IlVOT0JTRVJWQUJMRSIsInR5cGUiOiJVTktOT1dOIn0seyJieXRlX2xlbmd0aCI6bnVsbCwiYnl0ZV9sZW5ndGhfc3RhdGUiOiJVTk9CU0VSVkFCTEUiLCJtb2RlIjoiVU5LTk9XTiIsIm93bmVyX3N0YXRlIjoiVU5PQlNFUlZBQkxFIiwicGF0aCI6ImZpeHR1cmUvY2FwYWJpbGl0eS5waHAiLCJwcmVzZW5jZSI6IlVOT0JTRVJWQUJMRSIsInNoYTI1Nl9zdGF0ZSI6IlVOT0JTRVJWQUJMRSIsInR5cGUiOiJVTktOT1dOIn0seyJieXRlX2xlbmd0aCI6bnVsbCwiYnl0ZV9sZW5ndGhfc3RhdGUiOiJVTk9CU0VSVkFCTEUiLCJtb2RlIjoiVU5LTk9XTiIsIm93bmVyX3N0YXRlIjoiVU5PQlNFUlZBQkxFIiwicGF0aCI6ImZpeHR1cmUvaW5kZXguaHRtbCIsInByZXNlbmNlIjoiVU5PQlNFUlZBQkxFIiwic2hhMjU2X3N0YXRlIjoiVU5PQlNFUlZBQkxFIiwidHlwZSI6IlVOS05PV04ifV0sImV4dHJhX2VudHJ5X3N0YXRlIjoiVU5PQlNFUlZBQkxFIiwic3RhdGUiOiJVTk9CU0VSVkFCTEUifSwibG9jYWxfdGVtcF9zdGF0ZSI6IkFCU0VOVCIsIm5vdGVzX3ByZXNlbnQiOnRydWUsInBhbmVsX2ludmVudG9yeSI6IlVOT0JTRVJWQUJMRSIsInNjaGVtYV92ZXJzaW9uIjo1LCJ3b3JrX2ludmVudG9yeSI6eyJjaGlsZHJlbiI6W3siYnl0ZV9sZW5ndGgiOm51bGwsImJ5dGVfbGVuZ3RoX3N0YXRlIjoiVU5PQlNFUlZBQkxFIiwibW9kZSI6IlVOS05PV04iLCJvd25lcl9zdGF0ZSI6IlVOT0JTRVJWQUJMRSIsInBhdGgiOiJmaXJzdC5iaW4iLCJwcmVzZW5jZSI6IlVOT0JTRVJWQUJMRSIsInNoYTI1Nl9zdGF0ZSI6IlVOT0JTRVJWQUJMRSIsInRhcmdldF9zdGF0ZSI6IlVOT0JTRVJWQUJMRSIsInR5cGUiOiJVTktOT1dOIn0seyJieXRlX2xlbmd0aCI6bnVsbCwiYnl0ZV9sZW5ndGhfc3RhdGUiOiJVTk9CU0VSVkFCTEUiLCJtb2RlIjoiVU5LTk9XTiIsIm93bmVyX3N0YXRlIjoiVU5PQlNFUlZBQkxFIiwicGF0aCI6ImxpbmsuYmluIiwicHJlc2VuY2UiOiJVTk9CU0VSVkFCTEUiLCJzaGEyNTZfc3RhdGUiOiJVTk9CU0VSVkFCTEUiLCJ0YXJnZXRfc3RhdGUiOiJVTk9CU0VSVkFCTEUiLCJ0eXBlIjoiVU5LTk9XTiJ9LHsiYnl0ZV9sZW5ndGgiOm51bGwsImJ5dGVfbGVuZ3RoX3N0YXRlIjoiVU5PQlNFUlZBQkxFIiwibW9kZSI6IlVOS05PV04iLCJvd25lcl9zdGF0ZSI6IlVOT0JTRVJWQUJMRSIsInBhdGgiOiJzZWNvbmQuYmluIiwicHJlc2VuY2UiOiJVTk9CU0VSVkFCTEUiLCJzaGEyNTZfc3RhdGUiOiJVTk9CU0VSVkFCTEUiLCJ0YXJnZXRfc3RhdGUiOiJVTk9CU0VSVkFCTEUiLCJ0eXBlIjoiVU5LTk9XTiJ9XSwiZGlyZWN0b3J5Ijp7Im1vZGUiOiJVTktOT1dOIiwib3duZXJfc3RhdGUiOiJVTk9CU0VSVkFCTEUiLCJwcmVzZW5jZSI6IlVOT0JTRVJWQUJMRSIsInR5cGUiOiJVTktOT1dOIn0sImV4dHJhX2NoaWxkX3N0YXRlIjoiVU5PQlNFUlZBQkxFIiwic3RhdGUiOiJVTk9CU0VSVkFCTEVfUkVUQUlORUQifX0=
```

### Decoded field table

| Field | Decoded value |
| --- | --- |
| `capability_result` | `FAIL` |
| `cleanup_utc` | `2026-07-21T16:02:30Z` |
| `schema_version` | `5` |
| `failed_checks` | `CERTIFICATE`, `FILE_MANAGER_OBSERVABILITY`, `FINAL_INVENTORY`, `ROOT_INVENTORY` |
| `failure_classes` | `FIXTURE_STATE_RETAINED`, `PANEL_STATE_RETAINED`, `WORK_STATE_RETAINED` |
| `panel_inventory` | `UNOBSERVABLE` |
| `fixture_inventory.state` | `UNOBSERVABLE` |
| `fixture_inventory.extra_entry_state` | `UNOBSERVABLE` |
| all five ordered fixture rows | presence `UNOBSERVABLE`; type/mode `UNKNOWN`; length/SHA/owner `UNOBSERVABLE` |
| `work_inventory.state` | `UNOBSERVABLE_RETAINED` |
| `work_inventory.extra_child_state` | `UNOBSERVABLE` |
| `work_inventory.directory` | presence/owner `UNOBSERVABLE`; type/mode `UNKNOWN` |
| all three ordered work children | presence `UNOBSERVABLE`; type/mode `UNKNOWN`; length/SHA/target/owner `UNOBSERVABLE` |
| `local_temp_state` | `ABSENT` |
| client schema/version | `yakherd-capability-client-v3` / `3` |
| all six client state fields | `NOT_APPLICABLE` |
| `notes_present` | `true` |

The base64 preimage was constructed in process memory using raw-ASCII key
sorting, strict ASCII/no-escape serialization, the exact ordered fixture/work
rows, and the v13 literal client-key order. It was not materialized outside this
evidence document.

## Authority effect

This failed attempt grants no retry and no Implementation authority. The
existing IMPLEMENTATION task remains parked. Deployment, cron, SSH/SFTP, Git,
final staging auth/release, provider secret, live-model request, canary,
production, and publication remain blocked pending a new reviewed Architecture
candidate and the required independent gates.
