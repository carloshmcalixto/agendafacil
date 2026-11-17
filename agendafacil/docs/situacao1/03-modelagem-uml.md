# 3. Modelagem UML (revisada)

> Os diagramas estão em Mermaid: o GitHub os desenha automaticamente ao abrir este arquivo.

## 3.1 Diagrama de classes (domínio e persistência)

```mermaid
classDiagram
    class Cliente {
        +int id_cliente
        +str nome
        +str telefone
        +str email
        +datetime data_cadastro
        +validar(dados)
        +criar(dados) int
        +atualizar(id, dados)
        +excluir(id)
        +listar(busca)
    }
    class Servico {
        +int id_servico
        +str nome
        +str descricao
        +decimal preco
        +int duracao_min
        +bool ativo
        +validar(dados)
        +criar(dados) int
        +alternar_ativo(id)
    }
    class Agendamento {
        +int id_agendamento
        +datetime data_hora
        +StatusAgendamento status
        +str observacao
        +validar(dados)
        +criar(dados) int
        +verificar_conflito(inicio, duracao) bool
        +alterar_status(id, status)
        +resumo_do_dia(data) dict
    }
    class StatusAgendamento {
        <<enumeration>>
        AGENDADO
        CONCLUIDO
        CANCELADO
    }
    Cliente "1" --> "0..*" Agendamento : solicita
    Servico "1" --> "0..*" Agendamento : refere-se a
    Agendamento --> StatusAgendamento
```

## 3.2 Diagrama de sequência – Agendar atendimento

```mermaid
sequenceDiagram
    actor U as Atendente
    participant V as View (form.html + app.js)
    participant C as Controller (agendamentos.novo)
    participant M as Model (agendamento)
    participant DB as SQLite
    U->>V: preenche cliente, serviço, data/hora
    V->>V: valida campos obrigatórios (HTML5/JS)
    V->>C: POST /agendamentos/novo
    C->>M: criar(form)
    M->>DB: busca cliente e serviço
    M->>DB: lista agendamentos ativos do dia
    M->>M: verifica expediente e conflito
    alt dados válidos
        M->>DB: INSERT agendamento
        M-->>C: id
        C-->>U: redireciona para lista + "Agendamento realizado"
    else regra violada
        M-->>C: ValidacaoError(erros)
        C-->>V: renderiza formulário com mensagens
        V-->>U: mostra erros mantendo o que foi digitado
    end
```

## 3.3 Diagrama de atividades – Ciclo de vida do agendamento

```mermaid
stateDiagram-v2
    [*] --> AGENDADO : criar (válido)
    AGENDADO --> CONCLUIDO : atendimento realizado
    AGENDADO --> CANCELADO : cliente desistiu
    CONCLUIDO --> [*]
    CANCELADO --> [*] : horário liberado
```

## 3.4 Melhorias aplicadas em relação à PIT I

- Classe `StatusAgendamento` transformada em enumeração (antes era texto livre).
- Incluído o método `verificar_conflito`, que considera a duração do serviço.
- Atributo `ativo` em `Servico` no lugar da exclusão física.
- Sequência revisada para mostrar a validação em duas camadas (View e Model).
