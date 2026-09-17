# lopsa.com.pa — sitio web de LOPSA, S.A.

Sitio estático de **LOPSA, S.A.**, aplicadores especialistas en poliurea caliente en Panamá. Inicio breve y páginas
`/poliurea/`, `/aplicaciones/`, `/proceso/`, `/trabajos/`, `/equipo/` y `/contacto/`, además de
`/privacidad/`, `/aviso-legal/`, `/gracias/` y `/404.html`. Sin base de datos, sin framework: HTML, CSS y JavaScript
generados con Python a partir de archivos de datos.

El brief, los textos fuente, la identidad visual, el plan de trabajo y el estado vivo están en el repositorio
de gestión de LOPSA: `04_COMERCIAL/Web_LOPSA/`. Este repositorio es **el código y lo que se publica**.

## Cómo está organizado

| Carpeta / archivo | Qué es |
|---|---|
| `datos/*.json` | **El contenido.** `sitio.json` (datos de la empresa, textos de portada, contacto), `aplicaciones.json`, `poliurea.json`, `proceso.json`, `proyectos.json` (galería por etapas), `preguntas.json` y `imagenes.json` (manifiesto de fotos). |
| `plantillas/*.html` | Plantillas Jinja2: `base.html` (cabecera, pie, metadatos) y una por página. |
| `estaticos/` | CSS, JavaScript, logos, favicons y las fotos ya optimizadas (`img/`). |
| `preparar_imagenes.py` | Toma las fotos originales de `Fotos_LOPSA/` (repositorio de gestión), las recorta, difumina rótulos ajenos y exporta WebP **sin EXIF ni GPS**. |
| `construir_sitio.py` | Genera `dist/` (datos + plantillas + estáticos + `robots.txt` + `sitemap.xml`). |
| `verificar_sitio.py` | Revisa `dist/`: palabras prohibidas, un solo H1, imágenes y enlaces, metadatos y peso. Sale con error si algo falla. |
| `dist/` | **Lo que se publica.** Se versiona para que Netlify lo sirva sin construir nada. |
| `netlify.toml` | Carpeta a publicar, cabeceras de seguridad, caché y redirecciones. |
| `legacy/coming-soon/` | El «Coming Soon» en Next.js entregado por Isabel López el 02-sep-2026 (etiqueta `coming-soon-isabel`). Solo referencia. |

## Flujo de trabajo

Las instrucciones completas para cualquier sesión de Claude (y para cualquier persona) están en **`CLAUDE.md`**:
rama nueva desde `main` → `python construir_sitio.py` → `python verificar_sitio.py` (debe decir OK) → pull request →
merge a `main`. **Lo que llega a `main` lo publica Netlify solo**; no se despliega a mano. `dist/` nunca se edita a mano.

Requisitos: Python 3.12 o superior y `pip install -r requirements.txt` (Jinja2 y Pillow).
Previsualizar en local: `python -m http.server 8080 --directory dist`.

## Reglas de contenido

Están en `CLAUDE.md`, sección «Reglas de contenido (no se negocian)».

### Criterio visual vigente — 16 de septiembre de 2026

- Inicio breve con información principal y accesos a secciones independientes. Menú activo en escritorio y móvil; navegación disponible sin JavaScript. Los enlaces antiguos con anclas llevan a su nueva página.
- La fotografía de portada sigue siendo **el camión de LOPSA con el edificio de fondo**, fija, completa y sin carrusel en celular y escritorio.
- Cada sección tiene URL, título, descripción y canonical propios. El formulario vive únicamente en `/contacto/`; conserva todos los campos y atributos de Netlify. La atribución UTM se mantiene al navegar.

- Fotografía propia como protagonista, con títulos y números grandes. Sin efecto de goteo.
- Los cinco pasos del proceso se muestran completos; no se ocultan tras pestañas.
- `proyectos.json` contiene `etapas`, cada una con `titulo`, `texto` y `fotos` (`imagen`, `alt`, `pie`). La galería mezcla distintas intervenciones por estado inicial, preparación y recubrimiento. No agrupar por cliente ni por proyecto.
- El mensaje «Equipo capacitado y certificado» fue confirmado por la dirección. No añadir organismos ni sellos de certificación sin una fuente.
- Las fotos de Aplicaciones se muestran sin pies superpuestos por indicación de Manuel. Se conservan las fuentes y licencias en la documentación; la foto de estacionamientos es de [Jakub Żerdzicki / Unsplash](https://unsplash.com/photos/an-empty-parking-garage-with-yellow-and-black-stripes-81zwxdDiNAg), bajo la [licencia Unsplash](https://unsplash.com/license); no representa una obra de LOPSA.
- Las imágenes nuevas usan identificadores nuevos para renovar la caché. En la PC con acceso a los originales se incorporan mediante el manifiesto y `preparar_imagenes.py`; en sesiones remotas se reutilizan las versiones procesadas. Nunca publicar originales ni metadatos.

## Publicación y accesos

- **Hosting:** Netlify, sitio `lopsa-pty` del equipo «Lopsa», enlazado a este repositorio (rama `main`).
- **Formulario:** Netlify Forms (`cotizacion`); los avisos por correo se configuran en el panel de Netlify.
- **DNS:** zona en Cloudflare. Los servidores de nombre en NIC y el MX de Google no se tocan nunca.
- **Medición:** `sitio.json` → `gtm_id`. Vacío = no se carga nada.
