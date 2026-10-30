# Yakherd Concierge V1 - Static-Only Bounded Implementation Architecture V4

Document date: 2026-07-21
Plan schema: `yakherd-concierge-architecture-plan-v4`
Status: pre-intake candidate for independent Red Team review; no release or product implementation authority
Architecture owner: Architecture task
Product owner: Jeffrey Martin (`gigajeff`)

## 1. Decision, authority, and exact inputs

The owner selected Yakherd `v1.2.0` as the pinned Concierge target and
authorized Architecture to convert the static-only directive into a bounded
plan. This document does not claim that `v1.2.0` is public. Publication and
authentication remain later, separately reviewed work.

The exact product-direction input is:

- path: `docs/2026-07-21_yakherd_concierge_v1_build_directive_static_only.md`
- bytes: `17487`
- LF-delimited lines: `319`
- SHA-256: `15946d3266e38f4e579c9b35ce3bda7e621006f32cda35ceb5eb03cf53acf12d`
- author of record: Jeffrey Martin
- selected form: the LF-normalized durable repository copy, not the earlier
  17,804-byte CRLF attachment transport form.

The preserved prior candidates and reviews are:

| Record | Bytes | LF lines | SHA-256 | Verdict |
| --- | ---: | ---: | --- | --- |
| `docs/audits/yakherd/2026-07-21_yakherd_concierge_v1_build_directive_red_team.md` | 19030 | 164 | `274b6db4bc92fe40bfceee3efe70331814c52235db28d5ba4032ca88e98ca64a` | FAIL |
| `docs/2026-07-21_yakherd_concierge_v1_bounded_implementation_plan.md` | 68774 | 1391 | `216cea3bd5f262e487329f0fcc757666e52397e6d8e119882862b88739afa029` | candidate |
| `docs/audits/yakherd/2026-07-21_yakherd_concierge_v1_bounded_plan_red_team.md` | 16166 | 150 | `34b19607510fdd696904974e2cb56aced148ef2b46838dec72ce6fd5a62a6fda` | FAIL |
| `docs/2026-07-21_yakherd_concierge_v1_bounded_implementation_plan_v2.md` | 103293 | 1956 | `68f444c46992b0dd31c8b84f328d85b86cc6851e1c3693ca22bc8b44aca2809a` | candidate |
| `docs/audits/yakherd/2026-07-21_yakherd_concierge_v1_bounded_plan_red_team_v2.md` | 15149 | 137 | `32b1274e4350ea732b14565d9925fb8c4d9bd61728a60c6f63f039e41676b1ec` | FAIL |
| `docs/2026-07-21_yakherd_concierge_v1_bounded_implementation_plan_v3.md` | 142347 | 2589 | `d687860db50cb816d899043cee9f3e7825195602a0884fead242b6a92bc28b51` | candidate |
| `docs/audits/yakherd/2026-07-21_yakherd_concierge_v1_bounded_plan_red_team_v3.md` | 17272 | 141 | `2ecd834ef7a852d7daf4a55510241f5a60b33a72603b5cb08b62ceebb9d2df12` | FAIL |

V4 preserves every prior byte. It resolves V3 by removing, rather than
repairing, the executable governance layer. No resolver, runner, Job Object,
Python/Node command supervisor, command journal, or generated local run record
exists in the V4 construction gate. That machinery is unnecessary for a
static site and was the source of all four V3 P1 findings.

## 2. Standalone materialized-contract rule

V4 is standalone. The only normative bytes are V4 Sections 1-10 and the two
materialized appendices in this file. No consumer applies a transformation to
V3, resolves a V3 section number, or imports an omitted V3 clause.

The appendices were mechanically derived from the exact V3 candidate and are
embedded as readable Markdown:

| Payload | Bytes | LF lines | SHA-256 |
| --- | ---: | ---: | --- |
| Appendix A effective product contract, from the LF-delimited `## PC-2. Product boundary` heading immediately after the Appendix A heading through the LF before the Appendix B heading | 53296 | 1019 | `c67c7e87e79522976adec34f1f290820e5139b728043aa655ca81e51e1081e69` |
| Appendix B effective release/intake gates, from the LF-delimited `### Gate R-PREP - documentation-only release preparation` heading immediately after the Appendix B heading through the file's terminal LF | 13108 | 241 | `4a6ffa7d44095bd947fb2b6f75f616d9fecd0946822787cc56bc375f72073968` |

Appendix A materializes V3 Sections 2, 3, 6-13, and 16; namespaces all internal
product references as `PC-*`; removes construction-time execution; places the
first target execution at Gate C; and fixes the sequence to Gate X, C-PREP, C,
S, then T. Appendix B materializes V3 Gates R-PREP, R, B, and P; replaces every
runner/resolver clause with inert data/golden freezing; maps canonical JSON to
PC-10; and expressly excludes historical V3 Sections 14-15.

For provenance only, the source V3 fragments reproduced as:

| Source fragment | Bytes | LF lines | SHA-256 |
| --- | ---: | ---: | --- |
| V3 Sections 2-3 | 3823 | 70 | `0ffdea9296d6944f271ac86bd93e4a4e66441ed629ea313f9c1526ccc19afdb2` |
| V3 Gates R-PREP through P | 13561 | 249 | `d18e2aa7de617f50552d13fd9af2de1914615d7634c1645f5df316556da08739` |
| V3 Sections 6-13 | 46964 | 908 | `e7c87d12b68c52233802bba0572184d12de7ee944395da5ef56e6bdd26e434e9` |
| V3 Section 16 | 2304 | 39 | `d1236594488b60832848a5506182bc2c5dbf7cf455703a87a98dda6f8dd29d2a` |

Those source fragments and every other V3 byte are historical evidence only.
If an appendix payload identity differs from the table, Gate A fails; there is
no semantic fallback to V3.

## 3. Product boundary and central simplification

The complete product behavior is the materialized Appendix A together with
the static acceptance requirements in Sections 6-7. In short, V1 is one
charming static browser
concierge: it asks a fixed interview, mechanically drafts a master prompt,
lets the beginner edit and approve it, and downloads the deterministic five-
file Yakherd `v1.2.0` handoff. It has no backend, model call, account,
analytics, telemetry, package dependency, build step, or intentional user-data
egress.

Construction is deliberately inert. Gate I-W may create and read back static
bytes, but it may not execute, import, evaluate, compile, serve, or open any
target code. Gate X may inspect and hash those bytes but also may not execute
them. Runtime and functional claims belong only to a separately planned and
reviewed Gate C. Gate S is a final independent security/parser/evidence gate
after Gate C, not part of construction. It defaults to Sol xhigh because Gate
R already consumes the one Ultra review currently planned; a second Ultra
requires fresh owner permission.

## 4. Serial gates and exact authority

The gates are strictly serial. A missing record or FAIL parks every later gate.
PASS grants only the action named immediately after it.

### Gate A - V4 plan review, current gate

One independent Sol-xhigh Red Team reviews this exact V4 candidate, all eight
records in Section 1, both materialized Appendix payload identities, all four
historical source-fragment identities, and all nine PC-11 fixture identities. It may
exclusively create, fail-if-exists:

`docs/audits/yakherd/2026-07-21_yakherd_concierge_v1_bounded_plan_red_team_v4.md`

PASS authorizes Architecture only to perform the documentation-only Gate
R-PREP defined in Appendix B. Red Team returns its result to Architecture
only. It must not contact any Implementation task, including to report parked
status. Gate A grants no package/release mutation, Git mutation, network or
browser action, credential use, target-root creation, product intake, or
product work. The
repository-required local read-only Git metadata and diff checks are permitted;
Git staging, commits, tags, branches, remote/network operations, and every
other Git mutation remain forbidden.

### Gates R-PREP, R, B, and P - materialized exact contracts

Appendix B is the complete controlling contract for these four gates, in that
order. The summary is:

1. Gate R-PREP may create only
   `docs/2026-07-21_yakherd_v1.2.0_release_preparation_plan.md`; its independent
   reviewer may create only
   `docs/audits/yakherd/2026-07-21_yakherd_v1.2.0_release_preparation_plan_red_team.md`.
   It is documentation-only.
2. Gate R requires the separately reviewed exact release candidate, one final
   Sol Ultra release gate, explicit owner publication instruction, and public
   artifact authentication. It is the only release/publication authority.
3. Gate B creates the absent, separate, non-reparse
   `L:\dev\yakherd-web` root, performs the exact public-artifact v1.2.0 fresh
   install, records the complete installed baseline before bootstrap, and
   proves installed `AGENTS.md` is active. It does not create product files.
4. Gate P performs unchanged installed `product_intake.md`, exact provenance,
   owner promotion, complete before/after manifests, and combined independent
   review. Its post-intake plan incorporates this complete V4 and freezes all
   data/golden bytes required here. It contains no resolver/runner bytes.

The summary has no independent authority. If it differs from Appendix B, the
gate stops for a fresh Architecture candidate; no reader chooses between
competing interpretations.

### Gate I-W - inert static-byte construction

Only the combined Gate P PASS may contact the owner's existing
`IMPLEMENTATION` task with an actionable implementation assignment, and only
after that task
is attached solely to `L:\dev\yakherd-web`, demonstrates the installed
`AGENTS.md` is active, and relinquishes any writer role in the Yakherd engine
checkout. It uses Terra high, is the sole site writer, and receives exact
hashes for the post-intake plan/audit, Gate P manifests, release evidence, all
frozen data/golden bytes, and this Section 6 write set. No replacement task or
second writer may be created without owner direction.

Gate I-W may use only the exact task-host filesystem primitives frozen by the
combined Gate P plan and audit for directory-create, exclusive file-create,
byte-copy into an exclusively created file, byte-read, and SHA-256. Each
primitive is synchronous, addresses exactly one announced destination, returns
only after every destination handle is closed, and neither starts nor detaches
a child/background operation. A foreground task-host wrapper is permitted only
when it exposes completion or termination of the one direct filesystem
operation; it may not invoke a target file. The exact primitive name, version
or host identity, arguments, one-path effect, fail-if-exists behavior, flush and
handle-close behavior, and interruption semantics must be frozen at Gate P.
An unavailable or weaker primitive stops Gate I-W before mutation.

Within that boundary, Gate I-W may create exactly the six directories and 60
files in Section 6, one at a time, using fail-if-exists/no-overwrite semantics,
containment and reparse checks, flush, read-back, byte length, and SHA-256. It
may read installed governance files, the fixed external image/license sources,
and the exact authorizing records. It may not edit any installed Gate B/P path.

Gate I-W must not execute any target file through Python, Node, PowerShell, a
shell, a native binary, HTML, JavaScript, a test/verifier, ZIP code, a browser,
or a server. It must not import, evaluate, compile, parse as executable code,
or dynamically load a target file. The narrowly frozen task-host filesystem
operations above are control-plane activity, not target execution. They may
not be expanded into general shell or script authority. Network, dependency
install, Git, package managers, screenshots, credentials, hosting, and
deployment are forbidden.

Success is only `STATIC_SOURCE_READY_FOR_REVIEW`, never test PASS or product
completion. The writer reports the exact task/thread ID, model/effort, every
created path identity, the complete observed target inventory, and a transcript
cursor covering the entire assignment. It then stops with `autonomous next
action: Gate X independent static-source review`.

### Gate X - independent static-source review

One independent Sol-xhigh reviewer reads the complete target tree, authorizing
records, and the Gate I-W task transcript. It may use trusted read-only task
tools for byte reads, hashing, text parsing, and static analysis, but may not
execute or serve any target file or invoke a target test/verifier. It
independently reconstructs the complete tree manifest and verifies the exact
checks in Section 7.

Gate X may exclusively create, fail-if-exists, these external records in this
repository, finalizing Markdown before JSON:

- `docs/audits/yakherd/2026-07-21_yakherd_web_gate_x_static_source_red_team.md`
- `docs/audits/yakherd/2026-07-21_yakherd_web_gate_x_static_source_authorization.json`

A PASS states only that the exact static source is review-ready, target
execution was not authorized in I-W/X, and no target-execution command was
observed in the complete readable Implementation/review transcript. It does
not claim a process-audit proof about unobservable history. It authorizes
Architecture to draft the Gate C-PREP documents below; it does not authorize
runtime execution. A FAIL permits no repair, retry, deletion, or target
mutation. Architecture must write a separately reviewed recovery or revision
plan.

### Gate C-PREP and Gate C - separately reviewed runtime acceptance

