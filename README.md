# joseph-docs-public

> Status (2026-11-27): all joseph repositories are currently **private**. This repository keeps its
> public-layer rules (allowlist, 200-line cap, keyword scan) so a future visibility flip is a
> review, not a cleanup.

Public architecture authority, cross-repository contracts and shared agent rules for the
joseph-* package family.

- Public packages mount this repository as a submodule at `docs/` and generate a thin
  `AGENTS.md` from `rules/`. There is no prose documentation inside code repositories.
- `joseph-docs-private` pins this repository as a submodule at `public/` and holds only the
  internal delta (vendor, research and control-plane material). Public claims stand on public
  layers only.

Status: scaffold created 2026-11-26. Content lands under the `extract-joseph-docs` change (L1).

## Layout (target)

```
architecture/   principles, invariants, platform boundary profile, package map
contracts/      revision and receipt format, intent contract, engine-equivalence protocol,
                claim labels, data-source qualification
guides/         install, quickstart, testing thresholds, how to add a strategy or a source
rules/          shared-public agent rules; repos/<package>/local.md per package
```

## For consumers

```bash
git submodule add https://github.com/hanzhichao2000/joseph-docs-public.git docs
```

`AGENTS.md` is generated from this repository's `rules/`; the generated file records the pinned
commit in its header. Contract changes land here first; consumers bump the submodule pointer in
the same code PR.

## Enforcement

`public-layer.allow` is the whitelist for everything under `architecture/`, `contracts/`,
`guides/`, `reference/` and `rules/`. CI (`public-layer.yml`, GitHub-hosted) fails when a file
appears that is not whitelisted, or a whitelisted file is missing. Add public content by adding the file and its allowlist entry in the same PR; vendor, research and control-plane material goes to `joseph-docs-private` instead. Keep every public markdown file at or under 200 lines: short canonical contracts only, no full-text copies of long internal documents.
