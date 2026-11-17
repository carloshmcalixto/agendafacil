-- =============================================================
-- AgendaFácil - Projeto físico do banco de dados
-- SGBD: SQLite 3 (compatível com MySQL/PostgreSQL com ajustes mínimos)
-- =============================================================

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS cliente (
    id_cliente     INTEGER PRIMARY KEY AUTOINCREMENT,
    nome           VARCHAR(100) NOT NULL CHECK (length(trim(nome)) >= 3),
    telefone       VARCHAR(15)  NOT NULL,
    email          VARCHAR(120) UNIQUE,
    data_cadastro  TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS servico (
    id_servico     INTEGER PRIMARY KEY AUTOINCREMENT,
    nome           VARCHAR(80)  NOT NULL UNIQUE,
    descricao      VARCHAR(255),
    preco          NUMERIC(10,2) NOT NULL CHECK (preco > 0),
    duracao_min    INTEGER NOT NULL CHECK (duracao_min BETWEEN 5 AND 480),
    ativo          INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1))
);

CREATE TABLE IF NOT EXISTS agendamento (
    id_agendamento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente     INTEGER NOT NULL,
    id_servico     INTEGER NOT NULL,
    data_hora      TEXT NOT NULL,              -- formato ISO: AAAA-MM-DD HH:MM
    status         VARCHAR(10) NOT NULL DEFAULT 'AGENDADO'
                   CHECK (status IN ('AGENDADO', 'CONCLUIDO', 'CANCELADO')),
    observacao     VARCHAR(255),
    criado_em      TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente) ON DELETE RESTRICT,
    FOREIGN KEY (id_servico) REFERENCES servico (id_servico) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_agendamento_data ON agendamento (data_hora);
CREATE INDEX IF NOT EXISTS idx_agendamento_cliente ON agendamento (id_cliente);
