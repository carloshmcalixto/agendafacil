"""Testes de integração: front-end (rotas/telas) + back-end + banco."""
from datetime import datetime, timedelta


def proxima_segunda_10h():
    d = datetime.now() + timedelta(days=1)
    while d.weekday() != 0:
        d += timedelta(days=1)
    return d.strftime("%Y-%m-%dT10:00")


def test_paginas_principais_abrem(client):
    for url in ["/", "/clientes/", "/servicos/", "/agendamentos/",
                "/clientes/novo", "/servicos/novo", "/agendamentos/novo"]:
        assert client.get(url).status_code == 200, url


def test_pagina_inexistente_mostra_404_amigavel(client):
    r = client.get("/nao-existe")
    assert r.status_code == 404
    assert "Página não encontrada" in r.get_data(as_text=True)


def test_fluxo_completo_de_agendamento(client):
    # 1. cadastra cliente
    r = client.post("/clientes/novo", data={"nome": "Paula Reis", "telefone": "(11) 95555-4444"},
                    follow_redirects=True)
    assert "Cliente cadastrado com sucesso" in r.get_data(as_text=True)
    # 2. cadastra serviço
    r = client.post("/servicos/novo", data={"nome": "Escova", "preco": "50", "duracao_min": "40"},
                    follow_redirects=True)
    assert "Serviço cadastrado com sucesso" in r.get_data(as_text=True)
    # 3. agenda
    r = client.post("/agendamentos/novo", data={"id_cliente": "1", "id_servico": "1",
                                                "data_hora": proxima_segunda_10h()},
                    follow_redirects=True)
    html = r.get_data(as_text=True)
    assert "Agendamento realizado com sucesso" in html and "Paula Reis" in html
    # 4. conclui
    r = client.post("/agendamentos/1/status", data={"status": "CONCLUIDO"}, follow_redirects=True)
    assert "Status atualizado" in r.get_data(as_text=True)


def test_formulario_mostra_erros_de_validacao(client):
    r = client.post("/clientes/novo", data={"nome": "A", "telefone": "1"})
    html = r.get_data(as_text=True)
    assert r.status_code == 200
    assert "Nome deve ter pelo menos 3 caracteres." in html
    assert "Telefone inválido" in html
    # o que o usuário digitou é mantido no formulário
    assert 'value="A"' in html


def test_editar_cliente_inexistente_retorna_404(client):
    assert client.get("/clientes/999/editar").status_code == 404
