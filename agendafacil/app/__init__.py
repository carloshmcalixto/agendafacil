"""AgendaFácil - fábrica da aplicação Flask (padrão MVC)."""
import os
from pathlib import Path

from flask import Flask, render_template

from app import database


def create_app(config: dict = None) -> Flask:
    app = Flask(__name__)
    instance = Path(app.root_path).parent / "instance"
    instance.mkdir(exist_ok=True)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao"),
        DATABASE=str(instance / "agendafacil.db"),
        SEED=True,
    )
    if config:
        app.config.update(config)

    app.teardown_appcontext(database.close_db)

    with app.app_context():
        database.init_db(seed=app.config["SEED"])

    # Controllers (Blueprints)
    from app.controllers import agendamentos, backup, clientes, principal, servicos

    app.register_blueprint(principal.bp)
    app.register_blueprint(clientes.bp)
    app.register_blueprint(servicos.bp)
    app.register_blueprint(agendamentos.bp)
    app.register_blueprint(backup.bp)

    @app.template_filter("moeda")
    def moeda(valor):
        return f"R$ {float(valor or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @app.template_filter("data_br")
    def data_br(valor):
        # "2026-11-10 14:30" -> "10/11/2026 14:30"
        if not valor:
            return ""
        d, _, h = valor.partition(" ")
        a, m, dia = d.split("-")
        return f"{dia}/{m}/{a} {h}".strip()

    @app.errorhandler(404)
    def nao_encontrado(_e):
        return render_template("erro.html", codigo=404,
                               mensagem="Página não encontrada."), 404

    @app.errorhandler(500)
    def erro_interno(_e):
        return render_template("erro.html", codigo=500,
                               mensagem="Ocorreu um erro inesperado. Tente novamente."), 500

    return app
