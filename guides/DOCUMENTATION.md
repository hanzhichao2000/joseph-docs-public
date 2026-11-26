# Documentation Organization Guide

## Purpose

Keep each kind of project truth in one authority.

Use this reading order:

1. `README.md` for the project mission and repository map.
2. GitHub Issues and Milestones for live work, acceptance, and macro-roadmap facts.
3. The tier-required work item: PR for `routine`, Issue for `feature`, and Issue plus OpenSpec for
   `critical`.
4. `docs/architecture/` for current architecture contracts.

## Authority Model

| Surface | Role |
| --- | --- |
| GitHub Issues | Sole live work-status and acceptance authority. |
| GitHub Milestones | Sole macro roadmap. |
| GitHub Project (Roadmap board) | Coordination view only (directions, priorities, two-week iterations); never an authority. |
| `openspec/changes/**` | Optional technical detail and archive; not progress. |
| `docs/reports/**` | Durable evidence, receipts, and closeout detail. |
| `openspec/changes/archive/**` | Historical change specifications and task records. |
| `.sessions/<branch>/` | Temporary branch-local notes only. |

GitHub Issues are the sole live work-status and acceptance authority.
GitHub Milestones are the sole macro roadmap.
After owner-approved migration, version Milestones express engineering targets and `Future` contains
work without a concrete release target, including acceptance of delivered code. Version closeout
never grants business acceptance. The Project Roadmap board remains a coordination view:
Workstream follows existing `roadmap-workstream:*` labels independently of Milestone, Status groups
authoritative Issue states, and Iteration changes need explicit owner decisions. Use
`docs/guides/ROADMAP_BOARD.md` for mappings and separate Review/Acceptance filters. Reconcile actual
projection drift by live read-back; intentional grouping is not a status-label conflict.
OpenSpec is optional detailed record and archive.
OpenSpec task completion does not update GitHub progress.
Reports preserve evidence and history, not current progress.
GitHub outages pause progress transitions; local technical work may continue, but no
repository fallback progress ledger may be created.

## Directory Rules

| Directory | Purpose |
| --- | --- |
| Root | Permanent entry points and generated agent outputs. |
| `docs/architecture/` | Current architecture authority. |
| `docs/guides/` | Operating instructions. |
| `docs/plans/` | Design rationale and implementation blueprints, not current truth. |
| `docs/issues/` | Historical/non-authoritative [navigation](../issues/README.md) and 19 redirect stubs to 21 byte-preserved archived payloads; first two original paths absent. No local status or acceptance queue. |
| `docs/reports/` | Durable evidence and closeout records. |
| `TODO/backlog/` | Historical/non-authoritative [navigation](../../TODO/backlog/README.md), 58 redirect stubs to 58 byte-preserved payloads; unfinished engineering remains preserved, not completed by archival. Not a live queue or current-contract designation. |
| `TODO/sop/` | Standard operating procedures. |
| `TODO/archive/` | Historical local task records. |
| `logs/` | Chronological development logs. |
| `.sessions/` | Disposable branch/session notes. |

The root should contain only durable entry points such as `README.md`, `INSTALLATION.md`,
`HISTORY.md`, and generated agent files. Do not add temporary plans, generated roadmap projections,
status ledgers, investigation notes, or meeting reports there.

## Documentation Intake

Incoming material is temporary and must be reviewed promptly into the smallest owning location:
current contracts in `docs/architecture/`, evidence in `docs/reports/`, technical and vendor
references in `docs/reference/`, supporting images in `docs/reference/attachments/`, historical
design inputs in `docs/archive/`, and executable plans in `docs/plans/` or
`docs/superpowers/plans/`. Do not create an empty inbox shell.

## Plan Retention and Navigation

