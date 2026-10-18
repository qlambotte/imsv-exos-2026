<!-- MINUTEUR RÉUTILISABLE, même présentation que celui de l'échauffement (−1 min · Démarrer · +1 min · Réinitialiser).
     Usage, dans une slide d'un deck de slides/_seanceNN/ :

         ::: {.minuteur data-minutes="2"}
         {{{< include ../seance01/_minuteur.md >}}}
         :::

     - data-minutes : durée (2 si absent). Un bip retentit à la fin ; le chiffre devient orange sous 30 s, rouge à zéro.
     - Remis à zéro quand on quitte la slide. Styles : classes .et-* de seance01/theme.scss (.et-box).
     Ce fichier est un bloc HTML brut : ne pas y mettre de ligne markdown. -->
```{=html}
<style>
@keyframes et-pulse { 0%, 100% { opacity: 1; } 50% { opacity: .35; } }
</style>
<div class="et-timer"><div class="et-box">
  <div class="et-row">
    <button class="et-btn mn-minus" type="button" aria-label="Retirer une minute">−1 min</button>
    <div class="et-display mn-display">02:00</div>
    <button class="et-btn mn-plus" type="button" aria-label="Ajouter une minute">+1 min</button>
  </div>
  <div class="et-row">
    <button class="et-btn et-primary mn-toggle" type="button">Démarrer</button>
    <button class="et-btn mn-reset" type="button" aria-label="Réinitialiser">↺ Réinitialiser</button>
  </div>
</div></div>
<script>
(function () {
  if (window.__minuteurInit) return; window.__minuteurInit = true;
  var audioCtx = null;
  function beep() {
    try {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      var t0 = audioCtx.currentTime;
      [0, 0.35].forEach(function (o) {
        var osc = audioCtx.createOscillator(), g = audioCtx.createGain();
        osc.type = 'sine'; osc.frequency.value = 880;
        g.gain.setValueAtTime(0.0001, t0 + o);
        g.gain.exponentialRampToValueAtTime(0.3, t0 + o + 0.02);
        g.gain.exponentialRampToValueAtTime(0.0001, t0 + o + 0.28);
        osc.connect(g); g.connect(audioCtx.destination); osc.start(t0 + o); osc.stop(t0 + o + 0.3);
      });
    } catch (e) {}
  }
  function fmt(s) { s = Math.max(0, s); var m = Math.floor(s / 60), r = s % 60; return (m < 10 ? '0' : '') + m + ':' + (r < 10 ? '0' : '') + r; }
  function init(host) {
    if (host.__mn) return; var root = host.querySelector('.et-box'); if (!root) return; host.__mn = true;
    var DEFAULT = Math.round((parseFloat(host.getAttribute('data-minutes')) || 2) * 60);
    var display = root.querySelector('.mn-display'), toggle = root.querySelector('.mn-toggle');
    var section = host.closest('section'), remaining = DEFAULT, running = false, iv = null;
    function render() {
      display.textContent = fmt(remaining);
      display.classList.toggle('et-warn', running && remaining <= 30 && remaining > 0);
      display.classList.toggle('et-done', remaining === 0);
    }
    function stop() { running = false; toggle.textContent = remaining > 0 ? 'Reprendre' : 'Démarrer'; if (iv) { clearInterval(iv); iv = null; } }
    function start() {
      if (running) return;
      try { if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)(); if (audioCtx.state === 'suspended') audioCtx.resume(); } catch (e) {}
      if (remaining <= 0) remaining = DEFAULT;
      render(); running = true; toggle.textContent = 'Pause';
      iv = setInterval(function () { remaining -= 1; if (remaining <= 0) { remaining = 0; stop(); beep(); } render(); }, 1000);
    }
    function reset() { stop(); remaining = DEFAULT; toggle.textContent = 'Démarrer'; render(); }
    toggle.addEventListener('click', function () { running ? stop() : start(); });
    root.querySelector('.mn-minus').addEventListener('click', function () { remaining = Math.max(0, remaining - 60); render(); if (remaining === 0) stop(); });
    root.querySelector('.mn-plus').addEventListener('click', function () { remaining += 60; render(); });
    root.querySelector('.mn-reset').addEventListener('click', reset);
    render();
    (function watch() {
      if (!window.Reveal || !Reveal.on) { setTimeout(watch, 300); return; }
      Reveal.on('slidechanged', function () { if (section && !section.classList.contains('present')) reset(); });
    })();
  }
  function all() { Array.prototype.forEach.call(document.querySelectorAll('.minuteur'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', all); else all();
  setTimeout(all, 500);
})();
</script>
```
