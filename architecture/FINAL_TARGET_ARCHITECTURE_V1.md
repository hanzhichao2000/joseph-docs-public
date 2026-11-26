# Final Target Architecture v1

Status: Draft for team review  
Scope: Long-term target shape (not implementation plan)

## 1. Purpose

This document defines the final target shape of joseph-core as an integrated
quant operating system for both research and production operations.

Legacy portfolio-risk and strategy-specific design docs are reference-only inputs; they do not
override this target architecture or current portfolio governance.

The goal is not "auto-profit black box". The goal is:
- auditable decision chains,
- replayable behavior,
- controlled risk and market-rule compliance,
- scalable multi-asset and multi-venue extensibility.

## 2. Design Principles

- Platform before strategy: strategy is a plugin, governance is core.
- Same contract for research and production: config differs, code path does not.
- Evidence before return claims: detect and explain break first, then discuss PnL.
- Rules as first-class models: venue rules and market-state rules are centralized.
- Manual actions are first-class events: no side-channel operations.
- Replay by default: key decisions must be reproducible from snapshots.
- Declarative extension: add venues/assets via templates and adapters, not core rewrites.

## 3. Anti-Goals

- No separate "research codebase" and "production codebase".
- No silent drops (for example signal exists but no traceable outcome).
- No manual overwrite of historical reason chain.
- No module-local hidden rule logic bypassing central policy layers.
- No hidden timer control flow: timer schedule/cancel/fire must be first-class traceable events.

## 4. Module Map (Target)

- `core-kernel`: event bus, state reducers, timer queue, idempotency.
- `market-rules`: venue templates, session/limit rules, market-state transitions.
- `data-fabric`: normalized multi-asset data contracts and adapters.
- `research-signal`: factors and strategy signal generation.
- `allocation-aum`: capital allocation, constraints, rebalance planning.
- `risk-compliance`: pre-trade/post-trade risk control and forced actions.
- `execution`: order intent, validation, submission, fill lifecycle.
- `trace-verification`: trace integrity, replay, baseline regression acceptance.

Cross-layer hard rules:
- Strategy cannot directly mutate global state.
- Execution cannot bypass market/risk permissions.
- All critical rejections require reason metadata.

## 5. Unified Event Model

Tier-1 domain events:
- `MarketDataEvent`
- `MarketStateChangedEvent`
- `SignalGeneratedEvent`
- `SignalDroppedEvent`
- `AllocationDecidedEvent`
- `OrderIntentEvent`
- `OrderAcceptedEvent`
- `OrderRejectedEvent`
- `TimerScheduledEvent`
- `TimerCancelledEvent`
- `TimerFiredEvent`
- `OrderSubmittedEvent`
- `OrderFilledEvent`
- `RiskAlertEvent`
- `SettlementEvent`

Timer and recovery events:
- `TimerScheduledEvent`
- `TimerFiredEvent`
- `RecoveryEvaluatedEvent`
- `RecoveryAppliedEvent`

Event envelope minimum fields:
- `event_id`, `event_type`
- `occurred_at`, `ingested_at`
- `causal_id`, `parent_event_id`
- `symbol`, `venue`, `account_id`, `strategy_id` (when applicable)
- `reason_code` (required for rejection/blocking paths)
- `payload`

## 6. Reason and Audit Model

Three-layer reason model:
- `reason_code`: stable machine-readable enum.
- `reason_dtl`: structured details (JSON).
- `manual_note`: human context text.

Manual-operation audit fields:
- `actor_type` (`SYSTEM` or `HUMAN`)
- `actor_id`
- `action_source` (`UI`, `API`, `CLI`, `BATCH`)
- `approval_ref`
- `reason_chain` (append-only)

Hard rule:
- Reject/drop/manual-risk events must include `reason_code`.

## 7. Unified State Machines

### 7.1 MarketState

States:
- `NORMAL`, `REDUCE_ONLY`, `CIRCUIT_BREAK`, `HALTED`, `AUCTION`, `CLOSED`, `DEGRADED`

Key rules:
- Recovery must go through timer + evaluation events.
- Resume cannot bypass active venue/regulatory hard blocks.

### 7.2 PortfolioState

States:
- `FLAT`, `BUILDING`, `INVESTED`, `REBALANCING`, `LIQUIDATING`, `BLOCKED`

