import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="p3 install ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.repo = self.root / "source repo"
        self.home = self.root / "home"
        self.target = self.home / ".agents/skills"
        self.target.mkdir(parents=True)
        self.skill = self.repo / "skills/example"
        self.skill.mkdir(parents=True)
        (self.skill / "SKILL.md").write_text("---\nname: example\ndescription: Example.\n---\n")
        self.script = self.repo / "install.sh"
        shutil.copyfile(Path(__file__).resolve().parents[1] / "install.sh", self.script)

    def run_install(self, *args):
        return subprocess.run(
            ["bash", str(self.script), *map(str, args)],
            env={**os.environ, "HOME": str(self.home)},
            capture_output=True,
            text=True,
        )

    def test_preserves_another_installation_by_default(self):
        existing = self.target / "example"
        existing.symlink_to(self.root / "missing old installation")
        result = self.run_install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(existing.readlink(), self.root / "missing old installation")

    def test_replace_backs_up_directory_and_is_safe_to_repeat(self):
        existing = self.target / "example"
        existing.mkdir()
        (existing / "personal.md").write_text("keep this")
        result = self.run_install("--replace")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(existing.is_symlink())
        self.assertEqual(existing.resolve(), self.skill)
        backups = list((self.home / ".agents/skill-backups").glob("*/example/personal.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "keep this")
        first_link = existing.lstat()
        result = self.run_install("--replace")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(existing.lstat().st_mtime_ns, first_link.st_mtime_ns)
        self.assertEqual(len(list(backups[0].parents[2].glob("*/example/personal.md"))), 1)

    def test_replace_preserves_the_original_symlink(self):
        existing = self.target / "example"
        existing.symlink_to("../../previous skill")
        result = self.run_install("--replace")
        self.assertEqual(result.returncode, 0, result.stderr)
        backups = list((self.home / ".agents/skill-backups").iterdir())
        self.assertEqual(len(backups), 1)
        self.assertEqual(str((backups[0] / "example").readlink()), "../../previous skill")
        self.assertEqual(existing.resolve(), self.skill)

    def test_project_path_with_spaces(self):
        project = self.root / "client project"
        result = self.run_install("--project", project)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((project / ".agents/skills/example").resolve(), self.skill)
        self.assertFalse((self.target / "example").exists())

    def test_codex_links_to_the_same_source(self):
        result = self.run_install("--codex")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.home / ".codex/skills/example").resolve(), self.skill)
        self.assertFalse((self.target / "example").exists())

    def test_claude_links_to_the_same_source(self):
        result = self.run_install("--claude")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.home / ".claude/skills/example").resolve(), self.skill)
        self.assertFalse((self.target / "example").exists())

    def test_accepts_a_link_from_the_previous_installer(self):
        existing = self.target / "example"
        existing.symlink_to(str(self.skill) + "/")
        first_link = existing.lstat()
        self.assertEqual(self.run_install("--check").returncode, 0)
        self.assertEqual(self.run_install("--replace").returncode, 0)
        self.assertEqual(existing.lstat().st_mtime_ns, first_link.st_mtime_ns)
        self.assertFalse((self.home / ".agents/skill-backups").exists())

    def test_unknown_arguments_do_not_install(self):
        result = self.run_install("--unknown")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.target / "example").exists())

    def test_missing_project_does_not_install(self):
        result = self.run_install("--project")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.target / "example").exists())

    def test_check_verifies_links_without_changing_them(self):
        self.assertNotEqual(self.run_install("--check").returncode, 0)
        self.assertFalse((self.target / "example").exists())
        self.assertEqual(self.run_install().returncode, 0)
        self.assertEqual(self.run_install("--check").returncode, 0)
        (self.target / "example").unlink()
        self.assertNotEqual(self.run_install("--check").returncode, 0)


if __name__ == "__main__":
    unittest.main()
