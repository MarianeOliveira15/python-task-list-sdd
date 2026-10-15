import json
import os
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from uuid import uuid4


class TaskStorageError(Exception):
    pass


class TaskNotFoundError(TaskStorageError):
    def __init__(self, identifier: str) -> None:
        super().__init__(f"Nenhuma tarefa corresponde ao identificador '{identifier}'.")


class AmbiguousTaskError(TaskStorageError):
    def __init__(self, identifier: str) -> None:
        super().__init__(f"O identificador '{identifier}' corresponde a mais de uma tarefa.")


@dataclass
class Task:
    id: str
    description: str
    completed: bool = False


class TaskList:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path.home() / ".task-list" / "tasks.json"

    def list_tasks(self) -> list[Task]:
        return self._load()

    def add_task(self, description: str) -> Task:
        task = Task(id=str(uuid4()), description=description)
        tasks = self._load()
        tasks.append(task)
        self._save(tasks)
        return task

    def complete_task(self, identifier: str) -> Task:
        tasks = self._load()
        matches = [task for task in tasks if task.id.startswith(identifier)]
        if not matches:
            raise TaskNotFoundError(identifier)
        if len(matches) > 1:
            raise AmbiguousTaskError(identifier)

        task = matches[0]
        task.completed = True
        self._save(tasks)
        return task

    def _load(self) -> list[Task]:
        try:
            with self.path.open(encoding="utf-8") as task_file:
                records = json.load(task_file)
        except FileNotFoundError:
            return []
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise TaskStorageError(
                "O arquivo de tarefas contém JSON inválido ou codificação não UTF-8."
            ) from error
        except OSError as error:
            raise TaskStorageError(f"Não foi possível ler as tarefas: {error}") from error

        if not isinstance(records, list):
            raise TaskStorageError("O arquivo de tarefas deve conter uma lista JSON.")

        tasks = []
        for record in records:
            if (
                not isinstance(record, dict)
                or set(record) != {"id", "description", "completed"}
                or not isinstance(record.get("id"), str)
                or not isinstance(record.get("description"), str)
                or not isinstance(record.get("completed"), bool)
            ):
                raise TaskStorageError("O arquivo contém uma tarefa em formato inválido.")
            tasks.append(Task(**record))
        return tasks

    def _save(self, tasks: list[Task]) -> None:
        temporary_path: Path | None = None
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.path.parent,
                prefix=f".{self.path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)
                json.dump([asdict(task) for task in tasks], temporary_file, ensure_ascii=False, indent=2)
                temporary_file.write("\n")
            os.replace(temporary_path, self.path)
        except OSError as error:
            raise TaskStorageError(f"Não foi possível salvar as tarefas: {error}") from error
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()
