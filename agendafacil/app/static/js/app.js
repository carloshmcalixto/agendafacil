// AgendaFácil - comportamento do front-end (validação, máscara, confirmações)
document.addEventListener("DOMContentLoaded", () => {
  // Menu responsivo
  const btn = document.getElementById("menuBtn");
  const menu = document.getElementById("menu");
  if (btn) btn.addEventListener("click", () => menu.classList.toggle("aberto"));

  // Fechar alertas
  document.querySelectorAll(".alerta .fechar").forEach((b) =>
    b.addEventListener("click", () => b.parentElement.remove())
  );

  // Confirmação antes de ações destrutivas
  document.querySelectorAll("[data-confirmar]").forEach((el) =>
    el.addEventListener("click", (e) => {
      if (!confirm(el.dataset.confirmar)) e.preventDefault();
    })
  );

  // Máscara de telefone: (11) 98888-7777
  document.querySelectorAll('[data-mascara="telefone"]').forEach((input) =>
    input.addEventListener("input", () => {
      const d = input.value.replace(/\D/g, "").slice(0, 11);
      let v = d;
      if (d.length > 2) v = `(${d.slice(0, 2)}) ${d.slice(2)}`;
      if (d.length > 7) v = `(${d.slice(0, 2)}) ${d.slice(2, d.length - 4)}-${d.slice(-4)}`;
      input.value = v;
    })
  );

  // Validação no navegador (o servidor valida de novo - nunca confiar só no front)
  document.querySelectorAll("form[data-validar]").forEach((form) =>
    form.addEventListener("submit", (e) => {
      let ok = true;
      form.querySelectorAll(".msg-campo").forEach((m) => m.remove());
      form.querySelectorAll("input, select, textarea").forEach((campo) => {
        campo.classList.remove("invalido");
        if (!campo.checkValidity()) {
          ok = false;
          campo.classList.add("invalido");
          const msg = document.createElement("small");
          msg.className = "msg-campo";
          msg.textContent = campo.validationMessage;
          campo.insertAdjacentElement("afterend", msg);
        }
      });
      if (!ok) e.preventDefault();
    })
  );

  // Mostra duração/preço do serviço escolhido
  const servico = document.getElementById("servico");
  const info = document.getElementById("infoServico");
  if (servico && info) {
    const atualizar = () => {
      const op = servico.selectedOptions[0];
      info.textContent = op && op.dataset.duracao ? `Duração: ${op.dataset.duracao} minutos` : "";
    };
    servico.addEventListener("change", atualizar);
    atualizar();
  }
});