Key rules:
- Target changes are event-driven.
- Non-normal market states cannot create new risk exposure.

### 7.3 RiskState

States:
- `GREEN`, `YELLOW`, `ORANGE`, `RED`, `FORCED_EXIT`

Key rules:
- Escalation can be immediate.
- De-escalation requires observation window and recheck.

### 7.4 ExecutionState

States:
- `IDLE`, `INTENT`, `VALIDATED`, `QUEUED`, `SUBMITTED`, `PARTIAL_FILLED`,
  `FILLED`, `CANCELED`, `REJECTED`, `EXPIRED`

Key rules:
- Every transition must be event-backed and idempotent.
- Terminal states must be traceable to signal/allocation provenance.

Conflict priority:
- Regulatory and venue hard events > risk hard events > manual overrides > strategy intents.

## 8. Unified Object Model (Minimum Schema)

- `Instrument`: `instrument_id`, `asset_class`, `venue`, `symbol`, `currency`,
  `tick_size`, `lot_size`, `multiplier`, `trading_sessions`, `status`
- `Account`: `account_id`, `account_type`, `base_currency`, `equity`,
  `cash_available`, `margin_used`, `margin_available`, `leverage_limit`, `risk_state`
- `Position`: `position_id`, `account_id`, `instrument_id`, `direction`, `quantity`,
  `avg_price`, `mark_price`, `unrealized_pnl`, `realized_pnl`, `margin_occupied`
- `Order`: `order_id`, `account_id`, `instrument_id`, `side`, `offset`,
  `order_type`, `quantity`, `price`, `time_in_force`, `status`,
  `signal_id`, `allocation_id`, `causal_id`
- `Fill`: `fill_id`, `order_id`, `account_id`, `instrument_id`,
  `fill_price`, `fill_qty`, `commission`, `fee_breakdown`, `filled_at`
- `AllocationTarget`: `allocation_id`, `account_id`, `instrument_id`,
  `target_qty`, `target_exposure`, `current_qty`, `delta_qty`, `priority`

### 8.1 Target Authority Migration (M11)

The target-authority execution chain is being introduced incrementally:

```text
StrategyIntent -> PortfolioTarget -> ResolvedDelta -> execution -> TargetReconciler
```

In this migration section, `StrategyIntent -> PortfolioTarget -> ResolvedDelta` and
`core/contracts/target_authority.py::PortfolioTarget` refer to the current quantity-target
compatibility path unless the text explicitly references the restored target-state contracts in
`core/contracts/portfolio_target_state.py`.

Key migration objects:
- `PortfolioTarget` in `core/contracts/target_authority.py` is the current quantity-target
  compatibility path; it is the authority successor to `AllocationTarget` / `TargetPosition` only
  in that compatibility sense, not the restored portfolio budget/exposure authority model
- `TargetPosition` remains a compatibility model during migration
- `LegacyTargetPositionAdapter` provides explicit bridge from signed-net `TargetPosition`
- `TargetReconciler` reads projected state via `DecisionContext`, not private storage

Current status (M11):
- `StrategyIntent`, `PortfolioTarget`, `ResolvedDelta` compatibility models implemented
- `TargetReconciler` first slice implemented
- `DecisionArbiter` and `ExecutionPlan` planned for M12

Current status update (M11.5 / P5.5):
- M11 chain has moved from observation-only to **authority-driven control** on
  the official wrapper demo/backtest path
- cutover scope is explicit partial-chain replacement:
  `signals -> StrategyIntent -> PortfolioTarget -> ResolvedDelta -> AuthorityExecutionBridge`
- that cutover scope is current quantity-target compatibility only; restored target-state contracts
  live separately in `core/contracts/portfolio_target_state.py`
- downstream queue/fill/timer/trace/ledger machinery is intentionally unchanged
- non-official paths remain on legacy conversion in this slice

Current status update (M12 / P6 first slice):
- official wrapper demo path now inserts
  `ExecutionPlanBuilder -> DecisionArbiter -> PlanMaterializer`
  between `ResolvedDelta` and downstream execution
- first-slice candidate families: `REJECT`, `CLOSE_ONLY`, `DIRECT_SIMPLE`,
  `REDUCE_ONLY`
- `DecisionArbiter` returns both selected and rejected plan evidence
- non-official paths remain on legacy conversion in this slice

