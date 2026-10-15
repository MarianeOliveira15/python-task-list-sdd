import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TODO_SCRIPT = PROJECT_ROOT / "todo.py"


class TodoCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.home = Path(self.directory.name)
        self.environment = os.environ.copy()
        self.environment["HOME"] = str(self.home)
        self.environment["USERPROFILE"] = str(self.home)
        self.environment["PYTHONIOENCODING"] = "utf-8"

    def tearDown(self) -> None:
        self.directory.cleanup()

    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TODO_SCRIPT), *arguments],
            capture_output=True,
            check=False,
            cwd=PROJECT_ROOT,
            encoding="utf-8",
            env=self.environment,
        )

    def test_add_list_and_complete_by_prefix_across_invocations(self) -> None:
        added = self.run_cli("add", "Estudar Python")
        self.assertEqual(0, added.returncode, added.stderr)
        self.assertIn("Tarefa adicionada. ID: ", added.stdout)
        identifier = added.stdout.strip().split()[-1]

        listed = self.run_cli("list")
        self.assertIn(f"{identifier} | Pendente | Estudar Python", listed.stdout)

        completed = self.run_cli("complete", identifier[:8])
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("Tarefa marcada como concluída", completed.stdout)
        listed_again = self.run_cli("list")
        self.assertIn(f"{identifier} | Concluída | Estudar Python", listed_again.stdout)

    def test_empty_description_is_rejected_in_portuguese(self) -> None:
        result = self.run_cli("add", "   ")

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Erro:", result.stderr)
        self.assertIn("descrição", result.stderr)
        self.assertFalse((self.home / ".task-list" / "tasks.json").exists())

    def test_unknown_and_ambiguous_prefixes_are_reported_in_portuguese(self) -> None:
        data_path = self.home / ".task-list" / "tasks.json"
        data_path.parent.mkdir()
        data_path.write_text(
            json.dumps(
                [
                    {"id": "abc-1", "description": "Primeira", "completed": False},
                    {"id": "abc-2", "description": "Segunda", "completed": False},
                ]
            ),
            encoding="utf-8",
        )
        original = data_path.read_text(encoding="utf-8")

        unknown = self.run_cli("complete", "missing")
        ambiguous = self.run_cli("complete", "abc")

        self.assertNotEqual(0, unknown.returncode)
        self.assertIn("Nenhuma tarefa corresponde", unknown.stderr)
        self.assertNotEqual(0, ambiguous.returncode)
        self.assertIn("mais de uma tarefa", ambiguous.stderr)
        self.assertEqual(original, data_path.read_text(encoding="utf-8"))

    def test_empty_list_and_help_are_in_portuguese(self) -> None:
        listed = self.run_cli("list")
        help_result = self.run_cli("--help")
        missing_identifier = self.run_cli("complete")

        self.assertEqual("Nenhuma tarefa cadastrada.\n", listed.stdout)
        self.assertIn("uso:", help_result.stdout)
        self.assertIn("comandos", help_result.stdout)
        self.assertIn("mostra esta mensagem de ajuda e sai", help_result.stdout)
        self.assertNotIn("usage:", help_result.stdout)
        self.assertIn("obrigatórios", missing_identifier.stderr)
        self.assertNotIn("required", missing_identifier.stderr)

    def test_readme_command_examples_work_with_isolated_home(self) -> None:
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn('python todo.py add "Estudar Python"', readme)
        self.assertIn("python todo.py list", readme)
        self.assertIn("python todo.py complete 550e8400", readme)

        added = self.run_cli("add", "Estudar Python")
        identifier = added.stdout.strip().split()[-1]
        self.assertEqual(0, added.returncode, added.stderr)

        listed = self.run_cli("list")
        self.assertEqual(0, listed.returncode, listed.stderr)
        self.assertIn(f"{identifier} | Pendente | Estudar Python", listed.stdout)

        completed = self.run_cli("complete", identifier[:8])
        self.assertEqual(0, completed.returncode, completed.stderr)


if __name__ == "__main__":
    unittest.main()
