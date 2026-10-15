# Proposal

## Why

Não há uma forma simples de registrar e acompanhar tarefas pelo terminal. Uma CLI em Python permitirá adicionar tarefas, consultar a lista e marcar itens concluídos, mantendo os dados entre execuções.

## What Changes

- Adicionar uma interface de linha de comando em Python com operações para adicionar, listar e concluir tarefas.
- Persistir as tarefas localmente em um arquivo JSON para que permaneçam disponíveis entre execuções.
- Atribuir identificadores às tarefas para que uma tarefa específica possa ser concluída.

## Capabilities

### New Capabilities
- `task-list-cli`: gerenciamento de tarefas por linha de comando, incluindo inclusão, listagem, conclusão e persistência local.

### Modified Capabilities
- Nenhuma.

## Impact

- Novo programa Python de linha de comando e armazenamento local em JSON.
- Sem dependências externas esperadas; o caminho do arquivo de dados e a sintaxe exata dos comandos serão definidos no design.
