# -*- coding: utf-8 -*-
"""
Construye el sitio estático de lopsa.com.pa: datos/*.json + plantillas/ → dist/

Uso:  python construir_sitio.py
Después: python verificar_sitio.py   (falla con código 1 si algo no está bien)
Previsualizar: python -m http.server 8080 --directory dist
"""
import json
import os
import shutil
import hashlib
from datetime import date
from jinja2 import Environment, FileSystemLoader, select_autoescape

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")
PLANTILLAS = os.path.join(AQUI, "plantillas")
ESTATICOS = os.path.join(AQUI, "estaticos")
DIST = os.path.join(AQUI, "dist")

FECHAS_SITEMAP = os.path.join(DATOS, "_fechas_sitemap.json")
URLS_SITEMAP = ["/", "/poliurea/", "/aplicaciones/", "/proceso/", "/trabajos/", "/equipo/", "/contacto/", "/privacidad/", "/aviso-legal/"]

PAGINAS = {
    "index.html": "index.html",
    "poliurea.html": "poliurea/index.html",
    "aplicaciones.html": "aplicaciones/index.html",
    "proceso.html": "proceso/index.html",
    "trabajos.html": "trabajos/index.html",
    "equipo.html": "equipo/index.html",
    "contacto.html": "contacto/index.html",
    "privacidad.html": "privacidad/index.html",
    "aviso-legal.html": "aviso-legal/index.html",
    "gracias.html": "gracias/index.html",
    "404.html": "404.html",
}


def cargar(nombre):
    with open(os.path.join(DATOS, nombre), encoding="utf-8") as f:
        return json.load(f)


def fechas_sitemap(htmls, hoy):
    """lastmod real de cada página: la fecha avanza solo si cambió su HTML generado (huella SHA-256).

    Guarda las huellas y fechas en datos/_fechas_sitemap.json (se versiona con el resto). Así una
    construcción sin cambios no altera el sitemap y Google recibe fechas que puede creer.
    """
    try:
        with open(FECHAS_SITEMAP, encoding="utf-8") as f:
            previas = json.load(f).get("paginas", {})
    except (OSError, ValueError):
        previas = {}
    paginas = {}
    for url in URLS_SITEMAP:
        huella = hashlib.sha256(htmls[url].encode("utf-8")).hexdigest()
        anterior = previas.get(url, {})
        fecha = anterior.get("fecha") if anterior.get("sha256") == huella and anterior.get("fecha") else hoy
        paginas[url] = {"fecha": fecha, "sha256": huella}
    contenido = {
        "_nota": "Generado por construir_sitio.py: fecha de la última modificación real de cada página (lastmod del sitemap). La fecha cambia solo cuando cambia el HTML generado de esa página. No editar a mano.",
        "paginas": paginas,
    }
    texto = json.dumps(contenido, ensure_ascii=False, indent=2) + "\n"
    actual = None
    if os.path.exists(FECHAS_SITEMAP):
        with open(FECHAS_SITEMAP, encoding="utf-8") as f:
            actual = f.read()
    if texto != actual:
        with open(FECHAS_SITEMAP, "w", encoding="utf-8", newline="\n") as f:
            f.write(texto)
    return {url: datos["fecha"] for url, datos in paginas.items()}


def main():
    sitio = cargar("sitio.json")
    ctx = {
        "sitio": sitio,
        "aplicaciones": cargar("aplicaciones.json"),
        "poliurea": cargar("poliurea.json"),
        "proceso": cargar("proceso.json"),
        "proyectos": cargar("proyectos.json"),
        "preguntas": cargar("preguntas.json"),
        "img": cargar("_imagenes_generadas.json") if os.path.exists(os.path.join(DATOS, "_imagenes_generadas.json")) else {},
        "hoy": date.today().isoformat(),
        # La versión cambia con el contenido para renovar la caché del navegador.
        "version_css": hashlib.sha256(open(os.path.join(ESTATICOS, "css", "estilos.css"), encoding="utf-8").read().encode("utf-8")).hexdigest()[:12],
        "version_js": hashlib.sha256(open(os.path.join(ESTATICOS, "js", "sitio.js"), encoding="utf-8").read().encode("utf-8")).hexdigest()[:12],
    }
    env = Environment(
        loader=FileSystemLoader(PLANTILLAS),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    def wa(texto):
        from urllib.parse import quote
        return f"https://wa.me/{sitio['whatsapp_numero']}?text={quote(texto)}"

    env.filters["wa"] = wa
    env.globals["wa"] = wa

    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    # estáticos
    for carpeta in ("css", "js", "img"):
        origen = os.path.join(ESTATICOS, carpeta)
        if os.path.isdir(origen):
            shutil.copytree(origen, os.path.join(DIST, carpeta))
    for raiz_archivo in ("favicon.ico", "icon-192.png", "icon-512.png", "apple-touch-icon.png", "site.webmanifest"):
        p = os.path.join(ESTATICOS, raiz_archivo)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(DIST, raiz_archivo))
    # páginas
    htmls = {}
    for plantilla, destino in PAGINAS.items():
        pagina = "inicio" if plantilla == "index.html" else os.path.splitext(plantilla)[0]
        html = env.get_template(plantilla).render(**ctx, pagina=pagina)
        ruta = os.path.join(DIST, destino)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        url = "/" + destino[: -len("index.html")] if destino.endswith("index.html") else "/" + destino
        htmls[url] = html
        print(f"  {destino}  {len(html) // 1024} KB")
    # robots y sitemap (lastmod = última modificación real de cada página)
    with open(os.path.join(DIST, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {sitio['url']}/sitemap.xml\n")
    fechas = fechas_sitemap(htmls, ctx["hoy"])
    with open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in URLS_SITEMAP:
            f.write(f"  <url><loc>{sitio['url']}{u}</loc><lastmod>{fechas[u]}</lastmod></url>\n")
        f.write("</urlset>\n")
    total = sum(os.path.getsize(os.path.join(r, fn)) for r, _, fs in os.walk(DIST) for fn in fs)
    print(f"dist/ listo: {total // 1024} KB en total")


if __name__ == "__main__":
    main()
