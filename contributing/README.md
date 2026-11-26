# Contributing to a public joseph repository

Public repositories hold generic principles, short contracts, generic engine code without strategy
specifics, public provider interfaces, fixtures and tooling. Everything else is private.

## Before you open a pull request

- Default private. If the content names a strategy, a result, a vendor, the control plane, evidence,
  a credential or a host path, it does not belong here.
- Documentation: every markdown file is listed in `public-layer.allow` and is at most 200 lines;
  add the allowlist entry in the same PR.
- Code: no provider or backend literal in host modules; tests for every public behavior.
- Language: artifacts in English.

## Approval

Every public pull request is approved by a private-project lead before merge. CI (allowlist, line
cap, keyword scan, tests) is necessary, not sufficient.

## What happens to a violation

The change is not merged; if something landed, the repository or file is made private immediately,
cleaned, and only then re-reviewed.