Gate X PASS may authorize Architecture to create only:

`docs/2026-07-21_yakherd_concierge_v1_runtime_acceptance_plan.md`

Its independent reviewer may create only:

`docs/audits/yakherd/2026-07-21_yakherd_concierge_v1_runtime_acceptance_plan_red_team.md`

That future plan must bind exact runtime/tool identities, installed capability,
profiles, process lifetime, timeouts, request interception, local server,
Python/Node startup policy if used, output limits, evidence paths, cleanup,
failure recovery, and every runtime requirement in Appendix A PC-16.
Until its fresh PASS, no browser, server, target Python/Node, target test,
accessibility tool, screenshot, clipboard, download, or request interception is
authorized.

Gate C is the first gate that may execute target/browser/test code. It owns all
functional, deterministic-bundle, no-network runtime, two-OS, extraction,
fresh-install bridge, storage, clipboard/download, and accessibility evidence.
It may not change the Gate X-approved source bytes. Any source change returns
to Gate I-W and requires new Gate X and Gate C review.

### Gate S, T, G, H, D, and O - later only

- Gate S is one Sol-xhigh final independent security/parser/runtime-evidence
  review of unchanged Gate X source plus complete Gate C evidence. It performs
  no product mutation and no second runtime campaign. It may use Ultra only
  after fresh owner permission for a second Ultra review.
- Gate T is a separately reviewed same-writer owner/`STATUS.md` promotion of
  the exact Gate S-approved result.
- Gate G is the owner checkpoint for Git initialization, repository identity,
  visibility, commit, remote, and push.
- Gate H is read-only hosting/privacy capability inventory and owner host
  selection.
- Gate D is separately reviewed staging, rollback, production, and publication.
- Gate O is the beginner onboarding walkthrough and public handoff.

None is authorized by the current V4 review.

## 5. Gate I-W filesystem and failure contract

At Gate I-W entry, the target tree must equal the complete Gate P after-
manifest plus only the separately hash-bound containing post-intake plan and
combined Gate P audit. `.git` must be absent. The six Section 6 directories and
all 60 Section 6 files must be absent, with no case-fold aliases. Every
ancestor/destination must be contained and non-reparse. Any unknown child,
collision, symlink, junction, reparse point, other filesystem type, baseline
change, second writer, or unbound record stops before mutation.

The writer creates directories one level at a time. Text and binary files use
exclusive create/no overwrite. Every operation follows this sequence:

1. revalidate the complete current inventory and the next destination's absent
   state;
2. announce the one literal next path in the task transcript;
3. create only that directory or file;
4. flush if applicable;
5. read back type, byte length, and SHA-256 without interpreting the file;
6. compare with the frozen expected identity when one exists;
7. report the observed identity before proceeding.

The no-concurrent-writer invariant and revalidation narrow filesystem races;
the plan does not claim to prove historical kernel open flags from a transcript.
If the task/tool cannot provide exclusive file creation, it must stop before
the first file. Directory creation may proceed only while the same sole-writer
lock and absent-child inventory remain true.

No cleanup occurs on failure. If completion or termination of the current
filesystem primitive is observed, the writer stops all mutation, performs one
read-only inventory under the schema below, reports every retained or
unresolved path, and returns to Architecture. It does not retry, delete,
overwrite, move, rename, commit, reset, or publish. Gate I-W launches no target
process, so it cannot orphan a target executor.

If completion or termination of a control-plane mutation is not observable,
the exact status is `MUTATION_LIVENESS_UNKNOWN`. No later filesystem read,
cleanup, recovery, Gate X start, or inventory claim of stability/completeness
is authorized. The writer reports the last confirmed observations, marks the
one announced destination and every fact that could depend on it `UNKNOWN`,
sets `inventory_complete` false and `enumeration_error` to `INTERRUPTED`, and
parks all authority until an external state change or a separately reviewed
liveness/recovery plan permits another observation. A timeout is never treated
as proof that the task-host mutator stopped.

The Gate I-W failure handback and Gate X FAIL Markdown each embed one canonical
inventory object with top-level keys in this exact raw-ASCII order:
`enumeration_error`, `inventory_complete`, `rows`, `schema_version`.
`schema_version` is integer 1. `enumeration_error` is exactly `NONE`,
`ENUMERATION_FAILED`, `TRUNCATED`, or `INTERRUPTED`; `inventory_complete` is a
boolean. `rows` covers the ordinal-ASCII path union of every Gate P
after-manifest path, the two authorized post-manifest records, all 66 Section 6
destinations, and every other descendant actually observed. Each path appears
once.

This failure-inventory serializer is distinct from PC-10 only because it
permits JSON null. It is strict UTF-8 without BOM, uses no insignificant
whitespace, uses PC-10's string escaping, integer lexical form, raw-ASCII key
ordering, and malformed-scalar rejection, and has exactly one terminal LF.
Null is permitted only in `bytes_value` and `sha256_value` under the tuples
below; it is forbidden everywhere else.

Every row has keys in this exact raw-ASCII order: `bytes_state`, `bytes_value`,
`path`, `presence`, `sha256_state`, `sha256_value`, `type`.
`presence` is `ABSENT`, `PRESENT`, or `UNKNOWN`; `type` is `ABSENT`,
`DIRECTORY`, `REGULAR_FILE`, `OTHER`, or `UNKNOWN`; each state is `KNOWN`,
`NOT_APPLICABLE`, or `UNKNOWN`. State/value normalization is total:

- `ABSENT` presence requires `ABSENT` type, both states `NOT_APPLICABLE`, and
  both values null;
- `UNKNOWN` presence requires `UNKNOWN` type, both states `UNKNOWN`, and both
  values null;
- a present `DIRECTORY` requires both states `NOT_APPLICABLE` and both values
  null;
- a present `REGULAR_FILE` uses a nonnegative safe integer only when
  `bytes_state` is `KNOWN` and lowercase SHA-256 only when `sha256_state` is
  `KNOWN`; either unobservable fact uses `UNKNOWN` with null;
- a present `OTHER` uses both states `NOT_APPLICABLE` and both values null;
- a known-present path whose type cannot be observed uses `UNKNOWN` type, both
  states `UNKNOWN`, and both values null;
- no other tuple is legal.

`inventory_complete` is true only when namespace enumeration completed without
error or truncation and no row contains an `UNKNOWN` presence, type, byte, or
hash fact that is applicable to a regular file. `OTHER` may be completely
observed but is always a gate failure. When enumeration itself is incomplete,
the known rows remain, required-but-unobserved paths use truthful `UNKNOWN`
rows, `inventory_complete` is false, and no absence or tree-completeness claim
is made.

The Implementation transcript is part of Gate X input, not proof by itself.
Gate X independently compares the final filesystem to the Gate P manifests and
Section 6. A missing transcript range, truncated tool result, unexplained path,
or inability to establish the narrower observable claim that no
target-execution command appears in the complete transcript is FAIL.

## 6. Exact static write set

All paths are relative to `L:\dev\yakherd-web`. The six new directories, in
order, are:

1. `site`
2. `site/assets`
3. `site/data`
4. `site/fallback`
5. `tests/fixtures`
6. `tests/golden`

The 60 new files, in order, are:

1. `.gitattributes`
2. `LICENSE`
3. `NOTICE.md`
4. `site/index.html`
5. `site/concierge.html`
6. `site/next-steps.html`
7. `site/privacy.html`
8. `site/troubleshooting.html`
9. `site/404.html`
10. `site/assets/styles.css`
11. `site/assets/app.mjs`
12. `site/assets/concierge.mjs`
13. `site/assets/state.mjs`
14. `site/assets/bytes.mjs`
15. `site/assets/canonical-json.mjs`
16. `site/assets/crc32.mjs`
17. `site/assets/zip-store.mjs`
18. `site/assets/storage.mjs`
19. `site/assets/scanner.mjs`
20. `site/assets/content.v1.mjs`
21. `site/assets/yakherd2.png`
22. `site/data/interview.v1.json`
23. `site/data/prompt_template.v1.txt`
24. `site/data/secret_patterns.v1.json`
25. `site/data/high_stakes_terms.v1.json`
26. `site/data/yakherd_release.v1.json`
27. `site/fallback/master_prompt_template.txt`
28. `docs/CONCIERGE.md`
29. `docs/PRIVACY_BOUNDARY.md`
30. `docs/STATIC_SOURCE_POLICY.md`
31. `docs/BUNDLE_FORMAT.md`
32. `docs/CONTENT_PROVENANCE.md`
33. `tests/concierge_test_static_policy.py`
34. `tests/concierge_test_content_binding.py`
35. `tests/concierge_test_pages.py`
36. `tests/test_bytes.mjs`
37. `tests/test_state.mjs`
38. `tests/test_canonical_json.mjs`
39. `tests/test_crc32.mjs`
40. `tests/test_zip_store.mjs`
41. `tests/test_scanner.mjs`
42. `tests/test_storage.mjs`
43. `tests/test_interview.mjs`
44. `tests/fixtures/bundle_input.v1.json`
45. `tests/fixtures/prompt_ascii_lf.txt`
46. `tests/fixtures/prompt_unicode_lf.txt`
47. `tests/fixtures/prompt_empty.txt`
48. `tests/fixtures/prompt_rejected_lone_surrogate.json`
49. `tests/fixtures/prompt_rejected_delimiter.txt`
50. `tests/fixtures/secret_clean.txt`
51. `tests/fixtures/secret_positive.txt`
52. `tests/fixtures/high_stakes_clean.txt`
53. `tests/fixtures/high_stakes_positive.txt`
54. `tests/golden/MASTER_PROMPT.txt`
55. `tests/golden/MASTER_PROMPT_HANDOFF.txt`
56. `tests/golden/APPROVAL.json`
57. `tests/golden/BUNDLE_MANIFEST.json`
58. `tests/golden/OPEN_IN_CODEX.txt`
59. `tests/golden/yakherd_intake_6e7dd93a7067.zip`
60. `tests/golden/golden_identity.v1.json`

There is no file at `scripts/concierge_gate_i_runner.py` and no Concierge file
under `docs/run_records`. No wildcard or other path is authorized. In
particular, no runner, resolver, supervisor, journal, command record, generated
evidence, `_headers`, `_redirects`, hosting configuration, workflow, dependency
lockfile, package manifest, source map, hidden IDE file, screenshot, coverage,
cache, temporary file, generated test output, or archive other than file 59 may
be created.

`.gitattributes` is strict UTF-8, LF-only, no BOM, and exactly:

```text
* text=auto eol=lf
*.png binary
*.zip binary
```

`site/assets/yakherd2.png` is an exact copy of
`L:\dev\YAKHERD\yakherd2.png`: 3,028,501 bytes, SHA-256
`e45c1c5449fff67c0ea4f2b4ed3af9e4886793939f89a449c9e996e1367a4383`.
The source is checked before copy and destination after exclusive creation.
`yakherd.mp4` is never read, copied, hashed, inspected, moved, or touched.

`LICENSE` is an exact copy of `L:\dev\YAKHERD\LICENSE`, the Apache-2.0 engine
license: 11,358 bytes, SHA-256
`cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.
`NOTICE.md` is strict UTF-8/LF with one terminal LF and exactly:

```text
# Notice

Yakherd Concierge
Copyright 2026 Jeffrey Martin

Licensed under the Apache License, Version 2.0. See LICENSE.

