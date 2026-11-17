"""Model Cliente."""
import re
import sqlite3

from app.database import get_db
from app.models import ValidacaoError

RE_TELEFONE = re.compile(r"^\(?\d{2}\)?\s?9?\d{4}-?\d{4}$")
RE_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


def validar(dados: dict) -> dict:
    nome = (dados.get("nome") or "").strip()
    telefone = (dados.get("telefone") or "").strip()
    email = (dados.get("email") or "").strip().lower() or None

    erros = []
    if len(nome) < 3:
        erros.append("Nome deve ter pelo menos 3 caracteres.")
    if len(nome) > 100:
        erros.append("Nome deve ter no máximo 100 caracteres.")
    if not RE_TELEFONE.match(telefone):
        erros.append("Telefone inválido. Use o formato (11) 98888-7777.")
    if email and not RE_EMAIL.match(email):
        erros.append("E-mail inválido.")
    if erros:
        raise ValidacaoError(erros)
    return {"nome": nome, "telefone": telefone, "email": email}


def listar(busca: str = ""):
    sql = "SELECT * FROM cliente"
    params = ()
    if busca:
        sql += " WHERE nome LIKE ? OR telefone LIKE ?"
        params = (f"%{busca}%", f"%{busca}%")
    return get_db().execute(sql + " ORDER BY nome", params).fetchall()


def buscar(id_cliente: int):
    return get_db().execute(
        "SELECT * FROM cliente WHERE id_cliente = ?", (id_cliente,)
    ).fetchone()


def criar(dados: dict) -> int:
    d = validar(dados)
    db = get_db()
    try:
        cur = db.execute(
            "INSERT INTO cliente (nome, telefone, email) VALUES (?, ?, ?)",
            (d["nome"], d["telefone"], d["email"]),
        )
        db.commit()
    except sqlite3.IntegrityError:
        raise ValidacaoError("Já existe um cliente com este e-mail.")
    return cur.lastrowid


def atualizar(id_cliente: int, dados: dict):
    if buscar(id_cliente) is None:
        raise ValidacaoError("Cliente não encontrado.")
    d = validar(dados)
    db = get_db()
    try:
        db.execute(
            "UPDATE cliente SET nome = ?, telefone = ?, email = ? WHERE id_cliente = ?",
            (d["nome"], d["telefone"], d["email"], id_cliente),
        )
        db.commit()
    except sqlite3.IntegrityError:
        raise ValidacaoError("Já existe um cliente com este e-mail.")


def excluir(id_cliente: int):
    db = get_db()
    tem_agenda = db.execute(
        "SELECT 1 FROM agendamento WHERE id_cliente = ? LIMIT 1", (id_cliente,)
    ).fetchone()
    if tem_agenda:
        raise ValidacaoError(
            "Cliente possui agendamentos e não pode ser excluído."
        )
    db.execute("DELETE FROM cliente WHERE id_cliente = ?", (id_cliente,))
    db.commit()
