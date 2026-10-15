# Design

## Context

O repositório ainda não contém código de aplicação nem convenções de empacotamento. A capability e seus comportamentos estão definidos em `specs/task-list-cli/spec.md`. A solução pode usar apenas a biblioteca padrão do Python.

## Goals / Non-Goals

**Goals:**
- Manter a interface simples de executar diretamente com Python e previsível nos sistemas suportados pelo próprio Python.
- Preservar os dados sem depender de serviços ou instalação de pacotes.
- Reportar falhas de leitura e gravação sem substituir dados existentes silenciosamente.

**Non-Goals:**
- Sincronização entre máquinas, interface gráfica ou serviço de backend.
- Edição, remoção, prazos ou categorização de tarefas.

## Decisions

- Usar `argparse` com subcomandos `add`, `list` e `complete`, em um ponto de entrada `todo.py`. Isso mantém o uso simples (`python todo.py add "..."`) e evita dependências; uma CLI externa/framework adicionaria custo sem necessidade para este escopo. Toda a saída gerada pela CLI, incluindo ajuda, erros e confirmações, será em português; descrições digitadas pelo usuário permanecem inalteradas.
- Salvar os dados em `~/.task-list/tasks.json`, expandindo o diretório pessoal com `pathlib`. Um arquivo no diretório de execução poderia variar conforme o terminal e misturar dados com projetos; armazenamento em nuvem ou banco de dados seria desnecessário para uma lista local.
- Representar cada tarefa como um objeto JSON com identificador UUID, descrição e indicador booleano de conclusão. O arquivo ausente representa uma lista vazia; JSON inválido ou inacessível deve produzir erro explícito, sem redefinir a lista.
- Ao concluir, comparar o argumento recebido com o início dos identificadores armazenados. Prosseguir somente quando houver exatamente uma correspondência; para nenhuma ou múltiplas correspondências, informar em português e não alterar os dados. Isso permite abreviar UUIDs sem concluir uma tarefa errada; exigir sempre o ID completo seria menos conveniente.
- Gravar alterações por arquivo temporário no mesmo diretório seguido de substituição atômica, reduzindo o risco de deixar o arquivo parcialmente escrito. A implementação deve criar o diretório de dados quando necessário.

## Risks / Trade-offs

- [O arquivo JSON pode ser editado ou corrompido externamente] → Informar claramente falhas de leitura e não sobrescrever o conteúdo inválido.
- [As tarefas existem apenas no perfil local do usuário] → Isso é intencional para evitar dependências e exposição de dados; sincronização fica fora do escopo.

## Migration Plan

Não há migração: a capability é nova. O diretório e o arquivo JSON serão criados quando a primeira tarefa for salva.
