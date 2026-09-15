# Instrucciones para Claude — sitio web de LOPSA (lopsa.com.pa)

Este repositorio ES la página web de LOPSA, S.A. Todo lo que llega a la rama `main` se publica solo en
https://lopsa.com.pa (Netlify, en 1 a 3 minutos). Quien te escribe es un socio de LOPSA que **no programa**: te dirá
con palabras qué quiere cambiar. Tú haces el cambio, lo revisas, lo publicas y le confirmas con el enlace.

## Cómo hablar con la persona
- Español sencillo y frases cortas, sin jerga («commit», «PR», «merge») salvo que la persona pregunte.
- Si el pedido es ambiguo, pregunta UNA cosa concreta antes de tocar nada.
- Al terminar di qué cambió, en qué parte de la página y el enlace para verlo.

## Qué se edita para cada cosa
| Para cambiar... | Se edita |
|---|---|
| Textos de portada, contacto, horario, datos de la empresa, menú | `datos/sitio.json` |
| Tarjetas de aplicaciones (zinc, losas, canales, tanques, pisos, estacionamientos) | `datos/aplicaciones.json` |
| Sección «Poliurea» | `datos/poliurea.json` |
| Pasos del proceso | `datos/proceso.json` |
| Galería por etapas (sin dividir por proyectos) | `datos/proyectos.json` → `etapas` |
| Preguntas frecuentes | `datos/preguntas.json` |
| Estructura o diseño de una sección | `plantillas/*.html` y `estaticos/css/` |

- `dist/` es lo que se publica y **se genera solo**: nunca lo edites a mano.
- **Fotos:** solo se pueden usar las que ya están procesadas; sus nombres están en `datos/_imagenes_generadas.json`
  (por ejemplo `app-zinc`, `caso1-despues`, `nosotros-camion`). Para poner otra foto ya existente, cambia ese nombre
  en el `.json` que corresponda. **Fotos nuevas no se pueden subir desde aquí:** pide que las manden al grupo de
  WhatsApp de los socios y Manuel las sube. No corras `preparar_imagenes.py`: sus originales no están en este repositorio.
- No toques `netlify.toml`, `legacy/` ni el formulario `cotizacion` (su nombre, los atributos `data-netlify` y
  `netlify-honeypot`, ni el `name` de sus campos): de eso dependen los avisos de cotización que llegan por correo.

## Cómo hacer un cambio (siempre en este orden)
1. Parte de lo último publicado: `git fetch origin` y trabaja en una rama nueva creada desde `origin/main`
   (si la sesión ya te dio una rama, trae `origin/main` a ella antes de empezar).
2. Haz solo el cambio que se pidió.
3. `pip install -r requirements.txt` (una vez por sesión), luego `python construir_sitio.py` y
   `python verificar_sitio.py`. El verificador tiene que decir **OK**; si no, corrige y repite.
4. Revisa `git diff --stat`: que solo cambie lo pedido (más `dist/sitemap.xml`, que lleva la fecha del día).
5. Commit con mensaje en español, sube la rama y abre un pull request contra `main`.
6. Justo antes de fusionar, vuelve a traer `origin/main`. Si cambió (otro socio publicó algo), mézclalo en tu rama.
   Si hay conflicto dentro de `dist/`, no lo arregles a mano: quédate con cualquiera de las dos versiones, vuelve a
   correr `construir_sitio.py` y `verificar_sitio.py`, y haz commit.
7. **Fusiona tú el pull request a `main`**: si todo salió bien no hace falta pedir permiso. Si algo falló, NO
   publiques y explica en simple qué pasó.
8. Espera 2-3 minutos y comprueba en https://lopsa.com.pa (con `curl`, agregando `?v=` y un número para saltar la
   caché) que el cambio ya se ve. Si a los 10 minutos no aparece, Netlify pudo dejar la publicación pendiente de
   aprobación: dile a la persona que entre en https://app.netlify.com con admin@lopsa.com.pa → equipo **Lopsa** →
   sitio **lopsa-pty** → **Deploys** → la que diga *Pending approval* → aprobar.

## Reglas de contenido (no se negocian)
- **Sin RUC** en ninguna página. Ubicación pública: solo **«Ciudad de Panamá, Panamá»**, nunca la dirección exacta.
- Proyectos: sin nombre del cliente, ubicación, áreas ni descripción. En `datos/proyectos.json`, `mostrar_detalle`
  se queda en `false` hasta que Manuel López diga lo contrario.
- Criterio vigente (15-sep-2026): mostrar fotografías por estados iniciales, preparación y recubrimientos, mezclando
  intervenciones. No volver a separar proyectos. Proceso completo visible sin clics y sin efecto de goteo.
- Manuel ratificó «equipo capacitado y certificado» para aplicación de recubrimientos. No añadir certificadores ni
  sellos concretos sin respaldo.
- Garantía: **«10 años contra filtraciones»**. «Vida útil certificada de 25 años» solo para cubiertas. Ninguna otra cifra.
- Sin precios, tarifas ni descuentos. Sin marcas de materiales ni de equipos. Sin promesas que LOPSA no haya
  confirmado (plazos, certificaciones, «precio fijo»).
- LOPSA se presenta como especialista en poliurea caliente; la construcción es secundaria.
- Contacto público: WhatsApp y teléfono **+507 6604-4196**, correo **ventas@lopsa.com.pa**. Ningún otro teléfono
  ni correo personal.
- Español con tildes y ñ, trato de usted.

## Este repositorio es PÚBLICO
Todo lo que se sube se puede ver en internet, historial incluido. Nunca subas contraseñas, tokens, cédulas, datos
de clientes, fotos originales del celular (llevan la ubicación GPS) ni documentos internos de la empresa.
