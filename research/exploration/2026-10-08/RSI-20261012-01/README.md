# Recursive repository improvement kit

An offline implementation for improving this repository through small, evidenced changes. It is a **solo-checked prototype awaiting independent review**, not activated governance or a background agent. It uses Python's standard library and has no installation step.

The loop is: **observe a defect → state a hypothesis → freeze checks → make one scoped change → compare → review → retain or stop**. Improvements to the checks themselves use the same loop, retain earlier regression cases, and inherit the original limits. A gain never automatically edits code or grants approval.

## What is implemented

- **Evidence and reuse:** [catalog.json](catalog.json) pins eight existing artifacts by path and SHA-256, with their scope limits. [BACKLOG.json](BACKLOG.json) links concrete gaps to source evidence, expected outcomes and stop rules.
- **Evaluation before advancement:** [improve.py](improve.py) audits references and compares reports from the same frozen suite. Missing rows, changed receipts, incompatible suites and regressions prevent a gain recommendation. A complete gain returns `review_pending`, always with `accepted: false`.
- **Learning and recovery:** [suite.json](suite.json) retains concrete counterexamples. Next-cycle proposals preserve lineage, deadline, cycle cap and used repairs; child suites may add cases but must retain every parent audit case unchanged. A no-gain parent cannot advance through a supplied review label. [findings.json](findings.json) and exact earlier source versions in `history/` preserve this implementation's own errors.

## Run it

From the repository root:

```sh
cd /workspace/agent-governance
rsi_path=research/exploration/2026-10-08/RSI-20261012-01
python -B "$rsi_path/improve.py" audit --root . --registry "$rsi_path/catalog.json"
python -B "$rsi_path/verify.py"
python -B "$rsi_path/reproduce_findings.py"
python -B "$rsi_path/improve.py" assess --root "$rsi_path" --cycle cycle-001/cycle.json
python -B "$rsi_path/improve.py" next-plan --root "$rsi_path" --cycle cycle-001/cycle.json
```

The last command stops at independent review. CLI exit zero means the stated check completed; **it does not mean the change is accepted**. Audit exit1 reports issues; invalid inputs normally exit2. All commands print results and leave repository source untouched; fixture runners use temporary directories. There is no supplied-command execution, paid API, network access or agent dispatch.

To reproduce the two raw suite reports without overwriting saved evidence:

```sh
python -B "$rsi_path/improve.py" run-suite --suite "$rsi_path/suite.json" --method existence_v0
python -B "$rsi_path/improve.py" run-suite --suite "$rsi_path/suite.json" --method bound_v1
```

The baseline is a newly written **synthetic existence-only comparator**, not a historic measurement of the repository. It matches5/11fixed audit outcomes; the candidate matches11/11. Six additional failures are detected and the five previously matched controls stay matched. Twenty primary controls and sixteen additional probes matched in the solo check. These observations establish finite local behavior, not general reliability, efficiency, costs or agent superiority.

## Use the loop for another change

1. Record a concrete observation and source digest in the backlog. Name the decision it affects, expected improvement, permitted files and what would cause a stop. Avoid generating another idea batch.
2. Freeze a meaningful new regression case before implementation. An expanded child suite retains its parent's cases verbatim; run the previous candidate and proposed new method against the same expanded suite. Store raw outputs separately, with suite and producer-source hashes. Historical mistakes are never edited into passes.
3. Assess the byte-bound cycle. Stop on a regression, incomplete evidence, no gain or exhausted bound. A repair increments the inherited counter. Do not open a new root to evade a limit.
4. Obtain an actual distinct fixed-candidate review. The optional `next-plan --review <relative-json-path>` checks a **typed record** with `kind: independent_review`, `verdict: pass`, distinct `reviewer`/`implementer`, and exact `candidate`, `implementation` and `suite` references. Its output is only a proposal. Actual review and authority must be established outside the tool; arbitrary JSON labels are not authentication.
5. Before any permitted next implementation, record fresh ownership, a sourced objective, a unique cycle ID and the proposed inherited limits. Write a new cycle with bound `parent` and `parent_review` pointers. The tool checks ancestry, unchanged regressions and the preceding candidate method. It cannot dispatch work or promote a candidate.

The first example uses three maximum cycles, two total repair rounds, and an October15Perth end boundary. Those are frozen data for this lineage, not permission for three activations. Actual packages remain approximately60minutes including checks and checkpointing. This package used two repairs; none remain for this artifact. The old X01/06 counters and previous source artifacts are unchanged.

## Scope and trust limits

This is a cooperative local tool. Trusted repository root, freeze/oracle and supplied observations still need external review; a writable file, SHA-256 or different label is not proof of authority. Reports can be fabricated before freezing. The reviewer must independently reproduce results and inspect changed source. Fixture author and implementer are the same person in this solo package, so coverage and rubric validity are not independently established.

The audit handles explicitly listed regular files up to2MiB, rejects symlink paths, traversal, unbound/malformed digests and duplicate IDs, and preserves the zero-byte control. Root/process trust, hard links, concurrent tampering, arbitrary Markdown/prose truth and semantic equivalence remain outside its guarantees. Malformed input shapes may produce a nonzero diagnostic failure rather than a complete report; no such failure is acceptance. These limits require scrutiny in the pending review.

No existing policy, uploaded workflow, historical study or old NEXT07 is changed or silently activated. New bug/unknown observations belong in this package's [CHECKPOINT](CHECKPOINT.md) and [NEXT_PACKAGE](NEXT_PACKAGE.md). The owner's “Do it yourself” direction was honored: no subagents or Astra were used; runtime model identity remains unverified.
