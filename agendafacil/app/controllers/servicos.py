from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.models import ValidacaoError
from app.models import servico

bp = Blueprint("servicos", __name__, url_prefix="/servicos")


@bp.route("/")
def index():
    return render_template("servicos/lista.html", servicos=servico.listar())


@bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        try:
            servico.criar(request.form)
            flash("Serviço cadastrado com sucesso.", "sucesso")
            return redirect(url_for("servicos.index"))
        except ValidacaoError as e:
            for msg in e.erros:
                flash(msg, "erro")
    return render_template("servicos/form.html", s=request.form, titulo="Novo serviço")


@bp.route("/<int:id_servico>/editar", methods=["GET", "POST"])
def editar(id_servico):
    registro = servico.buscar(id_servico)
    if registro is None:
        abort(404)
    if request.method == "POST":
        try:
            servico.atualizar(id_servico, request.form)
            flash("Serviço atualizado.", "sucesso")
            return redirect(url_for("servicos.index"))
        except ValidacaoError as e:
            for msg in e.erros:
                flash(msg, "erro")
        registro = request.form
    return render_template("servicos/form.html", s=registro, titulo="Editar serviço")


@bp.route("/<int:id_servico>/ativar", methods=["POST"])
def ativar(id_servico):
    servico.alternar_ativo(id_servico)
    flash("Situação do serviço alterada.", "sucesso")
    return redirect(url_for("servicos.index"))
