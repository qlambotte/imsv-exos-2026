// QCM cliquables (page Séance récapitulative › Séries). Structure produite par slides/recap/make-wooclap.py :
//   .qcm (une série) > encadrés « Exercice » > .qcm-q[data-correct=k] > (.qcm-choix > ul > li)×4,
//   puis .qcm-expl (seulement si corrige-exos: true) ; en fin de série : .qcm-actions > boutons + score.
// « Valider la série » colore la réponse cochée (vert si bonne, rouge sinon), sans montrer la bonne
// réponse. Si les explications sont publiées, elles s'affichent après validation.
(function () {
  var css = [
    ".qcm-q{margin:.8em 0 1em}",
    ".qcm-q > p{margin-bottom:.3em}",
    ".qcm-choix ul{list-style:none;padding-left:.2em;margin:.2em 0}",
    ".qcm-choix li{position:relative;padding:.15em .4em .15em 1.7em;margin:.1em 0;border-radius:.3em;cursor:pointer}",
    ".qcm-choix li::before{content:'';position:absolute;left:.3em;top:.55em;width:.8em;height:.8em;border:1.5px solid rgba(127,127,127,.7);border-radius:50%}",
    ".qcm-choix li:hover{background:rgba(127,127,127,.08)}",
    ".qcm-choix li.sel::before{border-color:#1f5fbf;background:#1f5fbf;box-shadow:inset 0 0 0 2px var(--bs-body-bg, #fff)}",
    ".qcm-choix li.ok{background:rgba(46,125,70,.14)}",
    ".qcm-choix li.ok::before{border-color:#2e7d46;background:#2e7d46}",
    ".qcm-choix li.ko{background:rgba(181,56,31,.13)}",
    ".qcm-choix li.ko::before{border-color:#b5381f;background:#b5381f}",
    ".qcm-choix li.ok::after{content:' ✓';color:#2e7d46;font-weight:700}",
    ".qcm-choix li.ko::after{content:' ✗';color:#b5381f;font-weight:700}",
    ".qcm-done .qcm-choix li{cursor:default}",
    ".qcm-done .qcm-choix li:hover{background:none}",
    ".qcm-done .qcm-choix li.ok:hover{background:rgba(46,125,70,.14)}",
    ".qcm-done .qcm-choix li.ko:hover{background:rgba(181,56,31,.13)}",
    ".qcm-vide > p:first-child{color:#b5381f}",
    ".qcm-expl{display:none;font-size:.9em;border-left:3px solid rgba(46,125,70,.6);padding-left:.7em;margin-top:.4em}",
    ".qcm-expl ul{margin-bottom:0}",
    ".qcm-done .qcm-expl{display:block}",
    ".qcm-actions{display:flex;flex-wrap:wrap;gap:.6em;align-items:center;margin:.4em 0 2em}",
    ".qcm-actions button{border:1.5px solid #1f5fbf;border-radius:.4em;background:transparent;color:inherit;padding:.25em .9em;font-weight:600}",
    ".qcm-actions .qcm-valider{background:#1f5fbf;color:#fff}",
    ".qcm-actions .qcm-score{font-weight:600}"
  ].join("\n");
  var st = document.createElement("style");
  st.textContent = css;
  document.head.appendChild(st);

  function items(q) { return Array.prototype.slice.call(q.querySelectorAll(".qcm-choix li")); }

  document.querySelectorAll(".qcm").forEach(function (bloc) {
    var qs = Array.prototype.slice.call(bloc.querySelectorAll(".qcm-q"));
    var score = bloc.querySelector(".qcm-score");

    qs.forEach(function (q) {
      items(q).forEach(function (li) {
        li.setAttribute("role", "radio");
        li.setAttribute("tabindex", "0");
        function choisir() {
          if (bloc.classList.contains("qcm-done")) return;
          items(q).forEach(function (x) { x.classList.remove("sel"); x.setAttribute("aria-checked", "false"); });
          li.classList.add("sel");
          li.setAttribute("aria-checked", "true");
          q.classList.remove("qcm-vide");
        }
        li.addEventListener("click", choisir);
        li.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); choisir(); } });
      });
    });

    bloc.querySelector(".qcm-valider").addEventListener("click", function () {
      var vides = qs.filter(function (q) { return !q.querySelector(".qcm-choix li.sel"); });
      if (vides.length) {
        vides.forEach(function (q) { q.classList.add("qcm-vide"); });
        score.textContent = "Réponds à toutes les questions de la série avant de valider.";
        return;
      }
      var bons = 0;
      qs.forEach(function (q) {
        var lis = items(q);
        var k = parseInt(q.getAttribute("data-correct"), 10) - 1;
        var sel = lis.findIndex(function (x) { return x.classList.contains("sel"); });
        lis[sel].classList.remove("sel");
        lis[sel].classList.add(sel === k ? "ok" : "ko");
        if (sel === k) bons++;
      });
      bloc.classList.add("qcm-done");
      score.textContent = "Score : " + bons + " / " + qs.length;
    });

    bloc.querySelector(".qcm-reset").addEventListener("click", function () {
      bloc.classList.remove("qcm-done");
      qs.forEach(function (q) {
        q.classList.remove("qcm-vide");
        items(q).forEach(function (x) { x.classList.remove("sel", "ok", "ko"); x.setAttribute("aria-checked", "false"); });
      });
      score.textContent = "";
    });
  });
})();
