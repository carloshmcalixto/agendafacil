# 7. Plano e relatório de testes (verificação e validação)

## 7.1 Estratégia

| Nível | Ferramenta | O que verifica | Arquivo |
|---|---|---|---|
| Unitário | pytest | Regras de negócio de cada Model | `tests/test_cliente.py`, `test_servico.py`, `test_agendamento.py` |
| Integração | pytest + `app.test_client()` | Rotas, telas, Model e banco juntos | `tests/test_rotas.py` |
| Validação | Formulário com 5 usuários | Uso real e usabilidade | `02-formulario-teste-usuario.md` |

Cada teste roda num banco SQLite **novo e temporário** (fixture `app` em `tests/conftest.py`), então os
testes não interferem entre si nem no banco real. As datas são fixadas (`agora=datetime(2030, 1, 1)`)
para que o resultado não dependa do dia em que o teste é executado.

## 7.2 Casos de teste principais (rastreabilidade)

| ID | Regra | Caso | Resultado esperado | Teste automatizado | Status |
|---|---|---|---|---|---|
| CT01 | RN01 | Nome com 2 letras | Recusa: "Nome deve ter pelo menos 3 caracteres." | `test_nome_curto_e_rejeitado` | ✅ |
| CT02 | RN01 | Telefone "123" | Recusa: telefone inválido | `test_telefone_invalido_e_rejeitado` | ✅ |
| CT03 | RN02 | E-mail repetido (maiúsculas diferentes) | Recusa | `test_email_duplicado_e_rejeitado` | ✅ |
| CT04 | RN03 | Preço "0" ou "-10" | Recusa | `test_preco_invalido` | ✅ |
| CT05 | RN03 | Preço "29,90" | Aceita como 29.90 | `test_cria_servico_aceitando_virgula_no_preco` | ✅ |
| CT06 | RN04 | Agendar no passado | Recusa: "data/hora futura" | `test_rejeita_data_passada` | ✅ |
| CT07 | RN05 | Domingo | Recusa | `test_rejeita_domingo` | ✅ |
| CT08 | RN05 | 17:45 com serviço de 30 min | Recusa (terminaria 18:15) | `test_rejeita_fora_do_expediente` | ✅ |
| CT09 | RN05 | 17:30 com serviço de 30 min | Aceita (valor-limite) | `test_ultimo_horario_possivel` | ✅ |
| CT10 | RN06 | 10:15 com outro às 10:00 (30 min) | Recusa: conflito | `test_rejeita_conflito_de_horario` | ✅ |
| CT11 | RN06 | 10:30 logo após 10:00–10:30 | Aceita (intervalos encostados) | `test_horario_encostado_nao_e_conflito` | ✅ |
| CT12 | RN06 | Reagendar horário cancelado | Aceita | `test_cancelado_libera_horario` | ✅ |
| CT13 | RN07 | Cancelar um agendamento concluído | Recusa | `test_nao_altera_agendamento_ja_concluido` | ✅ |
| CT14 | RN08 | Excluir cliente com agendamento | Recusa | `test_nao_exclui_cliente_com_agendamento` | ✅ |
| CT15 | RN09 | Agendar serviço inativo | Recusa | `test_rejeita_servico_inativo` | ✅ |
| CT16 | RF08 | Indicadores do painel | total 3, faturado 40, previsto 80 | `test_resumo_do_dia` | ✅ |
| CT17 | RF01–RF07 | Fluxo cliente → serviço → agendar → concluir pela interface | Mensagens de sucesso | `test_fluxo_completo_de_agendamento` | ✅ |
| CT18 | RNF03 | Formulário inválido | Mostra erros e mantém dados digitados | `test_formulario_mostra_erros_de_validacao` | ✅ |
| CT19 | RNF03 | URL inexistente | Página 404 amigável | `test_pagina_inexistente_mostra_404_amigavel` | ✅ |

Técnicas usadas: **partição de equivalência** (válido e inválido), **análise de valor-limite** (17:30 e
17:45; 4 e 5 min; 480 e 481 min) e **teste baseado em fluxo** (CT17).

## 7.3 Execução

