from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.models import ValidacaoError
from app.models import agendamento, cliente, servico

bp = Blueprint("agendamentos", __name__, url_prefix="/agendamentos")


@bp.route("/")
def index():
    data = request.args.get("data", "")
    status = request.args.get("status", "")
    return render_template(
        "agendamentos/lista.html",
        agendamentos=agendamento.listar(data or None, status or None),
        data=data,
        status=status,
    )


@bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        try:
            agendamento.criar(request.form)
            flash("Agendamento realizado com sucesso.", "sucesso")
            return redirect(url_for("agendamentos.index"))
        except ValidacaoError as e:
            for msg in e.erros:
                flash(msg, "erro")
    return render_template(
        "agendamentos/form.html",
        a=request.form,
        clientes=cliente.listar(),
        servicos=servico.listar(somente_ativos=True),
    )


@bp.route("/<int:id_agendamento>/status", methods=["POST"])
def status(id_agendamento):
    try:
        agendamento.alterar_status(id_agendamento, request.form.get("status", ""))
        flash("Status atualizado.", "sucesso")
    except ValidacaoError as e:
        flash(e.erros[0], "erro")
    return redirect(request.referrer or url_for("agendamentos.index"))
