import pathlib, sys
root = pathlib.Path(__file__).resolve().parents[1]
allowed = {l.strip() for l in (root / "public-layer.allow").read_text().splitlines() if l.strip() and not l.startswith("#")}
actual = {p.relative_to(root).as_posix() for d in ("architecture", "contracts", "guides", "reference", "rules") for p in (root / d).rglob("*.md")} if (root / "reference").exists() or True else set()
extra = sorted(actual - allowed)
missing = sorted(allowed - actual)
if extra:
    print("Files in the public layer that are not whitelisted:")
    [print("  ", p) for p in extra]
if missing:
    print("Whitelisted files missing from the public layer:")
    [print("  ", p) for p in missing]
sys.exit(1 if extra or missing else 0)