The yakherd2.png artwork was supplied by Jeffrey Martin for Yakherd and is distributed with this repository under the same Apache-2.0 license.
```

`docs/CONTENT_PROVENANCE.md` repeats that statement and the literal source and
destination paths, byte length, SHA-256, source Git blob
`79fecd4306c7065c72846eaf0507293c191fff19`, source engine commit bound by Gate
R, copy task ID, and copy/read-back result; it contains no other asset. If the
owner cannot confirm image rights at Gate P, work stops for a new reviewed
plan; no substitute is allowed.

All text files are strict UTF-8, LF-only, BOM-free, follow their explicit
terminal-LF rule, and contain no trailing whitespace. Binary identities and all
Gate-P-frozen data/golden identities must match exactly. Files 33-43 are inert
test source during I-W/X; their presence does not authorize execution.

## 7. Exact Gate X static review and authorization JSON

Gate X first reconstructs a complete canonical target-tree manifest. The root
itself is excluded; every descendant directory and regular file is included.
Rows are in ordinal ASCII repository-path order and have exactly `bytes`,
`origin_relation`, `path`, `sha256`, and `type`.

- `type` is `DIRECTORY` or `REGULAR_FILE` only.
- directories have `bytes: 0` and `sha256: "NOT_APPLICABLE"`;
- files have a nonnegative safe-integer length and lowercase SHA-256;
- `origin_relation` is exactly `GATE_P_AFTER_MANIFEST`,
  `POST_GATE_P_PLAN`, `POST_GATE_P_AUDIT`, or `GATE_I_W_CREATED`;
- every Gate P after-manifest row remains byte/type identical;
- the two post-manifest records match their handed-off identities;
- the created relation covers exactly the six directories and 60 files in
  Section 6;
- `.git`, reparse points, aliases, case-fold collisions, other types, omitted
  children, and unexplained additions are forbidden.

Canonical JSON means the materialized PC-10 contract. The manifest hash
is SHA-256 over its canonical JSON array plus LF. The complete manifest, not
only its hash, is embedded in a PASS JSON. On FAIL, the Markdown audit embeds a
complete conservative observed inventory including `OTHER` and `UNKNOWN`
rows and identifies every retained/unresolved path; it does not emit a PASS
JSON.

Gate X verifies these checks exactly in this order:

1. `authorizations_exact`
2. `gate_p_tree_unchanged`
3. `implementation_transcript_complete`
4. `sole_writer_authority_consistent`
5. `no_target_execution_command_observed_in_complete_transcript`
6. `write_set_exact`
7. `tree_manifest_complete`
8. `text_encoding_and_line_rules_exact`
9. `binary_identities_exact`
10. `static_import_graph_closed`
11. `dynamic_code_surface_absent`
12. `network_api_surface_absent`
13. `external_subresource_surface_absent`
14. `unsafe_sink_surface_absent`
15. `content_module_matches_sources`
16. `release_pin_exact`
17. `intake_envelope_exact`
18. `canonical_json_source_matches_contract`
19. `zip32_source_matches_contract`
20. `golden_oracle_exact`
21. `secret_gate_source_fail_closed`
22. `high_stakes_source_fail_closed`
23. `approval_state_source_fail_closed`
24. `storage_copy_truthful`
25. `privacy_copy_truthful`
26. `accessibility_source_requirements_present`
27. `runtime_claims_deferred_to_gate_c`
28. `platform_observation_absent`
29. `generated_local_evidence_absent`
30. `internal_links_and_subresources_resolve`
31. `javascript_size_within_limit`
32. `informational_pages_meaningful_without_javascript`
33. `semantic_accessibility_source_contract_exact`
34. `unit_test_source_matrix_complete`

Each check is static and bounded. In particular,
`network_api_surface_absent` means the complete shipped source contains none of
the forbidden API/import/activation surfaces specified by Appendix A PC-6; it
is not a runtime no-request claim. Gate C alone may make
that runtime claim after interception. `zip32_source_matches_contract` means
the source and frozen oracle agree structurally; it does not claim that
unexecuted code reproduced the archive.

The five final checks preserve static source requirements deferred from later
acceptance without executing them. Every internal link and subresource must
resolve to a contained, regular, non-reparse file in `site`; total unminified
JavaScript is at most 153,600 bytes; and each informational page exposes
meaningful main content and navigation without JavaScript, while the Concierge
exposes its no-JavaScript notice and fallback.

The semantic/accessibility source contract requires each page to have exactly
one `h1`, named landmarks, associated labels, logical heading order, a skip
link, a valid `lang`, viewport metadata, and the exact meta CSP; it forbids
autoplay and motion-dependent operation. The reviewed CSS must contain visible
focus, 320px reflow, reduced-motion, forced-colors, and explicit reviewed color
pairs meeting 4.5:1 normal-text and 3:1 large-text contrast. These are static
source requirements; keyboard, zoom, screen-reader, computed contrast, and
browser behavior remain Gate C evidence.

The inert test-source matrix must directly cover empty, ASCII, Unicode, and LF
inputs; CR and lone-surrogate rejection; every approval invalidation and
checkbox deselection; direct shipped handlers; corrupt/quota/delete/multitab
storage; delimiter enforcement; canonical-JSON lexical bytes; CRC; ZIP32
headers and limits; deterministic golden reproduction; secret clean/positive;
high-stakes `ANSWERED` + `NO` + clean = false and positive/`UNKNOWN`/skip =
true; every frozen term; contradiction ordering; editor-size bounds; and
content binding. Gate X reviews the complete matrix statically; Gate C is the
first gate allowed to run it.

The Gate X PASS JSON is strict UTF-8 canonical JSON plus LF with exactly these
top-level keys:

```text
audit
authorizations
checks
directories
effective_contract
files
implementation
project_root
schema_version
status
transcript
tree_manifest
tree_manifest_sha256
unexpected_paths
```

The displayed sequence is the required raw-ASCII top-level key order.

`schema_version` is integer 1; `status` is `PASS`; `project_root` is literal
`L:\dev\yakherd-web`; `unexpected_paths` is an empty array.

`audit` has exactly `bytes`, `path`, and `sha256` and binds the finalized Gate X
Markdown audit. `authorizations` has exactly `gate_a_audit`,
`gate_p_combined_audit`, `gate_r_evidence`, `post_intake_plan`, and `v4_plan`.
Each authorization has exactly `bytes`, `path`, `sha256`, and `status`; statuses
are `PASS` for audits/evidence and `REVIEWED` for plans.

`effective_contract` has exactly `appendix_a_bytes`, `appendix_a_sha256`,
`appendix_b_bytes`, `appendix_b_sha256`, `v4_bytes`, `v4_path`, and `v4_sha256`.
The appendix values reproduce Section 2; V4 values bind this finalized plan.

`implementation` has exactly `effort`, `model`, `status`, `task_id`, and
`writer_authority`; values are `high`, `gpt-5.6-terra`,
`STATIC_SOURCE_READY_FOR_REVIEW`, the exact attached task ID, and
`SOLE_AUTHORIZED_WRITER`. `transcript` has exactly `complete_range_read`,
`end_cursor`, `no_target_execution_command_observed`, `start_cursor`, and
`thread_id`. The two booleans are true; strings are the exact
task/thread/cursor values and contain no user prompt or secret content. These
fields bind authority and observable transcript content, not unknowable
historical exclusivity. If the reviewer cannot read the complete range, it
fails rather than guessing.

`directories` has six rows in Section 6 order with exactly `after_type` =
`DIRECTORY`, `before_type` = `ABSENT`, and `path`. `files` has 60 rows in
Section 6 order with exactly `after_bytes`, `after_sha256`, `after_type` =
`REGULAR_FILE`, `before_type` = `ABSENT`, and `path`.

`checks` has 34 rows in the exact order above, each with exactly `name` and
`status: "PASS"`. `tree_manifest` is the complete array defined above and its
hash field matches its exact canonical LF-terminated bytes.

The reviewer finalizes Markdown, reads it back, then exclusively creates the
JSON once. It does not predict the JSON's own identity and writes nothing into
the target. A PASS JSON with any missing/extra key, reordered check, manifest
gap, unsupported claim, or noncanonical byte is invalid.

## 8. No-execution capability closure

The V3 resolver/runner, outer-timeout, ambient Python startup, and
`platform.*` findings are eliminated by absence:

- no PowerShell resolver or substituted value channel exists;
- no Python runner, child, watchdog, Job Object, or command supervisor exists;
- the authorized procedure starts no target process, so it has no target child
  whose lifetime can extend past a task-host timeout;
- `python -I`, `-B`, `-S`, site-packages, `.pth`, `sitecustomize`, Python
  version grammar, Python import roots, Node startup, process environment,
  hostname, OS, registry, WMI, socket, subprocess, and platform observations
  are `NOT_APPLICABLE` to Gates I-W and X;
- no machine/runtime/environment run-record fields exist;
- no target-command output exists or is retained because target commands are
  outside the authorized procedure.

The task tools and reviewer may themselves use trusted workspace read/write and
hash facilities within their exact authority. That is maintainer control-plane
activity, not execution of target bytes. They must not claim those facilities
prove browser behavior. Any need to run a target parser, syntax checker, test,
server, or module stops and is deferred to the separately reviewed Gate C plan.

## 9. Fixtures and frozen oracle

The nine materialized PC-11 fixture identities remain exact:

| Fixture | Bytes | SHA-256 |
| --- | ---: | --- |
| `prompt_ascii_lf.txt` | 15 | `6e7dd93a7067af125e7511989288fded9b9ac794bdc4dcdb2386c82be681d093` |
| `prompt_unicode_lf.txt` | 21 | `b7235def28ab82dbf8190a1823d762d844ba1c5108e24bde4e3216dbe94de823` |
| `prompt_empty.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `prompt_rejected_lone_surrogate.json` | 42 | `d896c43281e7792bee0f1b5b7f6015488e69476113bae8b70c7fb95dd3a87e6e` |
| `prompt_rejected_delimiter.txt` | 30 | `bae930977c32a38633deb764b057b94d26f25f9c9f7c7c83b2d3470d06253f2a` |
| `secret_clean.txt` | 50 | `71207f9ff2aa7fdea169735ab97f84fea19bda146dad3ec6268ac3ab07bfa03f` |
| `secret_positive.txt` | 70 | `de1bac33ed9c73e034c0208509ffc167d7a7f2a9de98e45e07153461c4e63d8b` |
| `high_stakes_clean.txt` | 29 | `653687b406ccdbdc1c9b8d4fed2d042bcd986f161c724a490f7b07a03cf66406` |
| `high_stakes_positive.txt` | 44 | `33aaf433ef6fb46e9770d220f4bc2f07872a5a0119f17b9a33f01cbdeeffc20f` |

The Unicode fixture uses one U+00E9 scalar encoded `c3 a9`. Gate P's
independent spec-only reference construction, outside the target and before
the product writer, freezes complete base64/length/hash identities for the
bundle input, five entries, ZIP, and golden identity. The Implementation writer
only transcribes those reviewed bytes. Gates I-W/X do not execute either the
reference construction or product implementation. Gate C performs the first
runtime reproduction.

## 10. Stop conditions, model routing, and current authority

Stop without workaround if any identity, appendix payload, historical source-
fragment identity, release artifact, intake delimiter, baseline/manifest, path,
source asset, license, golden byte, write-set row, transcript range, tree row,
or static check is absent, ambiguous, changed, unobservable, or contradictory.
Also stop if the work would need target execution before Gate C, a second
writer, dependency, network API, Git mutation or network Git action,
credential, browser, server,
hosting action, or unlisted file.

Do not substitute another release, repository, root, host, asset, task,
framework, test tool, path, or privacy promise. Failure returns to Architecture
for one exact revision or recovery plan and fresh review.

Model routing is:

- Luna medium for mechanical inventory/hash work when available;
- Terra medium/high for routine implementation/research;
- Sol high/xhigh for architecture, difficult debugging, and nonfinal review;
- one Sol Ultra only for a final independent security, parser, deployment, or
  release gate; Gate R is the sole Ultra currently planned, never use Ultra for
  routine drafting, and never create a second Ultra without owner permission;
- never two Implementation writers against the same checkout.

For the current Gate A review, Red Team may write only the absent V4 audit path
in Section 4. It must return PASS or FAIL against this exact candidate and may
not contact Implementation. PASS authorizes Architecture only to create the
exact Gate R-PREP documentation candidate and request its fresh independent
review. FAIL authorizes only preservation and one new exact Architecture
candidate.

Nothing here currently authorizes Gate R-PREP execution, release preparation
or mutation, Gate R/B/P/I-W/X/C-PREP/C/S/T/G/H/D/O, Implementation contact or
work, Git mutation or network Git action, network/browser/DreamHost,
credentials, dependencies, target-root creation, image copying, evidence
creation other than the sole Gate A audit, GitHub/PyPI, hosting, DNS, staging,
deployment, production, or publication. Gate A's repository-required local
read-only Git metadata and diff checks remain allowed.

## Appendix A - Effective Product Contract

## PC-2. Product boundary

Build one static browser application that guides a beginner through a fixed
interview, mechanically drafts a master prompt, lets the beginner edit and
approve it, and downloads a deterministic five-file ZIP handoff for Yakherd
`v1.2.0`.

