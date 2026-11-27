# Option capability contract

This contract describes the cnequity provider's option exports. Rows follow the shared
[data model](../../../contracts/data-model.md#option-rows-joseph_apimarket); they are data,
not tradable instrument specifications. Schema version is `cne-contract-0.25.0`.
All three declarations have `window_limits = None`.

| Capability | history_mode | coverage_start | derived_from |
|---|---|---|---|
| `option_contracts` | `snapshot_only` | `None` | `None` |
| `option_bars` | `by_date` | 2023-11-01 | `None` |
| `option_greeks` | `by_date` | 2023-11-01 | (`option_bars`, `option_contracts`) |

## Columns and units

- `option_contracts`: `symbol`, `exchange_code`, `exchange`, `product`, `product_name`,
  `underlying_kind`, `underlying_symbol`, `option_type`, `exercise_style`, `strike`,
  `multiplier`, `tick_size`, `expiry_date`, `expiry_month`, `list_date`, `first_seen_date`,
  `last_seen_date`, `dates_basis`, `source`, `data_version`, `fetched_at`. Strike and tick size
  are index points; multiplier is CNY/point. `list_date` and `expiry_date` may be null;
  `dates_basis = observed_truncated` means observed dates are truncated, not authoritative
  contract listing or expiry dates. The snapshot does not accept a window.
- `option_bars`: `symbol`, `exchange_code`, `exchange`, `product`, `underlying_symbol`,
  `option_type`, `strike`, `trade_date`, `open`, `high`, `low`, `close`, `settle`,
  `pre_settle`, `volume`, `open_interest`, `exercise_volume`, `oi_change`, `amount`,
  `implied_vol`, `series_implied_vol`, `delta`, `source`, `data_version`, `fetched_at`.
  Strike and prices are index points; implied volatilities are fractions. `pre_settle` is the
  previous trading session's settlement.
- `option_greeks`: `symbol`, `underlying_symbol`, `trade_date`, `status`, `model`, `rate_source`,
  `forward_source`, `source`, `data_version`, `fetched_at`, `rate`, `time_to_expiry`,
  `underlying_price`, `iv`, `delta`, `gamma`, `vega`, `theta`, `rho`. `iv` and `rate` are
  fractions, `time_to_expiry` is in years, and `underlying_price` is in index points.
  Filter by `status`: `ok`, `no_expiry`, `below_intrinsic`, or `expiry_day`.
  The model is `black76`, rate source `fallback_constant`, forward source `parity`.

## Windows and coverage

Dated exports require an inclusive window; snapshot exports reject one. An inverted window or a
start before the declared coverage start is rejected before contacting the source. When a dated
export has an interval covered by the calendar, it validates every natural calendar day in that
interval, then footer bounds, then distinct dates from the data column. Missing calendar days or
trading dates and an end beyond the calendar fail closed. A window prefix before the calendar start
is declared in the digest-protected, receipt-listed `<capability>.coverage.json` as
`calendar_unverified` with inclusive `start` and `end`; it is not a coverage promise. If the
entire window precedes the calendar start, `calendar_unverified` covers the entire window; no
completeness is promised and neither footer nor date-column checks are performed. The receipt's
window records the request, not a completeness guarantee. Pin a revision by (`revision_id`,
`window`, `content_digest`); snapshot-only exports have an empty window.
