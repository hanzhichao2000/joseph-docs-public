# <Topic>: a tutorial

Audience: who this is for  ·  Time: about N minutes  ·  Visibility: public | private

## What you will have at the end

One sentence; one picture or table if structure matters.

## Prerequisites

Tools, access, repos. Exactly what to install, nothing more.

## Steps

1. … (each step: one command or one action, then the output to expect)
2. …

## Verify

The command that proves it worked and the expected result.

## Next

Where to go from here (links).

---

## Filled example: mount the docs layer as a submodule

Audience: a package maintainer  ·  Time: 2 minutes  ·  Visibility: public

You will have: a package checkout whose `docs/` is the pinned docs layer.

Prerequisites: a clone of your package; the docs layer URL from `contracts/repo-map.md`.

```bash
git submodule add https://github.com/hanzhichao2000/joseph-docs-public.git docs
git submodule update --init --recursive
```

Verify: `test -f docs/rules/shared-public.md && echo ok` prints `ok`.

Next: `rules/doc-conventions.md` for where your package's docs live.
