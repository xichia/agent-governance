# X01 — Grounded acceptance experiment

Work package [T-GOV-013](../../../../records/tasks/T-GOV-013.md), derived from the reviewed [ideation shortlist](../SYNTHESIS.md). Current state: first reviewer finding repaired and 46-case execution complete, awaiting separate recheck; [candidate observations](RESULTS.md) are not final acceptance.

## Research question and comparison

Can explicit trusted input identities, dimensioned inventories and structured copy rules distinguish the known synthetic false-pass patterns from valid exceptions? This is an isolated candidate mechanism, not a replacement for the historical checker or evidence about role productivity. Independent fixtures test both rejection and acceptance; the unchanged historical report supplies the motivation, not a claim that unlike schemas are interchangeable.

The coordinator-supplied manifest is a trust assumption. Verifying an input digest against it establishes byte correspondence; it cannot establish authorship, honest reading, venue availability, authority or truth. Generated exact-copy matching deliberately restricts prose freedom. Claim-status/source metadata is inspectable, but semantic entailment, source retrieval and changes of epistemic status across revisions still need separate checks.

## Estimated one-hour package

| Stage | Estimated package allocation | Output |
|---|---|---|
| Frame contract and acceptance | 10 minutes | Fixed task/interface, protected paths, hypothesis and boundaries |
| Parallel implementation and independent fixtures | 25 minutes | Standard-library validator/docs and adversarial fixture runner |
| Separate fixed-candidate review and corrections | 15 minutes | Evidence-first findings, extra independent probe, dispositions |
| Coordinator verification and checkpoint | 10 minutes | Reproduced outcomes, preservation checks, results and next step |

These allocations estimate a coherent approximately one-hour workload. Parallel work, model speed and tool limits can shorten elapsed time; do not equate estimates with measured effort or wait to fill an hour. At the work limit, preserve incomplete state. No token/cost/queue measurements are available.

## Use after implementation

Run `PYTHONDONTWRITEBYTECODE=1 python research/exploration/2026-10-08/x01/run_cases.py` from the repository root. See [CONTRACT.md](CONTRACT.md) for exact accepted shape and semantics; [RESULTS.md](RESULTS.md) records the actual observations and review limitations.

## Next checkpoint

Continue the current package before opening another. Builder owns validator/contract; independent case author owns cases/runner; coordinator owns this README and results; separate reviewer owns its new review record. No other agent should duplicate these edits. Later X02 service-state completeness, X03 structure comparison and X04 context/memory studies remain separate questions. This package does not establish operational readiness or multi-agent superiority.