Concierge V1 does not install Yakherd, authenticate to GitHub, call the GitHub
API, or create, read, or modify the visitor's GitHub repositories. It may show
the exact public, user-initiated Yakherd repository/release links in PC-6.
It does not launch Codex tasks, run product code, call a model, create an account, receive
user input at a server, or deploy anything for the visitor. Those statements
describe runtime product behavior; they do not prohibit separately authorized
maintainers from using Git, tests, or deployment tools to build and publish the
static site.

Not in V1:

- model-backed interrogation or a relay endpoint;
- PHP, Workers, functions, APIs, forms, accounts, sessions, analytics, or
  telemetry;
- the complete governed repository export, local runner, workbench, or private
  GitHub backup;
- DreamHost capability work or the retired v15 preflight;
- a service worker, web manifest, Cache API, background sync, share API, or
  browser notifications;
- any dependency, package install, vendored library, build step, minifier, or
  generated production source.

## PC-3. Alternatives and selected architecture

Architecture considered three data-loading designs:

1. Runtime `fetch()` of JSON and text. Rejected because it makes the no-request
   boundary timing-dependent and requires `connect-src`.
2. Inline JSON/templates in HTML. Rejected because it needs inline content and
   duplicates authoritative resources in a difficult-to-audit form.
3. Versioned source data files plus one external, committed JavaScript content
   module containing their exact base64 bytes. Selected. A dependency-free
   verifier decodes that module and requires byte equality with every source
   data file. The browser loads only HTML, CSS, JavaScript, and the local image;
   no JavaScript networking API is needed.

Architecture selects plain HTML5, one CSS file, ES2020 JavaScript modules, and
ships standard-library-only Python verifier source and dependency-free Node
test source, first executed at Gate C. There is no compilation or
transformation step. The content module is committed source, not generated at
deploy time.

Every shipped JavaScript module and every Node test uses the unambiguous `.mjs`
extension. Every import specifier is a literal relative `.mjs` path. HTML entry
scripts use `type="module"`. Node therefore applies ES-module semantics without
`package.json`, a package `type`, an experimental flag, or ambient configuration.
Gate C-PREP binds the exact accepted Node runtime and startup policy before
any Implementation-authored module executes. The
Node tests do not use the `node --test` CLI. Seven test modules export
side-effect-free `runTests()` functions; `tests/test_interview.mjs` imports and
invokes them in the fixed V4 Section 6 order and then runs its own assertions in
the same direct Node process. This avoids the CLI test runner's default child-
process isolation and its version-dependent isolation flags. No package manifest is
created. A later local/browser capability gate must separately prove that the
selected local server and host serve `.mjs` as a JavaScript MIME type before
claiming browser support.

Hosting is deliberately not selected in this plan. Cloudflare Pages and
Netlify remain candidates. Transport headers, DNS, staging, rollback, and
production are Gate H/D work after a separately reviewed hosting inventory and
owner decision. Application-flow parity under a Gate-C-PREP-reviewed local server is Gate C
scope; TLS, redirects, response headers, caching, compression, MIME overrides,
and host logs are explicitly not locally identical.

## PC-6. Exact runtime resource and egress policy

The site has no runtime networking JavaScript. `content.v1.mjs` is ASCII LF,
has one terminal LF, and exports one frozen object named `CONTENT_V1` with
exactly these keys in this source order: `highStakesTermsBase64`,
`interviewBase64`, `promptTemplateBase64`, `releaseBase64`, and
`secretPatternsBase64`. Each value is one literal canonical RFC 4648 base64
string: padding is present exactly when RFC 4648 requires it, and no whitespace
or alternate alphabet is allowed. The values bind the exact bytes of the five
`site/data/*` source files. Gate X independently strict-base64 decodes each export with trusted read-only
tools and requires byte-for-byte equality with the source file. The inert
`concierge_test_content_binding.py` source expresses the same oracle and is
first executed at Gate C. Application code imports the module and decodes it in memory. It never
calls `fetch`.

In the defined clean, extension-free page-load trace, before the tester
activates any navigation link, the site-controlled request graph is the initial
navigation and the following same-origin static subresources referenced by
literal relative paths:

- `assets/styles.css`;
- the listed JavaScript modules reachable from `assets/app.mjs` or
  `assets/concierge.mjs` by literal relative import;
- `assets/yakherd2.png` on pages that display it.

Activation of a literal same-origin navigation link or one of the three static
external links is an intentional user navigation outside that load trace; it
may request that fixed destination and never incorporates user text. The
acceptance record must not relabel such a navigation, browser/platform traffic,
or an extension request as a site-code background request.

The interactive run begins only after all modules and embedded content bytes
are synchronously available and validated. From that ready state through ZIP
download, site application code intentionally initiates no request. User-agent,
extension, security-product, captive-portal, DNS, operating-system, and other
platform traffic is outside site control and is not described as absent.
Download uses a same-document
Blob URL created from locally computed bytes, immediately removes the anchor,
and revokes the Blob URL in a queued cleanup after the click. The user is told
that the downloaded file leaves browser-managed page memory and is controlled
by the browser and operating system.

An initially considered meta CSP was:

```text
default-src 'none'; base-uri 'none'; connect-src 'none'; font-src 'none'; form-action 'none'; img-src 'self' blob:; manifest-src 'none'; media-src 'none'; object-src 'none'; script-src 'self'; style-src 'self'; worker-src 'none'
```

That policy is rejected because this plan does not require a locally generated
image preview. Implementation must omit `blob:` from `img-src` and use
`img-src 'self'`; Blob downloads are navigation/download objects and do not
require `img-src`. The exact required meta CSP on every HTML page is:

```text
default-src 'none'; base-uri 'none'; connect-src 'none'; font-src 'none'; form-action 'none'; img-src 'self'; manifest-src 'none'; media-src 'none'; object-src 'none'; script-src 'self'; style-src 'self'; worker-src 'none'
```

The later host response adds `frame-ancestors 'none'`; the meta policy must not
claim to enforce it. Later response headers also add `X-Content-Type-Options:
nosniff`, `Referrer-Policy: no-referrer`, and the selected HTTPS policy.

No HTML form element is used. All controls are buttons, inputs, textareas,
selects, fieldsets, and ordinary links. Exact external navigation allowlist:

- `https://github.com/gigajeff/Yakherd`
- the Gate R GitHub `v1.2.0` release URL;
- the Gate R PyPI `1.2.0` URL.

External links are static literals, are never constructed from user data, use
`target="_blank"`, and use `rel="noopener noreferrer external"`. The Concierge
run screen contains no external link between the first answer and the download
result; help opens as same-origin page navigation only after an explicit user
action and warns that navigation may lose memory-only state.

Because informational pages must work without JavaScript,
`site/next-steps.html` contains the literal Gate R tag, commit, artifact names,
lengths, hashes, URLs, and commands. Gate X extracts those fixed text and anchor values with trusted read-only tools,
requires equality with `yakherd_release.v1.json`, and requires the home GitHub
anchor to equal the allowlist. No runtime code
sets or changes an external `href`.

All JavaScript source must be UTF-8 LF, ASCII except literal UI content imported
from the bound data module, and must use only literal relative imports. Dynamic
`import()`, import maps, inline scripts, inline event handlers, source maps,
`eval`, `Function`, string timers, HTML parser sinks, prototype mutation, and
computed access to browser-global capabilities are forbidden.

The verifier fails on any source occurrence or encoded equivalent of:

- `fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource`, `sendBeacon`,
  `RTCPeerConnection`, `WebTransport`, `importScripts`, `Worker`,
  `SharedWorker`, `serviceWorker`, `navigator.share`, `window.open`,
  `location.assign`, `location.replace`, `document.write`, `innerHTML`,
  `outerHTML`, or `insertAdjacentHTML`;
- `http:`, `https:`, protocol-relative URLs, `data:`, or remote schemes outside
  the three exact static anchor literals and the identical Gate R GitHub/PyPI
  values in `yakherd_release.v1.json`; the verifier strictly decodes every
  `content.v1.mjs` base64 export and applies the same rule to those bound bytes;
- HTML `form`, `iframe`, `object`, `embed`, `audio`, `video`, `source`, `track`,
  `portal`, `base`, `meta http-equiv="refresh"`, preload, prefetch, prerender,
  modulepreload, or service-worker registration;
- CSS backslash, `url(`, `image-set`, `src:`, `expression`, or `behavior`.
  The only permitted at-rules are the literal media queries
  `@media (prefers-reduced-motion: reduce)` and
  `@media (forced-colors: active)`; `@import`, `@font-face`, `@supports`,
  `@keyframes`, and every other at-rule fail.

The verifier is a conservative source tripwire, not proof of arbitrary
JavaScript or browser behavior. Gate S is an offline, read-only, exact-byte
source/security/parser/evidence review. Gate S does not launch a browser,
start an HTTP server, create a browser profile, intercept traffic, inspect a
network log, or receive browser, loopback-network, OS-matrix, or accessibility
authority.

Gate C, and only Gate C, owns runtime browser request interception. Gate C
remains parked until its exact Gate-C-PREP plan receives fresh independent
PASS. Gate S then reviews the unchanged source and complete Gate C evidence;
Gate T follows Gate S. The Gate-C-PREP plan must bind the exact browser names
and versions, temporary clean profile locations and lifecycle,
extension-disabled state, cache/storage initial state, local-server argv and
document URL, permitted loopback boundary, interception mechanism, evidence
paths, initiator classification, cleanup, and failure behavior before any
browser or server is started. The public copy says the design and CSP prevent the site code from
intentionally transmitting entered text; it does not claim that a test or
browser can mathematically prove all platform behavior.

Safe user-text sinks are exactly textarea/input `.value` and ordinary node
`.textContent`. User text never enters HTML, an attribute, a URL, CSS, a log,
an exception message, a filename, a test artifact, or evidence. Console calls
are forbidden in production source. Error UI uses fixed error codes and fixed
copy only.

The one runtime attribute exception is the ephemeral download anchor: `href`
receives an opaque browser-created Blob URL and `download` receives the fixed
prefix plus prompt-hash prefix from PC-11. Neither attribute contains
prompt text. The Blob itself intentionally contains the locally computed ZIP,
as disclosed to the user.

## PC-7. Exact interview and prompt assembly

`interview.v1.json` is canonical UTF-8 JSON with LF and one terminal LF. It has
schema `yakherd-interview-v1`, question count 11, and this fixed order:

1. `product_summary`: "What are you hoping to make?"
2. `audience`: "Who is it for?"
3. `core_actions`: "What are the three to seven most important things a user should be able to do?"
4. `data_stored`: "What information will it store, read, or change?"
5. `platforms`: "Where should it run?"
6. `hard_constraints`: "What rules, tools, budget, deadline, or technical limits are non-negotiable?"
7. `non_goals`: "What should this first version deliberately not do?"
8. `success_criteria`: "How will you know the first version works?"
9. `assumptions`: "What assumptions are you making? Leave blank if none."
10. `risks_open_questions`: "What worries you, and what is still undecided?"
11. `high_stakes`: "Could failure affect health, legal rights, money, physical safety, or essential services?"

The top-level object has exactly `questions`, `schema_version`, and `tree_id`;
their values are the question array, integer `1`, and string
`yakherd-interview-v1`. Each of questions 1-10 has exactly `answer_kind` =
`multiline`, `id`, `label`, `max_utf8_bytes` = `8000`, and `unknown_value` =
`UNKNOWN`. Question 11 has exactly `answer_kind` = `choice`, `choices` =
`["YES","NO","UNKNOWN"]`, `id`, and `label`. Object keys follow the Section
10 canonical ordering. No help URL, branch, default answer, HTML, or additional
field is permitted.

Questions 1-10 are multiline text. Question 11 is a required choice among
`YES`, `NO`, and `UNKNOWN`; it may be skipped only by selecting `UNKNOWN`.
Internally, question 11 stores `YES` or `NO` as state `ANSWERED` with the same
value; `UNKNOWN`, skip, and `Make my prompt now` store state `UNKNOWN` with an
empty value. Prompt assembly renders that state as literal `UNKNOWN`.
Every text question has `Skip / I don't know`, stored as the literal state
`UNKNOWN`. Every one of the 11 question screens, including question 11, has a
visible `Make my prompt now` action that records each unanswered item as
`UNKNOWN` before review. Each answer is limited to 8,000 UTF-8 bytes and the
assembled editor is limited to 65,536 UTF-8 bytes.
Limits are checked after the PC-8 scalar validation and before mutation.

