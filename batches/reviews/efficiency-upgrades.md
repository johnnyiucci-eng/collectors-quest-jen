# Efficiency upgrades — September13,2026

User authorized reducing repeated transcript loading, overlarge diagnostics and unnecessary repeat checks. Implemented `scripts/lore_workbench.py`, tested through its public interface with local filesystem/subprocess stand-ins. The codebase-design skill kept paging, field selection and conservative machine-check reuse behind one small workbench interface. Operating instructions are in [EFFICIENT-PROCESS.md](../EFFICIENT-PROCESS.md).

## Verified behavior

- Whole-window source pagination: CQ215 first page covers cursor0→11, second11→21, with no overlap. Source bytes and NBSPs remain intact. This is a pagination test, not an additional source-read claim.
- SHA-bound resume rejects changed source, even if the manifest hash was updated. Oversized items produce an explicit error rather than truncated evidence. Display is not marked as read or accepted.
- Answer/list views whitelist useful fields. Original wording, qualifications, exclusions and required evidence locations remain visible; recursive source quotes stay on disk. List membership is paged without arbitrary top-ten truncation.
- Real batch016 full answer packet serializes to4,294,550 characters; its five-failure diagnostic view is1,440 characters. This compares a full packet with a narrow diagnostic view, not equivalent evidence completeness or measured subscription savings.
- Real batch015 passed build, structure,50/50 tuned,50/50 original and its24-check acceptance gate. An unchanged second verification returned `reused` without rerunning the commands.
- Real batch016 still fails at57/62 tuned and56/62 original. Failed checks are not cached as success. No ledger was created, no questions or required windows were rewritten, and no binding was renewed.
- Full raw diagnostics are preserved in timestamped generated run folders. Machine-check receipts require exact inputs and generated output hashes; changed code, source, review documents or generated outputs invalidate reuse. A failed build stops downstream work.

## Actual integration issue and correction

Adding guidance directly to the old pilot workflow made nine collections' exact review bindings stale. The archive correctly dropped from52 to21 reviewed episodes. The added paragraphs were removed, restoring the original workflow bytes; the new guidance stays in the separate companion document linked from batches/README. Catalog verification returned52 reviewed episodes, excluding only the unfinished016. No old approval was reissued merely to accommodate an efficiency edit. Pilot80-check validation and batch002's24-check gate passed afterward.

## Verification and limits

The initial full suite passed206/206 tests in65.441seconds, including11 new workbench tests. Final verification after the small list-title display addition passed206/206 in67.779seconds. Final catalog remains52, with only016 excluded; `git diff --check` is clean. All earlier initial batch016 retrieval failures remain unresolved and visible.

No model switch, paid service, API job, publication, private import or persona change occurred. The main remaining cost is full transcript reading and independent semantic review. These improvements remove avoidable context and local reruns; they do not promise a specific allowance reduction or weaken A1–A8. Generated receipts are not security attestations or review approvals.
