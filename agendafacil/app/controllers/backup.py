"""Controller Backup: tela, download e restauração do backup."""
from flask import Blueprint, Response, flash, redirect, render_template, request, url_for

from app.models import ValidacaoError
from app.models import backup

bp = Blueprint("backup", __name__, url_prefix="/backup")

TAMANHO_MAXIMO = 5 * 1024 * 1024  # 5 MB


@bp.route("/")
def index():
    return render_template("backup.html", resumo=backup.resumo())


@bp.route("/baixar")
def baixar():
    return Response(
        backup.exportar_json(),
        mimetype="application/json",
        headers={"Content-Disposition": f'attachment; filename="{backup.nome_arquivo()}"'},
    )


@bp.route("/restaurar", methods=["POST"])
def restaurar():
    arquivo = request.files.get("arquivo")
    if not arquivo or not arquivo.filename:
        flash("Selecione o arquivo de backup (.json).", "erro")
        return redirect(url_for("backup.index"))
    conteudo = arquivo.read(TAMANHO_MAXIMO + 1)
    if len(conteudo) > TAMANHO_MAXIMO:
        flash("Arquivo muito grande para ser um backup do AgendaFácil.", "erro")
        return redirect(url_for("backup.index"))
    try:
        total = backup.restaurar(conteudo)
    except ValidacaoError as e:
        for erro in e.erros:
            flash(erro, "erro")
        return redirect(url_for("backup.index"))
    flash(f"Backup restaurado: {total['clientes']} clientes, {total['servicos']} serviços "
          f"e {total['agendamentos']} agendamentos.", "sucesso")
    return redirect(url_for("backup.index"))
