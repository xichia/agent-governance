# Research sources

Reviewed 2026-10-04. Institutional research concerns human organisations; applying it to LLM teams is a design analogy. Benchmark studies and vendor accounts do not validate this exact repository architecture. Original books below are foundational references, not claims of full-text examination.

| Source | Supports | Evidence limit |
| --- | --- | --- |
| [Ostrom Workshop: What is Polycentric Governance?](https://www.ostrom.indiana.edu/courses-teaching/teaching-tools/polycentric-goverance/what-is-pg.html) | Multiple decision centres, coordination, and governance beyond a single organisation | Research tradition about human governance; no agent experiment |
| Ostrom (1990), *Governing the Commons*, Cambridge University Press; [Nobel lecture page (2009)](https://www.nobelprize.org/prizes/economic-sciences/2009/ostrom/lecture/) | Boundaries, monitoring, conflict resolution, local rules, and nested institutions | Book is a bibliographic foundation; lecture page identifies the author's synthesis; neither validates an agent recipe |
| [Ostrom (2011), Background on the Institutional Analysis and Development Framework](https://doi.org/10.1111/j.1541-0072.2010.00394.x), *Policy Studies Journal* 39(1), 7–27 | Framework for analysing institutions and action situations | Publisher metadata/abstract checked; not a software implementation |
| Beer (1972), *Brain of the Firm*; (1979), *The Heart of Enterprise*; [Metaphorum's VSM overview and Beer recording](https://metaphorum.org/staffords-work/viable-system-model) | Operations, coordination, internal management/audit, adaptation, policy | Overview/archive checked; conceptual organisational model |
| [Horling & Lesser (2004), A Survey of Multi-Agent Organizational Paradigms](https://mas.cs.umass.edu/Documents/bhorling/horling-paradigms.pdf), *The Knowledge Engineering Review* 19(4), 281–316 | Explicit agent organisations; contingent choice among structures | Author-hosted survey; predates LLM agents |
| [Cemri et al. (2025), Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) | Failure taxonomy: design, inter-agent alignment, verification/termination | Studied frameworks/tasks; not universal failure rates or an ACL study |
| [Anthropic (2025-06-13), How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | Scoped delegation, evaluation, observability, checkpoints, integration costs | Vendor engineering account and internal evaluations; workload-specific |
| [NIST SP 800-207 (2020), Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final) | Least privilege and policy enforcement beyond assumed trust | Security architecture guidance, not evidence of improved agent performance |
| [Git: git-worktree](https://git-scm.com/docs/git-worktree) | Separate working trees sharing repository data | Concurrency tool, not a security boundary |
| [GitHub: About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) and [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) | Review routing, merge gates, stale approvals, bypass limits | Hosting configuration required; CODEOWNERS grants no per-path confidentiality |
| [AGENTS.md specification](https://agents.md/) | Predictable Markdown instruction discovery | Tool support varies; instruction files do not enforce permissions |

Operational documents are the proposed synthesis. Validate outcomes with the comparisons in [foundations](foundations.md), and validate permissions separately in the chosen runtime.