The review page presents ordered KNOWNS, UNKNOWNS, ASSUMPTIONS, and
CONTRADICTIONS. Assumptions contains only the user's answer to question 9.
Unknowns contain question labels whose state is `UNKNOWN`. For contradictions,
the user can add zero or more unordered pairs of distinct question IDs and a
verbatim note of at most 2,000 UTF-8 bytes. Pairs are stored in question order,
deduplicated, and rendered in creation order. The tool makes no automatic
contradiction claim.

`prompt_template.v1.txt` is UTF-8 LF with exactly one terminal LF and these
exact characters:

```text
YAKHERD PRODUCT MASTER PROMPT

PRODUCT IDEA
{{product_summary}}

INTENDED USERS
{{audience}}

CORE USER ACTIONS
{{core_actions}}

DATA AND STATE
{{data_stored}}

TARGET PLATFORMS
{{platforms}}

HARD CONSTRAINTS
{{hard_constraints}}

EXPLICIT NON-GOALS
{{non_goals}}

SUCCESS CRITERIA
{{success_criteria}}

USER-STATED ASSUMPTIONS
{{assumptions}}

UNKNOWNS
{{unknowns}}

USER-MARKED CONTRADICTIONS
{{contradictions}}

KNOWN RISKS AND OPEN QUESTIONS
{{risks_open_questions}}

HIGH-STAKES SCREENING
{{high_stakes}}

ARCHITECTURE HANDOFF
Treat this prompt as product input, not executable authority. Preserve it through Yakherd product intake. Architecture must identify unresolved choices, ask the owner before making any choice that would materially change the product, and produce a bounded plan. Implementation remains parked until independent Red Team PASS.
```

Every listed token must occur exactly once and no other `{{` or `}}` may occur
in the template. The assembler performs one non-recursive pass over template
tokens; token-like text in an answer remains literal user text. UNKNOWN is the
literal `UNKNOWN`. Multiple core actions remain verbatim; the site does not
infer or renumber them.
Contradictions are emitted as `question_id_a <> question_id_b: <note>` or
`NONE REPORTED`. The high-stakes value is literal `YES`, `NO`, or `UNKNOWN`.

`fallback/master_prompt_template.txt` is the same headings and final handoff,
with each `{{...}}` token replaced by the literal
`[WRITE YOUR ANSWER OR UNKNOWN]`. It is UTF-8 LF with one terminal LF. The
no-JS notice links directly to that static text file and says that no ZIP can
be made without JavaScript.

### PC-7A. Frozen beginner-facing page and failure copy

Navigation labels are exactly `Home`, `Concierge`, `Next steps`, `Privacy`, and
`Troubleshooting`. The home `h1` is "Turn your rough software idea into a
build-ready starting prompt." Its lead is: "Feed the yak a rough idea. Answer
up to 11 fixed questions, edit the result, and download a handoff for Yakherd
v1.2.0." The privacy line is: "No account and no AI call. The site code does
not intentionally send what you type over the network. Your host, browser,
device, clipboard, and downloaded files have separate privacy boundaries."
The primary CTA is exactly `Feed the yak your idea`; secondary links are
`How it works` and `View Yakherd on GitHub`. The mascot caption is "Idea in.
Prompt bundle out." It does not animate approval, code execution, or shipping.

The Concierge page and download result show this directive-required disclaimer
verbatim:

```text
This tool creates a starting prompt and a handoff file. It does not install Yakherd, run any code, or approve anything. Your Yakherd project's Architecture and Red Team roles still review everything.
```

Before any input control is enabled, Concierge requires
`window.isSecureContext === true`, `globalThis.crypto` to exist, and
`typeof globalThis.crypto.subtle?.digest === "function"`. Failure enters a
terminal no-input state; the app does not read stored session text or render an
editor. Exact failure copy: "This browser context cannot make the SHA-256
checks required for a safe bundle. Open yakherd.dev over HTTPS or use localhost
with a current browser. You can still use the plain master-prompt template."
The only actions are same-origin `Troubleshooting` and
`Open the plain template`. `file:` is unsupported even if a particular browser
exposes WebCrypto there. Any digest rejection later revokes approval and stops
copy/download with fixed error code `HASH_UNAVAILABLE`; no fallback hash is
implemented.

The Next steps page begins: "Your ZIP is a handoff, not an installer. Keep it
private if your idea is private." It shows the complete Gate R artifact names,
lengths, hashes, GitHub release URL, and PyPI version URL, then these literal
command templates:

```text
Windows PowerShell
py --version
git --version
py -m pip download --no-deps --only-binary=:all: --dest . "yakherd==1.2.0"
Get-FileHash -Algorithm SHA256 ".\<WHEEL_FILENAME>"
py -m pip install --no-index --no-deps ".\<WHEEL_FILENAME>"
yakherd init --target "C:\dev\my-project" --project-name "my-project" --dry-run
yakherd init --target "C:\dev\my-project" --project-name "my-project"

macOS shell
python3 --version
git --version
python3 -m pip download --no-deps --only-binary=:all: --dest . "yakherd==1.2.0"
shasum -a 256 "./<WHEEL_FILENAME>"
python3 -m pip install --no-index --no-deps "./<WHEEL_FILENAME>"
yakherd init --target "$HOME/dev/my-project" --project-name "my-project" --dry-run
yakherd init --target "$HOME/dev/my-project" --project-name "my-project"

Linux shell
python3 --version
git --version
python3 -m pip download --no-deps --only-binary=:all: --dest . "yakherd==1.2.0"
sha256sum "./<WHEEL_FILENAME>"
python3 -m pip install --no-index --no-deps "./<WHEEL_FILENAME>"
yakherd init --target "$HOME/dev/my-project" --project-name "my-project" --dry-run
yakherd init --target "$HOME/dev/my-project" --project-name "my-project"
```

At Gate R, `<WHEEL_FILENAME>` is replaced by the one literal reviewed wheel
filename; no angle-bracket placeholder ships. Adjacent copy says: "Compare the
printed SHA-256 with the wheel SHA-256 shown above. Stop if any character
differs. Then replace the example project path and name with your own.
Use a folder that does not exist or is empty. Read the dry-run result before
running the final command. Do not point fresh install at an existing project."
It then gives the exact seven numbered `OPEN_IN_CODEX.txt` steps from Section
9. It never says the site ran a command or created a repository.

The Privacy page uses the exact six boundary bullets in PC-13 and this
heading: "The site code does not intentionally send your idea. Copy, save,
download, browser, and device behavior have separate boundaries." It avoids
the absolute words "anonymous", "never retained", and
"nothing leaves the browser". The optional-save panel uses the exact storage
success/failure language in PC-13.

The Troubleshooting page contains these fixed problem headings and actions:

- `JavaScript is off`: use the plain template; ZIP creation is unavailable.
- `Secure hashing is unavailable`: use HTTPS or localhost in a current browser;
  do not proceed from `file:` or an insecure remote origin.
- `The download was blocked`: keep the approved page open, allow this one
  download in browser controls, and retry; the site cannot inspect the browser's
  download folder.
- `Copy did not work`: select the visible text and use the operating system's
  copy command; clipboard history or sync is outside the site's control.
- `Saved data could not be verified or deleted`: manage storage for this site
  in browser settings; the page cannot claim the data is gone.
- `Yakherd did not create all five roles`: return to the installed
  `START_HERE.md`, report the missing role, and do not pretend startup passed.
- `The pinned release is unavailable`: stop; do not install another release or
  use a branch in its place.

The 404 page says: "That page is not in this static release." and provides only
same-origin Home and Concierge links. The post-intake plan must include an
exact copy inventory for every other label, error, help paragraph, button,
link, command, `aria-label`, and live-region announcement before Gate I-W. No
user-facing prose is left to Implementation discretion.

## PC-8. Editor, Unicode, approval, and copy contract

The browser textarea value is the approval domain. Browsers expose a Unicode
string, not user-authored bytes. The UI states that textarea line breaks are LF
before approval. The site rejects any carriage return code point and any
unpaired UTF-16 surrogate. It performs no Unicode normalization. It encodes the
accepted scalar string with `TextEncoder` UTF-8, without BOM. Those exact bytes
are the approved prompt bytes. Empty prompt and prompt over 65,536 UTF-8 bytes
are rejected.

The site also rejects a prompt containing either exact delimiter as a complete
LF-delimited line:

- `MASTER PROMPT START`
- `MASTER PROMPT END`

This closes the v1.2.0 intake collision. Substrings that are not complete lines
are allowed.

Approval is one reducer transition. It requires the native checkbox to be
currently checked and the exact fixed statement visible:

```text
I wrote or reviewed this prompt and I approve this exact text.
```

The transition validates the string, captures the string, UTF-8 bytes, byte
length, SHA-256, a complete bundle-input fingerprint, and the checkbox state;
then makes the textarea read-only. The approval record is valid only while all
captured values still compare equal. The Download button re-encodes and
re-hashes immediately before bundle construction and fails closed on mismatch.

Approval first performs the PC-12 secret scan. A clean result continues.
A positive result enters `AWAITING_SECRET_ACK`, remains unapproved, leaves the
editor unlocked, shows the exact spans, and offers Edit (default) or the fixed
acknowledgment. Checking that acknowledgment records it only for the current
prompt SHA-256; the user must press Approve again. Approval then reads the
injected/current clock exactly once, after text, secret, and high-stakes
validation and before committing the transition. It converts that
value to the PC-10 `generated_at`; an invalid clock or conversion failure
leaves the state unapproved. Time passing after approval does not alter the
captured timestamp. The snapshot retains the exact editor JavaScript string,
an immutable copy of its UTF-8 bytes, and this canonical fingerprint object:

```text
approval_statement
checkbox_checked
editor_bytes
editor_sha256
generated_at
high_stakes_acknowledged
high_stakes_flagged
initial_draft_sha256
prompt_edited_by_user
release_pin_sha256
secret_acknowledged
secret_flagged
secret_scan_sha256
tool_version
yakherd_target_release
```

`checkbox_checked` is literal true. `editor_bytes` is the integer UTF-8 byte
count from 1 through 65,536. `initial_draft_sha256` is SHA-256 over the initial
draft encoded under the same PC-8 scalar/no-normalization/UTF-8 rules.
`secret_flagged` is the scan boolean;
`secret_acknowledged` is true exactly when flagged and the fixed acknowledgment
was checked for the same prompt hash, otherwise false. `secret_scan_sha256`
binds a PC-10 canonical JSON object with exactly `matches`,
`prompt_sha256`, and `schema_version` = 1. `matches` is an array in merged-range
order; each row has exactly `detector_ids`, `end_utf16`, and `start_utf16`.
Offsets are nonnegative integers, end is greater than start, and detector IDs
are unique in the PC-12 detector order. A clean result has `matches: []`.
Matched text and display labels are not retained in this object. The canonical
bytes have one terminal LF. All hashes are 64 lowercase hex.
`release_pin_sha256` binds the exact canonical
`yakherd_release.v1.json` bytes. At download, the reducer reconstructs this
object from current state while retaining only the captured `generated_at`,
serializes it under PC-10, reruns both scans, and requires exact byte
equality with the captured fingerprint plus exact editor-string/UTF-8-byte
equality. There is no object-identity shortcut.

Every transition that can alter editor text, answers, contradictions,
high-stakes state, acknowledgment, release pin, restored
state, or tool version revokes approval first, clears the checkbox, clears the
snapshot, and disables download. The only route back to editing is an explicit
`Edit prompt` action that revokes approval before removing read-only state.
Checkbox deselection also revokes approval. Program code cannot assign the
editor value outside the reducer/render module. Tests invoke the shipped event
handlers and reducer, not replicas.

Once approval commits, the approval, secret, and high-stakes checkboxes are
disabled. `Edit prompt` is the only route that re-enables them, and it revokes
the snapshot before doing so.

Copy actions are native user actions with this exact disclosure adjacent:
"Copying places this text on your device clipboard. Yakherd Concierge cannot
erase clipboard history or synced clipboard copies." A failed Clipboard API
write is reported without claiming success; the visible textarea remains
selectable for manual copy. Copy never creates approval. Download requires a
valid approval snapshot.

## PC-9. Exact v1.2.0 handoff and bundle file bytes

`site/data/yakherd_release.v1.json` is incomplete and Gate I-W must not begin
until Gate R has supplied every exact public value listed by Gate R in V4 Section 4. It is a
canonical object with keys:

