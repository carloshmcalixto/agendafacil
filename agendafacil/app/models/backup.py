"""Model Backup: exporta e restaura todos os dados do sistema em um arquivo JSON.

Melhoria sugerida na validação com usuários (PIT II - Situação 3): os testadores
sentiram falta de uma forma de guardar uma cópia de segurança dos dados.
"""
import json
import sqlite3
from datetime import datetime

from app.database import get_db
from app.models import ValidacaoError

VERSAO_FORMATO = 1
SISTEMA = "AgendaFácil"

# Ordem importa: agendamento depende de cliente e servico (chaves estrangeiras).
TABELAS = {
    "clientes": ("cliente", ["id_cliente", "nome", "telefone", "email", "data_cadastro"]),
    "servicos": ("servico", ["id_servico", "nome", "descricao", "preco", "duracao_min", "ativo"]),
    "agendamentos": ("agendamento", ["id_agendamento", "id_cliente", "id_servico", "data_hora",
                                     "status", "observacao", "criado_em"]),
}
OBRIGATORIOS = {
    "clientes": ["id_cliente", "nome", "telefone"],
    "servicos": ["id_servico", "nome", "preco", "duracao_min"],
    "agendamentos": ["id_agendamento", "id_cliente", "id_servico", "data_hora", "status"],
}


def resumo() -> dict:
    """Quantidade de registros de cada tabela (exibida na tela de backup)."""
    db = get_db()
    return {chave: db.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]
            for chave, (tabela, _) in TABELAS.items()}


def exportar(agora: datetime = None) -> dict:
    """Gera o conteúdo do backup com todos os registros."""
    agora = agora or datetime.now()
    db = get_db()
    dados = {"sistema": SISTEMA, "versao": VERSAO_FORMATO,
             "gerado_em": agora.strftime("%Y-%m-%d %H:%M:%S")}
    for chave, (tabela, colunas) in TABELAS.items():
        linhas = db.execute(f"SELECT {', '.join(colunas)} FROM {tabela} ORDER BY 1").fetchall()
        dados[chave] = [dict(linha) for linha in linhas]
    return dados


def exportar_json(agora: datetime = None) -> str:
    return json.dumps(exportar(agora), ensure_ascii=False, indent=2)


def nome_arquivo(agora: datetime = None) -> str:
    agora = agora or datetime.now()
    return f"agendafacil-backup-{agora.strftime('%Y-%m-%d-%H%M')}.json"


def _ler(conteudo) -> dict:
    if isinstance(conteudo, bytes):
        try:
            conteudo = conteudo.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise ValidacaoError("O arquivo não é um backup válido do AgendaFácil.")
    try:
        dados = json.loads(conteudo)
    except (TypeError, ValueError):
        raise ValidacaoError("O arquivo não é um backup válido do AgendaFácil.")
    if not isinstance(dados, dict) or dados.get("sistema") != SISTEMA:
        raise ValidacaoError("O arquivo não é um backup válido do AgendaFácil.")
    if dados.get("versao") != VERSAO_FORMATO:
        raise ValidacaoError("Versão de backup não suportada.")
    for chave in TABELAS:
        registros = dados.get(chave)
        if not isinstance(registros, list):
            raise ValidacaoError(f"Backup incompleto: falta a lista de {chave}.")
        for i, reg in enumerate(registros, start=1):
            faltando = [c for c in OBRIGATORIOS[chave] if not isinstance(reg, dict) or reg.get(c) in (None, "")]
            if faltando:
                raise ValidacaoError(f"Backup corrompido: registro {i} de {chave} sem {', '.join(faltando)}.")
    return dados


def restaurar(conteudo) -> dict:
    """Substitui todos os dados atuais pelos do backup.

    Tudo acontece em uma única transação: se qualquer registro for inválido,
    nada é alterado e os dados atuais são mantidos.
    """
    dados = _ler(conteudo)
    db = get_db()
    try:
        # O sqlite3 abre a transação automaticamente no primeiro DELETE.
        for _, (tabela, _) in reversed(list(TABELAS.items())):
            db.execute(f"DELETE FROM {tabela}")
        for chave, (tabela, colunas) in TABELAS.items():
            for reg in dados[chave]:
                cols = [c for c in colunas if reg.get(c) is not None]
                db.execute(f"INSERT INTO {tabela} ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
                           [reg[c] for c in cols])
        db.commit()
    except sqlite3.Error:
        db.rollback()
        raise ValidacaoError("O backup tem dados inconsistentes e não foi restaurado. Seus dados atuais foram mantidos.")
    return {chave: len(dados[chave]) for chave in TABELAS}
