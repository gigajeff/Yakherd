# Independent Red Team Review - Yakherd Concierge V1 Bounded Plan V4

Date: 2026-07-22

## Review target and reproduced identity

- path: `docs/2026-07-21_yakherd_concierge_v1_bounded_implementation_plan_v4.md`
- schema: `yakherd-concierge-architecture-plan-v4`
- observed bytes: `103529`
- observed LF-delimited lines: `1986`
- observed SHA-256: `240d775e380d281e8e43e39c24bf66161144d35c55e28cffbbeed3537432eb81`
- text form: strict UTF-8; LF-only; no BOM; exactly one terminal LF; zero trailing-whitespace lines

Every Section 1 input identity independently matched the repository bytes:

1. source directive: 17,487 bytes; 319 lines; SHA-256 `15946d3266e38f4e579c9b35ce3bda7e621006f32cda35ceb5eb03cf53acf12d`;
2. directive audit: 19,030 bytes; 164 lines; SHA-256 `274b6db4bc92fe40bfceee3efe70331814c52235db28d5ba4032ca88e98ca64a`;
3. bounded plan V1: 68,774 bytes; 1,391 lines; SHA-256 `216cea3bd5f262e487329f0fcc757666e52397e6d8e119882862b88739afa029`;
4. V1 plan audit: 16,166 bytes; 150 lines; SHA-256 `34b19607510fdd696904974e2cb56aced148ef2b46838dec72ce6fd5a62a6fda`;
5. bounded plan V2: 103,293 bytes; 1,956 lines; SHA-256 `68f444c46992b0dd31c8b84f328d85b86cc6851e1c3693ca22bc8b44aca2809a`;
6. V2 plan audit: 15,149 bytes; 137 lines; SHA-256 `32b1274e4350ea732b14565d9925fb8c4d9bd61728a60c6f63f039e41676b1ec`;
7. bounded plan V3: 142,347 bytes; 2,589 lines; SHA-256 `d687860db50cb816d899043cee9f3e7825195602a0884fead242b6a92bc28b51`;
8. V3 plan audit: 17,272 bytes; 141 lines; SHA-256 `2ecd834ef7a852d7daf4a55510241f5a60b33a72603b5cb08b62ceebb9d2df12`.

## Prioritized findings

### P0

No P0 finding was identified.

### P1

No P1 finding was identified.

### P2 - The supposedly standalone materialized contract contains three wrong or dangling internal references

V4 states that its Sections 1-10 and appendices are the only normative bytes, that no consumer resolves a V3 section number, and that Appendix A namespaces internal product references as `PC-*` (`candidate:44-63`). Three normative clauses violate that rule:

- the interview schema says its object keys follow "Section 10" (`candidate:951-958`), but V4 Section 10 is the stop/model/authority section; the governing canonical JSON contract is `PC-10` at `candidate:1323-1378`;
- beginner-facing handoff copy incorporates the seven `OPEN_IN_CODEX.txt` steps from "Section 9" (`candidate:1110-1117`), but V4 Section 9 is the fixture/oracle section; the exact seven steps are in `PC-9` at `candidate:1295-1317`;
- `PC-9` says Gate R supplies every exact public value listed by Gate R in "V4 Section 4" (`candidate:1251-1255`), but Section 4 is only a non-authoritative gate summary (`candidate:122-146`); the controlling value list is Appendix B Gate R at `candidate:1785-1799`.

These references force a later consumer to infer the intended clause or choose between a wrong target and the actual controlling text. That is incompatible with the plan's own standalone, exact, and no-competing-interpretation contract.

### P2 - Gate X can accept a syntactically present but ineffective meta CSP

The plan freezes the intended CSP policy string (`candidate:838-855`) and requires each page to have the "exact meta CSP" (`candidate:557-564`). It does not require the concrete element and placement needed for that policy to govern the document: a `<meta http-equiv="Content-Security-Policy" content="...">` inside `<head>` before every controlled resource or executable element.

Under the literal Gate X condition, the policy string can occur in a late or out-of-head meta element and satisfy the stated source presence check even though the browser ignores it or applies it only after earlier content has loaded. Because runtime browser work is deferred until Gate C, Gate X needs an exact structural and ordering check rather than only policy-value equality.

### P2 - The materialized accessibility acceptance contract omits two source-directive requirements