```
$ python -m pytest -v
tests/test_agendamento.py::test_agendamento_valido PASSED                [  2%]
tests/test_agendamento.py::test_aceita_formato_do_input_datetime_local PASSED [  4%]
tests/test_agendamento.py::test_rejeita_data_passada PASSED              [  6%]
tests/test_agendamento.py::test_rejeita_domingo PASSED                   [  8%]
tests/test_agendamento.py::test_rejeita_fora_do_expediente[07:30] PASSED [ 11%]
tests/test_agendamento.py::test_rejeita_fora_do_expediente[17:45] PASSED [ 13%]
tests/test_agendamento.py::test_rejeita_fora_do_expediente[18:00] PASSED [ 15%]
tests/test_agendamento.py::test_ultimo_horario_possivel PASSED           [ 17%]
tests/test_agendamento.py::test_rejeita_conflito_de_horario PASSED       [ 20%]
tests/test_agendamento.py::test_horario_encostado_nao_e_conflito PASSED  [ 22%]
tests/test_agendamento.py::test_cancelado_libera_horario PASSED          [ 24%]
tests/test_agendamento.py::test_rejeita_servico_inativo PASSED           [ 26%]
tests/test_agendamento.py::test_rejeita_cliente_inexistente PASSED       [ 28%]
tests/test_agendamento.py::test_rejeita_data_invalida PASSED             [ 31%]
tests/test_agendamento.py::test_nao_altera_agendamento_ja_concluido PASSED [ 33%]
tests/test_agendamento.py::test_resumo_do_dia PASSED                     [ 35%]
tests/test_agendamento.py::test_data_invalida_mostra_todos_os_erros PASSED [ 37%]
tests/test_cliente.py::test_cria_cliente_valido PASSED                   [ 40%]
tests/test_cliente.py::test_nome_curto_e_rejeitado PASSED                [ 42%]
tests/test_cliente.py::test_telefone_invalido_e_rejeitado[123] PASSED    [ 44%]
tests/test_cliente.py::test_telefone_invalido_e_rejeitado[(11) 1234] PASSED [ 46%]
tests/test_cliente.py::test_telefone_invalido_e_rejeitado[abc] PASSED    [ 48%]
tests/test_cliente.py::test_telefone_invalido_e_rejeitado[] PASSED       [ 51%]
tests/test_cliente.py::test_email_invalido_e_rejeitado PASSED            [ 53%]
tests/test_cliente.py::test_email_duplicado_e_rejeitado PASSED           [ 55%]
tests/test_cliente.py::test_busca_por_nome PASSED                        [ 57%]
tests/test_cliente.py::test_atualiza_cliente PASSED                      [ 60%]
tests/test_cliente.py::test_nao_exclui_cliente_com_agendamento PASSED    [ 62%]
tests/test_cliente.py::test_exclui_cliente_sem_agendamento PASSED        [ 64%]
tests/test_rotas.py::test_paginas_principais_abrem PASSED                [ 66%]
tests/test_rotas.py::test_pagina_inexistente_mostra_404_amigavel PASSED  [ 68%]
tests/test_rotas.py::test_fluxo_completo_de_agendamento PASSED           [ 71%]
tests/test_rotas.py::test_formulario_mostra_erros_de_validacao PASSED    [ 73%]
tests/test_rotas.py::test_editar_cliente_inexistente_retorna_404 PASSED  [ 75%]
tests/test_servico.py::test_cria_servico_aceitando_virgula_no_preco PASSED [ 77%]
tests/test_servico.py::test_preco_invalido[0] PASSED                     [ 80%]
tests/test_servico.py::test_preco_invalido[-10] PASSED                   [ 82%]
tests/test_servico.py::test_preco_invalido[abc] PASSED                   [ 84%]
tests/test_servico.py::test_preco_invalido[] PASSED                      [ 86%]
tests/test_servico.py::test_duracao_invalida[0] PASSED                   [ 88%]
tests/test_servico.py::test_duracao_invalida[4] PASSED                   [ 91%]
tests/test_servico.py::test_duracao_invalida[481] PASSED                 [ 93%]
tests/test_servico.py::test_duracao_invalida[x] PASSED                   [ 95%]
tests/test_servico.py::test_nome_duplicado PASSED                        [ 97%]
tests/test_servico.py::test_desativar_remove_da_lista_de_ativos PASSED   [100%]
============================== 45 passed in 0.61s ==============================
```

Saída real da execução em 13/11/2026 (Python 3, pytest 8).
