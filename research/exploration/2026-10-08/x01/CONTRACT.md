# X01 handoff validator contract, version 1

`validator.py` implements the bounded offline interface specified by T-GOV-013. It exposes `validate(payload, assignment, inputs) -> list[str]` and `render_copy(title, attendance)`. The validator does not mutate its arguments. Error messages are deterministic for a given input. It accepts JSON-like values and returns errors for malformed shapes or field types rather than treating them as valid.

## Trust boundary and dependencies

`assignment` is the trusted coordinator-supplied manifest. It contains nonempty `assignment_id`, `writer_session`, and `title`, positive integer `attendance`, `dependencies`, and `resources`. `payload` and `inputs` are candidate-controlled. Each dependency is `{path, version, sha256}`; paths are nonempty relative POSIX logical paths with no empty, `.` or `..` component, backslash, absolute prefix, or URI-scheme component (a component beginning with an RFC-style scheme prefix such as `https:`). Versions are positive integers (booleans are rejected); hashes are lowercase 64-character SHA-256 hex strings. A dependency path must be unique.

The handoff receipt list must contain exactly the assignment's dependency paths once each, with matching versions and hashes. Every assigned path must map in `inputs` to actual `bytes`; SHA-256 is calculated over those bytes and compared with the manifest hash. A candidate cannot make substituted bytes acceptable by recomputing only its receipt hash. Extra input keys are ignored. If there are no assigned dependencies, the receipt list must be empty.

This binding establishes only that supplied bytes match the trusted manifest's digest. It cannot establish who authored those bytes, whether the writer actually read them, or whether the assignment or authorization is authentic. `writer_session` is an exact string label check, not an authenticated identity.

## Candidate envelope

The payload has `handoff`, `attendance`, `title`, `states`, `marketing`, and `claims` fields. Handoff `assignment_id` and `writer_session` must match the assignment, and its status must be `ready_for_review`. Payload attendance and title must equal their assignment values. Unknown fields are ignored; this is not an exact-key schema.

Marketing title and attendance must match the assignment. The only supported copy is produced by `render_copy(title, attendance)`, exactly `"{title} welcomes {attendance} adults."` Arbitrary paraphrases are unsupported. In particular, copy saying 180 adults fails if the assigned attendance is 80. This is literal consistency validation, not semantic review of arbitrary prose.

## Resource and interval rules

Each resource entry is keyed by a nonempty resource ID and contains nonnegative integer `inventory_units` and `seats_per_unit`. Its total capacity is their product. Thus 10 units of 8 seats provide 80 seats; the validator never multiplies a total seat count by inventory quantity. One chair per chair unit is represented by `seats_per_unit: 1`.

`states` must be a nonempty list. Every state has a unique nonempty string `id`, integer `start` and `end` defining a nonempty half-open interval `[start,end)`, nonnegative integer `attendees`, and `seating` set to `seated` or `standing`. Booleans are not integers for this schema. Attendance in a state cannot exceed the assigned audience. At every overlapping time span, summed attendance cannot exceed the expected audience. Adjacent intervals do not overlap.

A seated state must name a known `chair_resource`; its attendees count against that resource's capacity. Simultaneously active states using the same resource aggregate against the same inventory. A standing state must set `chair_resource` to null. Explicit standing states are allowed. This checks only modeled attendees and chair capacity; it does not establish complete attendee, staff, service, access, layout, or operational readiness, and does not solve the broader X02 service-planning problem.

## Claims and evidence labels

`claims` may be empty. Each claim has a unique nonempty string `id`, nonempty string `text`, a `status`, and a source value. Allowed statuses are `supplied`, `verified`, `assumption`, and `unresolved`. A `supplied` claim must name a dependency path in the trusted manifest. A `verified` claim must include a nonempty HTTP(S) URL. This checks URL presence and shape only; it does not fetch the URL or establish that the claim is true. `assumption` and `unresolved` claims must retain a nonempty source/label so their stated status remains visible. No status semantically verifies free prose.

## Scope limits

This module is a research prototype, not a production security boundary, sandbox, schema canonicalizer, authenticated receipt system, or proof of authorship or actual reading. It ignores unknown fields, does not parse or validate arbitrary prose, does not verify URL reachability or factual truth, and cannot attest that the trusted assignment itself is correct. Its checks cover only the rules above. Passing validation does not certify that a handoff is safe, complete, authorized, or operationally ready.
