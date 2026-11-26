# Dependency direction

- Imports flow one way: models → dal → backtest → execution → strategies. New reverse imports are
  rejected by a guard test.
- The exception list only shrinks. Every exception names its owning issue and removal condition.
- Every host package carries its own guard: a host imports no provider plugin, no alpha backend and
  no strategy-specific implementation. The DAL host's guard forbids any provider literal in batch,
  preflight and manifest modules.
- Moving a package out while core still imports it in reverse does not count as a split.
