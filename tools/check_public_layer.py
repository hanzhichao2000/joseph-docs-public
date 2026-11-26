import pathlib, sys
root = pathlib.Path(__file__).resolve().parents[1]
allowed = {l.strip() for l in (root / "public-layer.allow").read_text().splitlines() if l.strip() and not l.startswith("#")}
actual = {p.relative_to(root).as_posix() for d in ("architecture", "contracts", "guides", "reference", "rules", "packages") for p in (root / d).rglob("*.md")} if (root / "reference").exists() or True else set()
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
sys.exit(1 if extra or missing or long else 0)
