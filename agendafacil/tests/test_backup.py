"""Testes do backup (melhoria sugerida pelos testadores na Situação 3)."""
import io
import json
from datetime import datetime

import pytest

from app.models import ValidacaoError
from app.models import agendamento, backup, cliente, servico

AGORA = datetime(2030, 1, 1, 9, 0)


@pytest.fixture
def dados(ctx):
    """Um cliente, dois serviços e um agendamento."""
    id_c = cliente.criar({"nome": "Maria Teste", "telefone": "(11) 98888-7777", "email": "maria@teste.com"})
    id_s = servico.criar({"nome": "Corte", "preco": "40", "duracao_min": "30"})
    servico.criar({"nome": "Barba", "preco": "30", "duracao_min": "20"})
    agendamento.criar({"id_cliente": id_c, "id_servico": id_s, "data_hora": "2030-01-07 10:00"}, agora=AGORA)


def test_exporta_todos_os_registros(dados):
    b = backup.exportar(AGORA)
    assert b["sistema"] == "AgendaFácil" and b["versao"] == 1
    assert b["gerado_em"] == "2030-01-01 09:00:00"
    assert len(b["clientes"]) == 1 and b["clientes"][0]["nome"] == "Maria Teste"
    assert len(b["servicos"]) == 2
    assert len(b["agendamentos"]) == 1 and b["agendamentos"][0]["status"] == "AGENDADO"


def test_nome_do_arquivo_tem_data_e_hora():
    assert backup.nome_arquivo(AGORA) == "agendafacil-backup-2030-01-01-0900.json"


def test_restaurar_recupera_os_dados_apos_perda(dados):
    arquivo = backup.exportar_json(AGORA)
    # simula perda/alteração dos dados depois do backup
    cliente.criar({"nome": "Cliente Novo", "telefone": "(11) 97777-6666"})
    agendamento.alterar_status(1, "CANCELADO")

    total = backup.restaurar(arquivo)

    assert total == {"clientes": 1, "servicos": 2, "agendamentos": 1}
    assert [c["nome"] for c in cliente.listar()] == ["Maria Teste"]
    assert agendamento.buscar(1)["status"] == "AGENDADO"


def test_arquivo_que_nao_e_backup_e_rejeitado(dados):
    for conteudo in ["isto não é json", "{}", json.dumps({"sistema": "Outro", "versao": 1})]:
        with pytest.raises(ValidacaoError, match="não é um backup válido"):
            backup.restaurar(conteudo)
    assert backup.resumo() == {"clientes": 1, "servicos": 2, "agendamentos": 1}


def test_backup_corrompido_nao_altera_os_dados_atuais(dados):
    b = backup.exportar(AGORA)
    b["agendamentos"][0]["id_cliente"] = 999        # cliente que não existe
    with pytest.raises(ValidacaoError, match="não foi restaurado"):
        backup.restaurar(json.dumps(b))
    # nada foi apagado: a transação foi desfeita
    assert backup.resumo() == {"clientes": 1, "servicos": 2, "agendamentos": 1}


def test_backup_sem_campo_obrigatorio_e_rejeitado(dados):
    b = backup.exportar(AGORA)
    del b["clientes"][0]["telefone"]
    with pytest.raises(ValidacaoError, match="sem telefone"):
        backup.restaurar(json.dumps(b))


def test_tela_e_download_do_backup(client):
    r = client.get("/backup/")
    assert r.status_code == 200 and "Baixar backup" in r.get_data(as_text=True)

    r = client.get("/backup/baixar")
    assert r.status_code == 200
    assert r.mimetype == "application/json"
    assert "attachment" in r.headers["Content-Disposition"]
    assert r.get_json()["sistema"] == "AgendaFácil"


def test_restaurar_pela_tela(client):
    arquivo = client.get("/backup/baixar").data
    client.post("/clientes/novo", data={"nome": "Paula Reis", "telefone": "(11) 95555-4444"})

    r = client.post("/backup/restaurar", data={"arquivo": (io.BytesIO(arquivo), "backup.json")},
                    content_type="multipart/form-data", follow_redirects=True)
    html = r.get_data(as_text=True)
    assert "Backup restaurado" in html
    assert "Paula Reis" not in client.get("/clientes/").get_data(as_text=True)


def test_restaurar_sem_arquivo_mostra_erro(client):
    r = client.post("/backup/restaurar", data={}, content_type="multipart/form-data", follow_redirects=True)
    assert "Selecione o arquivo de backup" in r.get_data(as_text=True)
