---
name: sdd-review
description: Use para revisar se uma change OpenSpec, o diff e as validações estão alinhados antes de arquivar.
---

# SDD Review

**Escopo:** revisar o alinhamento entre os artefatos de uma change e o código. Não corrige nada.

**Entradas:** a change OpenSpec indicada e o diff atual da branch.

**Workflow** (quando esta skill for usada):

1. Leia a change OpenSpec indicada pelo usuário.
2. Compare `proposal.md`, `design.md`, `tasks.md` e specs delta com o diff atual.
3. Verifique se cada task marcada tem evidência de validação.
4. Aponte drift, escopo vazado, critério sem teste ou gap não registrado.
5. Responda com findings priorizados e próximos passos.

**Saídas:** findings priorizados (arquivo, severidade, recomendação) e um veredito "pode arquivar?" sim/não.

**Como validar:** cada finding aponta um arquivo ou task concreto; sem evidência objetiva, o item vira dúvida a confirmar, não afirmação.

**Limites:** não implemente mudanças. Esta skill í somente de revisão.