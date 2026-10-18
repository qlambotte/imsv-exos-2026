<!-- MINUTEUR COMPACT RÉUTILISABLE (à placer sur n'importe quelle slide, p. ex. à côté d'un encadré Wooclap).
     Usage, dans une slide d'un deck de slides/_seanceNN/ :

         ::: {.minuteur data-minutes="2"}
         {{{< include ../seance01/_minuteur.md >}}}
         :::

     - data-minutes : durée (2 si absent). Boutons : ▶/❚❚ démarrer-pause, −1 min, +1 min, remise à zéro.
     - Un bip retentit à la fin. Le minuteur est remis à zéro quand on quitte la slide.
     - Pour la version complète (QR + jauge de bruit + minuteur), voir _travail.md.
     Ce fichier est un bloc HTML brut : ne pas y mettre de ligne markdown. -->
```{=html}
<style>
.reveal .mn-wrap { display: flex; align-items: center; justify-content: center; gap: 22px; font-family: inherit; color: #14304a; }
.reveal .mn-dial { width: 150px; height: 150px; display: block; flex: 0 0 auto; }
.reveal .mn-side { text-align: center; }
.reveal .mn-time { font-size: 56px; line-height: 1.1; font-variant-numeric: tabular-nums; }
.reveal .mn-time.mn-warn { color: #c0392b; }
.reveal .mn-ctl { display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 8px; }
.reveal .mn-play { width: 52px; height: 52px; border-radius: 50%; border: none; background: #1f5fbf; color: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; }
.reveal .mn-play svg { width: 24px; height: 24px; }
.reveal .mn-b { height: 38px; min-width: 46px; padding: 0 8px; border-radius: 19px; border: 2px solid #14304a; background: #fff; color: #14304a; font-size: 18px; cursor: pointer; font-family: inherit; }
</style>
<div class="mn-wrap">
  <svg class="mn-dial" viewBox="-110 -110 220 220" aria-label="Minuteur"></svg>
  <div class="mn-side">
    <div class="mn-time">02:00</div>
    <div class="mn-ctl">
      <button class="mn-b" type="button" data-d="-60" aria-label="Moins une minute">−1</button>
      <button class="mn-play" type="button" aria-label="Démarrer ou mettre en pause"></button>
      <button class="mn-b" type="button" data-d="60" aria-label="Plus une minute">+1</button>
      <button class="mn-b" type="button" data-d="0" aria-label="Remettre à zéro">↺</button>
    </div>
  </div>
</div>
<script>
(function () {
  if (window.__minuteurInit) return; window.__minuteurInit = true;
  var BLUE = '#1f5fbf', LIGHT = '#e7f0ff';
  var PLAY = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4l13 8-13 8z"/></svg>';
  var PAUSE = '<svg viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>';
  var actx = null;
  function beep() {
    try { actx = actx || new (window.AudioContext || window.webkitAudioContext)();
      [0, 0.35, 0.7].forEach(function (d) { var o = actx.createOscillator(), g = actx.createGain();
        o.frequency.value = 880; g.gain.value = 0.2; o.connect(g); g.connect(actx.destination);
        o.start(actx.currentTime + d); o.stop(actx.currentTime + d + 0.2); }); } catch (e) {}
  }
  function fmt(s) { s = Math.max(0, Math.ceil(s)); var m = Math.floor(s / 60), r = s % 60; return (m < 10 ? '0' : '') + m + ':' + (r < 10 ? '0' : '') + r; }
  function init(box) {
    if (box.__mn) return; box.__mn = true;
    var wrap = box.querySelector('.mn-wrap'); if (!wrap) return;
    var section = box.closest('section');
    var dial = wrap.querySelector('.mn-dial'), timeEl = wrap.querySelector('.mn-time'), btn = wrap.querySelector('.mn-play');
    var DUR = (parseFloat(box.getAttribute('data-minutes')) || 2) * 60, total = DUR, remaining = DUR, running = false, iv = null;
    dial.innerHTML = '<circle r="100" fill="' + LIGHT + '"/><path class="d" fill="' + BLUE + '"/><circle r="100" fill="none" stroke="#14304a" stroke-width="3"/><circle r="4" fill="#14304a"/>';
    var d = dial.querySelector('.d');
    function render() {
      timeEl.textContent = fmt(remaining); timeEl.classList.toggle('mn-warn', remaining <= 15 && remaining > 0);
      var f = total > 0 ? Math.min(1, remaining / total) : 0, a = f * 2 * Math.PI;
      if (f >= 0.9999) d.setAttribute('d', 'M0 -100A100 100 0 1 1 -0.01 -100Z');
      else if (f <= 0) d.setAttribute('d', '');
      else d.setAttribute('d', 'M0 0L0 -100A100 100 0 ' + (a > Math.PI ? 1 : 0) + ' 1 ' + (Math.sin(a) * 100).toFixed(2) + ' ' + (-Math.cos(a) * 100).toFixed(2) + 'Z');
      btn.innerHTML = running ? PAUSE : PLAY;
    }
    function stop() { running = false; clearInterval(iv); iv = null; render(); }
    function reset() { stop(); total = DUR; remaining = DUR; render(); }
    btn.addEventListener('click', function () {
      if (running) { stop(); return; }
      if (remaining <= 0) { total = DUR; remaining = DUR; }
      try { actx = actx || new (window.AudioContext || window.webkitAudioContext)(); } catch (e) {}
      running = true; iv = setInterval(function () { remaining -= 1; if (remaining <= 0) { remaining = 0; stop(); beep(); } render(); }, 1000); render(); btn.blur();
    });
    Array.prototype.forEach.call(wrap.querySelectorAll('.mn-b'), function (b) {
      b.addEventListener('click', function () {
        var dd = parseInt(b.getAttribute('data-d'), 10);
        if (dd === 0) reset(); else { remaining = Math.max(0, remaining + dd); total = Math.max(total, remaining); render(); }
        b.blur();
      });
    });
    render();
    function watch() {
      if (!window.Reveal || !Reveal.on) { setTimeout(watch, 300); return; }
      Reveal.on('slidechanged', function () { if (section && !section.classList.contains('present')) reset(); });
    }
    watch();
  }
  function all() { Array.prototype.forEach.call(document.querySelectorAll('.minuteur'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', all); else all();
  setTimeout(all, 500);
})();
</script>
```
