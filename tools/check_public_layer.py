import pathlib, sys
root = pathlib.Path(__file__).resolve().parents[1]
allowed = {l.strip() for l in (root / "public-layer.allow").read_text().splitlines() if l.strip() and not l.startswith("#")}
actual = {p.relative_to(root).as_posix() for d in ("architecture", "contracts", "guides", "reference", "rules", "packages", "contributing", "templates") for p in (root / d).rglob("*.md")} if (root / "reference").exists() or True else set()
extra = sorted(actual - allowed)
missing = sorted(allowed - actual)
if extra:
    print("Files in the public layer that are not whitelisted:")
    [print("  ", p) for p in extra]
if missing:
    print("Whitelisted files missing from the public layer:")
    [print("  ", p) for p in missing]
long = sorted(p for p in actual if (root / p).read_text(encoding="utf-8").count("\n") + 1 > 200)
if long:
    print("Public markdown files over 200 lines (keep the public layer thin):")
    [print("  ", p) for p in long]
scanned = []
for d in ("architecture", "contracts", "guides", "reference", "rules", "packages", "contributing", "templates"):
    for p in (root / d).rglob("*"):
        if p.is_file() and p.suffix in {".md", ".py", ".txt", ".yaml", ".yml", ".toml"} and "keywords" not in p.parts:
            scanned.append(p)
terms = []
for k in (root / "keywords").glob("*.txt"):
    for line in k.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            terms.append((k.name, line.lower()))
hits = []
for p in scanned:
    text = p.read_text(encoding="utf-8", errors="ignore").lower()
    for kname, term in terms:
        if term in text:
            hits.append((p.relative_to(root).as_posix(), term))
if hits:
    print("Keyword hits (proprietary strategy / vendor / private path):")
    [print("  ", f"{p}: {t}") for p, t in hits]
sys.exit(1 if extra or missing or long or hits else 0)
