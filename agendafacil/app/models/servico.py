"""Model Serviço."""
import sqlite3

from app.database import get_db
from app.models import ValidacaoError


def validar(dados: dict) -> dict:
    nome = (dados.get("nome") or "").strip()
    descricao = (dados.get("descricao") or "").strip() or None
    erros = []

    try:
        preco = round(float(str(dados.get("preco", "")).replace(",", ".")), 2)
        if preco <= 0:
            erros.append("Preço deve ser maior que zero.")
    except ValueError:
        preco = None
        erros.append("Preço inválido.")

    try:
        duracao = int(dados.get("duracao_min", ""))
        if not 5 <= duracao <= 480:
            erros.append("Duração deve estar entre 5 e 480 minutos.")
    except ValueError:
        duracao = None
        erros.append("Duração inválida.")

    if len(nome) < 3:
        erros.append("Nome do serviço deve ter pelo menos 3 caracteres.")
    if erros:
        raise ValidacaoError(erros)
    return {"nome": nome, "descricao": descricao, "preco": preco, "duracao_min": duracao}


def listar(somente_ativos: bool = False):
    sql = "SELECT * FROM servico"
    if somente_ativos:
        sql += " WHERE ativo = 1"
    return get_db().execute(sql + " ORDER BY nome").fetchall()


def buscar(id_servico: int):
    return get_db().execute(
        "SELECT * FROM servico WHERE id_servico = ?", (id_servico,)
    ).fetchone()


def criar(dados: dict) -> int:
    d = validar(dados)
    db = get_db()
    try:
        cur = db.execute(
            "INSERT INTO servico (nome, descricao, preco, duracao_min) VALUES (?, ?, ?, ?)",
            (d["nome"], d["descricao"], d["preco"], d["duracao_min"]),
        )
        db.commit()
    except sqlite3.IntegrityError:
        raise ValidacaoError("Já existe um serviço com este nome.")
    return cur.lastrowid


def atualizar(id_servico: int, dados: dict):
    if buscar(id_servico) is None:
        raise ValidacaoError("Serviço não encontrado.")
    d = validar(dados)
    db = get_db()
    try:
        db.execute(
            "UPDATE servico SET nome = ?, descricao = ?, preco = ?, duracao_min = ? "
            "WHERE id_servico = ?",
            (d["nome"], d["descricao"], d["preco"], d["duracao_min"], id_servico),
        )
        db.commit()
    except sqlite3.IntegrityError:
        raise ValidacaoError("Já existe um serviço com este nome.")


def alternar_ativo(id_servico: int):
    db = get_db()
    db.execute(
        "UPDATE servico SET ativo = 1 - ativo WHERE id_servico = ?", (id_servico,)
    )
    db.commit()
