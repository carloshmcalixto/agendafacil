from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.models import ValidacaoError
from app.models import cliente

bp = Blueprint("clientes", __name__, url_prefix="/clientes")


@bp.route("/")
def index():
    busca = request.args.get("q", "").strip()
    return render_template("clientes/lista.html", clientes=cliente.listar(busca), busca=busca)


@bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        try:
            cliente.criar(request.form)
            flash("Cliente cadastrado com sucesso.", "sucesso")
            return redirect(url_for("clientes.index"))
        except ValidacaoError as e:
            for msg in e.erros:
                flash(msg, "erro")
    return render_template("clientes/form.html", c=request.form, titulo="Novo cliente")


@bp.route("/<int:id_cliente>/editar", methods=["GET", "POST"])
def editar(id_cliente):
    registro = cliente.buscar(id_cliente)
    if registro is None:
        abort(404)
    if request.method == "POST":
        try:
            cliente.atualizar(id_cliente, request.form)
            flash("Cliente atualizado.", "sucesso")
            return redirect(url_for("clientes.index"))
        except ValidacaoError as e:
            for msg in e.erros:
                flash(msg, "erro")
        registro = request.form
    return render_template("clientes/form.html", c=registro, titulo="Editar cliente")


@bp.route("/<int:id_cliente>/excluir", methods=["POST"])
def excluir(id_cliente):
    try:
        cliente.excluir(id_cliente)
        flash("Cliente excluído.", "sucesso")
    except ValidacaoError as e:
        flash(e.erros[0], "erro")
    return redirect(url_for("clientes.index"))
