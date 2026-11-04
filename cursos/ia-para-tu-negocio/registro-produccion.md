# Registro de producción · IA para tu negocio desde el celular (AVS-G06)

Curso 6 del Aula Virtual Empresarial Soacha (ruta por metas, nivel 4 · Automatiza con IA, curso 16 ★). Gancho gratuito (unidades 1 a 3 del curso; las 4 a 7 van con el Pase), perfil P con Aprende como lección narrada, ≈ 1,5 horas. Propuesto y aprobado por David el 29 de octubre de 2026 y producido ese mismo día.
Respaldo: `moodle/ia-para-tu-negocio/respaldo-avs-g06-ia-para-tu-negocio.mbz`.

## Qué se hizo y con qué comando

| Paso | Qué produce | Comando | API |
| --- | --- | --- | --- |
| 1 | `investigacion.md` y `curso.json` (caso, personas, objetivos, textos) | a mano, con Claude | búsqueda web |
| 2 | `piezas/uN-aprende` (`contenido.js`) | a mano, con Claude | — |
| 2b | 15 pantallas del simulador (asistente sin marca), `piezas/uN-practica/contenido.js` y 6 vistas para las lecciones | `python3 pantallas/armar_pantallas.py` + `node pantallas/renderizar.mjs` | — |
| 3 | Mapas mentales (`mapas/*.png`) | `python3 mapas/armar_mapas.py` + `node mapas/renderizar.mjs` | — |
| 3 | Guías de estudio A5 (`guias-pdf/*.pdf`) | `python3 guias-pdf/armar_guias.py` + `node guias-pdf/renderizar_pdf.mjs` | — |
| 3 | Descargas (fórmula del pedido, 10 pedidos listos, semáforo de datos) | `python3 descargas/armar_descargas.py` + `node guias-pdf/renderizar_pdf.mjs descargas` | — |
| 4 | 21 narraciones (3 Entradas + 18 pantallas de Aprende), 7 min | `python3 plantillas/narrar.py cursos/ia-para-tu-negocio` | Resemble |
| 4b | 3 personajes + 6 ilustraciones | `python3 plantillas/ilustrar.py cursos/ia-para-tu-negocio` | Gemini (en este hilo; el equipo de David aún no estaba conectado) |
| 4c | 3 videos de Entrada | `python3 plantillas/video_entrada.py cursos/ia-para-tu-negocio` | — |
| 4d | 3 resúmenes y bienvenida | `python3 plantillas/video_resumen.py cursos/ia-para-tu-negocio u1-resumen` (y `u2-resumen`, `u3-resumen`, `bienvenida`) | Resemble |
| 4e | Imagen del curso 1080 × 1080 y 3 fichas de Llévatelo | `python3 plantillas/imagen_curso.py cursos/ia-para-tu-negocio` + `python3 plantillas/fichas.py cursos/ia-para-tu-negocio` | — |
| 5 | Páginas, vista previa y 6 SCORM | `python3 plantillas/armar_curso.py cursos/ia-para-tu-negocio --scorm` | — |
| 6 | Respaldo .mbz con todos los medios | `python3 moodle/publicar_curso.py cursos/ia-para-tu-negocio --corto AVS-G06` | — |
| 6b | Curso nuevo en Moodle | `python3 moodle/subir_moodle.py cursos/ia-para-tu-negocio` | Moodle |

## Gasto en APIs

| Servicio | Uso | Costo |
| --- | --- | --- |
| Resemble AI (voz Jota) | Narraciones 7 min + resúmenes y bienvenida | El precio depende del plan. |
| Gemini 2.5 Flash Image | 10 llamadas (9 usadas; el semáforo se rehízo porque mezcló las filas) | ≈ USD 0,39. Detalle en `ilustraciones/registro.json`. |

## Cambios al pipeline hechos con este curso

- Chromium del entorno cambió de versión: `plantillas/video_resumen.py` y los `renderizar*.mjs` de este curso ya no fijan la ruta `chromium-1194` (usan el navegador que trae Playwright).

## Pendiente en este curso

- Validar con el asesor de transformación digital y el abogado de la Cámara los [VERIFICAR] (lista en `investigacion.md` y en `moodle/ia-para-tu-negocio/quitado-al-publicar.txt`), sobre todo lo de la Ley 1581, la Circular Externa 002 de 2024 de la SIC y la Ley 1480.
- Si el asesor prefiere capturas reales de una app concreta, reemplazar las pantallas del simulador (`piezas/uN-practica/medios/`) y ajustar las zonas.
- Número de WhatsApp de la Cámara.
- Tramo Pase (U4-U7): instrucciones fijas, ventas en Excel con IA, imágenes para redes, medir la hora ahorrada.

## Subidas a Moodle

Las agrega `moodle/subir_moodle.py`.
- 2026-10-29 20:03 UTC · nuevo en Moodle: https://portal.edunest.co/course/view.php?id=15 · respaldo-avs-g06-ia-para-tu-negocio.mbz · 26/26 actividades en su sección
