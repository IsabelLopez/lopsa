# -*- coding: utf-8 -*-
"""
Verifica dist/ antes de publicar. Sale con código 1 si encuentra algo.

Comprueba: palabras prohibidas (marcas, cifras de garantía, promesas no ratificadas, datos privados),
un solo H1 por página, que todas las imágenes referenciadas existan, que los enlaces internos resuelvan,
que ninguna imagen conserve EXIF/GPS y que ninguna pase de 250 KB.
"""
import os
import re
import sys
import json
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree
from PIL import Image
from construir_sitio import PAGINAS

AQUI = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(AQUI, "dist")

PROHIBIDAS = [
    # marcas de material y equipo (regla de Manuel)
    "graco", "alchimica", "hyperdesmo", "adipan", "drizoro", "polinova", "tecnopol", "sherwin",
    # promesas no ratificadas / cifras de garantía
    "precio fijo", "24 horas hábiles", "24 h hábiles",  # «10 años contra filtraciones» ratificado por Manuel el 09-sep-2026
    "garantía de 25 años", "25 años de garantía",
    # claims prohibidos
    "certificado nsf", "aprobado por el minsa", "fda", "farmacéutic", "auto-extinguible", "ignífug",
    "contacto directo con alimentos",
    # datos privados y restos del placeholder
    "6983-9630", "315-2918", "coming soon", "próximamente", "lorem ipsum",
]