The controlling PC-16 acceptance list requires a qualified screen-reader walkthrough and a named separately authorized automated scanner (`candidate:1723-1725`), but it omits the source directive's explicit automated-scan success threshold of zero AA violations (`directive:281-284`). Merely naming and running a scanner does not define PASS.

The source directive also requires screen-reader announcements for step changes and errors (`directive:258-262`). V4's static accessibility checks cover headings, landmarks, labels, focus, reflow, contrast, and related CSS behavior (`candidate:557-564`), while the copy inventory merely freezes any live-region announcement text (`candidate:1143-1147`). Neither requires an operative live region or equivalent announcement mechanism, nor does PC-16 explicitly test those announcements. Since V4 declares itself the complete standalone controlling contract (`candidate:44-63`), a later Gate C-PREP cannot recover these omitted acceptance requirements by importing the directive.

### P2 - Failure-inventory row ordering is not total for required Unicode-path inputs

The failure schema requires rows for every manifest destination and every other descendant actually observed, ordered as an "ordinal-ASCII path union" (`candidate:303-311`). Its path domain is not ASCII-only: Gate P paths are normalized repository-relative strings and reject escape, type, duplicate, and case-fold defects, but do not reject valid Unicode path scalars (`candidate:1905-1916`). An unexpected Unicode descendant is therefore a required adverse input.

"Ordinal-ASCII" does not define how non-ASCII scalars are ordered. UTF-8 byte order, Unicode scalar order, and Windows/JavaScript UTF-16 code-unit order can disagree. Two otherwise conforming evidence builders can consequently serialize different row orders, or one can be unable to serialize the mandated observed path at all. This leaves the supposedly canonical Gate I-W failure handback and Gate X FAIL bytes underdetermined precisely on an abnormal filesystem state.

### P3

No separate P3 finding was identified.

## V3 regression review

V4 materially closes the six specifically requested V3 regressions:

- no resolver, authenticated dynamic-value carrier, Python runner, command supervisor, or generated run record exists in the V4 construction gate (`candidate:38-42`, `candidate:148-170`);
- the synchronous task-host filesystem primitive must complete or terminate without starting or detaching a child, and unknown mutator liveness parks all later reads and recovery (`candidate:160-170`, `candidate:286-301`), so no target runner can be orphaned;
- no target Python/Node/site code runs before Gate C; Gate I-W is inert byte construction and Gate X is static review (`candidate:148-153`, `candidate:462-470`);
- no `platform.*` runtime observation or capability-matrix promise remains in the pre-execution construction boundary;
- Gate A returns only to Architecture and expressly forbids Implementation contact (`candidate:104-120`);
- no bounded Python-version regex or runner grammar remains in Gate A/I-W/X.

The task-host liveness rule, `PRESENT` plus `UNKNOWN` inventory tuples, null-capable serializer normalization, observable-only transcript limits, source-versus-runtime network claim separation, frozen oracle independence, and first-execution-at-Gate-C boundary otherwise held under adversarial review. These closures do not cure the four P2 findings above.

## Reproduced materialized identities and exact-list checks

- Appendix A: 53,296 bytes; 1,019 LF-delimited lines; SHA-256 `c67c7e87e79522976adec34f1f290820e5139b728043aa655ca81e51e1081e69`.
- Appendix B: 13,108 bytes; 241 LF-delimited lines; SHA-256 `4a6ffa7d44095bd947fb2b6f75f616d9fecd0946822787cc56bc375f72073968`.
- V3 Sections 2-3 fragment: 3,823 bytes; 70 lines; SHA-256 `0ffdea9296d6944f271ac86bd93e4a4e66441ed629ea313f9c1526ccc19afdb2`.
- V3 Gates R-PREP through P fragment: 13,561 bytes; 249 lines; SHA-256 `d18e2aa7de617f50552d13fd9af2de1914615d7634c1645f5df316556da08739`.
- V3 Sections 6-13 fragment: 46,964 bytes; 908 lines; SHA-256 `e7c87d12b68c52233802bba0572184d12de7ee944395da5ef56e6bdd26e434e9`.
- V3 Section 16 fragment: 2,304 bytes; 39 lines; SHA-256 `d1236594488b60832848a5506182bc2c5dbf7cf455703a87a98dda6f8dd29d2a`.
- The exact write set parsed to six unique directories and 60 unique files in the advertised order, with no wildcard or duplicate.
- The Gate X list parsed to 34 unique checks in the advertised order.

