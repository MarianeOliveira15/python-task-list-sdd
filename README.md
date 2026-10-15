# Lista de tarefas em linha de comando

Aplicativo simples em Python para adicionar, listar e concluir tarefas. Não requer instalação de dependências: basta ter Python disponível.

## Uso

Na pasta do projeto, execute:

```powershell
python todo.py add "Estudar Python"
python todo.py list
```

O comando `add` mostra o ID da tarefa criada. Para concluí-la, informe o ID completo ou um prefixo que identifique uma única tarefa:

```powershell
python todo.py complete 550e8400
```

Substitua `550e8400` por um prefixo do ID mostrado pelo comando `add`. Se nenhum ID ou mais de um ID corresponder ao prefixo, a CLI informa o problema e não altera as tarefas. Para ver todos os comandos e opções, execute `python todo.py --help`.

## Armazenamento

As tarefas são mantidas entre execuções no arquivo JSON `~/.task-list/tasks.json`, dentro do diretório pessoal do usuário. O diretório e o arquivo são criados ao adicionar a primeira tarefa.
