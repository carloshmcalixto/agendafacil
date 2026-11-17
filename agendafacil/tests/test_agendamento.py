"""Testes unitários das regras de negócio de Agendamento."""
from datetime import datetime

import pytest

from app.models import ValidacaoError
from app.models import agendamento, servico

AGORA = datetime(2030, 1, 1, 9, 0)          # terça-feira
SEGUNDA = "2030-01-07"                       # segunda-feira
DOMINGO = "2030-01-06"


def agendar(base, hora, dia=SEGUNDA):
    return agendamento.criar({**base, "data_hora": f"{dia} {hora}"}, agora=AGORA)


def test_agendamento_valido(dados_base):
    id_a = agendar(dados_base, "10:00")
    a = agendamento.buscar(id_a)
    assert a["status"] == "AGENDADO" and a["data_hora"] == f"{SEGUNDA} 10:00"


def test_aceita_formato_do_input_datetime_local(dados_base):
    id_a = agendamento.criar({**dados_base, "data_hora": f"{SEGUNDA}T11:00"}, agora=AGORA)
    assert agendamento.buscar(id_a)["data_hora"] == f"{SEGUNDA} 11:00"


def test_rejeita_data_passada(dados_base):
    with pytest.raises(ValidacaoError, match="futura"):
        agendamento.criar({**dados_base, "data_hora": "2029-12-31 10:00"}, agora=AGORA)


def test_rejeita_domingo(dados_base):
    with pytest.raises(ValidacaoError, match="domingos"):
        agendar(dados_base, "10:00", DOMINGO)


@pytest.mark.parametrize("hora", ["07:30", "17:45", "18:00"])
def test_rejeita_fora_do_expediente(dados_base, hora):
    # serviço de 30 min: 17:45 terminaria 18:15
    with pytest.raises(ValidacaoError, match="entre 08:00 e 18:00"):
        agendar(dados_base, hora)


def test_ultimo_horario_possivel(dados_base):
    assert agendar(dados_base, "17:30")


def test_rejeita_conflito_de_horario(dados_base):
    agendar(dados_base, "10:00")
    with pytest.raises(ValidacaoError, match="Já existe um agendamento"):
        agendar(dados_base, "10:15")


def test_horario_encostado_nao_e_conflito(dados_base):
    agendar(dados_base, "10:00")
    assert agendar(dados_base, "10:30")


def test_cancelado_libera_horario(dados_base):
    id_a = agendar(dados_base, "10:00")
    agendamento.alterar_status(id_a, "CANCELADO")
    assert agendar(dados_base, "10:00")


def test_rejeita_servico_inativo(dados_base):
    servico.alternar_ativo(dados_base["id_servico"])
    with pytest.raises(ValidacaoError, match="inativo"):
        agendar(dados_base, "10:00")


def test_rejeita_cliente_inexistente(dados_base):
    with pytest.raises(ValidacaoError, match="cliente válido"):
        agendamento.criar(
            {"id_cliente": "999", "id_servico": dados_base["id_servico"],
             "data_hora": f"{SEGUNDA} 10:00"}, agora=AGORA)


def test_rejeita_data_invalida(dados_base):
    with pytest.raises(ValidacaoError, match="Data/hora inválida"):
        agendamento.criar({**dados_base, "data_hora": "amanhã"}, agora=AGORA)


def test_nao_altera_agendamento_ja_concluido(dados_base):
    id_a = agendar(dados_base, "10:00")
    agendamento.alterar_status(id_a, "CONCLUIDO")
    with pytest.raises(ValidacaoError, match="em aberto"):
        agendamento.alterar_status(id_a, "CANCELADO")


def test_resumo_do_dia(dados_base):
    a1 = agendar(dados_base, "09:00")
    agendar(dados_base, "10:00")
    a3 = agendar(dados_base, "11:00")
    agendamento.alterar_status(a1, "CONCLUIDO")
    agendamento.alterar_status(a3, "CANCELADO")
    r = agendamento.resumo_do_dia(SEGUNDA)
    assert r == {"total": 3, "agendados": 1, "concluidos": 1,
                 "faturamento": 40.0, "previsto": 80.0}


def test_data_invalida_mostra_todos_os_erros(ctx):
    """Data inválida não pode esconder os demais erros do formulário."""
    with pytest.raises(ValidacaoError) as erro:
        agendamento.criar({"id_cliente": "", "id_servico": "", "data_hora": "amanhã"}, agora=AGORA)
    mensagens = erro.value.erros
    assert "Data/hora inválida." in mensagens
    assert "Selecione um cliente válido." in mensagens
    assert "Selecione um serviço válido." in mensagens
