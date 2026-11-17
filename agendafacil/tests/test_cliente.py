"""Testes unitários do Model Cliente."""
import pytest

from app.models import ValidacaoError
from app.models import cliente


def test_cria_cliente_valido(ctx):
    id_c = cliente.criar({"nome": "João da Silva", "telefone": "(11) 91234-5678"})
    assert cliente.buscar(id_c)["nome"] == "João da Silva"


def test_nome_curto_e_rejeitado(ctx):
    with pytest.raises(ValidacaoError) as e:
        cliente.criar({"nome": "Jo", "telefone": "(11) 91234-5678"})
    assert "Nome deve ter pelo menos 3 caracteres." in e.value.erros


@pytest.mark.parametrize("telefone", ["123", "(11) 1234", "abc", ""])
def test_telefone_invalido_e_rejeitado(ctx, telefone):
    with pytest.raises(ValidacaoError):
        cliente.criar({"nome": "João", "telefone": telefone})


def test_email_invalido_e_rejeitado(ctx):
    with pytest.raises(ValidacaoError):
        cliente.criar({"nome": "João", "telefone": "11912345678", "email": "joao@"})


def test_email_duplicado_e_rejeitado(ctx):
    cliente.criar({"nome": "João", "telefone": "11912345678", "email": "j@x.com"})
    with pytest.raises(ValidacaoError, match="e-mail"):
        cliente.criar({"nome": "José", "telefone": "11912345679", "email": "J@X.com"})


def test_busca_por_nome(ctx):
    cliente.criar({"nome": "Carlos Alberto", "telefone": "11912345678"})
    cliente.criar({"nome": "Fernanda", "telefone": "11912345679"})
    assert [c["nome"] for c in cliente.listar("carl")] == ["Carlos Alberto"]


def test_atualiza_cliente(ctx):
    id_c = cliente.criar({"nome": "Carlos", "telefone": "11912345678"})
    cliente.atualizar(id_c, {"nome": "Carlos Souza", "telefone": "11912345678"})
    assert cliente.buscar(id_c)["nome"] == "Carlos Souza"


def test_nao_exclui_cliente_com_agendamento(dados_base):
    from datetime import datetime
    from app.models import agendamento

    agendamento.criar(
        {**dados_base, "data_hora": "2030-01-07 10:00"}, agora=datetime(2030, 1, 1)
    )
    with pytest.raises(ValidacaoError, match="possui agendamentos"):
        cliente.excluir(dados_base["id_cliente"])


def test_exclui_cliente_sem_agendamento(ctx):
    id_c = cliente.criar({"nome": "Temporário", "telefone": "11912345678"})
    cliente.excluir(id_c)
    assert cliente.buscar(id_c) is None
