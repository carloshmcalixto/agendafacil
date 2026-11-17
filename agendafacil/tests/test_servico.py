"""Testes unitários do Model Serviço."""
import pytest

from app.models import ValidacaoError
from app.models import servico


def test_cria_servico_aceitando_virgula_no_preco(ctx):
    id_s = servico.criar({"nome": "Barba", "preco": "29,90", "duracao_min": "20"})
    s = servico.buscar(id_s)
    assert s["preco"] == 29.90 and s["duracao_min"] == 20 and s["ativo"] == 1


@pytest.mark.parametrize("preco", ["0", "-10", "abc", ""])
def test_preco_invalido(ctx, preco):
    with pytest.raises(ValidacaoError):
        servico.criar({"nome": "Barba", "preco": preco, "duracao_min": "20"})


@pytest.mark.parametrize("duracao", ["0", "4", "481", "x"])
def test_duracao_invalida(ctx, duracao):
    with pytest.raises(ValidacaoError):
        servico.criar({"nome": "Barba", "preco": "30", "duracao_min": duracao})


def test_nome_duplicado(ctx):
    servico.criar({"nome": "Barba", "preco": "30", "duracao_min": "20"})
    with pytest.raises(ValidacaoError, match="Já existe"):
        servico.criar({"nome": "Barba", "preco": "35", "duracao_min": "25"})


def test_desativar_remove_da_lista_de_ativos(ctx):
    id_s = servico.criar({"nome": "Barba", "preco": "30", "duracao_min": "20"})
    servico.alternar_ativo(id_s)
    assert servico.listar(somente_ativos=True) == []
    assert len(servico.listar()) == 1
