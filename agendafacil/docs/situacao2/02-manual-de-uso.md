# 6. Manual de uso

## Instalação

Veja a seção "Como executar" no [README](../../README.md). Depois, acesse http://127.0.0.1:5000.

## 6.1 Painel do dia

![Painel](telas/01-painel.png)

Mostra os agendamentos da data escolhida e os indicadores: total, em aberto, concluídos, valor já
faturado (concluídos) e valor previsto (concluídos + em aberto). Troque a data no campo do canto superior.

## 6.2 Cadastrar cliente

Menu **Clientes → + Novo cliente**. Preencha nome e telefone (a máscara é aplicada ao digitar). O e-mail
é opcional. Use o campo de busca para localizar por nome ou telefone.

![Clientes](telas/04-clientes.png)

Se algum campo estiver errado, o sistema destaca o campo e explica o problema:

![Validação](telas/05-validacao.png)

## 6.3 Cadastrar serviço

Menu **Serviços → + Novo serviço**: nome, preço (aceita vírgula) e duração em minutos.
Para tirar um serviço de uso sem perder o histórico, clique em **Desativar**.

## 6.4 Agendar

Menu **Agendamentos → + Novo agendamento** (ou pelo botão do painel).

![Novo agendamento](telas/03-novo-agendamento.png)

O sistema recusa e explica quando:

- a data/hora já passou;
- é domingo ou fora do horário das 08:00 às 18:00 (o serviço precisa terminar até 18:00);
- o horário se sobrepõe a outro agendamento em aberto.

## 6.5 Concluir ou cancelar

Na lista de agendamentos ou no painel, use **Concluir** (atendimento feito) ou **Cancelar** (o horário
fica livre de novo). Use os filtros de data e status para encontrar agendamentos.

![Agendamentos](telas/02-agendamentos.png)

## 6.6 Backup dos dados

Menu **Backup**. A tela mostra quantos clientes, serviços e agendamentos existem.

![Backup](telas/07-backup.png)

- **Baixar backup**: salva um arquivo `agendafacil-backup-AAAA-MM-DD-HHMM.json` com todos os dados.
  Guarde-o em local seguro (pen drive, Google Drive, e-mail).
- **Restaurar backup**: escolha o arquivo `.json` e clique em **Restaurar**. O sistema pede confirmação,
  porque os dados atuais são substituídos pelos do arquivo. Se o arquivo for inválido ou estiver
  corrompido, nada é alterado e uma mensagem explica o problema.

> Na hospedagem gratuita do Render, os dados são reiniciados a cada nova publicação. Faça um backup antes
> de publicar uma nova versão e restaure depois.

## 6.7 No celular

![Celular](telas/06-celular.png)

O menu vira o botão ☰ e as tabelas viram cartões.
