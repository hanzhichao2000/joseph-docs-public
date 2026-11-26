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
| `export(capability, window, out_dir)` | `RevisionRecord` | shells out to the upstream, writes files, returns the record |
| `locate(record, root)` | `Path` | resolves a record under a revision root |

## `CapabilityDeclaration`

`capability_id` (e.g. `option_bars`), `schema_version`, `source` (e.g. `cnequity@0.25.0`),
`history_mode` (`by_date`, `snapshot_with_backfill`, `snapshot_only`), optional window limits.

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
