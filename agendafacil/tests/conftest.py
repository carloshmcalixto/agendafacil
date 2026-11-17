import pytest

from app import create_app


@pytest.fixture
def app(tmp_path):
    """Cada teste usa um banco novo e vazio (isolamento)."""
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "teste.db"), "SEED": False})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def ctx(app):
    with app.app_context():
        yield


@pytest.fixture
def dados_base(ctx):
    """Cria um cliente e um serviço de 30 minutos."""
    from app.models import cliente, servico

    id_c = cliente.criar({"nome": "Maria Teste", "telefone": "(11) 98888-7777", "email": "maria@teste.com"})
    id_s = servico.criar({"nome": "Corte", "preco": "40", "duracao_min": "30"})
    return {"id_cliente": id_c, "id_servico": id_s}
