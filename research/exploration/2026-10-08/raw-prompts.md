# Raw idea pool — prompt contracts

Generation only; entries are unranked and unevaluated. Ideas respond to the supplied rehearsal findings and remain proposals, not governance changes.

## P01 — Bind handoffs to exact assigned inputs

- **Lens:** Prompt contracts
- **Contributor/model/session:** `/root/ideation_prompts`; configured model `gpt-6-luna`; inherited generic GPT-6 identity; deployment identity unavailable.
- **Idea:** Give each task a compact receipt contract naming the required input paths and versions (or content hashes), required output paths, and an explicit acknowledgement format. The receiving agent must report the identifiers it actually used; integration checks those identifiers against the dispatch record. This addresses the report's observation that current handoff receipts do not bind exact upstream content.
- **Proposed observable test:** In an isolated mock handoff, submit (a) the assigned input bytes and matching receipt, (b) changed upstream bytes with a stale receipt, and (c) a correct hash under the wrong path/session. Record which cases are accepted, rejected, or require a fresh receipt; verify the valid case remains usable.
- **Assumption to verify:** The available execution environment can expose stable path/version or content-hash identifiers at dispatch and integration, and the receipt fields can be checked rather than trusted as free text.

## P02 — Make output schemas and cross-field invariants part of the contract

- **Lens:** Prompt contracts
- **Contributor/model/session:** `/root/ideation_prompts`; configured model `gpt-6-luna`; inherited generic GPT-6 identity; deployment identity unavailable.
- **Idea:** Define role outputs with typed fields, allowed citation categories, and explicit cross-field invariants; make the prompt state the same requirements enforced by validation. In the rehearsal domain, the contract could specify primary versus supporting citations, capacity units versus total inventory, and when chair accounting is required. This joins the written interface to the checker's actual acceptance rules.
- **Proposed observable test:** Run contract examples and deliberately malformed fixtures: wrong citation category, demand above a reduced inventory, omitted required chair accounting, and disagreement between structured attendance and free-text audience claims. Compare validator outcomes with the written contract; valid standing/transition exceptions must have an explicit representation and test fixture.
- **Assumption to verify:** Legitimate exceptions can be represented in a small stable schema without forcing every role into one output shape or rejecting valid scenarios.

## P03 — Label evidence, assumptions, and unresolved questions in every consequential claim

- **Lens:** Prompt contracts
- **Contributor/model/session:** `/root/ideation_prompts`; configured model `gpt-6-luna`; inherited generic GPT-6 identity; deployment identity unavailable.
- **Idea:** Require consequential claims in planning outputs to carry a compact status and basis: supplied/observed evidence, externally verified evidence with source, assumption, or unresolved question. The prompt should prohibit converting an assumption into a resolved fact during handoff or revision. This makes the rehearsal report's evidence/assumption distinction inspectable at the artifact level.
- **Proposed observable test:** Give contributors a fixture containing one supplied value, one unsupported venue assumption, one question, and one claim that requires a primary source. Check whether outputs preserve each status through a revision, cite verification where performed, and leave the unsupported assumption unresolved; inspect for status changes unsupported by new evidence.
- **Assumption to verify:** Contributors can apply a shared status vocabulary consistently across different role outputs, and the added labels make review easier without obscuring the useful prose.

## P04 — Specify readiness gates and what a review pass does not authorize

- **Lens:** Prompt contracts
- **Contributor/model/session:** `/root/ideation_prompts`; configured model `gpt-6-luna`; inherited generic GPT-6 identity; deployment identity unavailable.
- **Idea:** Put explicit decision gates in the task and reviewer contracts, with each gate's evidence and accountable decision owner. Require outputs to distinguish a bounded artifact/rehearsal review pass from readiness for operational use, and to list unmet gates without implying approval. This targets the report's open service/layout question and its warning that a rehearsal pass is not operational acceptance.
- **Proposed observable test:** Prepare paired fictional outputs with identical review findings except that one has an unresolved seating/service question and one has documented evidence against predeclared readiness criteria. Check whether the first is marked not ready or unresolved, whether the second is assessed only against the stated criteria, and whether neither output invents owner approval.
- **Assumption to verify:** The owner can state observable readiness criteria and decision authority for the intended task; otherwise the contract can mark the gate unconfigured but cannot determine readiness.

## P05 — Define delivery and recovery states for missing, late, or failed outputs

- **Lens:** Prompt contracts
- **Contributor/model/session:** `/root/ideation_prompts`; configured model `gpt-6-luna`; inherited generic GPT-6 identity; deployment identity unavailable.
- **Idea:** Give dispatch and response prompts a small delivery-state contract: accepted artifact, explicit no-artifact/startup failure, incomplete response, or timeout/unavailable. State what evidence is required for each state and what the coordinator may do next, including a bounded retry or reassignment only when authorized. A startup failure must not be mistaken for a delivered artifact.
- **Proposed observable test:** Use a controlled mock to produce a valid response, malformed response, explicit startup failure with no artifact, and no response before the declared deadline. Check that each produces the correct recorded state, that no missing output is accepted, and that any retry follows the declared bound and leaves a traceable handoff.
- **Assumption to verify:** The platform exposes enough event information to distinguish startup failure, incomplete delivery, and timeout; where it does not, the contract must preserve the state as unknown rather than infer a cause.
