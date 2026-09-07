# lopsa.com.pa — sitio web de LOPSA, S.A.

Sitio estático de **LOPSA, S.A.**, aplicadores especialistas en poliurea caliente en Panamá. Una página larga más
`/privacidad`, `/aviso-legal`, `/gracias` y `/404`. Sin base de datos, sin framework: HTML, CSS y JavaScript
generados con Python a partir de archivos de datos.

El brief, los textos fuente, la identidad visual, el plan de trabajo y el estado vivo están en el repositorio
de gestión de LOPSA: `04_COMERCIAL/Web_LOPSA/`. Este repositorio es **el código y lo que se publica**.

## Cómo está organizado

| Carpeta / archivo | Qué es |
|---|---|
| `datos/*.json` | **El contenido.** `sitio.json` (datos de la empresa, textos de portada, contacto), `aplicaciones.json`, `poliurea.json`, `proceso.json`, `proyectos.json`, `preguntas.json` y `imagenes.json` (manifiesto de fotos). Para cambiar un texto o agregar un proyecto se edita aquí. |
| `plantillas/*.html` | Plantillas Jinja2: `base.html` (cabecera, pie, metadatos) y una por página. |
| `estaticos/` | CSS, JavaScript, logos, favicons y las fotos ya optimizadas (`img/`). |
| `preparar_imagenes.py` | Toma las fotos originales de `Fotos_LOPSA/` (repositorio de gestión), las recorta, difumina rótulos ajenos y exporta WebP **sin EXIF ni GPS**. |
| `construir_sitio.py` | Genera `dist/` (datos + plantillas + estáticos + `robots.txt` + `sitemap.xml`). |
| `verificar_sitio.py` | Revisa `dist/`: palabras prohibidas, un solo H1, imágenes y enlaces, metadatos y peso. Sale con error si algo falla. |
| `dist/` | **Lo que se publica.** Se versiona para que Netlify lo sirva sin construir nada. |
| `netlify.toml` | Carpeta a publicar, cabeceras de seguridad, caché y redirecciones. |
| `legacy/coming-soon/` | El «Coming Soon» en Next.js entregado por Isabel López el 02-sep-2026 (etiqueta `coming-soon-isabel`). Solo referencia. |

## Flujo de trabajo

```
python preparar_imagenes.py      # solo cuando cambia el manifiesto de fotos
python construir_sitio.py        # datos + plantillas → dist/
python verificar_sitio.py        # debe decir OK
python -m http.server 8080 --directory dist   # previsualizar en http://localhost:8080
git add -A && git commit -m "…" && git push
npx netlify-cli deploy --prod --dir=dist       # publicar (token de Netlify de LOPSA)
```

Requisitos: Python 3.12 con `jinja2` y `Pillow` (el `.venv` del repositorio de gestión ya los tiene). Node solo
hace falta para la CLI de Netlify (`npx`), no para el sitio.

## Reglas de contenido (no se negocian)

- Español con tildes y ñ en todo texto visible.
- Nunca se nombran marcas de material ni de equipo.
- «Garantía por escrito», sin número de años. Los 25 años solo como vida útil certificada del sistema en cubiertas.
- Posicionamiento 100 % poliurea caliente; la construcción es una línea al final.
- Fotos propias, sin caras reconocibles sin autorización, sin rótulos de terceros y sin datos de GPS.
- Sin datos privados: el único teléfono es el +507 6604-4196 y los correos son `ventas@` y `admin@`.

## Publicación y accesos

- **Hosting:** Netlify, cuenta de LOPSA (`admin@lopsa.com.pa`). El token vive en `07_HERRAMIENTAS/config/` del
  repositorio de gestión, nunca aquí.
- **Formulario:** Netlify Forms (`cotizacion`), con aviso por correo a `ventas@` y copia a Manuel; se configura en
  el panel de Netlify.
- **DNS:** zona en Cloudflare. Solo se tocan los registros A y CNAME de `lopsa.com.pa` y `www`; los servidores de
  nombre en NIC y el MX de Google no se tocan nunca.
- **Medición:** `sitio.json` → `gtm_id`. Vacío = no se carga nada.
