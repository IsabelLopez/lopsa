/* lopsa.com.pa — comportamiento mínimo, sin dependencias */
(function () {
  'use strict';

  var WA = '50766044196';

  /* Menú móvil */
  var btnMenu = document.getElementById('btn-menu');
  var nav = document.getElementById('nav');
  if (btnMenu && nav) {
    btnMenu.addEventListener('click', function () {
      var abierto = btnMenu.getAttribute('aria-expanded') === 'true';
      btnMenu.setAttribute('aria-expanded', String(!abierto));
      nav.classList.toggle('abierto', !abierto);
      document.body.classList.toggle('menu-abierto', !abierto);
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        btnMenu.setAttribute('aria-expanded', 'false');
        nav.classList.remove('abierto');
        document.body.classList.remove('menu-abierto');
      }
    });
  }

  /* Pestañas del esquema de capas */
  var tabs = document.querySelectorAll('.pestanas [role="tab"]');
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      tabs.forEach(function (t) {
        var activo = t === tab;
        t.setAttribute('aria-selected', String(activo));
        t.tabIndex = activo ? 0 : -1;
        var panel = document.getElementById(t.getAttribute('aria-controls'));
        if (panel) panel.hidden = !activo;
      });
    });
  });

  /* Filtro de proyectos */
  var filtros = document.querySelectorAll('.filtros [data-filtro]');
  var casos = document.querySelectorAll('.caso');
  filtros.forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.getAttribute('data-filtro');
      filtros.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      casos.forEach(function (c) {
        c.hidden = !(f === 'Todos' || c.getAttribute('data-tipo') === f);
      });
    });
  });

  /* Visor de fotos */
  var visor = document.getElementById('visor');
  var visorImg = document.getElementById('visor-img');
  var visorPie = document.getElementById('visor-pie');
  if (visor && visorImg && typeof visor.showModal === 'function') {
    document.querySelectorAll('.caso__abrir').forEach(function (b) {
      b.addEventListener('click', function () {
        var img = b.querySelector('img');
        if (!img) return;
        var srcset = img.getAttribute('srcset') || '';
        var partes = srcset.split(',').map(function (s) { return s.trim().split(' ')[0]; }).filter(Boolean);
        visorImg.src = partes.length ? partes[partes.length - 1] : img.src;
        visorImg.alt = b.getAttribute('data-alt') || img.alt || '';
        visorPie.textContent = visorImg.alt;
        visor.showModal();
      });
    });
    document.getElementById('visor-cerrar').addEventListener('click', function () { visor.close(); });
    visor.addEventListener('click', function (e) { if (e.target === visor) visor.close(); });
  }

  /* Cotizador en tres toques */
  var chips = document.querySelectorAll('#cotizador .chips [data-tipo]');
  var area = document.getElementById('cot-area');
  var lugar = document.getElementById('cot-lugar');
  var enviar = document.getElementById('cot-enviar');
  var tipoElegido = '';
  function armar() {
    if (!enviar) return;
    var partes = ['Hola LOPSA, escribo desde lopsa.com.pa.'];
    if (tipoElegido) partes.push('Quiero cotizar: ' + tipoElegido + '.');
    else partes.push('Quiero cotizar un proyecto de poliurea caliente.');
    if (area && area.value) partes.push('Área aproximada: ' + area.value + ' m².');
    if (lugar && lugar.value) partes.push('Ubicación: ' + lugar.value.trim() + '.');
    enviar.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(partes.join(' '));
  }
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      tipoElegido = c.getAttribute('data-tipo');
      chips.forEach(function (x) { x.setAttribute('aria-pressed', String(x === c)); });
      armar();
    });
  });
  if (area) area.addEventListener('input', armar);
  if (lugar) lugar.addEventListener('input', armar);

  /* Botón flotante de WhatsApp: dos opciones; se oculta cuando el contacto está en pantalla */
  var flotante = document.getElementById('flotante');
  var btnFlotante = document.getElementById('btn-flotante');
  var menuFlotante = document.getElementById('flotante-menu');
  if (btnFlotante && menuFlotante) {
    btnFlotante.addEventListener('click', function () {
      var abierto = btnFlotante.getAttribute('aria-expanded') === 'true';
      btnFlotante.setAttribute('aria-expanded', String(!abierto));
      menuFlotante.hidden = abierto;
    });
    document.addEventListener('click', function (e) {
      if (!flotante.contains(e.target)) {
        btnFlotante.setAttribute('aria-expanded', 'false');
        menuFlotante.hidden = true;
      }
    });
  }
  var contacto = document.getElementById('contacto');
  var barra = document.getElementById('barra-movil');
  if (contacto && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entradas) {
      var visible = entradas[0].isIntersecting;
      if (flotante) flotante.classList.toggle('oculto', visible);
      if (barra) barra.classList.toggle('oculto', visible);
    }, { threshold: 0.2 }).observe(contacto);
  }

  /* Origen del formulario y medición de clics a WhatsApp (dataLayer si existe) */
  var origen = document.getElementById('form-origen');
  if (origen) {
    var q = new URLSearchParams(location.search);
    var fuente = q.get('utm_source') || q.get('origen') || document.referrer.replace(/^https?:\/\//, '').split('/')[0] || 'directo';
    origen.value = 'web · ' + fuente;
  }
  document.querySelectorAll('[data-wa]').forEach(function (a) {
    a.addEventListener('click', function () {
      if (window.dataLayer) window.dataLayer.push({ event: 'whatsapp_click', lugar: a.getAttribute('data-wa') });
    });
  });
})();
