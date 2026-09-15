# -*- coding: utf-8 -*-
"""
Prepara las fotos del sitio a partir del manifiesto datos/imagenes.json.

- Lee cada original desde la carpeta Fotos_LOPSA del repositorio LOPSA_CLAUDE (fuera de este repo).
- Corrige la orientación EXIF, recorta a la proporción pedida alrededor del punto de foco,
  difumina las zonas indicadas (rótulos de terceros) y exporta WebP (o JPG) en varios anchos.
- NO copia metadatos: el WebP sale sin EXIF ni coordenadas GPS (las fotos del celular las traen).
- Escribe datos/_imagenes_generadas.json con los anchos y la proporción de cada imagen,
  que construir_sitio.py usa para armar los srcset.

Uso:  python preparar_imagenes.py            (solo las que falten o cambien)
      python preparar_imagenes.py --todas    (regenera todo)
"""
import json
import os
import sys
import hashlib
from PIL import Image, ImageOps, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
MANIFIESTO = os.path.join(AQUI, "datos", "imagenes.json")
SALIDA = os.path.join(AQUI, "estaticos", "img")
GENERADAS = os.path.join(AQUI, "datos", "_imagenes_generadas.json")
CALIDAD_WEBP = 78
CALIDAD_JPG = 82


def ratio(texto):
    a, b = texto.split(":")
    return float(a) / float(b)


def recortar(im, prop, foco):
    """Recorta a la proporción `prop` (ancho/alto) manteniendo el punto de foco (fx, fy) dentro."""
    w, h = im.size
    if w / h > prop:
        nw, nh = int(round(h * prop)), h
    else:
        nw, nh = w, int(round(w / prop))
    fx, fy = foco
    x0 = int(round(fx * w - nw / 2))
    y0 = int(round(fy * h - nh / 2))
    x0 = max(0, min(x0, w - nw))
    y0 = max(0, min(y0, h - nh))
    return im.crop((x0, y0, x0 + nw, y0 + nh))


def difuminar(im, zonas):
    w, h = im.size
    for x0, y0, x1, y1 in zonas:
        caja = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
        parche = im.crop(caja).filter(ImageFilter.GaussianBlur(radius=max(6, (caja[2] - caja[0]) // 12)))
        im.paste(parche, caja)
    return im


def huella(entrada):
    return hashlib.md5(json.dumps(entrada, sort_keys=True).encode("utf-8")).hexdigest()[:10]


def main():
    todas = "--todas" in sys.argv
    m = json.load(open(MANIFIESTO, encoding="utf-8"))
    os.makedirs(SALIDA, exist_ok=True)
    previas = json.load(open(GENERADAS, encoding="utf-8")) if os.path.exists(GENERADAS) else {}
    generadas = {}
    errores = 0
    for e in m["imagenes"]:
        if "origen_abs" in e:
            origen = e["origen_abs"]
        elif "origen_material" in e:
            origen = os.path.join(m["raiz_material"], e["origen_material"])
        else:
            origen = os.path.join(m["raiz"], e["origen"])
        formato = e.get("formato", "webp")
        anchos = e["anchos"]
        h = huella({k: v for k, v in e.items()})
        if not os.path.exists(origen):
            print(f"  FALTA el original: {origen}")
            errores += 1
            continue
        if not todas and previas.get(e["id"], {}).get("huella") == h and all(
            os.path.exists(os.path.join(SALIDA, f"{e['id']}-{a}.{formato}")) for a in anchos
        ):
            generadas[e["id"]] = previas[e["id"]]
            continue
        im = Image.open(origen)
        im = ImageOps.exif_transpose(im).convert("RGB")
        if "caja" in e:
            w, hh = im.size
            l, t, r, b = e["caja"]
            im = im.crop((int(l * w), int(t * hh), int(r * w), int(b * hh)))
        if "desenfocar" in e:
            im = difuminar(im, e["desenfocar"])
        prop = ratio(e["recorte"])
        im = recortar(im, prop, e.get("foco", [0.5, 0.5]))
        for a in anchos:
            if a >= im.width:
                a_real = im.width
            else:
                a_real = a
            alto = int(round(a_real / prop))
            copia = im.resize((a_real, alto), Image.LANCZOS)
            destino = os.path.join(SALIDA, f"{e['id']}-{a}.{formato}")
            if formato == "jpg":
                copia.save(destino, "JPEG", quality=CALIDAD_JPG, optimize=True, progressive=True)
            else:
                copia.save(destino, "WEBP", quality=e.get("calidad", CALIDAD_WEBP), method=6)
            kb = os.path.getsize(destino) // 1024
            if kb > 250:
                print(f"  AVISO {os.path.basename(destino)} pesa {kb} KB (límite 250)")
        generadas[e["id"]] = {"anchos": anchos, "prop": round(prop, 4), "formato": formato, "huella": h}
        print(f"  ok {e['id']} ({', '.join(str(a) for a in anchos)})")
    json.dump(generadas, open(GENERADAS, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{len(generadas)} imágenes listas en estaticos/img · errores: {errores}")
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