All nine fixture preimages independently reproduced their advertised identities:

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

The Unicode fixture contains one U+00E9 scalar encoded as UTF-8 `c3 a9`.

The six current intended package-contract files named by V4 also matched the repository bytes:

- root `README.md`: 12,252 bytes; SHA-256 `3f520e55039fe34224eb40c4dff33dab0f43ab089043f835916931ee42c1df02`;
- package `README.md`: 4,778 bytes; SHA-256 `0bda1535ad5ec018bef7261ab5613294079f809a0871820cb73dab5049f7535b`;
- `RELEASE.json`: 473 bytes; SHA-256 `312c10d35f6c98985e5180589b57d8b37e89f29c6d7bf8a9e32f93a3f0d0206b`;
- `MANIFEST.json`: 7,006 bytes; SHA-256 `ab77d43608e329283324535476385eb05eb3b89d001f03901d13731318ce7609`;
- `START_HERE.md`: 3,104 bytes; SHA-256 `6fea578b3104abf2b61a7feace1ab5a617ef2693090743316710930bf7cf5241`;
- `product_intake.md`: 2,614 bytes; SHA-256 `c1582b88c5edabebd9981716621248011e8259110529a49609bb644ebf8be604`.

## Verdict

**FAIL.** No P0 or P1 was identified, but four P2 findings remain. Under the assignment's zero-P0/P1/P2 PASS rule, the exact V4 candidate is not safe to advance.

## Required revisions

1. Correct the three internal references to their one controlling materialized clauses (`PC-10`, `PC-9`, and Appendix B Gate R), then regenerate and bind every affected V4/appendix identity.
2. Define and statically verify the exact CSP meta element, required attributes, placement inside `<head>`, and ordering before every resource or executable element it governs.
3. Restore the zero-AA-violation scanner threshold and require/test operative screen-reader announcements for step changes and errors, without importing omitted historical text by implication.
4. Define one total path-ordering algorithm over the complete admitted Unicode-scalar path domain, or explicitly close the admitted path domain with fail-closed evidence semantics that remain representable for unexpected non-ASCII descendants.

Red Team has not repaired the plan or selected product bytes.

## Residual risk

After revision, Gate R-PREP and the later final Ultra release gate must still bind the complete public v1.2.0 supply chain. Gates P/X/C/S must independently review the frozen data/oracle bytes, static sources, browser behavior, deterministic cross-browser ZIP output, accessibility, runtime request evidence, and adverse filesystem states. Git, target-repository creation, product intake, Implementation, hosting, staging, DNS, deployment, and publication remain separate gates with no current authority.

## Authority effect

This FAIL authorizes Architecture only to preserve this audit and draft one revised exact Gate A candidate for fresh independent review. It does not authorize Gate R-PREP candidate creation or execution, release/package mutation, Gate R/B/P/I-W/X/C-PREP/C/S/T or any later gate, Implementation contact or work, Git mutation or network Git, browser/network/DreamHost, credentials, dependencies, images, evidence beyond this audit, creation of `L:\dev\yakherd-web`, hosting, DNS, staging, deployment, production, or publication.

The existing Implementation task remains parked and was not contacted.

## Validation and preservation

- `python -B scripts\verify_release.py`: PASS (`release_verification status=passed manifest_files=47 cache_paths=0`).
- `git diff --check`: PASS.
- Candidate and audit non-index UTF-8/LF/BOM/terminal-LF/trailing-whitespace validation: PASS for both files (`git diff --no-index --check` returned the expected difference status `1` with no whitespace error; strict UTF-8, LF-only, no BOM, exactly one terminal LF, and zero trailing-whitespace lines).
- Baseline Git state: branch `main`; HEAD `97b470f8342cfba619da8f13bd224b2c6c4e2e2a`; upstream `origin/main`; ahead/behind `0/0`; staged paths `0`; tracked-diff paths `0`.
- Only this authorized audit path was created. The candidate, every predecessor, package/release bytes, prior records, Git state, release state, product paths, network/browser/DreamHost, credentials, dependencies, images, target repository, hosting/DNS/staging/deployment/production/publication were not changed. `yakherd.mp4` was not read, hashed, inspected, moved, or touched.

autonomous next action: Architecture may preserve this FAIL and draft one revised exact Gate A candidate; Gate R-PREP and all product/release work remain parked.
