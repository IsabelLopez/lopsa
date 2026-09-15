/* lopsa.com.pa — comportamiento mínimo, sin dependencias */
(function () {
  'use strict';

  var WA = '50766044196';

  /* Menú móvil */
  var btnMenu = document.getElementById('btn-menu');
  var nav = document.getElementById('nav');
  if (btnMenu && nav) {
    var etiquetaMenu = btnMenu.querySelector('.visualmente-oculto');
    function esMenuMovil() {
      return window.getComputedStyle(btnMenu).display !== 'none';
    }
    function cambiarMenu(abierto, devolverFoco) {
      btnMenu.setAttribute('aria-expanded', String(abierto));
      nav.classList.toggle('abierto', abierto);
      document.body.classList.toggle('menu-abierto', abierto);
      nav.inert = esMenuMovil() && !abierto;
      if (etiquetaMenu) etiquetaMenu.textContent = abierto ? 'Cerrar menú' : 'Abrir menú';
      if (devolverFoco) btnMenu.focus();
    }
    btnMenu.addEventListener('click', function () {
      var abierto = btnMenu.getAttribute('aria-expanded') === 'true';
      cambiarMenu(!abierto, abierto);
      if (!abierto) {
        var primerEnlace = nav.querySelector('a[href]');
        if (primerEnlace) primerEnlace.focus();
      }
    });
    nav.addEventListener('click', function (e) {
      var enlace = e.target.closest('a[href]');
      if (enlace && btnMenu.getAttribute('aria-expanded') === 'true') {
        cambiarMenu(false, true);
        var destino = new URL(enlace.href, location.href);
        if (destino.pathname === location.pathname && destino.hash) {
          var seccion = document.getElementById(decodeURIComponent(destino.hash.slice(1)));
          if (seccion) {
            if (!seccion.hasAttribute('tabindex')) {
              seccion.setAttribute('tabindex', '-1');
              seccion.addEventListener('blur', function () { seccion.removeAttribute('tabindex'); }, { once: true });
            }
            seccion.focus({ preventScroll: true });
          }
        }
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && btnMenu.getAttribute('aria-expanded') === 'true') {
        e.preventDefault();
        cambiarMenu(false, true);
      }
    });
    window.addEventListener('resize', function () {
      var focoEnNav = nav.contains(document.activeElement);
      var focoEnBoton = document.activeElement === btnMenu;
      cambiarMenu(false, esMenuMovil() && focoEnNav);
      if (!esMenuMovil() && focoEnBoton) {
        var primerEnlace = nav.querySelector('a[href]');
        if (primerEnlace) primerEnlace.focus();
      }
    }, { passive: true });
    cambiarMenu(false, false);
  }

  /* Pestañas de capas en la ficha técnica complementaria. */
  document.querySelectorAll('.pestanas').forEach(function (lista) {
    var tabs = Array.prototype.slice.call(lista.querySelectorAll('[role="tab"]'));
    function activarTab(tab, enfocar) {
      tabs.forEach(function (t) {
        var activo = t === tab;
        t.setAttribute('aria-selected', String(activo));
        t.tabIndex = activo ? 0 : -1;
        var panel = document.getElementById(t.getAttribute('aria-controls'));
        if (panel) panel.hidden = !activo;
      });
      if (enfocar) tab.focus();
    }
    tabs.forEach(function (tab, indice) {
      tab.addEventListener('click', function () { activarTab(tab, false); });
      tab.addEventListener('keydown', function (e) {
        var siguiente;
        var vertical = lista.getAttribute('aria-orientation') === 'vertical';
        if (e.key === (vertical ? 'ArrowDown' : 'ArrowRight')) siguiente = (indice + 1) % tabs.length;
        else if (e.key === (vertical ? 'ArrowUp' : 'ArrowLeft')) siguiente = (indice - 1 + tabs.length) % tabs.length;
        else if (e.key === 'Home') siguiente = 0;
        else if (e.key === 'End') siguiente = tabs.length - 1;
        else return;
        e.preventDefault();
        activarTab(tabs[siguiente], true);
      });
    });

  });

  /* Visor de fotos */
  var visor = document.getElementById('visor');
  var visorImg = document.getElementById('visor-img');
  var visorPie = document.getElementById('visor-pie');
  if (visor && visorImg && typeof visor.showModal === 'function') {
    document.querySelectorAll('.foto-ampliable').forEach(function (b) {
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
