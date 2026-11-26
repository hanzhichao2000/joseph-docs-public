# Shared public rules

These rules apply to every public joseph-* package. A package's `AGENTS.md` is generated from
this file plus its own `repos/<package>/local.md`. Owner authorization, vendor/provider
operations, research governance and the roadmap control plane live in
`joseph-docs-private/rules/shared-private.md`.

## Critical invariants (generic form)

- No fallback close for data gaps: raise and fail fast; a fallback close is a failure signal.
- Forced-close and cleanup/rollover/finalize actions are close authority only, never rewritten to
  open; cleanup is per-leg/side-aware under hedged state.
- Unknown execution intent metadata fails fast in strict backtest flows.
- Every backtest test asserts equity == cash + unrealized P&L, ends with zero positions and zero
  unrealized P&L, and checks cumulative capital, not just daily returns.
- DataFrame schema is defined and validated at the DAL producer, not the consumer; numeric missing
  values use `float('nan')`, not `pd.NA`.
- Research, OOS, acceptance and baseline claims run against a governed real DAL. CSV, fixture or
  cache runs are `scaffold_only` / `diagnostic_only` / `blocked_gate`; an unavailable real DAL
  means `blocked_gate`, never a cache substitute.
- Changing a Protocol or interface updates every implementation in the same commit, with a
  conformance test that instantiates each implementation and calls every method.
- No `type: ignore[override]` debt; fix the signature. mypy stays at 0 errors at checkpoints.
- Defects and behavior changes start with a failing regression test. Tests assert executable
  behavior and machine-readable contracts, not documentation wording.

## Architecture principles (do not change)

- Intent separation: a strategy emits economic intent, not executable orders.
- Single target authority: the portfolio manager alone defines target-level meaning.
- Plan-first execution: candidate execution plans plus arbitration, no in-flight mutation.
- Deterministic snapshots per decision context and snapshot version; external re-entry requires a
  fresh snapshot and explicit lineage.
- Reconciliation over re-emission after every execution event, with reason metadata and lineage ids
  on every accept, reject, supersede and reconcile decision.
- Backtest and live share the trading core. The pilot experiment layer is outside that core by
  design and produces hypotheses only.
- Dashboard code only consumes data; validations belong in verification or tests.

## Package and repository conventions

- Packages split by runtime role, not distribution concern. `-native` names a private repository
  implementing a public host contract, admitted only after passing the host's public equivalence
  vectors.
- Hosts are plugins (DAL providers, alpha backends) discovered by entry points; hosts import no
  plugin. A guard test proves no provider or backend literal appears in host code.
- Documentation lives in the docs layer, mounted as a submodule at `docs/`; code repositories carry
  no prose documentation. `AGENTS.md` is generated and records the pinned docs commit.
- A cross-repository contract change lands in the docs layer first; the code PR bumps the submodule
  pointer. An un-bumped repository stays governed by the revision it pins.
- Evidence attaches to GitHub Issues as run manifests (revision ids, repository SHAs, CI run URL).
  No report trees are kept in code repositories; historical evidence resolves through
  `evidence/INDEX.json` to the commit that held it. History is never rewritten.

## Public boundary (short form)

- Default private, public by exception. Public repositories hold generic principles, short
  contracts, generic engine code without strategy specifics, public provider interfaces, fixtures
  and tooling.
- Example strategies and replications of published strategies (published parameters, cited
  source) may be public. Never in a public repository: a proprietary strategy, tuned results,
  research manifests, vendor details, control-plane or roadmap internals, evidence, credentials
  or host paths.
- Every public PR is approved by a private-project lead; each public repository enforces a file
  allowlist, a size cap and a keyword scan in CI. The full policy lives in joseph-docs-private.
