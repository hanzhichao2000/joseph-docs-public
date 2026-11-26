# Evidence and claims

- Evidence attaches to GitHub Issues as run manifests: revision ids, participating repository SHAs,
  CI run URL, and the issue it is posted to. Bulky artifacts are CI artifacts with bounded
  retention.
- Code repositories carry no report trees. Historical evidence resolves through
  `evidence/INDEX.json` (last commit SHA, file count, tree SHA) to the commit that held it.
  History is never rewritten; `blob/main/...` links to removed trees will 404 and are documented.
- Claim labels: `hypothesis_only` (pilot), `diagnostic_only`, `scaffold_only`, `blocked_gate`,
  claim-grade (a governed real DAL plus a platform-profile engine). A cache or fixture substitute
  for an unavailable real DAL is `blocked_gate`, never a substitute.
- Public claims stand on public layers only: docs-public, public packages and public backends. A
  private layer may extend but never complete public evidence.
