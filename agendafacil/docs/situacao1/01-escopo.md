# 1. Escopo do projeto (revisado na PIT II)

**Aluno:** Carlos Henrique Mathias Calixto · **RGM:** 36910767 · **Curso:** Engenharia de Software (EAD) · **Polo:** Diadema

## 1.1 Problema

Pequenos prestadores de serviço (barbearias, salões, manicures) costumam controlar a agenda em caderno
ou pelo WhatsApp. Isso causa **horários duplicados**, **esquecimentos** e nenhuma visão de quanto foi
faturado no dia.

## 1.2 Objetivo

Oferecer um sistema web simples, acessível pelo computador ou pelo celular, para registrar clientes,
serviços e agendamentos, impedindo conflitos de horário e mostrando um resumo diário.

## 1.3 Público-alvo

- **Atendente/proprietário**: único perfil de usuário nesta versão; opera o sistema no balcão ou no celular.

## 1.4 Dentro do escopo (versão 1.0)

| # | Item |
|---|---|
| E1 | Manter clientes (cadastrar, editar, buscar, excluir) |
| E2 | Manter serviços (cadastrar, editar, ativar e desativar) |
| E3 | Registrar agendamentos com validação de expediente e de conflito |
| E4 | Concluir ou cancelar agendamentos |
| E5 | Painel diário com indicadores |

## 1.5 Fora do escopo (versões futuras)

- Login com múltiplos usuários e perfis
- Vários profissionais atendendo em paralelo (agenda por profissional)
- Envio de lembretes por WhatsApp ou e-mail
- Agendamento feito pelo próprio cliente (portal público)

## 1.6 O que mudou desde a PIT I (ciclo Kaizen)

| Antes (PIT I) | Depois (PIT II) | Motivo |
|---|---|---|
| Agendamento só guardava a hora de início | Conflito é calculado com a **duração do serviço** | Um corte de 50 min às 10:00 ocupava só o slot das 10:00 |
| Exclusão física de serviços | Serviço é **desativado** | Excluir quebrava o histórico de agendamentos |
| Status livre (texto) | Status restrito: AGENDADO, CONCLUIDO, CANCELADO | Integridade dos dados e relatórios |
| Tela só para desktop | Layout responsivo | Feedback de colegas: o dono usa o celular no balcão |
| Login previsto na v1 | Movido para versão futura | Foco em entregar o fluxo principal funcionando e testado |
