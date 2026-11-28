"""Check documentation scope, size, and public keyword policy."""

from pathlib import Path

from check_keywords import check


DOC_DIRECTORIES = (
    "architecture", "contracts", "guides", "reference", "rules", "packages",
    "contributing", "templates",
)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    allowed = {
        line.strip()
        for line in (root / "public-layer.allow").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    actual = {
        path.relative_to(root).as_posix()
        for directory in DOC_DIRECTORIES
        for path in (root / directory).rglob("*.md")
        if path.is_file()
    }
    if (root / "README.md").is_file():
        actual.add("README.md")

    extra = sorted(actual - allowed)
    missing = sorted(allowed - actual)
    long = sorted(
        path for path in actual
        if len((root / path).read_text(encoding="utf-8").splitlines()) > 200
    )
    for heading, paths in (
        ("Files in the public layer that are not whitelisted:", extra),
        ("Whitelisted files missing from the public layer:", missing),
        ("Public markdown files over 200 lines:", long),
    ):
        if paths:
            print(f"{heading} {len(paths)}")

    keyword_status = check(root / "keywords" / "public-boundary.txt", root)
    return max(int(bool(extra or missing or long)), keyword_status)


if __name__ == "__main__":
    raise SystemExit(main())