class Analizador(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.imgs = []
        self.hrefs = []
        self.srcsets = []
        self.ids = Counter()
        self.clases = Counter()
        self.titulos = []
        self.descripciones = []
        self.canonicals = []
        self.og_urls = []
        self.formularios = []
        self.formulario_actual = None
        self.en_titulo = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids[a["id"]] += 1
        self.clases.update(a.get("class", "").split())
        if tag == "title":
            self.titulos.append("")
            self.en_titulo = True
        if tag == "meta" and a.get("name") == "description":
            self.descripciones.append(a.get("content", ""))
        if tag == "link" and "canonical" in a.get("rel", "").split():
            self.canonicals.append(a.get("href", ""))
        if tag == "meta" and a.get("property") == "og:url":
            self.og_urls.append(a.get("content", ""))
        if tag == "form":
            self.formulario_actual = {"atributos": a, "campos": []}
            self.formularios.append(self.formulario_actual)
            if a.get("action"):
                self.hrefs.append(a["action"])
        if tag in ("input", "select", "textarea") and self.formulario_actual is not None:
            self.formulario_actual["campos"].append((tag, a))
        if tag == "h1":
            self.h1 += 1
        if tag in ("img", "source"):
            if a.get("src"):
                self.imgs.append(a["src"])
            if a.get("srcset"):
                self.srcsets.append(a["srcset"])
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        if tag == "meta" and a.get("property") == "og:image" and a.get("content"):
            self.imgs.append(a["content"])

    def handle_endtag(self, tag):
        if tag == "title":
            self.en_titulo = False
        if tag == "form":
            self.formulario_actual = None

    def handle_data(self, data):
        if self.en_titulo:
            self.titulos[-1] += data


def ruta_publica(rel):
    rel = rel.replace(os.sep, "/")
    return "/" + (rel[:-10] if rel.endswith("index.html") else rel)


def resolver_local(referencia, pagina, sitio_url):
    """Resuelve rutas, parámetros y fragmentos como lo haría el navegador."""
    url = urlsplit(urljoin(sitio_url + pagina, referencia))
    if url.scheme not in ("http", "https") or url.netloc != urlsplit(sitio_url).netloc:
        return None
    local = os.path.abspath(os.path.join(DIST, unquote(url.path).lstrip("/")))
    if os.path.commonpath([DIST, local]) != DIST:
        return local, unquote(url.fragment)
    if os.path.isdir(local):
        local = os.path.join(local, "index.html")
    return local, unquote(url.fragment)


def main():
    if not os.path.isdir(DIST):
        print("No existe dist/: corre primero construir_sitio.py")
        sys.exit(1)
    problemas = []
    with open(os.path.join(AQUI, "datos", "sitio.json"), encoding="utf-8") as f:
        sitio = json.load(f)
    sitio_url = sitio["url"].rstrip("/")
    paginas = []
    for r, _, fs in os.walk(DIST):
        for fn in fs:
            if fn.endswith(".html"):
                paginas.append(os.path.join(r, fn))
    esperadas = {os.path.abspath(os.path.join(DIST, destino)) for destino in PAGINAS.values()}
    for faltante in sorted(esperadas - set(paginas)):
        problemas.append(f"Falta la página {os.path.relpath(faltante, DIST)}")
    analizadas = {}
    htmls = {}
    for p in paginas:
        htmls[p] = open(p, encoding="utf-8").read()
        an = Analizador()
        an.feed(htmls[p])
        analizadas[p] = an
    formularios = []
    titulos = {}
    for p in paginas:
        html = htmls[p]
        rel = os.path.relpath(p, DIST)
        bajo = html.lower()
        for palabra in PROHIBIDAS:
            # FDA es una sigla, no una coincidencia dentro de la huella hexadecimal de un recurso.
            coincide = re.search(r"\bfda\b", bajo) if palabra == "fda" else palabra in bajo
            if coincide:
                problemas.append(f"{rel}: contiene «{palabra}»")
        if re.search(r"\bruc\b", bajo):
            problemas.append(f"{rel}: contiene RUC")
        an = analizadas[p]
        if an.h1 != 1:
            problemas.append(f"{rel}: tiene {an.h1} H1 (debe ser 1)")
        for identificador, cantidad in an.ids.items():
            if cantidad > 1:
                problemas.append(f"{rel}: id duplicado {identificador}")
        if len(an.titulos) != 1 or not an.titulos[0].strip():
            problemas.append(f"{rel}: debe tener un título no vacío")
        elif an.titulos[0] in titulos:
            problemas.append(f"{rel}: repite el título de {titulos[an.titulos[0]]}")
        else:
            titulos[an.titulos[0]] = rel
        if len(an.descripciones) != 1 or not an.descripciones[0].strip():
            problemas.append(f"{rel}: debe tener una descripción no vacía")
        canonical = sitio_url + ruta_publica(rel)
        if an.canonicals != [canonical]:
            problemas.append(f"{rel}: canonical incorrecto; se esperaba {canonical}")
        if an.og_urls != [canonical]:
            problemas.append(f"{rel}: og:url debe coincidir con su canonical")
        formularios.extend((rel, form) for form in an.formularios)
        rutas = set()
        for s in an.imgs:
            rutas.add(s)
        for ss in an.srcsets:
            for parte in ss.split(","):
                rutas.add(parte.strip().split(" ")[0])
        for ruta in rutas:
            destino = resolver_local(ruta, ruta_publica(rel), sitio_url)
            if destino and not os.path.isfile(destino[0]):
                problemas.append(f"{rel}: imagen inexistente {ruta}")
        for h in an.hrefs:
            correos_permitidos = {"ventas@lopsa.com.pa"}
            if rel.replace(os.sep, "/") == "privacidad/index.html":
                correos_permitidos.add(sitio.get("correo_datos"))
            if h.startswith("mailto:") and h[7:].split("?")[0] not in correos_permitidos:
                problemas.append(f"{rel}: correo público no autorizado {h}")
            if h.startswith("tel:") and re.sub(r"\D", "", h) != "50766044196":
                problemas.append(f"{rel}: teléfono público no autorizado {h}")
            destino = resolver_local(h, ruta_publica(rel), sitio_url)
            if destino is None:
                continue
            local, fragmento = destino
            if not os.path.isfile(local):
                problemas.append(f"{rel}: enlace roto {h}")
            elif fragmento and local in analizadas and fragmento not in analizadas[local].ids:
                problemas.append(f"{rel}: ancla inexistente {h}")
    # El formulario conserva el contrato de Netlify y vive solo en Contacto.
    if len(formularios) != 1:
        problemas.append(f"Debe existir un formulario en Contacto; se encontraron {len(formularios)}")
    else:
        rel, formulario = formularios[0]
        if rel.replace(os.sep, "/") != "contacto/index.html":
            problemas.append("El formulario debe estar en contacto/index.html")
        atributos = {"name": "cotizacion", "method": "POST", "action": "/gracias/", "data-netlify": "true", "netlify-honeypot": "campo-extra"}
        for clave, valor in atributos.items():
            if formulario["atributos"].get(clave) != valor:
                problemas.append(f"Formulario: atributo {clave} alterado")
        campos = formulario["campos"]
        nombres = Counter(a.get("name") for _, a in campos)
        esperados = Counter(["form-name", "origen", "campo-extra", "nombre", "empresa", "correo", "telefono", "tipo", "area", "ubicacion", "mensaje", "acepta"])
        if nombres != esperados:
            problemas.append("Formulario: se modificaron los nombres o la cantidad de campos")
        por_nombre = {a.get("name"): a for _, a in campos}
        if por_nombre.get("form-name", {}).get("value") != "cotizacion":
            problemas.append("Formulario: form-name debe conservar el valor cotizacion")
        for nombre in ("nombre", "correo", "telefono", "tipo", "acepta"):
            if "required" not in por_nombre.get(nombre, {}):
                problemas.append(f"Formulario: {nombre} debe ser obligatorio")
    # La división en páginas conserva todas las tarjetas, etapas y respaldos.
    contenidos = [("aplicaciones/index.html", "tarjeta", 6), ("proceso/index.html", "etapa", 5), ("proceso/index.html", "respaldo-sistema__item", 8), ("poliurea/index.html", "comparativa", 1)]
    for rel, clase, cantidad in contenidos:
        an = analizadas.get(os.path.join(DIST, rel.replace("/", os.sep)))
        if an is not None and an.clases[clase] != cantidad:
            problemas.append(f"{rel}: debe conservar {cantidad} elementos con clase {clase}")
    if sitio.get("direccion_linea") != "Ciudad de Panamá, Panamá":
        problemas.append("La ubicación pública debe ser Ciudad de Panamá, Panamá")
    with open(os.path.join(AQUI, "datos", "proyectos.json"), encoding="utf-8") as f:
        if json.load(f).get("mostrar_detalle") is not False:
            problemas.append("Los proyectos deben conservar mostrar_detalle en false")
    try:
        sitemap = ElementTree.parse(os.path.join(DIST, "sitemap.xml"))
        urls = {elemento.text for elemento in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
        rutas = {ruta_publica(destino) for destino in PAGINAS.values() if destino not in ("404.html", "gracias/index.html")}
        if urls != {sitio_url + ruta for ruta in rutas}:
            problemas.append("El sitemap debe incluir todas las páginas públicas y excluir Gracias y 404")
    except (OSError, ElementTree.ParseError) as e:
        problemas.append(f"No se pudo verificar el sitemap: {e}")
    # imágenes: sin EXIF y peso
    carpeta_img = os.path.join(DIST, "img")
    if os.path.isdir(carpeta_img):
        for fn in os.listdir(carpeta_img):
            ruta = os.path.join(carpeta_img, fn)
            if fn.lower().endswith((".webp", ".jpg", ".jpeg", ".png")):
                kb = os.path.getsize(ruta) // 1024
                if kb > 250:
                    problemas.append(f"img/{fn}: pesa {kb} KB (máximo 250)")
                try:
                    im = Image.open(ruta)
                    exif = im.getexif()
                    if len(exif) > 0 or "exif" in im.info:
                        problemas.append(f"img/{fn}: conserva metadatos EXIF")
                except Exception as e:
                    problemas.append(f"img/{fn}: no se pudo abrir ({e})")
    if problemas:
        print("PROBLEMAS:")
        for p in problemas:
            print("  -", p)
        sys.exit(1)
    print(f"OK: {len(paginas)} páginas verificadas; H1, metadatos, canonical, formulario, contenido, sitemap, imágenes y enlaces con sus anclas en orden.")


if __name__ == "__main__":
    main()