```text
engine_commit
github_release_url
manifest_bytes
manifest_sha256
package_readme_bytes
package_readme_sha256
product_intake_bytes
product_intake_sha256
pypi_version_url
release_json_bytes
release_json_sha256
root_readme_bytes
root_readme_sha256
sdist_bytes
sdist_filename
sdist_sha256
sdist_url
start_here_bytes
start_here_sha256
tag
version
wheel_bytes
wheel_filename
wheel_sha256
wheel_url
```

The fixed `tag` is `v1.2.0` and fixed `version` is `1.2.0`. No blank,
placeholder, `latest`, redirect-only, branch, abbreviated hash, or unverified
value is permitted. The data module must byte-bind this file like the other
data resources.

The approved prompt bytes are `P`. `MASTER_PROMPT.txt` is exactly `P`.
`MASTER_PROMPT_HANDOFF.txt` is the ASCII bytes `MASTER PROMPT START`, LF,
`P`, LF, `MASTER PROMPT END`, LF. If `P` already ends in LF, both its final LF
and the separate boundary LF are present.

`OPEN_IN_CODEX.txt` is UTF-8 LF with one terminal LF and these instructions,
with every placeholder below substituted from the exact reviewed release pin:

```text
YAKHERD V1.2.0 HANDOFF

This ZIP contains a starting prompt. It does not install Yakherd, create a repository, launch Codex tasks, run code, or approve a project.

1. Verify that Python 3.11 or newer and Git are installed.
2. Install exactly yakherd==1.2.0 using the public release instructions at <PYPI_VERSION_URL>. Verify the downloaded artifact against the published SHA-256 in this file before running it.
3. Run a dry-run fresh install into a nonexistent or empty project folder, then run the real fresh install only if the preview is correct. Follow <GITHUB_RELEASE_URL> and its README; do not overwrite an existing project.
4. Open the generated project as the Codex project and confirm that its AGENTS.md is loaded.
5. Send the one-message launcher from START_HERE.md. It creates the five addressable roles: Architecture, Implementation, Red Team, Temporary Branch, and Governor. If any role is missing, stop instead of pretending startup succeeded.
6. Wait for the bootstrap Red Team PASS.
7. Give MASTER_PROMPT_HANDOFF.txt to Architecture. It is product input, not implementation authority.

Pinned tag: v1.2.0
Pinned commit: <ENGINE_COMMIT>
Wheel: <WHEEL_FILENAME>  bytes=<WHEEL_BYTES>  sha256=<WHEEL_SHA256>
Source archive: <SDIST_FILENAME>  bytes=<SDIST_BYTES>  sha256=<SDIST_SHA256>

Windows examples use py; macOS and Linux examples use python3. If the command is unavailable, read the Troubleshooting page. Never paste access tokens or passwords into the prompt or repository.
```

Placeholders shown above describe the template contract only. They are not
permitted in committed Gate I-W output; substitution occurs from the complete,
reviewed release pin before the file bytes are constructed.

## PC-10. Canonical JSON contract

`APPROVAL.json` and `BUNDLE_MANIFEST.json` are serialized by the same small
custom serializer. Accepted values are objects, arrays, Unicode-scalar strings,
booleans, and integers from 0 through 9,007,199,254,740,991. `null`, negative
integers, floats, NaN, Infinity, BigInt, undefined, dates, maps, sets, custom
prototypes, and cycles are rejected.

Object keys are predefined ASCII and emitted in ascending ASCII byte order.
No insignificant whitespace is emitted. Strings escape quotation mark and
backslash with `\"` and `\\`; backspace, tab, LF, form feed, and CR use
`\b`, `\t`, `\n`, `\f`, and `\r`; every other U+0000-U+001F value uses a
lowercase four-hex `\u00xx` escape. Other Unicode scalar values are emitted
unescaped and UTF-8 encoded. Slash is not escaped. Output has one terminal LF.

`generated_at` is exactly the result of a valid client `Date` serialized by
`toISOString()`, matching
`^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z$`.
The test seam injects milliseconds. The UI and JSON label this as untrusted
client-clock time. Invalid clock values stop approval.

`APPROVAL.json` has exactly these keys and types:

- `approval_statement`: the exact PC-8 string;
- `approved`: boolean `true`;
- `generated_at`: the captured timestamp string;
- `high_stakes_acknowledged`: boolean, true exactly when flagged and the fixed
  acknowledgment was checked, otherwise false;
- `high_stakes_flagged`: boolean from PC-12;
- `prompt_bytes`: integer from 1 through 65,536;
- `prompt_edited_by_user`: boolean, true only if the approved editor string
  differs from the initial mechanically assembled draft by exact JavaScript
  string comparison;
- `prompt_sha256`: 64 lowercase hex characters over `MASTER_PROMPT.txt`;
- `schema_version`: integer `1`;
- `timestamp_source`: string `client`;
- `tool`: string `yakherd-concierge`;
- `tool_version`: string `1.0.0`;
- `yakherd_target_release`: string `v1.2.0`.

No other field is permitted. The serializer sorts them; the order above is
descriptive, not a second serialization order.

`BUNDLE_MANIFEST.json` has exactly `bundle_schema_version`, `files`, and
`yakherd_target_release`. Schema version is `1`. `files` lists the other four
files, not the manifest itself, in this fixed order:

1. `MASTER_PROMPT.txt`
2. `MASTER_PROMPT_HANDOFF.txt`
3. `APPROVAL.json`
4. `OPEN_IN_CODEX.txt`

`bundle_schema_version` is integer 1 and `yakherd_target_release` is string
`v1.2.0`. Each entry has exactly `bytes` (integer 0 through 262,144), `path`
(one of the four literal ASCII names), and `sha256` (64 lowercase hex). The
manifest serializer still sorts each object's keys; array order remains fixed.

## PC-11. Exact ZIP32 Store-only contract

The archive contains exactly the five directive filenames in fixed order, with
`BUNDLE_MANIFEST.json` fourth and `OPEN_IN_CODEX.txt` fifth. Names are literal
ASCII but the UTF-8 flag is set. Each entry is Store-only and its bytes are the
bytes defined above.

All integers are little-endian. Local header values:

- signature `0x04034b50`;
- version needed `20`;
- general-purpose flags `0x0800` only;
- compression method `0`;
- DOS time `0x0000` and DOS date `0x0021` (1980-01-01 00:00:00);
- IEEE CRC-32, compressed size, and uncompressed size in the header;
- filename byte length and filename bytes;
- extra-field length `0`; no data descriptor.

Central header values:

- signature `0x02014b50`;
- version made by `0x0314` (Unix, ZIP 2.0);
- version needed, flags, method, time, date, CRC, sizes, name length, and name
  bytes identical to the local values;
- extra length `0`, comment length `0`, disk start `0`, internal attributes
  `0`, external attributes `0x81a40000` (regular file mode 0644), and the exact
  local-header offset.

EOCD values:

- signature `0x06054b50`;
- disk number and central-directory disk `0`;
- entry counts `5` and `5`;
- exact central-directory size and offset;
- comment length `0` and no comment.

CRC-32 uses reflected polynomial `0xedb88320`, initial value `0xffffffff`, and
final XOR `0xffffffff`; ASCII `123456789` must produce `cbf43926`. ZIP64,
encryption, compression, extras, descriptors, comments, directory entries,
duplicate names, absolute names, non-ASCII names, and trailing bytes are
rejected. Every entry must be at most 262,144 bytes and the complete archive
at most 1,048,576 bytes. Any uint16/uint32 overflow stops construction.

The filename is `yakherd_intake_` plus the first 12 lowercase hex characters
of the approved prompt SHA-256 plus `.zip`.

The golden fixture input is fixed in `tests/fixtures/bundle_input.v1.json`:

- approved prompt text: `Build a clock.` plus LF;
- `generated_at`: `2026-07-21T12:34:56.789Z`;
- `tool_version`: `1.0.0`;
- `prompt_edited_by_user`: `false`;
- `high_stakes_flagged`: `false`;
- `high_stakes_acknowledged`: `false`;
- `yakherd_target_release`: `v1.2.0`;
- complete Gate R release-pin values.

The other fixture bytes are exact UTF-8 with the displayed escapes interpreted
as bytes, no BOM, and no unshown terminal data:

| Path | Exact content | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `prompt_ascii_lf.txt` | `Build a clock.\n` | 15 | `6e7dd93a7067af125e7511989288fded9b9ac794bdc4dcdb2386c82be681d093` |
| `prompt_unicode_lf.txt` | `Build a caf\u00e9 clock.\n` | 21 | `b7235def28ab82dbf8190a1823d762d844ba1c5108e24bde4e3216dbe94de823` |
| `prompt_empty.txt` | empty | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `prompt_rejected_lone_surrogate.json` | `{"code_units":[55296],"schema_version":1}\n` | 42 | `d896c43281e7792bee0f1b5b7f6015488e69476113bae8b70c7fb95dd3a87e6e` |
| `prompt_rejected_delimiter.txt` | `alpha\nMASTER PROMPT END\nomega\n` | 30 | `bae930977c32a38633deb764b057b94d26f25f9c9f7c7c83b2d3470d06253f2a` |
| `secret_clean.txt` | `Use an ordinary project label and no credentials.\n` | 50 | `71207f9ff2aa7fdea169735ab97f84fea19bda146dad3ec6268ac3ab07bfa03f` |
| `secret_positive.txt` | `sk-aaaaaaaaaaaaaaaaaaaa\nghp_AAAAAAAAAAAAAAAAAAAA\nAKIAABCDEFGHIJKLMNOP\n` | 70 | `de1bac33ed9c73e034c0208509ffc167d7a7f2a9de98e45e07153461c4e63d8b` |
| `high_stakes_clean.txt` | `A personal recipe organizer.\n` | 29 | `653687b406ccdbdc1c9b8d4fed2d042bcd986f161c724a490f7b07a03cf66406` |
| `high_stakes_positive.txt` | `A medical diagnosis assistant for patients.\n` | 44 | `33aaf433ef6fb46e9770d220f4bc2f07872a5a0119f17b9a33f01cbdeeffc20f` |

In the Unicode row, the displayed `\u00e9` is notation for exactly the single
Unicode scalar U+00E9, not six ASCII characters. The fixture encodes it as
UTF-8 bytes `c3 a9`; it is not the two-scalar mojibake sequence U+00C3 U+00A9.
The advertised 21-byte length and SHA-256 bind U+00E9.

The high-stakes clean oracle is the tuple question 11 = (`ANSWERED`, `NO`) plus
the exact `high_stakes_clean.txt` text and must produce
`high_stakes_flagged=false`. The positive oracle uses that same explicit `NO`
plus `high_stakes_positive.txt` and must produce true from the term scan. An
`UNKNOWN`, skipped, or unanswered question 11 must produce true even with the
clean text. Tests assert all three outcomes, including the directive's required
clean no-false-block case.

Because `bundle_input.v1.json` includes public artifact identities that do not
yet exist, the post-intake plan must print that complete canonical file, byte
length, and SHA-256 before Gate I-W. A placeholder fixture is forbidden.

Before the product writer starts, Architecture must use a spec-only reference
construction that shares no source with the browser modules to calculate every
expected entry and ZIP byte. The post-intake plan embeds RFC 4648 base64 of the
complete exact bytes of `bundle_input.v1.json`, all five golden entry files,
the golden ZIP, and `golden_identity.v1.json`, plus each decoded byte length and
SHA-256. Red Team independently decodes and reconstructs the values directly
from PC-9 through PC-11, checks the complete ZIP headers/offsets/CRC/manifest, and
must reproduce every identity in the same combined Gate P review that may authorize Gate I-W.
The reference construction is temporary review work; no generator or package
is placed in the product checkout. The Implementation writer may transcribe
only those reviewed bytes and may not choose or refresh an expected value.

The prompt SHA-256 prefix is fixed as `6e7dd93a7067`; that fixes the golden ZIP
path named in V4 Section 6. `golden_identity.v1.json` is PC-10 canonical JSON
with exactly `bundle_input_bytes`, `bundle_input_sha256`, `entries`,
`schema_version`, `zip_bytes`, `zip_path`, and `zip_sha256`. Schema version is
integer 1. Byte values are nonnegative safe integers. Hashes are 64 lowercase
hex. `zip_path` is the exact V4 Section 6 golden ZIP path. `entries` has five rows
in ZIP order, each with exactly `bytes`, `path`, and `sha256`. It does not hash
itself. The post-intake plan binds the complete identity-file bytes and hash.

