# Package map (target)

Six packages by runtime role. joseph-core is the transitional source of extraction.

| Package | Visibility | Role | Delegates to |
|---|---|---|---|
| joseph-api | public | shared data model and API: Instrument/Future/Option/Exchange, bar/tick/settlement/margin/fee DTOs, revision record DTOs | nothing (bottom of the DAG) |
| joseph-dal (host + plugins) | public | data boundary, capabilities, preflight, revisions | cnequity, akshare, vn.py (sources); dal-tsl (private vendor provider) |
| joseph-alpha (host + alpha-lite) | public | factor/model/strategy definitions, batch and incremental backends | alpha-native (private) |
| joseph-mini | public | runtime, portfolio, account, OMS, hard-risk, day-engine, simulator contract | none; single JO execution authority |
| joseph-pilot | public | vectorbt experiments, no live | vectorbt; unrelated to the trading core |
| joseph-live | public | live runtime on mini's live-engine | vn.py EventEngine, gateways, report normalization (never the order owner) |
| joseph-native | private | tick simulator kernel | implements mini's public simulator contract |
| joseph-alpha-native | private | accelerated alpha backend | implements alpha's public backend protocol |

Conventions:

- `joseph-api` imports nothing from other joseph packages; every package (dal, alpha, pilot, mini, live and the private backends) may import it. The DAL interface and preflight live in joseph-dal; canonical JO order commands live in joseph-mini; factor definitions live in joseph-alpha.

- `-native` = private repository implementing a public host contract, admitted only after passing
  the host's public equivalence vectors (exact for discrete outputs, declared tolerance for floats).
- pilot and mini share no code; the only shared substrate is a pinned revision. Promotion is
  re-implementation through a migration skill, never an equivalence claim.
- Public claims stand on public layers only; results produced with a private backend are private.
