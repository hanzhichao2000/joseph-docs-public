# Core dependency direction

The architecture guard in `tests/architecture/test_core_boundary_imports.py` limits new coupling
without imposing a numbered layer hierarchy. A core unit is a direct `joseph_core` subpackage or a
root-level module. A direction is an import from one unit to another; file-level identities count
once per importing file and imported unit.

## Scan boundary

The statement-path scan covers Python files in the core-shipped `joseph_core`, `joseph_workspaces`
and `joseph_agent_tools` roots. It includes package initializers, relative imports, imports inside
functions and conditional blocks, and `from joseph_core import X`. It attributes a statement to
its own file; it does not trace re-exports, symbol or type aliases, or dynamic imports. Unattributable
research-root forms fail closed. The existing experiment import guard remains independent.

## Research experiment boundary

Files outside `joseph_core/research/` must not import research experiment implementations unless
listed in the research exception table. Experiment units include research subpackages and root
modules, except the generic root modules `contract`, `study_contracts`, `study_lifecycle`,
`study_registry` and `validator`. Research-internal importers are excluded from this rule. The
exception identity is the importing file and experiment unit.

## Direction and exceptions

For a baseline pair importing in both directions, the direction with fewer importing files is frozen;
when counts are equal, both are frozen. Each frozen file and direction is listed explicitly. New
imports in frozen directions fail, and new two-way pairs are prohibited. A clean one-way direction
flip is permitted. Research pairs use the separate experiment rule.

Exception tables and recorded sizes live in the guard. Observed frozen imports must match their
exceptions, and each table's actual size must match its recorded size. When an import is removed,
remove its exception and reduce the recorded size in the same change. For an equal-count pair,
removing the last import in one direction makes the pair one-way: remove both directions' exception
entries and add the surviving direction to `_ONE_WAY_BASELINE`. The current snapshot cannot detect
omission of that migration if only one direction remains; reviewers must check the migration. The
guard prohibits the pair becoming two-way again, while a clean direction flip is permitted. Increasing
a recorded size is a rule change requiring an owner decision cited in the owning Issue; retained pairs
keep their exceptions and linked decisions.

These tables are a baseline, not approval of the coupling. The check is ordinary regression
protection, not a security boundary against changes to the guard or its baselines: a count alone
cannot prevent a same-size substitution. If an import and its exception have both disappeared but
the recorded size has not decreased, the check reports the current and recorded counts; the current
snapshot cannot identify the deleted file.

Execution participant authority obtains the concrete backtest `DayEngine` and `PendingOrderQueue`
classes through an execution-owned registry populated by those backtest modules. Exact-type and
subclass checks remain distinct; an unregistered class does not match. Fill simulators live in
`joseph_core.execution.fill_simulators`; their `__module__` retains
`joseph_core.backtest.execution.fill_simulators`, which re-exports the same classes for persisted
configuration and pickle paths.

Provider adapters depend on the shared `TradingCalendar` and `ReadOnlyDataView` contracts in
`models.trading_calendar` and `models.read_only_data_view`, and on trader API contracts in
`models.trader_api`. The former backtest,
Runtime, and trading import paths re-export the same objects for compatibility. Backtest,
runtime, and trading may import providers; providers must not import those layers.

Canonical hashing and field aliases live in models; backtest errors and forced-close request
contracts live in core. Their former modules re-export the same objects with their original module
identity. Risk uses a structural registry contract, and execution uses a structural timer contract.
Trading context retains its exception: it needs `rank_by`, absent from enhanced manager config.
Universe manager retains its exception: its base returns validated observed-D1 authority records.

Performance metrics, signal semantics and the optimize historical-access adapter live in
`models.performance_metrics`, `core.contracts.signal_semantics` and
`historical_access.optimize_adapter` respectively. Their former modules re-export the same objects,
whose original `__module__` values preserve pickle and dotted-name compatibility.

Exact metadata admission uses a DAL-owned exact-type registry for optimization participants.
Importing the optimization module registers its DAL class before any instance can exist, so
the previous exact-type allowlist behavior is preserved and unexpected types remain rejected.
Factor admission and memory estimates are owned by models and DAL respectively; their former
factor-runtime paths re-export the same objects. The batch run contract lives in `test_broker`;
`cli.batch` re-exports the same objects for compatibility.

The learning handoff contract (`LearningPositionBinding`, `LearningTerminalExpiry` and
`DeferredLearningDecisionHandoff`, on their shared frozen base) lives in
`strategies.learning_handoff`; `backtest.learning.contracts` re-exports the same objects and the
carrier types the backtest-owned decision structurally, so no strategy file imports backtest.
The option accounting output contract is owned by its producer: `backtest.option_accounting_output`
defines the schema, row records and exporter, `verification.option_accounting_output` re-exports
the same objects, and recorded provenance source paths point at the new module location.

The configuration loader logs through the standard library and `setup_logging` routes the config
package's records into the configured sinks; `logging` keeps reading its settings from `config`,
so that pair is one-way. The base `UniverseManager` lives in `joseph_core.universe.manager_base`
and annotates the observed binding with protocols owned by the universe unit;
`joseph_core.backtest.universe` re-exports the class, and only `backtest` imports `universe`.

Removal must preserve runtime behavior, public interfaces, configuration targets and persisted
identity. Trading-core slices and any retained thick dependency require the owner decisions specified
in the change; this document does not authorize those edits or claim their completion.

See the [change design](../../openspec/changes/ratchet-core-dependency-direction-863/design.md)
for the historical baseline, exception inventory and planned removal slices.
