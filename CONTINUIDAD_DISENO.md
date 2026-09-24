# Continuidad del diseño de lopsa.com.pa

Actualizado: **24-sep-2026**. Relevo público para continuar el mismo trabajo desde cualquier sesión o modelo.
Las reglas y el procedimiento viven únicamente en [CLAUDE.md](CLAUDE.md); este archivo registra estado,
decisiones y evidencia. Las instrucciones antiguas del historial no sustituyen las decisiones vigentes.

## Estado de referencia

| Estado | Evidencia y alcance |
|---|---|
| Diseño publicado vigente | Inicio breve y seis páginas independientes, incorporados en [PR #13](https://github.com/IsabelLopez/lopsa/pull/13), versión [58d1d34](https://github.com/IsabelLopez/lopsa/commit/58d1d34), 16-sep-2026. Conserva los ajustes visuales de los PR #6–12 indicados abajo. Sitio: [lopsa.com.pa](https://lopsa.com.pa/). |
| Base actual de producción | `IsabelLopez/lopsa`, rama `main`, [b26454d](https://github.com/IsabelLopez/lopsa/commit/b26454dcc3e7e9a92eb7abf05a0b2a45e9763822), 21-sep-2026, consultada con `git fetch` el 24-sep. Incluye [PR #14](https://github.com/IsabelLopez/lopsa/pull/14), [#15](https://github.com/IsabelLopez/lopsa/pull/15), [#16](https://github.com/IsabelLopez/lopsa/pull/16) y [#17](https://github.com/IsabelLopez/lopsa/pull/17) de SEO/medición y [#18](https://github.com/IsabelLopez/lopsa/pull/18) de instrucciones. Esta lectura de Git no certifica el identificador del despliegue activo de Netlify. |
| Trabajo de esta revisión | [PR #19](https://github.com/IsabelLopez/lopsa/pull/19), rama `docs/continuidad-diseno-20260924`: este relevo y la entrada en `CLAUDE.md`. Solo documentación. Consultar el estado del PR para saber si sigue abierto o está integrado; no propone cambios visuales ni modifica el sitio generado. |
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

Las capturas locales no incluidas en Git no son una referencia disponible para otro equipo. Para comparar
el resultado, usar el sitio, esta versión de los archivos y las referencias anteriores; si se añade una
captura al relevo, debe ser pública, estar versionada o tener un enlace accesible y señalar fecha y versión.

## Pendientes y siguiente paso

- Consultar [PR #19](https://github.com/IsabelLopez/lopsa/pull/19): si está integrado, continuar con la nueva
  tarea; si está abierto, completar su revisión e integración. El estado de una revisión no se transforma
  en «publicado» hasta verificar su integración y, si cambia el sitio, su despliegue.
- La presencia del código de medición no demuestra recepción de eventos. Queda por comprobar en la
  herramienta correspondiente la recepción de `whatsapp_click` y `generate_lead`, sin confundir un clic
  o una prueba con una consulta real. Este relevo no certifica ese resultado.
- Para la próxima tarea, retomar el diseño anterior y el alcance solicitado; registrar cualquier cambio
  aprobado en esta tabla con su referencia, conservando el antecedente en el punto de continuidad.

## Puntos de continuidad

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
