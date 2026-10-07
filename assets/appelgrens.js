/* Formulär: skickas som e-post via besökarens e-postprogram (ingen server behövs). */
document.querySelectorAll("form[data-mailto]").forEach((form) => {
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const fields = [...form.querySelectorAll("input, select, textarea")];
    const bad = fields.find((el) => !el.checkValidity());
    fields.forEach((el) => el.toggleAttribute("aria-invalid", !el.checkValidity()));
    if (bad) { bad.focus(); bad.reportValidity(); return; }

    const lines = fields.filter((el) => el.value.trim()).map((el) => `${el.dataset.label || el.name}: ${el.value.trim()}`);
    const topic = form.querySelector("[name=tjanst]")?.value;
    const subject = form.dataset.subject + (topic ? ` – ${topic}` : "");
    location.href = `mailto:${form.dataset.mailto}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join("\n"))}`;

    const ok = form.querySelector(".form-ok");
    if (ok) { ok.hidden = false; ok.focus(); }
  });
  form.addEventListener("input", (e) => { if (e.target.checkValidity()) e.target.removeAttribute("aria-invalid"); });
});

/* Förvald tjänst i offertformuläret, t.ex. kontakt.html?tjanst=service#offert */
const vald = new URLSearchParams(location.search).get("tjanst");
const select = document.querySelector("select[name=tjanst]");
if (vald && select) {
  const opt = [...select.options].find((o) => o.dataset.slug === vald);
  if (opt) select.value = opt.value;
}

/* Mobilmeny: fäll ut tjänsterna */
document.querySelectorAll(".sub-toggle").forEach((btn) => btn.addEventListener("click", () => {
  const open = btn.getAttribute("aria-expanded") !== "true";
  btn.setAttribute("aria-expanded", String(open));
  document.getElementById(btn.getAttribute("aria-controls")).hidden = !open;
}));
