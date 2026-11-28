# joseph-docs-public

> Status (2026-11-27): this repository is **public**. Its public-layer rules (allowlist, 200-line cap,
> keyword scan) keep growth explicit; private material lives in joseph-docs-private.

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

Run `python3 tools/check_public_layer.py` from the repository checkout. CI runs the same check.
Add each new public document and its entry in `public-layer.allow` in the same PR. Public Markdown,
including the root README, is limited to 200 lines.

The automated keyword check reads tracked paths and text using
`keywords/public-boundary.txt`, which contains only publishable markers. Missing or empty policy
inputs fail the check. Its diagnostics report match counts. Keep internal plans, tracker
references, and project-specific review material in the appropriate private channel. Approval
also requires private review of the same candidate revision.

The scanner can run against another public checkout with
`python3 tools/check_keywords.py keywords/public-boundary.txt <checkout>`. Downstream mirrors of
the scanner and list are maintained as copies of these public sources.