Current status update (M12.5 / P6.5 wider rollout):
- all `authority-enabled` backtest paths now default to the same plan-first
  skeleton (`ExecutionPlanBuilder -> DecisionArbiter -> PlanMaterializer`)
- `authority_in_control=True` is the semantic rollout trigger in backtest;
  `plan_first_enabled` no longer acts as an official-demo-only switch
- `authority_in_control=False` backtest paths remain outside the arbiter slice
- unsupported authority-enabled paths must fail fast; no silent fallback to
  non-plan-first authority mode or legacy direct conversion

Current status update (M4 continuation convergence):
- M3 reconciliation remains the formal residual contract
- continuation lifecycle authority after reconciliation moves to
  `OrderManager.decide_continuation()`
- `PlanMaterializer.materialize_continuation()` owns the current execution boundary: every valid
  `CONTINUE` raises `NotImplementedError` referencing GitHub Issue #216 before its compatibility
  bridge or any execution-side collection can mutate; non-`CONTINUE` decisions materialize nothing
- `DayEngine` propagates that unsupported-operation error while retaining reconciliation,
  continuation-decision, and lineage diagnostics
- GitHub Issue #216 owns the missing prepared-event, atomic lifecycle, and deferred-publication
  capability required to enable continuation materialization
- residual continuation lineage is surfaced with
  `target_id/delta_id/plan_id/residual_delta_id/continuation_chain_id`
- strategy and external-signal re-entry are forbidden for residual continuation

Compatibility rule:
- Evolve by adding fields; do not silently change existing field semantics.

### 8.2 E-line Target-State Boundary (Q2M776)

The portfolio target-authority boundary is now split explicitly:

- `PortfolioTarget` in `core/contracts/portfolio_target_state.py` owns portfolio budget, exposure,
  risk, and constraint semantics, with `PortfolioBudgetTarget` retained as the interim restored
  target name.
- `AdmittedPortfolioTarget` owns the post-admission result.
- `ExecutionProjection` owns rounded contract quantity and delta quantity.
- `OrderIntent` bridges projection to concrete order materialization.
- the existing quantity-shaped `PortfolioTarget` remains a compatibility projection path for
  current quantity-target compatibility consumers.

## 9. Plugin Contracts

Required adapter types:
- `DataAdapter`
- `RuleAdapter`
- `AUMAdapter` / `PortfolioManager`
- `RiskAdapter`
- `ExecutionAdapter`
- `VerificationAdapter`

Contract-level requirements:
- standardized result status (`OK`, `RETRY`, `DENY`, `ERROR`)
- mandatory reason metadata on deny/reject paths
- adapter versioning and startup conformance checks
- gray rollout and deprecation lifecycle controls

Runtime-facing bundle rule:
- runtime should expose a formal runtime-owned bundle of run-time services and
  immutable inputs to upper layers rather than requiring scattered owner
  lookups; the current bridge-first implementation uses `RuntimePorts` as the
  first formalization of that bundle

## 10. SLO and Operational Quality

Core SLO dimensions:
- delivery reliability
- end-to-end latency
- accounting consistency
- replay reproducibility
- audit coverage
- risk enforcement effectiveness

Release gates:
- all P0/P1 controls pass,
- baseline regression gate passes (or approved break report exists),
- audit chain health is green.
- versioned release evidence is complete (M8): code version, data version,
  and baseline artifact version must be present in `ReleaseVersionContext`
  when `require_version_context` is enabled.

## 11. Ops and Permission Model

Role model:
- `Researcher`, `Trader`, `RiskOfficer`, `Ops`, `Auditor`, `Admin`

Control model:
- RBAC + ABAC
- high-risk writes require approval workflow
- manual overrides must be eventized and post-checked by risk re-evaluation

Failure behavior:
- fail-closed for risk and audit critical paths
- degraded mode defaults to risk-reducing behavior

## 12. Governance Rules

- Architecture docs are source of truth for cross-module contracts.
- Interface changes must update architecture docs in the same PR.
- Baseline validation is mandatory for iterative changes.

## 13. Non-Negotiable Architecture Contracts

The following contracts are mandatory and testable. They override style-level guidance.

### C-01 Event Envelope Contract

Required fields for all persisted events:
- `schema_version`
- `producer_id`
- `producer_version`
- `idempotency_key`
- `policy_version` (if decision-bearing event)

