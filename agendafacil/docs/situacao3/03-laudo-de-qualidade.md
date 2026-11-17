# 9. Laudo de qualidade

**Sistema:** AgendaFácil · **Responsável:** Carlos Henrique Mathias Calixto (RGM 36910767)

## A. Verificação (testes automatizados)

| Item | Resultado |
|---|---|
| Testes executados | 45 |
| Aprovados | 45 (100%) |
| Regras de negócio cobertas | RN01 a RN09 |
| Evidência | Saída do `pytest -v` em `01-plano-e-relatorio-de-testes.md` |

## B. Validação com usuários – resumo

| Testador | Data | O que testou e funcionou | Falhas relatadas | Não testado / faltou |
|---|---|---|---|---|
| Gabriel Ramos | 14/11/2026 | Inclusão de cliente e agendamento de horário | Nenhuma | — |
| Daniele Francisca | 14/11/2026 | Dois agendamentos no mesmo horário: o sistema bloqueou corretamente, informando conflito | Nenhuma | — |
| Gustavo Silva | 14/11/2026 | Inclusão de novos serviços | Nenhuma | Backup de segurança dos dados |
| Roseli Ramos | 15/11/2026 | Cadastro de várias pessoas, inclusive com o mesmo nome | Nenhuma | — |
| Enzo Carlo | 15/11/2026 | Vários agendamentos em vários dias | Nenhuma | Botão de backup |

## C. Erros encontrados e melhorias

Nenhum defeito foi relatado pelos 5 testadores.

| # | Relatado por | Descrição | Classificação | Prioridade | Status |
|---|---|---|---|---|---|
| 1 | Gustavo Silva e Enzo Carlo | Falta de backup dos dados do sistema | Nova funcionalidade (não é defeito) | Média | Registrada como melhoria para a próxima versão |

### Sugestões não adotadas

Não houve outras sugestões além do backup.

## D. Conclusão

Os testes automatizados (45 de 45 aprovados) e a validação com 5 usuários não encontraram defeitos.
As funcionalidades testadas (cadastro de clientes e serviços, agendamentos em vários dias e bloqueio de
conflito de horário) funcionaram como esperado. A única sugestão recebida, o backup dos dados, apareceu
em 2 dos 5 relatos e foi registrada como melhoria para a próxima versão.
