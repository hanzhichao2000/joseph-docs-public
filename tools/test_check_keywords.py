import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCANNER = Path(__file__).with_name("check_keywords.py")


class PublicKeywordCheckTest(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        self.policy = self.root / "policy.txt"
        self.marker = "example-" + "local"
        self.policy.write_text(f"# public rules\n{self.marker}\n", encoding="utf-8")

    def track(self, path: Path) -> None:
        subprocess.run(
            ["git", "-C", str(self.root), "add", "--", str(path)],
            check=True,
        )

    def run_scan(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCANNER), str(self.policy), str(self.root)],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_policy_and_untracked_outputs_are_not_scanned(self) -> None:
        self.track(self.policy)
        (self.root / "local-cache.txt").write_text(self.marker, encoding="utf-8")
        self.assertEqual(self.run_scan().returncode, 0)

    def test_reports_matches_without_logging_paths_or_contents(self) -> None:
        readme = self.root / "README.md"
        readme.write_text(self.marker.upper(), encoding="utf-8")
        self.track(readme)
        matching_path = self.root / f"{self.marker}.txt"
        matching_path.write_text("example", encoding="utf-8")
        self.track(matching_path)
        result = self.run_scan()
        self.assertEqual(result.returncode, 1)
        self.assertIn("1 path, 1 text matches", result.stderr)
        self.assertNotIn(self.marker.lower(), result.stderr.lower())
        self.assertNotIn("README.md", result.stderr)

    def test_reads_working_tree_content_for_indexed_paths(self) -> None:
        path = self.root / "example.txt"
        path.write_text(self.marker, encoding="utf-8")
        self.track(path)
        path.write_text("clean", encoding="utf-8")
        self.assertEqual(self.run_scan().returncode, 0)
        self.track(path)
        path.write_text(self.marker, encoding="utf-8")
        self.assertEqual(self.run_scan().returncode, 1)

    def test_scans_symlink_target_text(self) -> None:
        link = self.root / "link"
        os.symlink(self.marker, link)
        self.track(link)
        result = self.run_scan()
        self.assertEqual(result.returncode, 1)
        self.assertIn("0 path, 1 text matches", result.stderr)

    def test_fails_for_a_missing_or_empty_policy(self) -> None:
        self.policy.unlink()
        for label in ("missing", "empty"):
            with self.subTest(label=label):
                if label == "empty":
                    self.policy.write_text("# no active rules\n", encoding="utf-8")
                result = self.run_scan()
                self.assertEqual(result.returncode, 2)
                self.assertIn("public keyword list", result.stderr)


if __name__ == "__main__":
    unittest.main()
