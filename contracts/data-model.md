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

## Option rows (`joseph_api.market`)

Rows of the option data lake as the source holds them — data, not tradable instrument specs (no
margin, no commissions). Source strings are verbatim: `symbol` is the lake's compact symbol
(`IO2403C3500.CFE`), `exchange_code` the joseph option-symbol form (`IO2403-C-3500`); `exchange`
is the shared enum mapped from the lake code (`CFE` → `CFFEX`). The internal symbol is the
exchange code plus `exchange_code` (`CFFEX.IO2403-C-3500`); there is no compact-symbol parser.
Dates are as held — null when the source no longer dates a contract. Missing numerics (`None` or
nan) become nan.

| Type | Fields | Units / semantics |
|---|---|---|
| `OptionContract` | `symbol`, `exchange_code`, `exchange`, `product`, `product_name`, `underlying_kind`, `underlying_symbol`, `option_type`, `exercise_style`, `strike`, `multiplier`, `tick_size`, `expiry_date`, `expiry_month`, `list_date`, `first_seen_date`, `last_seen_date`, `dates_basis`, `source`, `data_version`, `fetched_at` | `strike` in index points; `multiplier` CNY per point; `option_type` `C`/`P` as held |
| `OptionBar` | `symbol`, `exchange_code`, `exchange`, `product`, `underlying_symbol`, `option_type`, `strike`, `trade_date`, `open`, `high`, `low`, `close`, `settle`, `pre_settle`, `volume`, `open_interest`, `exercise_volume`, `oi_change`, `amount`, `implied_vol`, `series_implied_vol`, `delta`, `source`, `data_version`, `fetched_at` | prices in index points; `settle` is the exchange settlement, and on the expiry date the intrinsic value at the underlying's final settlement |
| `OptionGreek` | `symbol`, `underlying_symbol`, `trade_date`, `status`, `model`, `rate_source`, `forward_source`, `source`, `data_version`, `fetched_at`, `rate`, `time_to_expiry`, `underlying_price`, `iv`, `delta`, `gamma`, `vega`, `theta`, `rho` | derived by the lake; filter on `status` |

`pre_settle` is present in the exported data but absent from the lake's registered contract
(0.25.0); the row follows the data.

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
