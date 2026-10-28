<!-- SLIDE « AU TRAVAIL » RÉUTILISABLE : QR du site · jauge de bruit · minuteur.
     Usage, dans n'importe quel deck (une ligne sous un titre de slide) :

         ## Au travail {.travail data-minutes="30"}

         {{{< include ../seance01/_travail.md >}}}

     (chemin relatif au deck : ../seance01/_travail.md depuis slides/_seanceNN/)
     - data-minutes : durée du minuteur (30 si absent) ; le titre est masqué à l'écran.
     - classe .sans-jauge (## Au travail {.travail .sans-jauge data-minutes="35"}) : ni jauge de bruit
       ni sonnerie à la fin du minuteur (décision après le sondage d'octobre 2026, à partir de la séance 6).
     - Jauge : bouton micro = on/off ; « Calibrer » = mesure 3 s le bruit ambiant (pièce calme) et recale l'échelle ;
       curseur « Bruit maximal » = seuil ; cloche = alerte sonore on/off (off par défaut) ; badge = nombre de dépassements.
       Le micro est coupé quand on quitte la slide. Réglages (seuil, calibrage) gardés dans le navigateur.
     - QR : change l'adresse avec `python3 make-travail-qr.py URL` (dans ce dossier).
     Ce fichier est un bloc HTML brut : ne pas y mettre de ligne markdown. -->
```{=html}
<style>
.reveal section.travail > h2 { display: none; }
.reveal section.travail.sans-jauge .tv-gauge { display: none; }
.reveal .tv-wrap { display: flex; align-items: center; justify-content: space-between; gap: 36px; height: 640px; padding: 0 10px; box-sizing: border-box; font-family: inherit; color: #14304a; }
.reveal .tv-qr { flex: 0 0 260px; text-align: center; }
.reveal .tv-qr-svg { width: 240px; height: 240px; display: block; margin: 0 auto 14px; border: 3px solid #14304a; border-radius: 10px; box-sizing: content-box; }
.reveal .tv-cap { font-size: 22px; line-height: 1.3; }
.reveal .tv-gauge { flex: 1 1 auto; text-align: center; }
.reveal .tv-arc { width: 500px; height: 268px; display: block; margin: 0 auto; }
.reveal .tv-title { font-size: 26px; margin: 6px 0 10px; }
.reveal .tv-thr { width: 500px; max-width: 100%; accent-color: #1f5fbf; }
.reveal .tv-row { display: flex; justify-content: center; align-items: center; gap: 26px; margin-top: 18px; }
.reveal .tv-btn { width: 64px; height: 64px; border-radius: 50%; border: 2px solid #14304a; background: #fff; color: #14304a; cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; }
.reveal .tv-btn svg { width: 30px; height: 30px; }
.reveal .tv-btn.tv-on { background: #1f5fbf; border-color: #1f5fbf; color: #fff; }
.reveal .tv-btn.tv-alert { background: #c0392b; border-color: #c0392b; color: #fff; }
.reveal .tv-count { min-width: 96px; height: 56px; border-radius: 28px; background: #e7f0ff; color: #1f5fbf; font-size: 30px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px; }
.reveal .tv-count svg { width: 24px; height: 24px; }
.reveal .tv-small { height: 44px; padding: 0 18px; border-radius: 22px; border: 2px solid #14304a; background: #fff; color: #14304a; font-size: 20px; cursor: pointer; font-family: inherit; }
.reveal .tv-state { font-size: 20px; min-height: 26px; margin-top: 8px; }
.reveal .tv-timer { flex: 0 0 300px; text-align: center; }
.reveal .tv-dial { width: 270px; height: 270px; display: block; margin: 0 auto; }
.reveal .tv-time { font-size: 54px; font-variant-numeric: tabular-nums; margin: 6px 0; }
.reveal .tv-time.tv-warn { color: #c0392b; }
.reveal .tv-tctl { display: flex; justify-content: center; align-items: center; gap: 14px; }
.reveal .tv-play { width: 64px; height: 64px; border-radius: 50%; border: none; background: #1f5fbf; color: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; padding: 0; }
.reveal .tv-play svg { width: 28px; height: 28px; }
.reveal .tv-mini { display: flex; justify-content: center; gap: 6px; margin-top: 14px; }
.reveal .tv-mini button { height: 40px; min-width: 50px; padding: 0 8px; border-radius: 20px; border: 2px solid #14304a; background: #fff; color: #14304a; font-size: 19px; cursor: pointer; font-family: inherit; }
</style>
<div class="tv-wrap">
  <div class="tv-qr">
<!--QR--><svg class="tv-qr-svg" viewBox="-2 -2 33 33" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="QR code du site"><rect x="-2" y="-2" width="33" height="33" fill="#fff"/><path d="M0 0h7v1h-7zM8 0h1v1h-1zM13 0h1v1h-1zM15 0h2v1h-2zM22 0h7v1h-7zM0 1h1v1h-1zM6 1h1v1h-1zM8 1h1v1h-1zM11 1h2v1h-2zM14 1h1v1h-1zM16 1h1v1h-1zM19 1h2v1h-2zM22 1h1v1h-1zM28 1h1v1h-1zM0 2h1v1h-1zM2 2h3v1h-3zM6 2h1v1h-1zM8 2h2v1h-2zM12 2h1v1h-1zM14 2h1v1h-1zM17 2h2v1h-2zM22 2h1v1h-1zM24 2h3v1h-3zM28 2h1v1h-1zM0 3h1v1h-1zM2 3h3v1h-3zM6 3h1v1h-1zM8 3h3v1h-3zM12 3h2v1h-2zM16 3h1v1h-1zM18 3h2v1h-2zM22 3h1v1h-1zM24 3h3v1h-3zM28 3h1v1h-1zM0 4h1v1h-1zM2 4h3v1h-3zM6 4h1v1h-1zM9 4h2v1h-2zM12 4h1v1h-1zM14 4h3v1h-3zM18 4h1v1h-1zM22 4h1v1h-1zM24 4h3v1h-3zM28 4h1v1h-1zM0 5h1v1h-1zM6 5h1v1h-1zM8 5h3v1h-3zM13 5h1v1h-1zM17 5h4v1h-4zM22 5h1v1h-1zM28 5h1v1h-1zM0 6h7v1h-7zM8 6h1v1h-1zM10 6h1v1h-1zM12 6h1v1h-1zM14 6h1v1h-1zM16 6h1v1h-1zM18 6h1v1h-1zM20 6h1v1h-1zM22 6h7v1h-7zM10 7h2v1h-2zM14 7h4v1h-4zM20 7h1v1h-1zM0 8h2v1h-2zM4 8h3v1h-3zM10 8h1v1h-1zM12 8h1v1h-1zM14 8h6v1h-6zM23 8h1v1h-1zM25 8h4v1h-4zM0 9h2v1h-2zM3 9h1v1h-1zM5 9h1v1h-1zM13 9h1v1h-1zM15 9h4v1h-4zM22 9h7v1h-7zM1 10h3v1h-3zM6 10h5v1h-5zM13 10h1v1h-1zM15 10h1v1h-1zM18 10h1v1h-1zM20 10h3v1h-3zM28 10h1v1h-1zM1 11h3v1h-3zM5 11h1v1h-1zM7 11h1v1h-1zM9 11h1v1h-1zM12 11h1v1h-1zM15 11h1v1h-1zM17 11h1v1h-1zM21 11h1v1h-1zM24 11h2v1h-2zM27 11h2v1h-2zM0 12h2v1h-2zM3 12h2v1h-2zM6 12h1v1h-1zM11 12h1v1h-1zM14 12h1v1h-1zM17 12h1v1h-1zM20 12h2v1h-2zM27 12h1v1h-1zM4 13h2v1h-2zM8 13h1v1h-1zM10 13h1v1h-1zM12 13h2v1h-2zM15 13h4v1h-4zM22 13h7v1h-7zM2 14h1v1h-1zM5 14h2v1h-2zM10 14h3v1h-3zM15 14h1v1h-1zM17 14h1v1h-1zM20 14h1v1h-1zM25 14h2v1h-2zM28 14h1v1h-1zM0 15h1v1h-1zM2 15h4v1h-4zM8 15h4v1h-4zM15 15h1v1h-1zM17 15h4v1h-4zM23 15h1v1h-1zM27 15h2v1h-2zM4 16h1v1h-1zM6 16h2v1h-2zM9 16h1v1h-1zM12 16h1v1h-1zM14 16h2v1h-2zM17 16h1v1h-1zM19 16h3v1h-3zM27 16h1v1h-1zM0 17h2v1h-2zM3 17h1v1h-1zM5 17h1v1h-1zM7 17h4v1h-4zM13 17h1v1h-1zM15 17h1v1h-1zM17 17h2v1h-2zM21 17h5v1h-5zM27 17h2v1h-2zM3 18h8v1h-8zM13 18h1v1h-1zM15 18h2v1h-2zM18 18h1v1h-1zM22 18h2v1h-2zM26 18h1v1h-1zM28 18h1v1h-1zM2 19h4v1h-4zM12 19h1v1h-1zM17 19h6v1h-6zM24 19h1v1h-1zM27 19h2v1h-2zM0 20h3v1h-3zM6 20h3v1h-3zM11 20h1v1h-1zM14 20h1v1h-1zM16 20h3v1h-3zM20 20h6v1h-6zM28 20h1v1h-1zM8 21h1v1h-1zM12 21h2v1h-2zM15 21h6v1h-6zM24 21h1v1h-1zM28 21h1v1h-1zM0 22h7v1h-7zM9 22h7v1h-7zM18 22h3v1h-3zM22 22h1v1h-1zM24 22h3v1h-3zM28 22h1v1h-1zM0 23h1v1h-1zM6 23h1v1h-1zM8 23h4v1h-4zM16 23h3v1h-3zM20 23h1v1h-1zM24 23h1v1h-1zM0 24h1v1h-1zM2 24h3v1h-3zM6 24h1v1h-1zM8 24h2v1h-2zM12 24h1v1h-1zM14 24h1v1h-1zM16 24h2v1h-2zM19 24h7v1h-7zM28 24h1v1h-1zM0 25h1v1h-1zM2 25h3v1h-3zM6 25h1v1h-1zM9 25h2v1h-2zM14 25h5v1h-5zM20 25h2v1h-2zM28 25h1v1h-1zM0 26h1v1h-1zM2 26h3v1h-3zM6 26h1v1h-1zM10 26h1v1h-1zM13 26h3v1h-3zM17 26h1v1h-1zM19 26h1v1h-1zM25 26h4v1h-4zM0 27h1v1h-1zM6 27h1v1h-1zM8 27h3v1h-3zM12 27h1v1h-1zM14 27h2v1h-2zM17 27h2v1h-2zM20 27h1v1h-1zM22 27h1v1h-1zM25 27h1v1h-1zM27 27h2v1h-2zM0 28h7v1h-7zM8 28h1v1h-1zM10 28h6v1h-6zM17 28h1v1h-1zM20 28h1v1h-1zM24 28h1v1h-1zM27 28h1v1h-1z" fill="#000" shape-rendering="crispEdges"/></svg><!--/QR-->
    <div class="tv-cap">Le site de la séance :<br>indices, solutions, fiches</div>
  </div>
  <div class="tv-gauge">
    <svg class="tv-arc" viewBox="0 0 560 300" aria-label="Jauge de bruit"></svg>
    <div class="tv-title">Bruit maximal</div>
    <input class="tv-thr" type="range" min="10" max="95" value="60" aria-label="Seuil de bruit maximal">
    <div class="tv-row">
      <button class="tv-btn tv-bell" type="button" title="Alerte sonore on/off" aria-label="Alerte sonore">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0112 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 003.4 0"/></svg>
      </button>
      <div class="tv-count" title="Nombre de dépassements"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="13" r="7"/><path d="M12 9v4l2 2"/><path d="M5 3L2 6M19 3l3 3"/></svg><span class="tv-n">0</span></div>
      <button class="tv-btn tv-mic" type="button" title="Micro on/off" aria-label="Micro">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0014 0"/><path d="M12 18v4"/></svg>
      </button>
      <button class="tv-small tv-cal" type="button">Calibrer</button>
    </div>
    <div class="tv-state"></div>
  </div>
  <div class="tv-timer">
    <svg class="tv-dial" viewBox="-150 -150 300 300" aria-label="Minuteur"></svg>
    <div class="tv-time">30:00</div>
    <div class="tv-tctl">
      <button class="tv-play" type="button" aria-label="Démarrer / pause"></button>
    </div>
    <div class="tv-mini">
      <button type="button" data-d="-300">−5</button><button type="button" data-d="-60">−1</button><button type="button" data-d="60">+1</button><button type="button" data-d="300">+5</button><button type="button" data-d="0">↺</button>
    </div>
  </div>
</div>
<script>
(function () {
  var PLAY = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4l13 8-13 8z"/></svg>';
  var PAUSE = '<svg viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>';
  var BLUE = '#1f5fbf', LIGHT = '#e7f0ff', REDL = '#fbe3e0', RED = '#c0392b';
  var audioCtx = null, active = null;     // un seul micro actif à la fois

  function ctx() {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') audioCtx.resume();
    return audioCtx;
  }
  function beep(freq, n) {
    try {
      var c = ctx(), t0 = c.currentTime;
      for (var i = 0; i < n; i++) {
        var o = c.createOscillator(), g = c.createGain();
        o.type = 'sine'; o.frequency.value = freq;
        g.gain.setValueAtTime(0.0001, t0 + i * 0.35);
        g.gain.exponentialRampToValueAtTime(0.3, t0 + i * 0.35 + 0.02);
        g.gain.exponentialRampToValueAtTime(0.0001, t0 + i * 0.35 + 0.28);
        o.connect(g); g.connect(c.destination);
        o.start(t0 + i * 0.35); o.stop(t0 + i * 0.35 + 0.3);
      }
    } catch (e) {}
  }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem('tv-' + k); localStorage.setItem('tv-' + k, v); } catch (e) {} return null; }

  function setup(wrap) {
    var $ = function (s) { return wrap.querySelector(s); };
    var section = wrap.closest('section');

    /* ---------- jauge ---------- */
    var arc = $('.tv-arc'), thr = $('.tv-thr'), btnMic = $('.tv-mic'), btnBell = $('.tv-bell'),
        nEl = $('.tv-n'), stateEl = $('.tv-state'), btnCal = $('.tv-cal');
    var CX = 280, CY = 280, R1 = 270, R0 = 160;       // demi-anneau
    function pt(a, r) { return [CX + r * Math.cos(Math.PI * (1 - a)), CY - r * Math.sin(Math.PI * (1 - a))]; }
    function sector(a0, a1) {
      var p = [pt(a0, R1), pt(a1, R1), pt(a1, R0), pt(a0, R0)];
      return 'M' + p[0] + 'A' + R1 + ' ' + R1 + ' 0 0 1 ' + p[1] + 'L' + p[2] + 'A' + R0 + ' ' + R0 + ' 0 0 0 ' + p[3] + 'Z';
    }
    arc.innerHTML = '<path class="a-ok" fill="' + LIGHT + '"/><path class="a-no" fill="' + REDL + '"/><path class="a-lv" fill="' + BLUE + '"/>';
    var pOk = arc.querySelector('.a-ok'), pNo = arc.querySelector('.a-no'), pLv = arc.querySelector('.a-lv');
    var floorDb = parseFloat(store('floor')) || -75, RANGE = 40;
    var savedThr = parseFloat(store('thr')); if (savedThr) thr.value = savedThr;
    var level = 0, over = 0, count = 0, bell = false, micOn = false, stream = null, an = null, buf = null, raf = 0, calUntil = 0, calSum = 0, calN = 0, tOver = 0, quiet = 0, lastBeep = 0;
    function drawZones() {
      var t = thr.value / 100;
      pOk.setAttribute('d', sector(0, t)); pNo.setAttribute('d', sector(t, 1));
    }
    function drawLevel() {
      var t = thr.value / 100;
      pLv.setAttribute('fill', level > t ? RED : BLUE);
      pLv.setAttribute('d', level > 0.004 ? sector(0, level) : '');
    }
    drawZones(); drawLevel();
    thr.addEventListener('input', function () { drawZones(); drawLevel(); store('thr', thr.value); });
    thr.addEventListener('change', function () { thr.blur(); });
    btnBell.addEventListener('click', function () { bell = !bell; btnBell.classList.toggle('tv-on', bell); if (bell) beep(660, 1); });

    function say(t) { stateEl.textContent = t || ''; }
    function stopMic() {
      micOn = false; btnMic.classList.remove('tv-on'); cancelAnimationFrame(raf);
      if (stream) { stream.getTracks().forEach(function (t) { t.stop(); }); stream = null; }
      level = 0; drawLevel(); if (active === api) active = null;
    }
    function startMic(then) {
      if (active && active !== api) active.stop();
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) { say('Micro indisponible dans ce navigateur.'); return; }
      navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: false, noiseSuppression: false, autoGainControl: false } }).then(function (s) {
        stream = s; var c = ctx(); an = c.createAnalyser(); an.fftSize = 1024; buf = new Float32Array(an.fftSize);
        c.createMediaStreamSource(s).connect(an);
        micOn = true; active = api; btnMic.classList.add('tv-on'); say(''); loop(); if (then) then();
      }).catch(function () { say('Accès au micro refusé.'); });
    }
    btnMic.addEventListener('click', function () { micOn ? stopMic() : startMic(); });
    btnCal.addEventListener('click', function () {
      function go() { calUntil = performance.now() + 3000; calSum = 0; calN = 0; say('Calibrage : silence pendant 3 s…'); }
      micOn ? go() : startMic(go);
    });
    function loop() {
      if (!micOn) return;
      an.getFloatTimeDomainData(buf);
      var s = 0; for (var i = 0; i < buf.length; i++) s += buf[i] * buf[i];
      var db = 20 * Math.log10(Math.sqrt(s / buf.length) + 1e-9), now = performance.now();
      if (calUntil) {
        calSum += db; calN++;
        if (now > calUntil) { calUntil = 0; floorDb = calSum / calN - 6; store('floor', floorDb); say('Calibré : le bruit ambiant est à environ 15 %.'); setTimeout(function () { say(''); }, 4000); }
      }
      var raw = Math.max(0, Math.min(1, (db - floorDb) / RANGE));
      level += (raw - level) * (raw > level ? 0.5 : 0.07);
      var t = thr.value / 100;
      if (level > t) { tOver = tOver || now; quiet = 0;
        if (now - tOver > 600 && !over) { over = 1; count++; nEl.textContent = count; btnMic.classList.add('tv-alert'); setTimeout(function () { btnMic.classList.remove('tv-alert'); }, 1200);
          if (bell && now - lastBeep > 3000) { beep(880, 2); lastBeep = now; } }
      } else { tOver = 0; if (level < t - 0.05) { quiet = quiet || now; if (now - quiet > 1000) over = 0; } }
      drawLevel(); raf = requestAnimationFrame(loop);
    }

    /* ---------- minuteur ---------- */
    var dial = $('.tv-dial'), timeEl = $('.tv-time'), btnPlay = $('.tv-play');
    var DUR = (parseFloat(section && section.getAttribute('data-minutes')) || 30) * 60, remaining = DUR, running = false, iv = null;
    var ticks = '';
    for (var m = 0; m < 60; m++) {
      var a = m * Math.PI / 30, big = m % 5 === 0, r2 = big ? 128 : 134;
      ticks += '<line x1="' + (Math.sin(a) * 140).toFixed(1) + '" y1="' + (-Math.cos(a) * 140).toFixed(1) + '" x2="' + (Math.sin(a) * r2).toFixed(1) + '" y2="' + (-Math.cos(a) * r2).toFixed(1) + '" stroke="#14304a" stroke-width="' + (big ? 2 : 1) + '"/>';
      if (big) ticks += '<text x="' + (Math.sin(a) * 114).toFixed(1) + '" y="' + (-Math.cos(a) * 114 + 6).toFixed(1) + '" text-anchor="middle" font-size="16" fill="#14304a">' + m + '</text>';
    }
    dial.innerHTML = '<circle r="100" fill="' + LIGHT + '"/><path class="d-rem" fill="' + BLUE + '"/>' + ticks + '<circle r="4" fill="#14304a"/>';
    var dRem = dial.querySelector('.d-rem');
    function fmt(s) { s = Math.max(0, Math.ceil(s)); var mm = Math.floor(s / 60), ss = s % 60; return (mm < 10 ? '0' : '') + mm + ':' + (ss < 10 ? '0' : '') + ss; }
    function render() {
      timeEl.textContent = fmt(remaining); timeEl.classList.toggle('tv-warn', remaining <= 30);
      var f = Math.min(1, remaining / 3600), a = f * 2 * Math.PI;
      if (f >= 0.9999) dRem.setAttribute('d', 'M0 -100A100 100 0 1 1 -0.01 -100Z');
      else if (f <= 0) dRem.setAttribute('d', '');
      else dRem.setAttribute('d', 'M0 0L0 -100A100 100 0 ' + (a > Math.PI ? 1 : 0) + ' 1 ' + (Math.sin(a) * 100).toFixed(2) + ' ' + (-Math.cos(a) * 100).toFixed(2) + 'Z');
      btnPlay.innerHTML = running ? PAUSE : PLAY;
    }
    function stopT() { running = false; clearInterval(iv); iv = null; render(); }
    function tick() { remaining -= 1; if (remaining <= 0) { remaining = 0; stopT(); if (!(section && section.classList.contains('sans-jauge'))) beep(880, 2); } render(); }
    btnPlay.addEventListener('click', function () {
      if (running) { stopT(); return; }
      if (remaining <= 0) remaining = DUR;
      try { ctx(); } catch (e) {}
      running = true; iv = setInterval(tick, 1000); render();
    });
    Array.prototype.forEach.call(wrap.querySelectorAll('.tv-mini button'), function (b) {
      b.addEventListener('click', function () {
        var d = parseInt(b.getAttribute('data-d'), 10);
        if (d === 0) { stopT(); remaining = DUR; } else remaining = Math.max(0, remaining + d);
        render(); b.blur();
      });
    });
    render();
    var api = { stop: stopMic };

    // micro coupé dès qu'on quitte la slide
    function watch() {
      if (!window.Reveal) { setTimeout(watch, 300); return; }
      window.Reveal.on('slidechanged', function (e) { if (micOn && section && e.currentSlide !== section) stopMic(); });
    }
    watch();
  }
  function boot() { Array.prototype.forEach.call(document.querySelectorAll('.tv-wrap'), setup); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
</script>
```
