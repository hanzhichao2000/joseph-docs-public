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
| (none) | margin and commission PIT history | — | hard gap; prerequisite for any physical-account claim |

Until a margin/commission source is qualified, physical-account scenarios remain diagnostic
regardless of engine. "Zero TSL" has two readings and they are never merged: zero live calls
(strict-local) is required; TSL-free input provenance is claimed per family and is currently
unattainable for margin and commission.