Age triggers review only. Retain a live Issue-owned blueprint/handoff or a named body-consumer
compatibility exception until the owning Issue or dependency is resolved. Future relocations require
individual reference/owner review; do not label every remaining document current.
[Plan navigation](../plans/README.md), [active entrance](../plans/active/README.md) and
[superpowers entrance](../superpowers/plans/README.md) distinguish execution-facing blueprints,
compatibility bodies, historical redirects and explicit retention without creating a status queue.
The approved plan batches preserve 363 payloads across the two entrances: 362 minimal plan redirects
and one replacement active-README navigation, not renewed historical acceptance. The final 15 follow
the earlier eight and grouped 340 plans; 20 originals are retained with zero unresolved identities.
See the [archive inventory](../archive/phase0-hygiene-20260929/README.md) for membership and bytes/modes.
July 20 bounded-factor-loader retention remains conditional on the virtual-5m handoff; replacement
topology is not asserted frozen. Historical-window gates, data-root-storage-policy and evidence
consumers remain unchanged. Preserve history before retirement; redirects do not satisfy body hashes.

## Conditional Change Documentation

For `routine` changes, GitHub Issue, OpenSpec, session notes, report, and daily log are optional. A
`feature` needs an Issue and a concise Goal/Behavior change/Out of scope/Verification design note.
Use the complete managed workflow below for `critical` changes.

Claim labels and the seven-field Joseph preflight apply only to research, evidence/acceptance,
status/release, or other critical claim-bearing work.

## Managed Critical Change Workflow

Every `critical` change requires a GitHub Issue and an OpenSpec change. Apply the remaining
documentation only when its authority or claim is part of the change:

1. Keep live state and acceptance in the Issue and macro scheduling in its Milestone.
2. Keep detailed scope and tasks in OpenSpec when the critical change needs them.
3. Use native OpenSpec validation and archive independently of Issue acceptance.
4. Keep native Project Status `In progress` while review or acceptance remains. An owner-delegated
   agent may review and close bounded engineering delivery, including feature and critical work,
   only after a merged PR completes every requirement, all applicable gates pass, and evidence is
   recorded on the Issue. Important demo, business, and research acceptance belongs in a separately
   linked acceptance Issue with its criteria, relationships, history, and acceptor preserved. Do
   not silently move unfinished delivery scope into that Issue or treat merge alone as completion.
   Authorized completed closure maps to `Done`; unresolved authority remains open (see
   `docs/architecture/GITHUB_ROADMAP_CONTROL_PLANE.md` § Tiered Closure).
5. Use `docs/reports/**` only for research, acceptance, release, or other claim-bearing evidence.

Do not duplicate the forward queue in a tracked Markdown board. Promote a local backlog entry using
the workflow tier: a `routine` change may move directly to a PR, a `feature` needs an Issue, and a
`critical` change needs both an Issue and OpenSpec.

## Session Documents

Use `.sessions/<branch>/` only when short-lived `PLAN.md`, `TODO.md`, `STATUS.md`, `NOTES.md`, or
temporary artifacts are useful. These files are optional working memory, not roadmap, queue, or
acceptance authority. When session notes exist, delete them on merge unless a concise handoff has
continuing historical value.

## Logs

Historical logs and bi-weekly summaries are conditional, not mandatory.
The two-week GitHub coordination cadence remains required; reconcile Issue and Milestone facts
and make explicit iteration rollover decisions whether or not a summary is written.
When useful, a summary records historical facts from GitHub Issues and Milestones, not live status
or acceptance. Do not fabricate retrospective logs.

When a daily log is useful, name it `YYYYMMDD.md` or `YYYYMMDD-<topic>.md`; optional bi-weekly
summaries use `YYYYMMDD-bi-weekly-progress.md`. Move older logs under `logs/archive/YYYY-MM/`
only after preservation and owner-approved disposition.

## Review Checklist

- Update the owning authority instead of copying its facts into another document.
- Verify Issue status, Milestone membership, and explicit acceptance directly in GitHub.
- Apply Issue, OpenSpec, and report requirements by workflow tier.
- Archive completed OpenSpec changes and preserve reports required by claim-bearing decisions.
- When temporary session notes exist, remove them after merge or retain a concise handoff.

## Quick Reference

```text
project-root/
├── README.md
├── INSTALLATION.md
├── HISTORY.md
├── docs/
│   ├── architecture/                  # current design authority
│   └── reports/                       # durable evidence
├── openspec/changes/
│   ├── <change>/                      # optional technical detail
│   └── archive/                       # historical changes
├── TODO/{backlog,sop,archive}/
└── .sessions/<branch>/                # temporary notes
```
