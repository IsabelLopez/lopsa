# Continuidad del diseño de lopsa.com.pa

Actualizado: **07-oct-2026**. Relevo público para continuar el mismo trabajo desde cualquier sesión o modelo.
Las reglas y el procedimiento viven únicamente en [CLAUDE.md](CLAUDE.md); este archivo registra estado,
decisiones y evidencia. Las instrucciones antiguas del historial no sustituyen las decisiones vigentes.

## Estado de referencia

| Estado | Evidencia y alcance |
|---|---|
| Diseño publicado vigente | Inicio breve y seis páginas independientes, incorporados en [PR #13](https://github.com/IsabelLopez/lopsa/pull/13), versión [58d1d34](https://github.com/IsabelLopez/lopsa/commit/58d1d34), 16-sep-2026. Conserva los ajustes visuales de los PR #6–12 indicados abajo. Sitio: [lopsa.com.pa](https://lopsa.com.pa/). |
| Base actual de producción | `IsabelLopez/lopsa`, rama `main`, [9e3c199](https://github.com/IsabelLopez/lopsa/commit/9e3c199), integración de [PR #21](https://github.com/IsabelLopez/lopsa/pull/21) (06-oct-2026), consultada con `git fetch` el 07-oct. Incluye [PR #14](https://github.com/IsabelLopez/lopsa/pull/14), [#15](https://github.com/IsabelLopez/lopsa/pull/15), [#16](https://github.com/IsabelLopez/lopsa/pull/16), [#17](https://github.com/IsabelLopez/lopsa/pull/17) y [#20](https://github.com/IsabelLopez/lopsa/pull/20) de SEO/medición, [#18](https://github.com/IsabelLopez/lopsa/pull/18)–[#19](https://github.com/IsabelLopez/lopsa/pull/19) de instrucciones y [#21](https://github.com/IsabelLopez/lopsa/pull/21) de fotos. Esta lectura de Git no certifica el identificador del despliegue activo de Netlify. |
| Trabajo de esta revisión | [PR #22](https://github.com/IsabelLopez/lopsa/pull/22), rama `web/enlace-instagram-20261007`: enlace visible a Instagram (@lopsa_pa) con ícono en el pie y junto al botón de WhatsApp en Contacto. Sin otros cambios visuales. Consultar el estado del PR para saber si está integrado. |
| Propuestas visuales nuevas | Ninguna aprobada o implementada en esta revisión. Cualquier propuesta futura debe registrar su alcance y referencia aparte del diseño vigente. |

## Decisiones visuales vigentes

| Conservar | Referencia pública y archivos actuales |
|---|---|
| **Inicio breve y seis páginas.** Poliurea, Aplicaciones, Proceso, Trabajos, Equipo y Contacto tienen rutas propias. Conservar navegación móvil y de escritorio, funcionamiento sin JavaScript y enlaces antiguos. No volver a la página única larga. | [PR #13](https://github.com/IsabelLopez/lopsa/pull/13); [plantillas/index.html](plantillas/index.html), [plantillas/base.html](plantillas/base.html), [datos/sitio.json](datos/sitio.json). |
| **Portada fija del camión con edificio de fondo.** Fotografía completa también en celular; sin carrusel ni recorte móvil alternativo. La plantilla usa `hero-escritorio` en todos los anchos. | [Versión 81049fe](https://github.com/IsabelLopez/lopsa/commit/81049fe), reafirmada en [PR #13](https://github.com/IsabelLopez/lopsa/pull/13); [plantillas/index.html](plantillas/index.html), [datos/imagenes.json](datos/imagenes.json). |
| **Identidad vigente.** Fotografía protagonista, títulos y cifras grandes; marino `#1a2f50`, azul `#2e5a88`, dorado `#c9a554`, bronce `#876522`, hueso `#f6f5f1` y blanco. Títulos Nunito Sans y cuerpo Inter. Sin efecto de goteo. | [PR #6](https://github.com/IsabelLopez/lopsa/pull/6); valores actuales en [estaticos/css/estilos.css](estaticos/css/estilos.css). |
| **Proceso completo visible.** Los cinco pasos se leen sin pestañas ni controles que oculten etapas. | [PR #6](https://github.com/IsabelLopez/lopsa/pull/6); [plantillas/proceso.html](plantillas/proceso.html), [datos/proceso.json](datos/proceso.json). |
| **Galería por tres etapas.** Estados iniciales, preparación y recubrimientos mezclan intervenciones; no agrupar por cliente o proyecto. Conservar `mostrar_detalle: false` y los límites de contenido de `CLAUDE.md`. | [PR #6](https://github.com/IsabelLopez/lopsa/pull/6); [plantillas/trabajos.html](plantillas/trabajos.html), [datos/proyectos.json](datos/proyectos.json). |
| **Aplicaciones sin pies superpuestos sobre fotos.** Conservar las imágenes procesadas y sus fuentes; la fotografía externa de estacionamiento no representa una obra de LOPSA. | [PR #7](https://github.com/IsabelLopez/lopsa/pull/7); [plantillas/aplicaciones.html](plantillas/aplicaciones.html), fuente y licencia en [README.md](README.md). |
| **Poliurea: cifras compactas, capas rotuladas y una tabla.** Nombres y líneas dentro de la ilustración; comparación común para PC y celular, con desplazamiento horizontal y criterio fijo. No reemplazarla por fichas móviles. | [PR #11](https://github.com/IsabelLopez/lopsa/pull/11); [plantillas/poliurea.html](plantillas/poliurea.html), [datos/poliurea.json](datos/poliurea.json), [estaticos/css/estilos.css](estaticos/css/estilos.css). |
| **Respaldo técnico con alcance preciso.** Ocho tarjetas: dos por fila en celular y cuatro en escritorio; acordeón «Consultar Ficha Técnica». Conservar los alcances técnicos establecidos en `CLAUDE.md`. | [PR #12](https://github.com/IsabelLopez/lopsa/pull/12); [plantillas/proceso.html](plantillas/proceso.html), [datos/proceso.json](datos/proceso.json), [estaticos/css/estilos.css](estaticos/css/estilos.css). |
| **Instagram visible, sin Facebook.** Ícono de Instagram (@lopsa_pa) bajo el lema del pie, dorado sobre marino, y botón cuadrado marino de 48 px junto a «Escribir por WhatsApp» en Contacto (en 320 px baja a la línea siguiente). SVG en línea con `aria-label="Instagram de LOPSA"`; abre en otra pestaña. Facebook no se enlaza de forma visible. | [PR #22](https://github.com/IsabelLopez/lopsa/pull/22); [plantillas/base.html](plantillas/base.html), [plantillas/contacto.html](plantillas/contacto.html), [plantillas/_macros.html](plantillas/_macros.html) (`icono_instagram`), [estaticos/css/estilos.css](estaticos/css/estilos.css) (`.pie__instagram`, `.boton-icono`), [datos/sitio.json](datos/sitio.json) (`instagram`). |

Las capturas locales no incluidas en Git no son una referencia disponible para otro equipo. Para comparar
el resultado, usar el sitio, esta versión de los archivos y las referencias anteriores; si se añade una
captura al relevo, debe ser pública, estar versionada o tener un enlace accesible y señalar fecha y versión.

## Pendientes y siguiente paso

- [PR #20](https://github.com/IsabelLopez/lopsa/pull/20) y [PR #21](https://github.com/IsabelLopez/lopsa/pull/21)
  están integrados y verificados en producción: JSON-LD y sitemap; fotos `-v4` en 200 y versiones retiradas en 404
  (comprobado de nuevo el 07-oct). Consultar [PR #22](https://github.com/IsabelLopez/lopsa/pull/22): si está
  integrado, comprobar que el ícono de Instagram se ve en el pie y en Contacto. El estado de una revisión no se
  transforma en «publicado» hasta verificar su integración y su despliegue.
- Las páginas por aplicación y los casos de obra son una propuesta en preparación, pendiente de aprobación
  de la dirección de LOPSA. No publicarlas sin esa aprobación; deben reutilizar los componentes y el diseño
  vigentes de esta tabla, sin nuevas afirmaciones técnicas ni datos de clientes.
- La presencia del código de medición no demuestra recepción de eventos. Queda por comprobar en la
  herramienta correspondiente la recepción de `whatsapp_click` y `generate_lead`, sin confundir un clic
  o una prueba con una consulta real. Este relevo no certifica ese resultado.
- Para la próxima tarea, retomar el diseño anterior y el alcance solicitado; registrar cualquier cambio
  aprobado en esta tabla con su referencia, conservando el antecedente en el punto de continuidad.

## Puntos de continuidad

### 07-oct-2026 — enlace visible a Instagram

- **Hecho:** la web solo mencionaba Instagram en los datos estructurados (`sameAs`), sin enlace visible. Ahora hay
  un ícono de Instagram enlazado a https://www.instagram.com/lopsa_pa/ en el pie de todas las páginas y junto al
  botón de WhatsApp en Contacto. Solo Instagram: Facebook no se enlaza de forma visible. Regla nueva en
  `CLAUDE.md`. Estado: integrado mediante PR si su página lo indica; propuesto mientras siga abierto.
- **Archivos / versión:** `plantillas/_macros.html`, `plantillas/base.html`, `plantillas/contacto.html`,
  `estaticos/css/estilos.css`, `dist/`, `datos/_fechas_sitemap.json`, `CLAUDE.md`; rama
  `web/enlace-instagram-20261007` sobre `9e3c199`, [PR #22](https://github.com/IsabelLopez/lopsa/pull/22).
- **Revisión:** verificador **OK, 11 páginas**; diff de `dist/` limitado al pie, a las acciones de Contacto, a la
  versión del CSS y al `lastmod`; Chrome sin cabeza en 320, 390, 768, 1024, 1440 y 1920 px sobre 10 páginas, sin
  desbordes ni errores de JavaScript; enlace visible en todas (42×42 px en el pie, 48×48 px en Contacto); estados
  al pasar el cursor y foco de teclado comprobados. Datos estructurados sin cambios.
- **Pendiente:** comprobar en producción, tras la integración, que el HTML servido coincide con `dist/`.
- **Siguiente acción:** cualquier red social nueva se añade solo con orden de la dirección y con este mismo patrón.

### 06-oct-2026 — fotos sin personas identificables ni emblemas ajenos

- **Hecho:** Proceso (pasos 2 y 3) y Trabajos («Preparación mecánica del piso» y «Sellado del encuentro losa–muro»)
  usan recortes de las mismas fotos sin caras reconocibles, emblemas de otras empresas ni marcas: `paso-2-v4`,
  `paso-3-v4`, `galeria-preparacion-piso-v4` y `galeria-preparacion-juntas-v4`. Se retiraron del sitio publicado
  `paso-2-v3`, `paso-3-v3`, `galeria-preparacion-piso-v3`, `galeria-preparacion-juntas-v3` y `nosotros-cuadrilla`.
  Pies de foto sin cambios; texto alternativo ajustado. Regla nueva en `CLAUDE.md`.
- **Archivos / versión:** `datos/imagenes.json`, `datos/_imagenes_generadas.json`, `datos/proceso.json`,
  `datos/proyectos.json`, `estaticos/img/` y `dist/`; [PR #21](https://github.com/IsabelLopez/lopsa/pull/21).
- **Revisión:** verificador **OK, 11 páginas**; diff limitado a las etiquetas `<img>` de Proceso y Trabajos; recortes
  revisados ampliados; capturas de escritorio con las mismas ranuras. Revisadas también las demás fotos con personas
  (techos de zinc, equipo y drenaje): sin rostros identificables a su tamaño publicado.
- **Pendiente:** comprobar en producción que las versiones nuevas cargan y que las retiradas ya no responden.
- **Siguiente acción:** antes de incorporar una foto con personas, revisar caras, emblemas y marcas a tamaño completo.

### 06-oct-2026 — SEO técnico sin cambios visuales

- **Hecho:** datos estructurados de la portada completados (tipo `HomeAndConstructionBusiness`, catálogo con las
  seis aplicaciones publicadas, punto de contacto, lema y `sameAs` con Instagram, la página pública de Facebook
  «LOPSA, S.A.» y la ficha de Google); `BreadcrumbList` en las seis páginas con migas visibles; `lastmod` del
  sitemap con la fecha real de cada página (`datos/_fechas_sitemap.json`); el verificador comprueba JSON-LD y
  fechas. La FAQ estructurada de Contacto ya existía con las ocho preguntas publicadas: no se duplicó.
  Estado: integrado mediante PR si su página lo indica; propuesto mientras siga abierto.
- **Archivos / versión:** `construir_sitio.py`, `verificar_sitio.py`, `plantillas/base.html`, `index.html` y las
  seis plantillas con migas, `datos/sitio.json` (`facebook`), `datos/_fechas_sitemap.json`, `CLAUDE.md`, `README.md`;
  rama `seo/datos-estructurados-lastmod-20261006` sobre `71ff5fa`, [PR #20](https://github.com/IsabelLopez/lopsa/pull/20).
- **Revisión:** construcción estable en dos pasadas; verificador **OK, 11 páginas**; prueba negativa del
  verificador; diff de `dist/` limitado a JSON-LD y sitemap; validator.schema.org con 0 errores en portada,
  Contacto y Aplicaciones; capturas de escritorio y móvil idénticas a la versión anterior.
- **Pendiente:** comprobar producción tras la integración. Diseño, textos visibles, formulario y fotografías sin cambios.
- **Siguiente acción:** retomar desde este relevo; cualquier página nueva requiere aprobación y debe reutilizar
  las decisiones visuales vigentes.

### 24-sep-2026 — documentación de continuidad

- **Hecho:** referencia pública de las decisiones vigentes y obligación común de retomar/actualizar el
  relevo. Procedimiento Git corregido para identificar el repositorio de producción por su URL.
- **Archivos / versión:** `CLAUDE.md` y `CONTINUIDAD_DISENO.md`, rama `docs/continuidad-diseno-20260924`,
  sobre `b26454d`; revisión en [PR #19](https://github.com/IsabelLopez/lopsa/pull/19). Sin cambios en datos,
  plantillas, estilos ni `dist/`.
- **Revisión:** `python construir_sitio.py` completado; `python verificar_sitio.py` → **OK, 11 páginas**.
  Veinte enlaces locales comprobados, sin destinos ausentes; `git diff --check` sin errores. La construcción
  solo cambió la fecha de `dist/sitemap.xml`; se restauró ese resultado generado a su versión de base para
  conservar esta revisión exclusivamente documental. `git diff --exit-code -- dist` sin diferencias.
- **Pendiente:** consultar el estado de [PR #19](https://github.com/IsabelLopez/lopsa/pull/19); el enlace
  conserva el resultado de revisión e integración. Sin rediseño propuesto.
- **Siguiente acción:** si el PR está integrado, retomar la nueva tarea con este diseño como referencia;
  si está abierto, completar la revisión e integración según `CLAUDE.md` y el alcance de la sesión.

### Plantilla para el siguiente avance

```text
Fecha — tarea y alcance autorizado / referencia de la decisión
Hecho: resultado concreto; indicar si es propuesta, aprobado, integrado o publicado.
Archivos / versión: rutas, rama y commit o enlace de revisión/despliegue.
Revisión: qué se comprobó, resultado y qué sigue sin verificar.
Pendiente: trabajo restante o bloqueo real.
Siguiente acción: un paso concreto para quien retome.
```
