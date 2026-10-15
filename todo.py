import argparse
import sys
from collections.abc import Sequence

from task_list import TaskList, TaskStorageError


class PortugueseArgumentParser(argparse.ArgumentParser):
    def format_help(self) -> str:
        return self._translate(super().format_help())

    def format_usage(self) -> str:
        return self._translate(super().format_usage())

    def error(self, message: str) -> None:
        message = self._translate(message)
        self.print_usage(sys.stderr)
        self.exit(2, f"{self.prog}: erro: {message}\n")

    @staticmethod
    def _translate(message: str) -> str:
        translations = {
            "usage:": "uso:",
            "positional arguments": "argumentos posicionais",
            "options": "opções",
            "show this help message and exit": "mostra esta mensagem de ajuda e sai",
            "the following arguments are required:": "os seguintes argumentos são obrigatórios:",
            "unrecognized arguments:": "argumentos não reconhecidos:",
            "invalid choice:": "opção inválida:",
        }
        for source, translation in translations.items():
            message = message.replace(source, translation)
        return message


def build_parser() -> argparse.ArgumentParser:
    parser = PortugueseArgumentParser(
        prog="todo",
        description="Adicione, liste e conclua suas tarefas.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True, title="comandos")

    add_parser = subparsers.add_parser("add", help="adiciona uma tarefa")
    add_parser.add_argument("description", metavar="DESCRIÇÃO", help="descrição da tarefa")

    subparsers.add_parser("list", help="lista todas as tarefas")

    complete_parser = subparsers.add_parser("complete", help="conclui uma tarefa pelo ID ou prefixo")
    complete_parser.add_argument("identifier", metavar="ID", help="ID completo ou prefixo único da tarefa")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    arguments = parser.parse_args(argv)
    task_list = TaskList()

    try:
        if arguments.command == "add":
            if not arguments.description.strip():
                print("Erro: A descrição da tarefa não pode ficar vazia.", file=sys.stderr)
                return 2
            task = task_list.add_task(arguments.description)
            print(f"Tarefa adicionada. ID: {task.id}")
        elif arguments.command == "list":
            tasks = task_list.list_tasks()
            if not tasks:
                print("Nenhuma tarefa cadastrada.")
                return 0
            for task in tasks:
                status = "Concluída" if task.completed else "Pendente"
                print(f"{task.id} | {status} | {task.description}")
        else:
            task = task_list.complete_task(arguments.identifier)
            print(f"Tarefa marcada como concluída: {task.description}")
    except TaskStorageError as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