Gate X and Gate S statically review the shipped verifier and browser sources
against the frozen oracle without executing them. Their first authorized
execution and byte-for-byte comparison is Gate C.
Neither implementation may import, invoke, or derive expected values from the
other. Tests fail on any difference and never update golden bytes. Gate S
independently checks the frozen oracle and finalized tree before accepting the
parser boundary.

## PC-12. Secret and high-stakes gates

`secret_patterns.v1.json` freezes these ASCII detectors and their display
labels:

- `private_key`, label `Private-key header`:
  `-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----`;
- `openai_like`, label `API-key-shaped text`: `sk-[A-Za-z0-9_-]{20,}`;
- `github_token`, label `GitHub-token-shaped text`:
  `gh[pousr]_[A-Za-z0-9]{20,}`;
- `aws_access_key`, label `AWS-access-key-shaped text`:
  `AKIA[0-9A-Z]{16}`;
- `jwt_like`, label `JWT-shaped text`:
  `eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}`;
- `password_adjacent`, label `Password- or secret-labeled value`,
  ASCII-case-insensitive:
  `(api[_ -]?key|token|password|passwd|secret)[ \t]*[:=][ \t]*[^ \t\r\n]{8,}`;
- `entropy_token`, label `High-entropy token-shaped text`:
  `[A-Za-z0-9_-]{32,}` only when the matched ASCII string contains an
  uppercase letter, lowercase letter, and digit, has at least 16 distinct
  characters, and no one character occupies more than 25 percent of the
  match. This is deliberately described as a token-shape heuristic, not an
  entropy measurement guarantee.

The file is canonical JSON with exactly `detectors` and `schema_version` = 1.
The detector array is in the order above. Regex detector objects have exactly
`flags`, `id`, `kind`, `label`, and `pattern`; `kind` is `regex`, and `flags`
is either the empty string or `i` only as stated above. The entropy detector
has exactly `alphabet`, `id`, `kind` = `entropy_ascii`, `label`,
`max_dominant_percent` = 25, `min_bytes` = 32, `min_unique` = 16, and
`required_classes` = `["upper","lower","digit"]`. The percentage check is
the exact integer inequality `dominant_count * 100 <= length * 25`. Runtime
constructs only the named fixed regular expressions and adds the global scan
flag itself.

Matching runs on the exact editor JavaScript string. Because all patterns are
ASCII, match offsets are UTF-16 code-unit half-open ranges that begin and end
on ASCII code units. Sort by start, then longer match, then detector order;
merge overlaps into one flagged range while retaining all labels. The warning
shows the exact range through `.textContent`, never HTML, and offers Edit
(default) or a separate `Download anyway` checkbox with exact text: "I
understand this may include a secret and still want to download it." Any edit
clears this acknowledgment. The check occurs before approval as specified in
PC-8; after checking, the user presses Approve again, and download later
requires the same prompt hash and scan result. Detectors are best-effort and
never described as proof that text is secret-free.

`high_stakes_terms.v1.json` contains exactly these ASCII lowercase terms:

```text
diagnosis
medical
medicine
patient
prescription
legal advice
lawsuit
contract rights
investment
financial advice
trading
credit decision
life safety
emergency
industrial control
essential service
```

The file is canonical JSON with exactly `schema_version` = 1 and `terms` = the
array above in that order. Blank, duplicate, uppercase, or additional terms
fail content validation.

Matching uses ASCII lowercase and substring search on answers and the editor;
it performs no locale or Unicode normalization. `high_stakes_flagged` is true
unless question 11 is explicitly `ANSWERED` with value `NO`, and is also true
whenever a term matches. Thus `YES`, `UNKNOWN`, skipped, and unanswered states
all fail closed into the acknowledgment gate. A short warning is visible for every
user, even when false: "Software can cause harm. If health, legal rights,
money, physical safety, or essential services are involved, use qualified
human experts." When flagged, the site also says: "Yakherd and its agents are
not suitable for regulated or safety-critical products without qualified human
experts. This bundle does not change that." Download is blocked until a
separate checkbox says: "I understand this prompt needs qualified human review
before anyone relies on the resulting software." Editing or changing answers
clears it.

## PC-13. Honest storage and privacy state machine

Default state is memory-only. Controls use `autocomplete="off"` and
`spellcheck="false"`, but copy states that browsers, extensions, operating
systems, input methods, crash recovery, form restoration, backups, and synced
devices are outside the site's control. The site says: "This page does not
intentionally save your text unless you turn on Save in this browser. Your
browser or device may still restore or retain data. Use Clear this session,
close the tab, and manage downloaded or clipboard copies yourself."

Optional persistence uses `localStorage` only, at the exact origin-scoped key
`yakherd.concierge.v1.session`. IndexedDB, cookies, sessionStorage, Cache API,
URL state, history state, and server state are forbidden. The stored canonical
JSON has exactly these top-level keys and types:

- `answers`: an 11-row array in question order; each row has exactly `id`,
  `state`, and `value`. ID is the fixed question ID, state is `ANSWERED` or
  `UNKNOWN`, and value is a validated scalar string up to 8,000 UTF-8 bytes for
  `ANSWERED` or the empty string for `UNKNOWN`. Zero-length text becomes
  `UNKNOWN`; nonempty whitespace is retained verbatim. For question 11 only,
  an `ANSWERED` value must be exactly `YES` or `NO`; `UNKNOWN` must have an empty
  value. Any other restored combination rejects the entire stored object,
  attempts current-key removal, restores nothing, and flags high stakes until
  the user explicitly answers `NO`.
- `contradictions`: an array of rows with exactly `id_a`, `id_b`, and `note`,
  under the ordering, uniqueness, and 2,000-byte rules in PC-7.
- `current_step`: integer 0-13, where 0-10 are questions, 11 is review, 12 is
  editor, and 13 is approval; the download result is never persisted.
- `editor_text`: validated scalar string, empty before drafting and otherwise
  at most 65,536 UTF-8 bytes.
- `expires_at_ms`: nonnegative safe integer.
- `initial_draft`: validated scalar string, empty before drafting and otherwise
  at most 65,536 UTF-8 bytes.
- `saved_at_ms`: nonnegative safe integer.
- `schema_version`: integer 1.

No additional or missing key, row, ID, or type is accepted. The object uses the
PC-10 canonical serializer and is at most 262,144 UTF-8 bytes. It never
stores a valid approval snapshot or either download-anyway acknowledgment;
restoration always requires fresh approval and acknowledgments.

The same fixed PC-12 secret detectors run before every persistence write
over every answer value, contradiction note, `editor_text`, and
`initial_draft`, with fields scanned separately so boundaries cannot create or
hide a match. A positive result prevents the write, turns Save off, attempts
verified removal of the current key, and says: `Potential secret-shaped text
was not saved by this transition. Continue in memory only. A prior browser copy
may remain unless current-key removal was verified, and other browser or device
copies are outside this page's control.` There is no Save-anyway override.

On initial storage read, schema/size/scalar validation and the same secret scan
occur before any stored user text is rendered or offered for restoration. A
positive result restores nothing, flags high stakes, attempts current-key
removal, and reports only the affected fixed field IDs and UTF-16 ranges, never
the matched text. It says whether current-key absence was observed and repeats
that other platform copies may remain.

Expiry is `saved_at_ms + 604800000`, based on the untrusted client clock.
Expiry is checked on initial read and every state transition. Invalid JSON,
wrong schema, impossible type/range, expired value, or clock rollback before
`saved_at_ms` causes a best-effort `removeItem` and no restoration. Save claims
success only when `setItem`, immediate `getItem`, and exact string comparison
all succeed. Delete claims success only when immediate `getItem` returns
`null`. Quota, security, read, write, or deletion failure uses fixed truthful
copy: data may remain in browser storage; the site cannot verify deletion.
The seven-day value is an application read/use policy, not a browser-retention
upper bound or scheduled deletion. If the page never runs again, the site does
not execute expiry cleanup. Browser restoration, sync, backups, and copies can
retain data longer.

Turning Save on performs one immediate synchronous save. While enabled, every
successful reducer transition that changes a stored field constructs a new
object, captures `saved_at_ms` from `Date.now()`, derives `expires_at_ms` with
checked safe-integer addition, serializes, bounds, writes, reads, and compares
before the UI says: `The current site-storage key was written and read back.
If this page runs after seven days, the site will treat that value as expired
and try to remove it. Your browser, restored sessions, sync, or backups may
retain copies longer.` There is no
timer, debounce, unload handler, or background write. A failed operation turns
autosave off without retry and says: `Save could not be verified. Your current
work is still on this page, and a browser copy may remain.` Turning Save
off or choosing Delete attempts verified removal and says either: `The current
site-storage key is absent on immediate read-back. Browser, restored-session,
synced, or backup copies may remain.` or `The current site-storage key could
not be verified absent; use browser site-data settings. Other browser or device
copies are outside this page's control.`

V1 stores at most one replace-in-place saved session at that sole key. The UI
therefore exposes both directive-required actions: `Delete this saved session`
and `Delete all saved sessions`. In V1 both run the same one-key removal and
immediate-null read-back contract above; neither implies browser-wide deletion.
If future versions add keys or multiple sessions, this equivalence expires and
requires a new reviewed storage schema.

The `storage` event for this exact key from another tab invalidates approval,
stops autosave, and requires an explicit Reload or Keep this tab decision; no
automatic merge occurs. Reload reparses under the same rules. Keep this tab
performs no write until the user explicitly re-enables save.

`Clear this session` revokes approval, clears in-memory state and controls,
attempts and verifies removal of the one key, and reports verified/uncertain
separately. It cannot delete clipboard contents, downloaded files, host logs,
browser history, extensions, backups, or platform restoration state.

The privacy page and adjacent disclosure say, in substance and without broader
claims:

- site application code does not intentionally send typed answers or prompts
  over the network;
- the static host necessarily receives ordinary page/asset requests and may
  retain IP address, user-agent, time, and request metadata under its own
  policy; the site has no client analytics;
- optional save is origin-local browser storage and can fail or be retained by
  the platform;
- copying and downloading are intentional transfers to OS-managed locations;
- handing the file to Codex/Yakherd is a later user action governed by those
  tools, not by this site;
- no account and no site-issued login are used; the word "anonymous" is not
  used as an absolute claim;
- secret and high-stakes checks are local best-effort warnings, not guarantees.

## PC-16. Later acceptance requirements retained from the directive

The following remain required for product completion but are intentionally not
part of Gate I-W or Gate X:

- identical bundle bytes for the fixed fixture in current Chromium, Firefox,
  and WebKit on at least two operating systems;
- Gate C request interception in separately authorized clean, extension-
  disabled temporary profiles. The permitted site-origin graph is the initial
  loopback document navigation and the exact reviewed same-origin static
  subresources. From `interactive-ready` through download, there must be no
  site-code-initiated request. Non-site browser/platform traffic is classified
  separately and cannot be converted into a product claim. Gate S performs no
  part of this runtime check;
- ZIP extraction with default tools on Windows, macOS, and Linux, followed by
  exact hashes;
- a fresh public-artifact `v1.2.0` install and unchanged `product_intake.md`
  bridge preserving prompt length/hash, including terminal LF;
- keyboard-only, 320px reflow, zoom, forced-colors, reduced-motion, and
  qualified screen-reader walkthrough, plus a named automated scanner whose
  installation/capability is separately authorized;
- no-JS and secure-context/insecure-context behavior;
- Gate C proof that the unmodified committed site completes the full
  application flow under `python -m http.server`, serves `.mjs` with an
  executable JavaScript MIME type, and produces the reviewed deterministic
  bundle, while separately recording that TLS, redirects, response headers,
  caching, compression, and logs are not locally production-equivalent;
- post-Gate-C Gate S exact-source security/parser/runtime-evidence Red Team PASS;
- Gate T PASS and successful same-writer promotion of the reviewed result to
  its real owner paths and compact `STATUS.md`, with supersession/staleness and
  Git-absence visibility recorded;
- GitHub, staging, hosting headers, custom error, MIME, caching, compression,
  redirects, public allowlist, rollback, and production evidence;
- staging and production serving the same committed site bytes.

The final Definition of Done is all of the above, including Gate T promotion,
plus an owner-approved public release. A plan PASS, Gate X static-source PASS,
Gate C runtime PASS, or staging PASS is not product completion.

## Appendix B - Effective Release and Intake Gates

