# Plantillas HTML5 · Aula Virtual Empresarial Soacha

Moldes de cada paso del curso (metodología de `../artefactos/produccion-aula-soacha.html`).
Abre `index.html` en el navegador para verlas todas en tamaño celular.

## Qué hay

| Carpeta | Qué es | Cómo llega a Moodle |
| --- | --- | --- |
| `comun/aula.css` | Sistema visual común (colores, tipos, botones, espacios por llenar) | Pegar una vez en Boost Union > SCSS adicional. El empaquetador también lo mete en cada SCORM. |
| `comun/aula.js` | Motor: conexión SCORM 1.2, nota, punto de regreso, espacios por llenar | Va dentro de cada paquete SCORM. |
| `componentes/<molde>/` | 7 componentes interactivos: `index.html` (lógica) + `contenido.js` (textos y medios) | `python3 empaquetar.py` → `scorm/<molde>.zip` → Agregar actividad > Paquete SCORM |
| `fragmentos/*.html` | 8 bloques para Página, Etiqueta o resumen de sección | Editor de Moodle en modo código: pegar lo que está entre `COPIAR DESDE AQUÍ` y `HASTA AQUÍ` |
| `scorm/*.zip` | Paquetes de prueba de cada molde, con los espacios por llenar | Subir tal cual para probar en Moodle y en la app |

Campos opcionales de `curso.json` para no depender de textos del curso 1: `revisor` (quién revisa los resúmenes), `mapa_curso_nota`,
`inicio.video_nota`, `cierre.rubrica` (3 criterios del reto final), `llevatelo.etiqueta_formula` (p. ej. "La regla") y descargas como
`{"texto": "...", "archivo": "uN-....pdf"}` con el archivo en `descargas/` (el botón se enlaza solo).

## Convenciones

- `[texto entre corchetes]` se ve resaltado en gris con borde punteado: es lo que se reemplaza.
- Un medio con `src: ""` se muestra como espacio rayado con la indicación de qué va (formato, duración, peso).
  Al llenarlo: `src: "medios/video-u2.mp4"` y el archivo en `medios/`.
- `{{dato}}` en un texto toma el valor de `datos` en `contenido.js`: así las cifras normativas (UVT, topes, fechas)
  se actualizan cada año sin tocar la pieza. Lo no validado se marca `[VERIFICAR]`.
- `**negrita**` funciona en todos los textos.

## Producir un curso completo

1. Crea `cursos/<id>/curso.json` copiando el de `cursos/plata-negocio/` (nivel, perfil, caso, objetivos y textos).
2. Por cada paso con molde HTML5 de la receta del perfil, crea `cursos/<id>/piezas/uN-<paso>/contenido.js`
   copiando el `contenido.js` del molde (K: `leccion-interactiva` y `calculadora`).
3. Define en `curso.json` el formato del resumen de unidad, `"resumen_formato": "video"` o `"audio"` (solo uno; se puede cambiar por unidad con `resumen.formato`).
   Arma los mapas mentales copiando `cursos/plata-negocio/mapas/` (cambia el contenido de `armar_mapas.py`, luego `python3 armar_mapas.py`
   y `node renderizar.mjs`). Si existen `mapas/mapa-curso.png` y `mapas/uN-mapa.png`, las páginas de Inicio y Llévatelo los muestran;
   si no, dejan el espacio marcado. NotebookLM no se usa para los mapas porque no deja descargarlos.
   Arma las guías de estudio copiando `cursos/plata-negocio/guias-pdf/` (contenido en `armar_guias.py`, logo en `marca/`;
   luego `python3 armar_guias.py` y `node renderizar_pdf.mjs`). Si existen `guias-pdf/uN-guia.pdf`, Llévatelo pone el botón de descarga.
4. Narraciones con Resemble AI: agrega a `curso.json`
   `"narracion": {"voz": "<id de la voz>", "secciones": ["entrada", "aprende"]}` y `narracion: true` en cada `uN-aprende/contenido.js`;
   luego `python3 plantillas/narrar.py cursos/<id>` (clave en la variable de entorno `RESEMBLE_API_KEY`). Genera MP3 mono de 64 kbps:
   el caso de cada Entrada en `medios-moodle/uN-entrada-narracion.mp3` y cada pantalla de Aprende en `piezas/uN-aprende/medios/narracion-K.mp3`.
   `narraciones.json` guarda el texto leído; solo se regenera lo que cambió.
4b. Ilustraciones con Gemini (opcional): describe en `cursos/<id>/ilustraciones.json` el estilo, los personajes y cada escena
   con sus destinos; luego `python3 plantillas/ilustrar.py cursos/<id>` (clave en `GEMINI_API_KEY`, modelo por defecto Gemini 2.5 Flash Image,
   ≈ USD 0,039 por imagen). Dibuja primero una hoja por personaje y la usa de referencia en cada escena para que se vean iguales.
   Deja la Entrada en `medios-moodle/uN-entrada.jpg` y las de las lecciones en `piezas/uN-aprende/medios/ilustracion-K.jpg`
   (en `contenido.js`: `src: "medios/ilustracion-K.jpg", alt: "..."`). `ilustraciones/registro.json` lleva cada imagen pagada y su costo;
   no vuelve a pagar una imagen cuyo texto no cambió (`--solo <id>` rehace una).
4c. Video de Entrada (opcional): `python3 plantillas/video_entrada.py cursos/<id>` junta la ilustración de la Entrada y su narración de
   Resemble en `medios-moodle/uN-entrada.mp4` (+ `.vtt`), con título, subtítulos y la pregunta de la unidad. No llama a ninguna API.
   Si existe, la Entrada muestra el video en lugar de la imagen y el reproductor de audio.
4d. Bienvenida y resúmenes en video (automáticos, reemplazan a NotebookLM desde el curso 2): escribe `video/bienvenida.json` y
   `video/uN-resumen.json` (5 diapositivas: portada, listas, frase y cierre, cada una con su texto en pantalla y su "voz"; "imagen"
   opcional con una ruta de `ilustraciones/`). Toma los textos del guion de 60 s al final de `notebooklm/fuentes/uN-guion.md`.
   Luego `python3 plantillas/video_resumen.py cursos/<id> bienvenida` y `... uN-resumen`: video vertical con voz de Resemble y
   subtítulos en `medios-moodle/`. Inicio y el Resumen de cada unidad lo muestran solos. Ejemplo completo: `cursos/formaliza-tu-negocio/video/`.
5. `python3 plantillas/armar_curso.py cursos/<id> --scorm` genera `estructura.md`, `paginas/` (fragmentos llenos),
   `vista-previa/` y `scorm/`. La vista previa lista lo que falta validar y los medios por producir.
6. `python3 moodle/publicar_curso.py cursos/<id> --corto AVS-Gnn` arma el respaldo .mbz con todos los medios.
7. En Moodle, en cada actividad SCORM: calificación = puntuación más alta, finalización = "requiere estado aprobado o completado".

Una pieza suelta sigue funcionando como antes: `python3 empaquetar.py calculadora --curso <pieza>` (lee `cursos/<pieza>/` dentro de `plantillas/`).

## Pendiente de decidir con el cliente

- Logo y colores definitivos (hoy blanco, rojo, negro y grises). Se cambian solo en `:root` de `aula.css`.
- Si el editor de Moodle del sitio permite `<details>` y clases (requiere que el rol tenga "contenido de confianza" o que el filtro HTML no las limpie). Probar un fragmento antes de producir en serie.
