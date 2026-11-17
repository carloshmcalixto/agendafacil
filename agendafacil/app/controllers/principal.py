from datetime import date

from flask import Blueprint, render_template, request

from app.models import agendamento

bp = Blueprint("principal", __name__)


@bp.route("/")
def painel():
    dia = request.args.get("data") or date.today().isoformat()
    return render_template(
        "painel.html",
        dia=dia,
        resumo=agendamento.resumo_do_dia(dia),
        agenda=agendamento.listar(dia),
    )
