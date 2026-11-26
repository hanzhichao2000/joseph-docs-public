# Fidelity tiers and promotion

| Tier | Engine | Guarantees | Claim label |
|---|---|---|---|
| pilot | vectorbt on a pinned revision | none from the platform profile; experiment accounting only | hypothesis_only |
| day | joseph-mini day-engine | full platform profile at bar fidelity | claim-grade with a qualified source |
| tick | joseph-native via mini's contract | simulator invariants (shared liquidity budget, determinism) | claim-grade; private evidence only |
| live | mini live-engine + vn.py gateway | account, HALT, single execution authority | live evidence |

No engine-equivalence protocol exists between pilot and mini. A pilot result enters the platform
only through re-implementation and an independent mini run, whose result is a new result rather
than a confirmation of the pilot number.