### Gate R-PREP - documentation-only release preparation

Gate R-PREP is documentation-only. Architecture may read the current tracked
Yakherd release inputs and read-only Git metadata and may exclusively create,
with no overwrite, this one candidate:

`docs/2026-07-21_yakherd_v1.2.0_release_preparation_plan.md`

Independent Red Team may exclusively create, with no overwrite, this one
review:

`docs/audits/yakherd/2026-07-21_yakherd_v1.2.0_release_preparation_plan_red_team.md`

No other path may change. The candidate must freeze the proposed package and
release write set, source baseline, validation commands, artifact output and
retention paths, artifact inventory/schema, public-name/version expectations,
credential boundary, failure cleanup, publication transaction, rollback, and
fresh final-review boundary. It may describe later actions but cannot perform
them.

A FAIL permits only a new documentation-only candidate and fresh review. A
PASS may authorize only a separately bounded local release-candidate slice
whose exact paths and commands were reviewed. It does not authorize a tag,
push, GitHub release, PyPI upload, public mutation, or publication.

### Gate R - separately reviewed release candidate, final gate, publication, and authentication

This is a separate Yakherd engine release task, not website implementation. It
requires a fresh release candidate, all checks in `docs/RELEASE.md`, an exact
artifact inventory, independent final release review, and explicit publication
authority. Per the owner's model policy, the final release gate uses one Sol
Ultra reviewer; Ultra is not used for preparation.

Gate R cannot begin from Gate A alone. Local candidate preparation requires a
PASS at Gate R-PREP. Publication additionally requires exact completed artifact
identities, one final independent Sol Ultra release PASS, and explicit human
publication authority after those identities are known. Preparation or review
never implies publication.

The release evidence must bind all of the following before Gate B:

- tag `v1.2.0` and its full 40-hex commit;
- GitHub release URL;
- PyPI project-version URL;
- wheel and sdist direct immutable-version URLs, filenames, byte lengths, and
  lowercase SHA-256 values;
- `README.md`, package `README.md`, package `RELEASE.json`, package
  `MANIFEST.json`, installed `START_HERE.md`, and installed
  `docs/prompts/product_intake.md` paths, lengths, and SHA-256 values;
- the exact `yakherd==1.2.0` installation command and its supported Python
  range;
- evidence that a fresh install from each public artifact passes the release
  smoke test;
- public observations from GitHub and PyPI after publication.

The current intended package contract, which Gate R must either preserve or
explicitly supersede in a newly reviewed candidate, is:

- current engine baseline commit:
  `97b470f8342cfba619da8f13bd224b2c6c4e2e2a`;
- root `README.md`: 12,252 bytes, SHA-256
  `3f520ed064dd57da8bee7260bf02502f12ab8c0198d907b849d66a3365367f02`;
- package `README.md`: 4,778 bytes, SHA-256
  `0bda15f2a8c73198ffb62647b67c880d6b33530225df9110faca09be4951354b`;
- `RELEASE.json`: 473 bytes, SHA-256
  `312c10bd906d82d3b17215040196cae93444bd19ae4f3685733f16ea19e6c06b`;
- `MANIFEST.json`: 7,006 bytes, SHA-256
  `ab77d4af2b30edaeb2f4811cf2d659e4271187fd666c52fa896ac0ed6ec3f609`;
- bootstrap SHA-256 from `RELEASE.json`:
  `c41f4f5d11e5eb3bfed9eabfdef7444e28612d124a26101df8bfb3628837a8bb`;
- installed `START_HERE.md`: 3,104 bytes, SHA-256
  `6fea5767314320f646c85a4b48de67f6ce564f5c248baa5ec8896023c421d241`;
- installed `product_intake.md`: 2,614 bytes, SHA-256
  `c1582bcc7918eeb547bcae8d4ceec14cfbe36267ed7313131012b0ba95c32604`.

Gate R writes its evidence only to an exact path named in its separately
reviewed release authorization. This plan supplies no tag, GitHub, PyPI,
credential, network, or publication authority.

### Gate B - create the separate governed project root

Target local root: `L:\dev\yakherd-web`.

This gate requires a separate authorization after Gate R. At entry:

- the literal target must not exist;
- `L:\dev` must resolve to the intended parent;
- the target and every ancestor from `L:\dev` downward must not be a symlink,
  junction, mount point, or other reparse point;
- the operator must record the resolved absolute target and parent;
- no GitHub repository, remote, credential, or network write is authorized;
- no existing path may be overwritten.

The gate creates the directory and performs a fresh `yakherd==1.2.0` install
using the exact public artifact and command bound at Gate R, with project name
`yakherd-web`. It first runs the installer's dry run. It then records the
installation receipt, exact installed path inventory, hashes, and verifier
output. Before the bootstrap prompt may write anything, Gate B freezes a
canonical `gate_b_installed_baseline` in its separately reviewed external
evidence path. It is a PC-10 canonical JSON array plus LF in ASCII
repository-path order, covers every descendant directory and regular file,
excludes the root, and has rows containing exactly `bytes`, `path`, `sha256`,
and `type`. Directories use type `DIRECTORY`, bytes 0, and SHA
`NOT_APPLICABLE`; regular files use type `REGULAR_FILE`, a nonnegative safe-
integer byte count, and 64-lowercase-hex SHA-256. Any reparse point, other type,
duplicate, case-fold collision, or escape fails Gate B. Its evidence separately
binds the exact `JEFF_STRICT_SSOT_INSTALL.json` identity; the receipt hash is
not used as a substitute for the full baseline hash. No site file is written.
The fresh bootstrap Red Team prompt then runs from the new root and must PASS.

The current Implementation task attached to `L:\dev\YAKHERD` is not an
authorized writer for the site. Before Gate I-W, exactly one Implementation task
must be attached to `L:\dev\yakherd-web`, must demonstrate that the installed
`AGENTS.md` is loaded, and must be the sole product writer. No second
Implementation writer may target that checkout.

Git initialization, branch creation, GitHub repository creation, visibility,
remote creation, push, PR, and publication remain parked for their normal
post-bootstrap owner checkpoint. "Separate repository" at Gate B means a
separate future repository root; it does not smuggle Git authority into this
plan.

### Gate P - unchanged product intake in yakherd-web

After the bootstrap PASS, Architecture receives one handoff whose exact bytes
are:

```text
MASTER PROMPT START
<the exact 17,487 bytes identified in Section 1>
MASTER PROMPT END
```

If the selected prompt ends in LF, the envelope contains that LF plus the one
separate LF immediately preceding `MASTER PROMPT END`; the intake parser
removes only the boundary LF and therefore preserves the prompt's terminal LF.

Architecture follows the installed, hash-bound `product_intake.md` without
modification. In the same bounded intake transaction, it creates the raw
prompt and exact provenance, reads them back, records byte length/hash, makes
the explicit `DECISIONS.md` owner-promotion entry and corresponding `SSOT.md`
owner update while retaining that raw input is not executable authority,
updates the affected Architecture-owned paths and compact `STATUS.md` required
by the installed completion contract, and writes a new, standalone post-intake
candidate at
`docs/plans/yakherd_concierge_v1_implementation_plan.md`. That file must bind the installed raw prompt/provenance/owner-decision
identities, actual Gate R release values, bootstrap evidence, exact V4 Sections
5-10, the complete Effective Product Contract in Appendix A, every resolved
fixture identity, canonical bytes/hashes for every data file, the complete
beginner-facing copy inventory in PC-7A, and its own exact write/review
boundaries. Historical V3 Sections 14-15 are expressly excluded.

The post-intake candidate contains complete canonical strict-base64 blocks for
every Gate-P-frozen data and golden file in V4 Section 6, with decoded byte
length and lowercase SHA-256. It contains no executable runner, resolver,
generator, supervisor, command journal, or generated local-evidence block. The
combined Gate P Red Team independently decodes, hashes, and reviews every
frozen byte.

Before Gate P performs its first mutation, Architecture constructs in memory
the canonical `pre_gate_p_manifest`. It covers every descendant directory and
regular file then present below `L:\dev\yakherd-web`; the repository root is
excluded. It is a PC-10 canonical JSON array in ordinal repository-path
order. Each row contains exactly `bytes`, `origin_relation`, `path`, `sha256`,
and `type`.

`type` is exactly `DIRECTORY` or `REGULAR_FILE`. Directories use `bytes: 0` and
`sha256: "NOT_APPLICABLE"`. Regular files use a nonnegative safe-integer byte
length and a 64-lowercase-hex SHA-256. Paths are unique normalized repository-
relative strings. A symlink, junction, reparse point, other filesystem type,
escape, duplicate, or case-fold collision fails Gate P before mutation.

`origin_relation` is exactly one of:

- `GATE_B_INSTALLED_BASELINE`: the row is identical to the complete post-
  install inventory bound by Gate B, including the separately bound identity
  of `JEFF_STRICT_SSOT_INSTALL.json`; or
- `BOOTSTRAP_CREATED`: the row is one of the five
  `docs/run_records/bootstrap_cold_resume_<RUN_ID>_*.json` files or the one
  `docs/reviews/bootstrap_cold_resume_<RUN_ID>.md` file authorized by the
  installed bootstrap prompt.

All six `BOOTSTRAP_CREATED` rows use the same accepted UTC `<RUN_ID>`, are
linked by the bootstrap PASS review, and retain their observed identities. No
directory row is `BOOTSTRAP_CREATED`, because the required parent directories
are part of the installed baseline. The exact delta from the Gate B installed
baseline to `pre_gate_p_manifest` must be those six regular files: no deletion,
replacement, type change, additional path, or other byte change is permitted.

The post-intake candidate embeds the complete canonical
`pre_gate_p_manifest`, its byte length, and its SHA-256. It also embeds a
canonical Gate P after-manifest for the pre-review project tree except the plan
file containing the manifests. The after-manifest uses the same ordering,
path, type, byte, and hash rules, with rows containing exactly `after_bytes`,
`after_sha256`, `after_type`, `baseline_relation`, and `path`.

`baseline_relation` is exactly one of:

- `UNCHANGED_PRE_GATE_P_BASELINE`: the path and identity equal its
  `pre_gate_p_manifest` row;
- `CHANGED_BY_GATE_P`: the path existed in `pre_gate_p_manifest`, is in the
  exact Gate P write set, and has the reviewed after-identity; or
- `CREATED_BY_GATE_P`: the path was absent from `pre_gate_p_manifest`, is in
  the exact Gate P create set, and has the reviewed after-identity.

Rows cover every descendant directory and regular file except the containing
plan and future combined audit. Every `pre_gate_p_manifest` row maps to exactly
one unchanged or changed after-row; every created after-row was absent from the
pre-manifest. An omitted path, unexplained addition, deletion, type change, or
relation mismatch fails Gate P. The plan prints both complete manifest bytes,
lengths, and SHA-256 values.

The containing plan and future audit are excluded only to avoid self-reference
and prediction. Gate I-W receives and validates their independently observed identities before
its first mutation; Gate X independently rebinds them as two
additional pre-existing records. The combined Gate P Red Team independently
reconstructs the pre-manifest from the Gate B installed baseline plus the six
accepted bootstrap artifacts, verifies the complete before/after relation,
and binds both manifest identities.

Every Gate P decision/owner/status byte says that its effect is conditional on
PASS at the one fixed combined-audit path. Therefore no unreviewed post-audit
edit is needed: FAIL leaves a non-authoritative retained candidate requiring a
reviewed recovery plan, while PASS makes the exact already-reviewed promotion
effective. `STATUS.md` points to that fixed predicate instead of predicting a
verdict. Gate I-W accepts the separately bound containing plan and combined audit as the
only post-manifest pre-existing records; no other post-manifest mutation is
accepted.

Architecture then sends the raw prompt hash, provenance, exact owner changes,
SSOT/status/affected-owner diff, extraction path, plan and after-manifest
identities, unresolved questions, and complete diff together to independent
Red Team. That one review covers the full
unchanged-intake transaction and the implementation candidate at
`docs/reviews/yakherd_concierge_v1_implementation_plan_red_team.md`. Neither
review path nor plan path may pre-exist. PASS must confirm that the installed
raw prompt is exactly 17,487 bytes with the Section 1 SHA-256 and that every
intake/owner/plan step conforms to the installed contract. There is no earlier
partial "intake PASS." The current pre-intake plan is a design input to that
work, not the executable authorization. Any substitution is a new Architecture
revision and fresh review.
