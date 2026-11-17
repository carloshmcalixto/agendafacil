# 9. Laudo de qualidade

**Sistema:** AgendaFácil · **Responsável:** Carlos Henrique Mathias Calixto (RGM 36910767)

## A. Verificação (testes automatizados)

| Item | Resultado |
|---|---|
| Testes executados | 54 (45 da versão 1.0 + 9 do backup, versão 1.1) |
| Aprovados | 54 (100%) |
| Regras de negócio cobertas | RN01 a RN09 e RF09 (backup) |
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
| 1 | Gustavo Silva e Enzo Carlo | Falta de backup dos dados do sistema | Nova funcionalidade (não é defeito) | Média | **Implementada na versão 1.1**: menu Backup com "Baixar backup" (arquivo JSON) e "Restaurar backup", com 9 testes automatizados |

### Sugestões não adotadas

Não houve outras sugestões além do backup.

## D. Conclusão

Os testes automatizados (45 de 45 aprovados) e a validação com 5 usuários não encontraram defeitos.
As funcionalidades testadas (cadastro de clientes e serviços, agendamentos em vários dias e bloqueio de
conflito de horário) funcionaram como esperado. A única sugestão recebida, o backup dos dados, apareceu
em 2 dos 5 relatos e foi implementada na versão 1.1: o menu **Backup** permite baixar todos os dados em um
arquivo JSON e restaurá-los depois. A restauração valida o arquivo e roda em uma única transação, então um
arquivo inválido não altera os dados atuais. Com isso, o sistema passou a ter 54 testes automatizados, todos aprovados.
