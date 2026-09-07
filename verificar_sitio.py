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
from html.parser import HTMLParser
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(AQUI, "dist")

PROHIBIDAS = [
    # marcas de material y equipo (regla de Manuel)
    "graco", "alchimica", "hyperdesmo", "adipan", "drizoro", "polinova", "tecnopol", "sherwin",
    # promesas no ratificadas / cifras de garantía
    "precio fijo", "24 horas hábiles", "24 h hábiles", "garantía de 10 años", "10 años de garantía",
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

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
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


def main():
    if not os.path.isdir(DIST):
        print("No existe dist/: corre primero construir_sitio.py")
        sys.exit(1)
    problemas = []
    paginas = []
    for r, _, fs in os.walk(DIST):
        for fn in fs:
            if fn.endswith(".html"):
                paginas.append(os.path.join(r, fn))
    for p in paginas:
        html = open(p, encoding="utf-8").read()
        rel = os.path.relpath(p, DIST)
        bajo = html.lower()
        for palabra in PROHIBIDAS:
            if palabra in bajo:
                problemas.append(f"{rel}: contiene «{palabra}»")
        an = Analizador()
        an.feed(html)
        if an.h1 != 1:
            problemas.append(f"{rel}: tiene {an.h1} H1 (debe ser 1)")
        rutas = set()
        for s in an.imgs:
            rutas.add(s)
        for ss in an.srcsets:
            for parte in ss.split(","):
                rutas.add(parte.strip().split(" ")[0])
        for ruta in rutas:
            if ruta.startswith("http"):
                ruta = ruta.replace("https://lopsa.com.pa", "")
            local = os.path.join(DIST, ruta.lstrip("/"))
            if not os.path.exists(local):
                problemas.append(f"{rel}: imagen inexistente {ruta}")
        for h in an.hrefs:
            if h.startswith("#") or h.startswith("http") or h.startswith("mailto:") or h.startswith("tel:"):
                continue
            destino = h.split("#")[0]
            local = os.path.join(DIST, destino.lstrip("/"))
            if destino.endswith("/"):
                local = os.path.join(local, "index.html")
            if not os.path.exists(local):
                problemas.append(f"{rel}: enlace roto {h}")
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
    print(f"OK: {len(paginas)} páginas verificadas, sin palabras prohibidas, un H1 por página, imágenes y enlaces en orden.")


if __name__ == "__main__":
    main()
