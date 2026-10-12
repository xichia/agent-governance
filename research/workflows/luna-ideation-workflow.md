# Luna Ideation Workflow

Bulk ideation and synthesis — a proposed adaptation of the [Luna Workflow](luna-workflow.md).

## Purpose and status

Drafted 2026-10-05 from the owner's request for a bulk ideation and synthesis adaptation. The proposed name preserves the existing Luna spelling and distinguishes this workflow by purpose. Naming remains open to refinement.

Developed through Luna implementation and separate Luna review on 2026-10-05. [Independent recheck](../04_Projects/2026-10-05-luna-ideation-workflow/reviews/review-r02.md) passed after two process gaps were corrected. Validation covered a supplied synthetic pool and edge-case inspection, not a full live ideation trial.

Use the Luna Workflow to implement a defined outcome. Use this adaptation when the useful outcome is a broad set of possibilities, an organised shortlist, and a synthesis that helps the owner choose what to pursue.

## Reusable prompt

Use this prompt as a standalone instruction. Adapt the bracketed fields before starting; if a field is missing, state a reasonable assumption or ask only when the missing information could materially change the exploration.

```text
Use the Luna Ideation Workflow to explore the question below. This is an exploration task: develop and compare possibilities to help the owner choose a direction, rather than implement a predefined outcome.

QUESTION
[What are we exploring?]

AUDIENCE AND CONTEXT
[Who is this for, and what relevant context should shape the ideas?]

HARD CONSTRAINTS
[Requirements every viable candidate must satisfy, such as budget, time, safety, policy, or available resources. Write “none stated” if there are none.]

EVALUATION CRITERIA
[How should viable ideas be compared? Include priorities or weights only if they matter.]

DESIRED OUTPUT
[What decision or next step should the exploration support?]

ROLES AND COORDINATION
- You are the coordinator. You own the brief, decide whether more exploration is useful, organise and evaluate the pool, integrate the results, and report the limits of the work.
- Use Luna contributors for ideation and assign a separate Luna reviewer to the review step when available. Give contributors the same brief and constraints, plus distinct lenses. Keep generation separate from evaluation.
- If delegation or a separate reviewer is unavailable, continue in one model. Say so plainly, perform the stages sequentially, and describe the review as a self-check rather than independent review. Do not imply that agents, parallel work, or independent agreement occurred when they did not. Report independent review as unavailable; a self-check cannot earn an independent-review pass.

BOUNDED DEFAULTS
- Start with 20 ideas in four distinct lenses, up to five ideas per lens. Choose lenses that fit the question; examples include practical improvements, overlooked needs, unconventional approaches, and combinations or adaptations. Change these defaults only when the owner requests it or the brief gives a clear reason.
- Use at most one additional targeted batch of up to eight ideas, and only to address a named coverage gap. Stop after that batch or sooner when the brief's coverage and output needs are met.
- Return up to five shortlist candidates. Five is a ceiling, not a quota: return fewer when fewer candidates meet the constraints and criteria. Do not pad the shortlist with weak, redundant, or infeasible ideas. If none qualify, say so and identify what would need to change.

PROCESS
1. Frame the brief. Separate supplied facts, assumptions, and open questions. Identify hard constraints (pass/fail) separately from evaluation criteria (comparative). If a material ambiguity cannot be responsibly assumed, ask a focused question before generating.
2. Generate the bounded batches. Give every idea a stable ID and record its originating lens and contributor, if any. Keep ideas concise and materially distinct; do not treat wording variations as new ideas.
3. Preserve the raw pool. Cluster related ideas and merge only genuine duplicates. Retain meaningful variants and distinctive outliers. When merging duplicates, keep the original IDs and note which idea is the cluster representative so every later choice remains traceable.
4. Check coverage and evaluate. Name any material gap before using the optional targeted batch. Assess each candidate against the hard constraints and each stated criterion; give concise reasons and mark infeasible candidates with the specific constraint they fail. Distinguish evidence supplied or verified from assumptions, estimates, and model judgement. Do not present scores, confidence, or agreement as evidence. Flag factual claims that need checking, and verify time-sensitive or consequential claims before relying on them in a recommendation.
5. Synthesize. Identify useful themes, tradeoffs, and combinations. Label any candidate created by combining or reframing ideas as “synthesis-created,” give it a new ID, and evaluate it against the same constraints and criteria before considering it for the shortlist. Link each shortlisted candidate to its source ID or IDs and explain why it qualifies.
6. Independent review. Give the separate reviewer the brief, assumptions, hard constraints, criteria, raw pool and provenance, duplicate clusters, candidate evaluations, synthesis-created candidates, and proposed shortlist. Ask them to check coverage against the requested lenses, feasibility against every hard constraint, traceability to source IDs, duplicate and variant treatment, criterion-based reasoning, weak or padded shortlist choices, uncertainty versus evidence, and any consequential factual claims or missed edge cases. Require a concise report listing each finding with severity (material or nonblocking), affected IDs/sections, reason, and a specific proposed correction or rationale. The coordinator must record a disposition for every finding: fixed, accepted as a nonblocking tradeoff with rationale, or unresolved/blocking. Do not classify a correctness, evidence, or hard-constraint failure as an accepted nonblocking tradeoff. A candidate that fails a hard constraint must be removed or explicitly marked infeasible; it cannot remain shortlisted because the finding was accepted.
7. Fix and recheck. For material findings, revise the affected evaluation, candidate, shortlist, or synthesis, preserving IDs and provenance where possible. Send the reviewer the finding, disposition, and changed material for a targeted recheck against that finding; also ask whether the change introduced a related issue. Allow at most two repair/recheck rounds total. If a material finding remains unresolved after round two, report the workflow as incomplete/blocked and name the finding; do not claim a pass. Record accepted nonblocking tradeoffs and why they do not affect correctness, feasibility, or the decision.
8. Stop and report. Stop when the requested output and useful coverage are achieved, or when the batch limit is reached. State any remaining gap or blocker instead of generating filler. Recommend one practical next experiment or decision, without treating the recommendation as an approved commitment. Give a final review status: “pass” only when an independent review occurred and no material findings remain; “pass with accepted nonblocking tradeoffs” only when an independent review occurred and only documented nonblocking findings remain; “incomplete/blocked” when any material finding remains; or “independent review unavailable — self-check only” when no separate reviewer could participate. Never report acceptance of the overall workflow as passed when independent review was required but unavailable or a material correctness/constraint finding remains unresolved.

OUTPUT
- Brief, assumptions, hard constraints, and criteria.
- Raw idea pool with IDs and source lenses/contributors; mark duplicate clusters and retained variants.
- Clustered themes and any coverage gap or targeted batch.
- Shortlist (up to five) with source IDs, constraint check, rationale, tradeoffs, and material uncertainty. If fewer than five qualify, explain why; if none qualify, say so.
- Synthesis, including any synthesis-created candidates and their evaluation.
- Independent review findings, affected IDs/sections, dispositions, any repairs and targeted rechecks, and final review status. If no separate reviewer was available, identify the self-check and mark independent review unavailable.
- Next experiment or decision, plus evidence that still needs verification and any blocker.

Keep ideas, evidence, assumptions, and recommendations visibly distinct. Be concise enough for the owner to compare options, and do not hide weak coverage behind a polished synthesis.
```

## Try it

Copy the reusable prompt into a request and fill in its bracketed fields. For a quick start, use:

```text
Question: [question]
Audience and context: [context]
Hard constraints: [constraints, or “none stated”]
Evaluation criteria: [criteria]
Desired output: [decision or next step]
```

This is a standalone prompt, not an installed skill or a new skill invocation command. Creating this document does not start a delegated workflow run. Repository confirmation rules apply to any resulting external action.

## How to tell whether it worked

- The pool covers the requested angles and contains materially different ideas, not just rewordings.
- The shortlist can be traced to the pool, with reasons tied to the agreed criteria.
- The synthesis preserves important tradeoffs and uncertainty and provides a concrete next experiment or decision.
- A trial run produces the agreed outputs within its batch limit; any extra batch addresses a named gap.

Next action: try the reviewed prompt on a real ideation question and refine the name, batch size, or output structure based on the result. Blocker: none for the developed prompt; a trial requires a topic.
