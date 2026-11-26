# Data model contract (joseph-api)

Field-level contract for the shared data model. `joseph-api` implements it; every package may import
it; it imports no other joseph package. Missing numeric values are `float('nan')`, never `pd.NA`.

## Instruments (`joseph_api.instruments`, `joseph_api.enums`)

| Type | Key fields | Notes |
|---|---|---|
| `Exchange`, `AssetType`, `Currency` | enums | `EXCHANGE_DEFAULT_CURRENCY` maps exchange → currency |
| `Instrument` | `symbol`, `exchange`, `asset_type`, `currency`, `multiplier`, `tick_size`, `maturity_date` | base; `InstrumentRegistry` holds known instruments |
| `Future` | `Instrument` + `underlying`, `contract_month`, `expiry` | physical contract; `product` derived from symbol |
| `Option` | `Instrument` + `underlying`, `right` (call/put), `strike`, `expiry` | exercise style optional |
| `ProductCostConfig`, `CostConfig` | `fee_open`, `fee_close`, `fee_close_today`, `fee_unit` (per lot / per notional), `slippage_ticks` | per product; defaults allowed |
| `TradingCalendar` | sessions, holidays | `is_session(date)`, `next_session(date)` |

Symbol utilities normalize case and product extraction (`symbol_utils`). `DataFieldAlias` names
(`field_alias`) are the canonical column names; the pandas normalization that produces them lives in
joseph-dal, not here.

## Market and account DTOs (`joseph_api.market`)

| Type | Fields | Units / semantics |
|---|---|---|
| `Bar` | `symbol`, `exchange`, `start`, `end`, `open`, `high`, `low`, `close`, `volume`, `open_interest` (nan when absent), `freq` | prices in quote currency; `freq` like `5min`, `1d` |
| `Tick` | `symbol`, `exchange`, `ts`, `last`, `bid`, `ask`, `bid_volume`, `ask_volume`, `volume`, `open_interest` | nan when a side is absent |
| `Settlement` | `symbol`, `trade_date`, `settlement_price`, `prev_settlement` | exchange settlement |
| `Margin` | `symbol`, `trade_date`, `margin_rate` (long/short), `margin_per_lot` | PIT-dated; provenance declared by the source |
| `Fee` | `symbol`, `trade_date`, `fee_open`, `fee_close`, `fee_close_today`, `fee_unit` | PIT-dated |

## Revision record (`joseph_api.revisions`, the #893 shape)

| Field | Type | Rule |
|---|---|---|
| `capability_id` | str | dataset capability, e.g. `futures_bars` |
| `schema_version` | str | record schema version |
| `source` | str | source name, e.g. `cnequity@0.25.0` |
| `revision_id` | str | immutable id from the source or a digest |
| `content_digest` | str | digest over capability, version, source and the ordered file list |
| `files` | list of `RevisionFile` | `path` (relative), `digest`, `size` |
| `window` | optional `start`/`end` | covered dates |

Serialization is JSON with sorted keys; a round-trip is byte-identical; unknown fields are rejected;
`path` must be relative.
