"""Model Agendamento - concentra as principais regras de negócio."""
from datetime import datetime, timedelta

from app.database import get_db
from app.models import ValidacaoError
from app.models import cliente as cliente_model
from app.models import servico as servico_model

FORMATO = "%Y-%m-%d %H:%M"
ABERTURA = 8   # 08:00
FECHAMENTO = 18  # 18:00
STATUS_VALIDOS = ("AGENDADO", "CONCLUIDO", "CANCELADO")


def _parse_data_hora(valor: str) -> datetime:
    valor = (valor or "").strip().replace("T", " ")
    try:
        return datetime.strptime(valor, FORMATO)
    except ValueError:
        raise ValidacaoError("Data/hora inválida.")


def verificar_conflito(inicio: datetime, duracao_min: int, ignorar_id=None) -> bool:
    """True se o intervalo [inicio, inicio+duracao) se sobrepõe a outro agendamento ativo."""
    fim = inicio + timedelta(minutes=duracao_min)
    dia = inicio.strftime("%Y-%m-%d")
    linhas = get_db().execute(
        "SELECT a.id_agendamento, a.data_hora, s.duracao_min "
        "FROM agendamento a JOIN servico s ON s.id_servico = a.id_servico "
        "WHERE a.status = 'AGENDADO' AND substr(a.data_hora, 1, 10) = ?",
        (dia,),
    ).fetchall()
    for l in linhas:
        if ignorar_id and l["id_agendamento"] == ignorar_id:
            continue
        outro_ini = datetime.strptime(l["data_hora"], FORMATO)
        outro_fim = outro_ini + timedelta(minutes=l["duracao_min"])
        if inicio < outro_fim and outro_ini < fim:
            return True
    return False


def validar(dados: dict, agora: datetime = None, ignorar_id=None) -> dict:
    agora = agora or datetime.now()
    erros = []

    try:
        id_cliente = int(dados.get("id_cliente", ""))
    except ValueError:
        id_cliente = None
    try:
        id_servico = int(dados.get("id_servico", ""))
    except ValueError:
        id_servico = None

    cliente = cliente_model.buscar(id_cliente) if id_cliente else None
    servico = servico_model.buscar(id_servico) if id_servico else None
    if cliente is None:
        erros.append("Selecione um cliente válido.")
    if servico is None:
        erros.append("Selecione um serviço válido.")
    elif not servico["ativo"]:
        erros.append("Este serviço está inativo.")

    try:
        inicio = _parse_data_hora(dados.get("data_hora"))
    except ValidacaoError as e:
        inicio = None
        erros.extend(e.erros)

    if inicio is not None:
        if inicio <= agora:
            erros.append("O agendamento deve ser para uma data/hora futura.")
        if inicio.weekday() == 6:
            erros.append("Não há atendimento aos domingos.")

    if servico is not None and inicio is not None:
        fim = inicio + timedelta(minutes=servico["duracao_min"])
        limite = inicio.replace(hour=FECHAMENTO, minute=0)
        if inicio.hour < ABERTURA or fim > limite:
            erros.append(
                f"O atendimento deve ocorrer entre {ABERTURA:02d}:00 e {FECHAMENTO:02d}:00."
            )
        elif verificar_conflito(inicio, servico["duracao_min"], ignorar_id):
            erros.append("Já existe um agendamento neste horário.")

    if erros:
        raise ValidacaoError(erros)
    return {
        "id_cliente": id_cliente,
        "id_servico": id_servico,
        "data_hora": inicio.strftime(FORMATO),
        "observacao": (dados.get("observacao") or "").strip() or None,
    }


def listar(data: str = None, status: str = None):
    sql = (
        "SELECT a.*, c.nome AS cliente, c.telefone, s.nome AS servico, s.preco, s.duracao_min "
        "FROM agendamento a "
        "JOIN cliente c ON c.id_cliente = a.id_cliente "
        "JOIN servico s ON s.id_servico = a.id_servico WHERE 1 = 1"
    )
    params = []
    if data:
        sql += " AND substr(a.data_hora, 1, 10) = ?"
        params.append(data)
    if status in STATUS_VALIDOS:
        sql += " AND a.status = ?"
        params.append(status)
    return get_db().execute(sql + " ORDER BY a.data_hora", params).fetchall()


def buscar(id_agendamento: int):
    return get_db().execute(
        "SELECT * FROM agendamento WHERE id_agendamento = ?", (id_agendamento,)
    ).fetchone()


def criar(dados: dict, agora: datetime = None) -> int:
    d = validar(dados, agora)
    db = get_db()
    cur = db.execute(
        "INSERT INTO agendamento (id_cliente, id_servico, data_hora, observacao) "
        "VALUES (?, ?, ?, ?)",
        (d["id_cliente"], d["id_servico"], d["data_hora"], d["observacao"]),
    )
    db.commit()
    return cur.lastrowid


def alterar_status(id_agendamento: int, novo_status: str):
    ag = buscar(id_agendamento)
    if ag is None:
        raise ValidacaoError("Agendamento não encontrado.")
    if novo_status not in STATUS_VALIDOS:
        raise ValidacaoError("Status inválido.")
    if ag["status"] != "AGENDADO":
        raise ValidacaoError("Somente agendamentos em aberto podem ser alterados.")
    db = get_db()
    db.execute(
        "UPDATE agendamento SET status = ? WHERE id_agendamento = ?",
        (novo_status, id_agendamento),
    )
    db.commit()


def resumo_do_dia(data: str):
    """Indicadores exibidos no painel inicial."""
    linhas = listar(data)
    agendados = [l for l in linhas if l["status"] == "AGENDADO"]
    concluidos = [l for l in linhas if l["status"] == "CONCLUIDO"]
    return {
        "total": len(linhas),
        "agendados": len(agendados),
        "concluidos": len(concluidos),
        "faturamento": round(sum(l["preco"] for l in concluidos), 2),
        "previsto": round(sum(l["preco"] for l in agendados + concluidos), 2),
    }
