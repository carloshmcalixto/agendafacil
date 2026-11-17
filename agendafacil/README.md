# AgendaFácil

Sistema web de agendamento para pequenos prestadores de serviço (barbearias, salões de beleza, estúdios).
Projeto desenvolvido na disciplina **Projeto Integrador Transdisciplinar em Engenharia de Software II**.

> **Aplicação online:** link do Render (será adicionado após a publicação)

## Funcionalidades

- Cadastro, edição, busca e exclusão de **clientes** (com validação de telefone e e-mail)
- Cadastro de **serviços** com preço e duração, ativação e desativação
- **Agendamentos** com regras de negócio:
  - somente datas futuras, de segunda a sábado, das 08:00 às 18:00
  - bloqueio de conflito de horário, considerando a duração do serviço
  - status: Agendado → Concluído ou Cancelado (cancelar libera o horário)
- **Painel do dia** com total de atendimentos, faturado e previsto
- Layout responsivo (computador e celular), mensagens de erro amigáveis e páginas 404/500

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Front-end | HTML5, CSS3, JavaScript (sem framework) e templates Jinja2 |
| Back-end | Python 3.12+ com Flask 3, padrão **MVC** |
| Banco de dados | SQLite 3 (script SQL compatível com MySQL/PostgreSQL) |
| Testes | pytest (unitários e de integração) |
| Hospedagem sugerida | Render.com ou PythonAnywhere (gratuitos) |

## Como executar

```bash
git clone https://github.com/carloshmcalixto/agendafacil.git
cd agendafacil
python -m venv .venv
# Windows: .venv\Scripts\activate    Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Acesse http://127.0.0.1:5000. O banco `instance/agendafacil.db` é criado na primeira execução, já com
serviços e clientes de exemplo.

## Como rodar os testes

```bash
python -m pytest -v
```

Resultado atual: **45 testes aprovados** (veja `docs/situacao3/01-plano-e-relatorio-de-testes.md`).

## Estrutura do repositório

```
agendafacil/
├── app/
│   ├── models/          # M - regras de negócio e acesso ao banco
│   ├── controllers/     # C - rotas (Blueprints) que ligam Model e View
│   ├── templates/       # V - telas HTML (Jinja2)
│   └── static/          # CSS e JavaScript
├── database/            # schema.sql (projeto físico) e seed.sql
├── tests/               # testes automatizados (pytest)
├── docs/
│   ├── situacao1/       # escopo, requisitos, UML, banco de dados e dicionário
│   ├── situacao2/       # arquitetura, manual de uso e telas
│   └── situacao3/       # testes, formulário dos colegas e laudo de qualidade
├── run.py
└── requirements.txt
```

## Documentação

1. [Escopo revisado](docs/situacao1/01-escopo.md)
2. [Requisitos e casos de uso](docs/situacao1/02-requisitos-e-casos-de-uso.md)
3. [Modelagem UML](docs/situacao1/03-modelagem-uml.md)
4. [Banco de dados e dicionário de dados](docs/situacao1/04-banco-de-dados.md)
5. [Arquitetura MVC](docs/situacao2/01-arquitetura-mvc.md)
6. [Manual de uso](docs/situacao2/02-manual-de-uso.md)
7. [Plano e relatório de testes](docs/situacao3/01-plano-e-relatorio-de-testes.md)
8. [Formulário de teste por usuários](docs/situacao3/02-formulario-teste-usuario.md)
9. [Laudo de qualidade](docs/situacao3/03-laudo-de-qualidade.md)

## Autor

Carlos Henrique Mathias Calixto · RGM 36910767 · Engenharia de Software (Bacharelado – EAD) · Polo Diadema
