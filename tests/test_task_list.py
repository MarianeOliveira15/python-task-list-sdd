import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from task_list import (
    AmbiguousTaskError,
    TaskList,
    TaskNotFoundError,
    TaskStorageError,
)


class TaskListTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.path = Path(self.directory.name) / "nested" / "tasks.json"
        self.task_list = TaskList(self.path)

    def tearDown(self) -> None:
        self.directory.cleanup()

    def test_adds_and_reloads_incomplete_task(self) -> None:
        task = self.task_list.add_task("Estudar Python")

        self.assertTrue(task.id)
        self.assertFalse(task.completed)
        self.assertEqual([task], self.task_list.list_tasks())

    def test_completes_task_by_unique_id_prefix_and_reloads(self) -> None:
        task = self.task_list.add_task("Estudar Python")

        completed = self.task_list.complete_task(task.id[:8])

        self.assertTrue(completed.completed)
        self.assertTrue(self.task_list.list_tasks()[0].completed)

    def test_unknown_or_ambiguous_prefix_does_not_change_file(self) -> None:
        self.path.parent.mkdir(parents=True)
        self.path.write_text(
            json.dumps(
                [
                    {"id": "abc-1", "description": "Primeira", "completed": False},
                    {"id": "abc-2", "description": "Segunda", "completed": False},
                ]
            ),
            encoding="utf-8",
        )
        original = self.path.read_text(encoding="utf-8")

        with self.assertRaises(TaskNotFoundError):
            self.task_list.complete_task("missing")
        with self.assertRaises(AmbiguousTaskError):
            self.task_list.complete_task("abc")

        self.assertEqual(original, self.path.read_text(encoding="utf-8"))

    def test_missing_file_represents_empty_task_list(self) -> None:
        self.assertEqual([], self.task_list.list_tasks())


class InvalidStorageTests(unittest.TestCase):
    def test_unreadable_file_reports_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            task_list = TaskList(path)

            with patch.object(Path, "open", side_effect=PermissionError("acesso negado")):
                with self.assertRaisesRegex(TaskStorageError, "Não foi possível ler"):
                    task_list.add_task("Nova tarefa")

            self.assertFalse(path.exists())

    def test_invalid_json_reports_error_without_overwriting_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            original = "{not valid json"
            path.write_text(original, encoding="utf-8")
            task_list = TaskList(path)

            with self.assertRaisesRegex(TaskStorageError, "JSON inválido"):
                task_list.add_task("Nova tarefa")

            self.assertEqual(original, path.read_text(encoding="utf-8"))

    def test_invalid_utf8_reports_error_without_overwriting_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            original = b"\xff"
            path.write_bytes(original)
            task_list = TaskList(path)

            with self.assertRaisesRegex(TaskStorageError, "JSON inválido"):
                task_list.add_task("Nova tarefa")

            self.assertEqual(original, path.read_bytes())

    def test_invalid_task_record_reports_error_without_overwriting_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            original = '[{"id": "x", "description": "Tarefa", "completed": "não"}]'
            path.write_text(original, encoding="utf-8")
            task_list = TaskList(path)

            with self.assertRaisesRegex(TaskStorageError, "formato inválido"):
                task_list.add_task("Nova tarefa")

            self.assertEqual(original, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
