# Provider protocol (joseph-dal)

How a DAL provider plugin is discovered, what it declares, and how the host treats replay and
strict-local mode. joseph-dal implements the host side; `dal-cnequity` is the first plugin.

## Discovery

- Entry-point group: `joseph_dal.providers`. The entry-point name is the provider id
  (`cnequity`, `akshare`, `vnpy`, `tsl`); the object implements `DataProvider`.
- The host never imports a provider module by name and contains no provider literal (guard test).

## `DataProvider` (protocol)

| Member | Type | Meaning |
|---|---|---|
| `capabilities` | `tuple[CapabilityDeclaration, ...]` | datasets the provider can produce |
| `replay_policy` | `"never_replay_dispatched" \| "idempotent_refetch"` | see Replay |
| `transports` | `tuple["live", "file"]` | what it needs at run time |
| `export(capability, window, out_dir)` | `RevisionRecord` | materializes files or references existing files under `out_dir` as documented below |
| `locate(record, root)` | `Path` | resolves a record under a revision root |

## Export

A materializing export obtains data from its upstream, writes revision files under `out_dir`,
and returns their verifiable record.

A file-only provider can opt in to in-place export by documenting the supported requests and
revision root requirements. For a supported request, `out_dir` must resolve to the existing
revision root accepted by the provider. The provider returns a record that verifies against
the existing files contained under that root. In-place export makes no writes to the root,
copies no files, and contacts no upstream. The caller can save the receipt outside the root.

## `CapabilityDeclaration`

`capability_id` (e.g. `option_bars`), `schema_version`, `source`, `history_mode`,
optional `window_limits`, `coverage_start` and `derived_from` declare the export contract.
`coverage_start` is the source's earliest data date, not a completeness guarantee.
`derived_from` names input capabilities when applicable. A receipt may record `calendar_unverified`
as an inclusive date range at the start of the window preceding the source calendar's first date;
coverage validation applies only from the calendar start and makes no coverage promise for that prefix.

A `by_date` export requires a window; `snapshot_only` rejects a window; and
`snapshot_with_backfill` accepts either. An inverted window or a start before the declared
`coverage_start` is rejected before contacting the source. All current cnequity declarations have
`window_limits = None`; enforcement of non-empty limits is not implemented and is future work.

For calendar-checked exports with an interval covered by the calendar, the source calendar must
include every natural day in that interval. The provider checks calendar continuity, then Parquet
footer boundaries, then reads actual distinct dates from the date column; footer bounds alone
cannot prove completeness. Missing calendar days, missing trading dates, and windows extending
beyond the calendar end fail closed. A prefix before the calendar's first date is not
calendar-verified and carries no coverage promise. The revision lists a digest-protected
`<capability>.coverage.json` containing `calendar_unverified: {start, end}` with inclusive prefix
dates. If the entire window precedes the calendar start, `calendar_unverified` covers the entire
window; no completeness is promised and neither footer nor date-column checks are performed.
A receipt window records the request, not a completeness guarantee.

## Replay

- `never_replay_dispatched`: a dispatched, in-flight or unknown-completion request is never
  replayed. A fresh request recomputed from coverage after an interruption is a new request. An
  undispatched rejection may adopt one successor. (TSL.)
- `idempotent_refetch`: an idempotent re-fetch is a new request. (cnequity, akshare.)
- The host planner's `on_gap` is `dispatch` or `reject`; `dispatch` is only allowed when the
  provider's policy permits a fresh request; otherwise the gap is reported, never filled silently.

## Strict-local

`read_policy = strict_local` refuses any provider whose `transports` include `"live"` at
construction time (`LiveTransportRefused`). Only receipt-listed files are read; a missing file
fails by name; no partial read.

## Record

Every `export` returns a `joseph_api.RevisionRecord` (capability, schema version, source, revision
id, content digest, ordered file list with per-file digests, optional window). Paths are relative;
the digest is independent of the root directory.

The ordered file list relative to the revision root defines revision membership. A
single-path result from `locate` is insufficient to identify a multi-file revision.