Enforcement:
- Event bus rejects events missing required fields.
- Rejected event emits `SYS_EVENT_SCHEMA_REJECTED`.

Acceptance:
- CI conformance test verifies required fields exist for all event models.

### C-02 Replay Determinism Contract

Replay scope:
- order lifecycle,
- risk decisions,
- ledger balances.

Enforcement:
- Derived events must be deterministic under fixed input, fixed version, fixed seed.

Acceptance:
- Same event stream replayed twice must produce identical terminal order states and ledger state.

### C-03 Fail-Closed / Fail-Open Matrix Contract

Fail-closed paths:
- risk decision service,
- permission decision service,
- ledger write path,
- audit append path for high-risk actions.

Fail-open paths:
- dashboard projection,
- non-critical analytics exporters.

Enforcement:
- Runtime policy matrix loaded at startup and verified.

Acceptance:
- Chaos tests assert mandatory fail-closed paths block trading when unavailable.

### C-04 Permission Arbitration Contract

Every order submission must include one `PermissionDecision` object:
- `verdict` (`ALLOW`, `REDUCE_ONLY`, `DENY`)
- `reasons[]`
- `policy_version`
- `decision_id`

Enforcement:
- Execution adapter rejects submit when `PermissionDecision` is absent.

Acceptance:
- Integration test proves no `OrderSubmittedEvent` exists without `decision_id`.

### C-05 Correction and Amendment Contract

Historical data and state corrections must be append-only events:
- `StateCorrectionEvent`
- `TradeAmendmentEvent`
- `DataCorrectionEvent`

Enforcement:
- Direct mutation/deletion of historical events is forbidden.

Acceptance:
- Reconciliation suite verifies corrected state can be derived from original stream + correction events.

### C-06 Ledger Source-of-Truth Contract

Ledger is authoritative for:
- cash,
- margin,
- fees,
- realized/unrealized pnl balances.

Enforcement:
- Position and analytics views are projections; they cannot authoritatively override ledger.

Acceptance:
- Invariant checks must pass on every batch:
  `equity = cash + unrealized_pnl`.

### C-07 Cross-State Invariants Contract

Mandatory invariants:
- non-normal market states must not allow risk-increasing open orders,
- `RiskState=RED` must block all risk-increasing intents,
- terminal execution states require provenance (`signal_id`, `allocation_id`, `causal_id`).

Enforcement:
- Reducer-level invariant guard rejects invalid transitions.

Acceptance:
- Invariant test suite runs as release gate; any violation is P0 fail.

### C-08 Strategy Isolation Contract

Each strategy has hard budgets:
- max event rate,
- max compute time per window,
- max snapshot read quota.

Enforcement:
- Budget breach triggers throttling or quarantine.

Acceptance:
- Load tests prove one strategy cannot degrade global SLA beyond configured budget limits.

### C-09 Forced-Risk Action Closure Contract

Forced risk actions must be closed-loop:
- trigger,
- order intent generation,
- submit/fill outcome,
- retry/escalation,
- terminal resolution.

Enforcement:
- A forced action without terminal resolution within timeout escalates to P0.

Acceptance:
- Integration tests simulate reject/fail paths and verify escalation events are emitted.

### C-10 Research-Production Conformance Contract

"Same contract" is proven by conformance suite, not by statement.

Required checks:
- same schema validation,
- same permission checks,
- same risk checks,
- same replay determinism checks.

Enforcement:
- Research mode cannot disable mandatory production contracts.

Acceptance:
- Conformance suite must pass in both research and production profiles.

### C-11 Snapshot Contract

State rebuild must support bounded recovery time via snapshots.

Required snapshot metadata:
- `snapshot_version`
- `event_offset`
- `producer_version_set`
- `checksum`

Enforcement:
- Recovery uses latest valid snapshot + forward replay.

Acceptance:
- MTTR target and snapshot equivalence tests are release-gated.

### C-12 Break-Glass Contract

Emergency override is allowed only through explicit protocol:
- dual approval,
- limited action scope,
- maximum TTL,
- mandatory post-action reconciliation.

Enforcement:
- All break-glass actions emit highest severity alerts and immutable audit chain entries.

Acceptance:
- Quarterly drill must prove forced flatten works when normal gates are degraded.

### C-13 Data Root and Manifest Contract

