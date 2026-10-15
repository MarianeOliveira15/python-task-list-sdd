# task-list-cli Specification

## Purpose

Esta capability permite gerenciar tarefas pessoais por uma interface de linha de comando em Python, mantendo a lista local disponível entre diferentes execuções.

## Requirements

### Requirement: Adicionar uma tarefa
A CLI SHALL criar e persistir uma nova tarefa com identificador único e status não concluído quando receber uma descrição não vazia.

#### Scenario: Adicionar uma tarefa
- **WHEN** o usuário adiciona uma tarefa com descrição não vazia
- **THEN** a CLI cria uma tarefa não concluída, atribui um identificador único, persiste a tarefa e informa o identificador

#### Scenario: Adicionar uma tarefa vazia
- **WHEN** o usuário adiciona uma descrição que contém apenas espaços em branco
- **THEN** a CLI informa um erro de entrada e não cria a tarefa

### Requirement: Listar tarefas
A CLI SHALL exibir o identificador, a descrição e o status de conclusão de cada tarefa armazenada.

#### Scenario: Listar tarefas existentes
- **WHEN** o usuário lista as tarefas e há tarefas cadastradas
- **THEN** a CLI exibe cada tarefa com seu identificador, descrição e indicação se está pendente ou concluída

#### Scenario: Listar uma lista vazia
- **WHEN** o usuário lista as tarefas e não há nenhuma cadastrada
- **THEN** a CLI informa que não há tarefas

### Requirement: Exibir mensagens em português
A CLI SHALL apresentar suas mensagens voltadas ao usuário em português, incluindo mensagens de sucesso e erro e a ajuda dos comandos.

#### Scenario: Exibir retorno dos comandos
- **WHEN** a CLI exibe ajuda, confirmação de sucesso ou erro
- **THEN** a mensagem gerada pela CLI está em português

### Requirement: Concluir uma tarefa
A CLI SHALL marcar uma tarefa como concluída quando o usuário fornecer seu identificador ou um prefixo que corresponda a exatamente uma tarefa.

#### Scenario: Concluir tarefa por prefixo de identificador
- **WHEN** o usuário conclui uma tarefa usando seu identificador completo ou um prefixo que corresponda a exatamente uma tarefa
- **THEN** a tarefa é marcada como concluída, a alteração é persistida e a CLI confirma a conclusão

#### Scenario: Concluir tarefa com prefixo desconhecido
- **WHEN** o usuário tenta concluir uma tarefa usando um prefixo que não corresponde a nenhuma tarefa
- **THEN** a CLI informa em português que nenhuma tarefa corresponde e mantém as tarefas armazenadas inalteradas

#### Scenario: Concluir tarefa com prefixo ambíguo
- **WHEN** o usuário tenta concluir uma tarefa usando um prefixo que corresponde a mais de uma tarefa
- **THEN** a CLI informa em português que o prefixo é ambíguo e mantém as tarefas armazenadas inalteradas

### Requirement: Persistir tarefas localmente
A CLI SHALL manter descrições, identificadores e status de conclusão das tarefas em armazenamento JSON local entre invocações separadas.

#### Scenario: Recarregar tarefas persistidas
- **WHEN** a CLI inicia após tarefas terem sido salvas por uma invocação anterior
- **THEN** essas tarefas estão disponíveis com suas descrições e status de conclusão previamente salvos
