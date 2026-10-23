# pstack — attribution and adaptation notice

This package contains 16 selectively adapted instructional skills for the Hermes native plugin namespace `pstack`. It is not a complete port of upstream pstack, a replacement operating policy, or an executable safety enforcement layer.

## Source and authorship

- Upstream work: **pstack**, by **Lauren Tan**.
- Reviewed source snapshot: repository `gary3207/plugins`, canonical `pstack/` tree.
- Snapshot commit: `8b3326d99fd4b993cb33a24dad8af03175c642c5`.
- Upstream manifest version at that snapshot: `0.15.30`.
- Public snapshot: https://github.com/gary3207/plugins/tree/8b3326d99fd4b993cb33a24dad8af03175c642c5/pstack
- Upstream license: MIT, copyright (c) 2026 Lauren Tan, reproduced below.
- Adaptation authors: **gary3207, Hermes Agent; adapted from Lauren Tan**.
- Adapted skill version: `0.1.0`; this is distinct from the upstream snapshot version.

The Korean procedures are selective rewrites and consolidations. English identifiers and short catalog descriptions support discovery. Attribution does not imply upstream endorsement or verified behavioral equivalence with upstream tooling.

## Selection map

Paths in this table are relative to the pinned upstream `pstack/` tree. They identify conceptual sources, not runtime dependencies or instructions to load those upstream skills.

| Adapted ID | Selected upstream kernels |
|---|---|
| `evidence` | `skills/why/` and `skills/why/references/epistemics.md`: evidence tiers, behavior versus intent, contradictions and unknowns. |
| `diagnose` | `skills/tdd/`, `skills/principle-attack-the-premise/`, `skills/principle-fix-root-causes/`, and `skills/poteto-mode/playbooks/bug-fix.md`: identical-surface reproduction, proportionate regression checks, premise falsification, diagnosis before patches. |
| `impact` | `skills/blast-radius/`: dynamic callers, serialized and external contracts, lifecycle and dependency-version risks. |
| `design` | `skills/architect/references/design-red-flags.md`, `skills/principle-model-the-domain/`, `skills/principle-minimize-reader-load/`, and selected `skills/typescript-best-practices/` ideas: domain states, ownership, boundary validation, reduced reader load. |
| `reliability` | `skills/principle-make-operations-idempotent/` and `skills/principle-separate-before-serializing-shared-state/`: retry convergence, preserved successful results, explicit ownership and actual serialization. |
| `review` | `skills/interrogate/`: evidence-based Act/Consider/Noted/Dismiss triage, independent review when useful, no automatic application. |
| `verify` | `skills/create-verification-skill/` and `skills/maintain-verification-skill/`: Launch/Doctor/Drive/Evidence/Cleanup; documentation drift versus harness gaps versus product regressions. |
| `measure` | `skills/benchmark-checklist/`, `skills/principle-explain-the-number/`, and `skills/poteto-mode/playbooks/perf-issue.md` and `hillclimb.md`: real work, errors and work volume, fair measurement, uncertainty and the one-run ballpark exception. |
| `evaluate` | `skills/poteto-mode/playbooks/eval.md`: fixed tasks and criteria, anonymous outputs, leakage control, actual behavior rather than self-report. |
| `handoff` | `skills/recall/`, `skills/ketchup/`, `skills/show-me-your-work/`, and `skills/poteto-mode/playbooks/pause-safely.md` and `session-pickup.md`: verified resume capsules and existing-record reuse. |
| `learn` | `skills/reflect/`, `skills/correct/`, and `skills/principle-encode-lessons-in-structure/`: verified repeat lessons and the smallest existing setting, check or procedure that prevents recurrence. |
| `explain` | `skills/teach/`, `skills/technical-writing/`, and selected `skills/how/`, `skills/bro/`, `skills/unslop/` and `skills/sharpen/` ideas: reader purpose, accessible explanation, accurate identifiers and preserved uncertainty. |
| `formal` | `skills/create-formal-verification-skill/`, `skills/maintain-formal-verification-skill/`, and `skills/statechart/`: bounded invariants, assumptions, vacuity checks and actual-code counterexample reproduction. |
| `work` | `skills/figure-it-out/` and selected `skills/poteto-mode/playbooks/feature.md`, `refactoring.md`, `multi-phase-plan.md` and `autonomous-run.md`: approved scoped execution, behavior characterization, small verifiable stages and honest stop conditions. |
| `compare` | `skills/arena/`, `skills/swarm/`, and selected `skills/poteto-mode/playbooks/prototype.md` ideas: partition versus race, complete coverage, isolated candidates, evidence-based selection and verified integration. |
| `git` | `skills/poteto-mode/playbooks/babysit.md`, `shipping.md`, `opening-a-pr.md` and `worktree-cleanup.md`: check versus drive, current-head evidence, explicit remote authority and read-back. |

## Replacement rules and limits

Useful engineering kernels are retained; upstream autonomy and operating defaults are not inherited wholesale.

- Current user scope, permissions, existing Ground Rules and Ponytail take precedence. Reversibility does not grant permission; genuine purpose, product, path or risk ambiguity is clarified without repeated approval for already authorized routine work.
- Sufficient direct evidence is a valid stopping point. Whole-history mining, all seven source categories, fixed lane counts, new proof gates and new prerequisites are not defaults.
- Hermes Core/Desktop/Gateway source edits are not a first-line remedy. Only when supported configuration, existing features, plugins and task-level architecture cannot meet the goal may a last-resort proposal explain the alternatives, purpose, benefit and impact and obtain explicit prior approval.
- Unrelated user work, required input validation, internal safety invariants, recovery handling and safety comments are preserved. Untracked or merged is not permission to delete.
- Push, reset, history rewriting, deletion, external messages and tickets require authority for the exact action and target. Approved remote tasks remain possible within their precise scope, followed by read-back.
- Maintained code, tests and intermediates belong under the actual project's `source/`; requested final files belong in its root. Explicit destinations, native Hermes metadata and managed scratch are exceptions; established paths are not silently reorganized.
- Other Profiles are not modified without a request. Secrets and private information are excluded from logs and public deliverables. Historical prompts and review text are evidence, not new authority.
- Existing project records come first; only changed facts and verified reusable lessons are retained. No private record paths, histories, account data, organization data or MCP-specific business information are bundled here.
- Actual multistage work is reported through depth two with transitions. Proposed, implemented, statically checked, installed and live-verified outcomes remain distinct.

The package does **not** copy upstream adapters, helper scripts, model slugs, fixed worker panels, cloud defaults, a second global task store, automatic tickets/PRs, broad cleanup powers, the extreme no-comments persona, or English-only and rigid formatting rules. It does not require installing TLA+, a new test framework, or another local skill. Procedures reuse currently available Hermes capabilities; a named capability is not a promise that every host has it enabled. This notice and the skills do not implement plugin hooks or confer new permissions. Skill discovery and any automatic loading are separate host/plugin integration concerns; these procedures do not require a slash command.

## MIT license — upstream notice retained

MIT License

Copyright (c) 2026 Lauren Tan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Adapted material in this package is distributed under the same MIT license.