Core data boundary is environment-selected and manifest-driven:
- Fixture root: `JOSEPH_FIXTURES_ROOT`
- Full-data/reference root: `JOSEPH_DATA_ROOT`
- Root contract models: `DataRootDescriptor`, `DataManifest`, `DatasetType`
- Manifest loading: `load_manifest(...)` with schema compatibility check

Runtime data resolution (M7):
- `RuntimeDataResolver` is the single runtime-owned resolver for external data roots.
- Consumers call `resolver.resolve(dataset_type)` to obtain `ResolvedDataRoot` metadata.
- `ResolvedDataRoot` exposes `manifest`, `available_datasets`, `data_version`, `source_family` — no raw paths.
- `BacktestEngine.data_resolver` and `RuntimePorts.data_resolver` carry the resolver through official paths.
- Official consumers (`BacktraderComparator`, `DataManager`) resolve through `RuntimeDataResolver`.

Enforcement:
- Core/runtime code must not hardcode repo-local CSV layout assumptions.
- Core/runtime code must not implement git/repo/branch/tag resolution logic.
- Selected root must contain a valid manifest with compatible `schema_version`.
- Official consumers must resolve data through `RuntimeDataResolver`, not direct `load_manifest` calls.

Acceptance:
- Conformance tests prove fixture-facing paths can run from external fixture root.
- Conformance tests prove one runtime/reference path resolves via `JOSEPH_DATA_ROOT`.
- Missing manifest or incompatible schema version fails fast before dataset consumption.
- Integration tests verify resolver metadata flows into `BacktestEngine.dal_provider` and `build_read_only_data_view`.

## 14. Responsibility Boundaries

- Permission correctness owner: market-rules + risk-compliance.
- Submit safety owner: execution.
- Accounting correctness owner: ledger/accounting reducer.
- Replay correctness owner: core-kernel + verification.
- Emergency execution owner: ops + risk officer dual control.
- Data version selection owner: bootstrap/operator layer (outside core runtime).
- Data contract enforcement owner: core data boundary (`DataManifest` + schema checks).
- Data resolution owner: runtime layer (`RuntimeDataResolver`).
- Release evidence owner: governance layer (`ReleaseVersionContext` + `ReleaseGateRunner`).

Ambiguous ownership is treated as architecture defect and blocks release.

## 15. Demo Wrapper Layer

Package: `joseph_core/demo/`

Role: Thin orchestration layer that runs official demo scenarios through formal system
paths, judges demo readiness, and renders acceptance-first summaries.

Components:
- `DemoScenario` — declares scenario mode, config, and expected artifacts.
- `DemoRunner` — calls formal backtest or live/mock execution chains.
- `DemoReadinessGate` — produces structured ready/not_ready verdict from evidence.
- `DemoSummary` — aggregates verdict, trace families, and visibility into one object.
- `OperatorReport` (`joseph_core/operator/models`) — shared report shape that both ctl
  diagnostics (`from_diagnosis()`) and demo summary (`from_demo_summary()`) produce.
  Downstream consumers (MiniTUI, dashboards, CI) read this single JSON contract.
- `MiniTUI` — plain-text renderer for terminal review; renders both `DemoSummary`
  (`render_demo_summary()`) and `OperatorReport` (`render_operator_report()`).

Boundary rules:
- The demo layer must not introduce parallel business semantics.
- The demo layer must not bypass runtime/provider/core paths.
- MiniTUI and dashboard code must only consume data — assertions belong in
  verification or tests.
- Every later architectural phase must preserve the official backtest demo path.

### M11/M12 Runtime Boundary

Current branch-state boundary for the first provider-backed live slice:

- `ProviderRuntimeAssembly` owns provider build/startup/shutdown and returns the runtime-owned `RuntimeStartupResult`.
- `LiveTradingGateway` consumes runtime-owned startup outcome and rollout authorization; it must not define its own provider bootstrap semantics.
- `ReadinessGate` is fail-closed: no checks or `SKIP`-only checks are operationally equivalent to `FAIL`.
- `RolloutContext` models explicit `SHADOW`, `CANARY`, and `FULL` stages plus operator-visible rollback triggers.
- `live_mock` is the controlled official path for this slice; backtest remains outside provider-runtime rollout evidence.
- Operator-facing evidence is carried through `DemoRunResult` / `DemoSummary` (`readiness_summary`, `rollout_stage`) and governance CLI (`rollout-status`, `readiness-check`).
