# Instrucciones para cualquier agente — sitio web de LOPSA (lopsa.com.pa)

Este repositorio ES la página web de LOPSA, S.A. Todo lo que llega a la rama `main` del repositorio de
producción [IsabelLopez/lopsa](https://github.com/IsabelLopez/lopsa) se publica solo en
https://lopsa.com.pa (Netlify, en 1 a 3 minutos). Quien te escribe es un socio de LOPSA que **no programa**: te dirá
con palabras qué quiere cambiar. Tú haces el cambio, lo revisas, lo publicas y le confirmas con el enlace.

## Continuidad entre sesiones y modelos
- Estas son las reglas comunes para Claude, Codex y cualquier otro agente; `AGENTS.md` apunta aquí.
- Antes de trabajar, lee [CONTINUIDAD_DISENO.md](CONTINUIDAD_DISENO.md) y los cambios posteriores de la rama.
  Retoma lo aprobado y lo pendiente desde sus archivos y referencias. Cambiar de modelo o aplicación no
  autoriza a rediseñar ni a sustituir recursos aprobados por preferencias propias.
- Registra allí cada avance relevante al producirse: decisión o alcance autorizado, archivos y versión,
  revisión realizada, pendientes y siguiente acción. Antes de un corte o cambio de sesión deja un punto de
  continuidad, aunque el trabajo siga incompleto. Las propuestas se identifican por separado; una rama o un
  pull request no prueban que algo esté publicado. Conserva la referencia anterior al actualizar el estado.
- El relevo contiene solo información pública. No depende de una memoria privada de la aplicación; las
  reglas se cambian aquí y el estado con sus evidencias se actualiza en el relevo.

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
- Estructura vigente (16-sep-2026): inicio breve y seis páginas: `/poliurea/`, `/aplicaciones/`, `/proceso/`, `/trabajos/`, `/equipo/`, `/contacto/`. No reunir de nuevo todo el contenido en una página larga. Las plantillas llevan el mismo nombre y el constructor registra las rutas y el sitemap.
- El formulario y las preguntas frecuentes viven en `plantillas/contacto.html`. El visor pertenece a `plantillas/trabajos.html`. Navegación en `sitio.nav` usa `url` y `pagina`; conservar `aria-current` y compatibilidad con enlaces antiguos.
- **Fotos:** solo se pueden usar las que ya están procesadas; sus nombres están en `datos/_imagenes_generadas.json`
  (por ejemplo `app-zinc`, `caso1-despues`, `nosotros-camion`). Para poner otra foto ya existente, cambia ese nombre
  en el `.json` que corresponda. **Fotos nuevas no se pueden subir desde aquí:** pide que las manden al grupo de
  WhatsApp de los socios y Manuel las sube. No corras `preparar_imagenes.py`: sus originales no están en este repositorio.
- No toques `netlify.toml`, `legacy/` ni el formulario `cotizacion` (su nombre, los atributos `data-netlify` y
  `netlify-honeypot`, ni el `name` de sus campos): de eso dependen los avisos de cotización que llegan por correo.

## Cómo hacer un cambio (siempre en este orden)
1. Identifica con `git remote -v` el remoto cuya URL corresponde a **`IsabelLopez/lopsa`**, repositorio de
   producción. No presupongas que se llama `origin`: puede llamarse `isabel`, y `origin` puede ser un espejo.
   Haz `git fetch <remoto-produccion>` y crea una rama desde `<remoto-produccion>/main` (si ya te dieron una
   rama, incorpora esa referencia antes de empezar). Si falta ese remoto, añádelo con la URL de producción
   sin cambiar el destino de otros remotos. Comprueba por separado el despliegue al confirmar lo publicado.
2. Haz solo el cambio que se pidió.
3. `pip install -r requirements.txt` (una vez por sesión), luego `python construir_sitio.py` y
   `python verificar_sitio.py`. El verificador tiene que decir **OK**; si no, corrige y repite.
4. Revisa `git diff --stat`: que solo cambie lo pedido (más `dist/sitemap.xml`, que lleva la fecha del día).
5. Commit con mensaje en español, sube la rama al remoto de producción y abre un pull request contra `main`
   en **`IsabelLopez/lopsa`**. Con GitHub CLI indica `--repo IsabelLopez/lopsa` para no usar el espejo por error.
6. Justo antes de fusionar, vuelve a traer `<remoto-produccion>/main`. Si cambió (otro socio publicó algo), mézclalo en tu rama.
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
- Portada vigente: fotografía fija del **camión con edificio de fondo**, completa también en celular, sin carrusel. Inicio corto con mensaje principal y accesos a Poliurea, Aplicaciones y Trabajos; Proceso y Equipo en menú y enlaces. El contenido técnico queda en páginas independientes.
- Dentro de Poliurea: explicación para personas sin conocimientos previos, cifras y capas visibles sin clics.
- Cifras en franja compacta; render con nombres y líneas dentro de la imagen. Una misma tabla comparativa en PC y celular, con desplazamiento horizontal y criterio fijo; no volver a convertirla en fichas móviles. Destacar ventajas reales, sin afirmar superioridad universal ni inventar garantías de otras familias.
- Garantía: **«10 años contra filtraciones en cubiertas»**. Separar de **25 años de vida útil estimada W3 en cubiertas**.
- **8–14 segundos** es formación de gel, referencia de la ficha técnica española del sistema; no secado completo ni habilitación instantánea. La ficha internacional da otros tiempos: la puesta en servicio depende del producto suministrado, curado, acabado y uso. Promover reducción de paradas y planificación por zonas.
- Respaldo público documentado: ETE 11/0016, CE, W3, BROOF(t1) sobre concreto, ensayo de migración al agua, raíces, difusión de radón y declaración del fabricante para áreas alimentarias. Mantener el alcance y tipo de documento de cada tarjeta; no extender a certificación de LOPSA, todos los soportes o todos los productos. En celular mostrar dos tarjetas por fila. Acordeón: «Consultar Ficha Técnica».
- Sin precios, tarifas ni descuentos. Sin marcas de materiales ni de equipos. Sin promesas que LOPSA no haya
  confirmado (plazos, certificaciones, «precio fijo»).
- LOPSA se presenta como especialista en poliurea caliente; la construcción es secundaria.
- Contacto público: WhatsApp y teléfono **+507 6604-4196**, correo **ventas@lopsa.com.pa**. Ningún otro teléfono
  ni correo personal.
- Español con tildes y ñ, trato de usted.

## Este repositorio es PÚBLICO
Todo lo que se sube se puede ver en internet, historial incluido. Nunca subas contraseñas, tokens, cédulas, datos
de clientes, fotos originales del celular (llevan la ubicación GPS) ni documentos internos de la empresa.
