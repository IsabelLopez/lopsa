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

  /* Pestañas de capas y proceso; sin JavaScript, el proceso se lee completo. */
  document.querySelectorAll('.pestanas, .proceso-tabs').forEach(function (lista) {
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
    if (lista.classList.contains('proceso-tabs') && tabs.length) {
      lista.hidden = false;
      activarTab(tabs[0], false);
    }
  });

  /* La capa desciende por la escena fija al avanzar, sin bloquear rueda ni tacto. */
  var recubrimiento = document.querySelector('.recubrimiento');
  var capa = recubrimiento && recubrimiento.querySelector('.recubrimiento__capa');
  if (capa) {
    var escena = recubrimiento.querySelector('.recubrimiento__escena');
    var textoCapa = recubrimiento.querySelector('.recubrimiento__texto');
    var reducirMovimiento = window.matchMedia('(prefers-reduced-motion: reduce), (max-height: 640px)');
    var observadorCapa;
    var cuadroCapa = 0;
    var siguiendoCapa = false;
    function limitar(valor) {
      return Math.min(1, Math.max(0, valor));
    }
    function mostrarCobertura(progreso) {
      recubrimiento.style.setProperty('--avance', progreso.toFixed(4));
      recubrimiento.style.setProperty('--revelado', limitar((progreso - 0.62) / 0.16).toFixed(4));
      recubrimiento.classList.toggle('recubierto', progreso >= 0.65);
      if (textoCapa) textoCapa.inert = progreso < 0.65;
    }
    function pintarCapa() {
      cuadroCapa = 0;
      var posicion = recubrimiento.getBoundingClientRect();
      var recorrido = posicion.height - escena.getBoundingClientRect().height;
      var margenSuperior = parseFloat(window.getComputedStyle(escena).top) || 0;
      mostrarCobertura(recorrido > 0 ? limitar((margenSuperior - posicion.top) / recorrido) : 1);
    }
    function solicitarCuadro() {
      if (!cuadroCapa) cuadroCapa = window.requestAnimationFrame(pintarCapa);
    }
    function detenerCapa() {
      window.removeEventListener('scroll', solicitarCuadro);
      window.removeEventListener('resize', solicitarCuadro);
      if (cuadroCapa) window.cancelAnimationFrame(cuadroCapa);
      cuadroCapa = 0;
      siguiendoCapa = false;
    }
    function configurarCapa() {
      detenerCapa();
      if (observadorCapa) observadorCapa.disconnect();
      var estatico = reducirMovimiento.matches || !('IntersectionObserver' in window) || !escena;
      recubrimiento.classList.toggle('sin-movimiento', estatico);
      recubrimiento.classList.toggle('con-movimiento', !estatico);
      if (estatico) {
        mostrarCobertura(1);
        return;
      }
      pintarCapa();
      var observador = new IntersectionObserver(function (entradas) {
        if (observadorCapa !== observador || recubrimiento.classList.contains('sin-movimiento')) return;
        if (entradas[0].isIntersecting) {
          if (!siguiendoCapa) {
            window.addEventListener('scroll', solicitarCuadro, { passive: true });
            window.addEventListener('resize', solicitarCuadro, { passive: true });
            siguiendoCapa = true;
          }
          solicitarCuadro();
        } else {
          detenerCapa();
          pintarCapa();
        }
      });
      observadorCapa = observador;
      observadorCapa.observe(recubrimiento);
    }
    if (reducirMovimiento.addEventListener) reducirMovimiento.addEventListener('change', configurarCapa);
    else reducirMovimiento.addListener(configurarCapa);
    configurarCapa();
  }

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
