# Data source disposition

Every source produces revisions in the host's record shape (capability id, version, source,
revision id, content digest, receipt plus immutable relative-path file list with per-file
digests). Engines read revisions, never live sources, for replay.

| Source | Datasets | Status | Gap |
|---|---|---|---|
| TSL | 5-minute bars, per-day metadata, settlement, margin, fees | governed today; private dal-tsl plugin | vendor-bound; cold path unreliable |
| cnequity | A-share daily, constituents, industry, calendar; CFE futures_bars, futures_contracts | candidate governed after qualification | no futures minute history; no margin |
| akshare / Sina | CFFEX 5-minute by contract, fees table, contract info, daily | diagnostic until qualified | expired-contract availability to verify; no margin |
| vn.py / CTP | ticks, realtime, query_history | gateway; history depth account-gated | broker account required |
| DSX (Data-Source-X) | CFFEX five-level L2 snapshots, one file per trading day (37 raw columns mapped to a 41-field core contract) | landed; source-qualified at engineering/diagnostic level; private converter; not a claim-grade input | no tick trades; no queue position; per-contract order only (global order is the reader's delivery precondition); counter interpretation admitted for one format and product only; limited local window; lineage not public |
| (none) | margin and commission PIT history | — | hard gap; prerequisite for any physical-account claim |

Until a margin/commission source is qualified, physical-account scenarios remain diagnostic
regardless of engine. "Zero TSL" has two readings and they are never merged: zero live calls
(strict-local) is required; TSL-free input provenance is claimed per family and is currently
unattainable for margin and commission.
