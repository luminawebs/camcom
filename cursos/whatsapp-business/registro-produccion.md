# Registro de producción · Vende más por WhatsApp Business (AVS-G04)

Curso 4 del Aula Virtual Empresarial Soacha (nivel 3 · Vende más). Gancho gratuito (unidades 1 a 3 del curso; las 4 a 7 van con el Pase), perfil P con Aprende como lección narrada, ≈ 1,5 horas. Pedido de David el 14 de octubre de 2026 y producido ese mismo día.
Respaldo: `moodle/whatsapp-business/respaldo-avs-g04-whatsapp-business.mbz` (≈ 15 MB, 26 actividades, 5 secciones).

## Qué se hizo y con qué comando

| Paso | Qué produce | Comando | API |
| --- | --- | --- | --- |
| 1 | `investigacion.md` y `curso.json` (caso, personas, objetivos, textos) | a mano, con Claude | búsqueda web |
| 2 | `piezas/uN-aprende` (`contenido.js`) | a mano, con Claude | — |
| 2b | 15 pantallas del simulador, `piezas/uN-practica/contenido.js` y 5 vistas para las lecciones | `python3 pantallas/armar_pantallas.py` + `node pantallas/renderizar.mjs` | — |
| 3 | Mapas mentales (`mapas/*.png`) | `python3 mapas/armar_mapas.py` + `node mapas/renderizar.mjs` | — |
| 3 | Guías de estudio A5 (`guias-pdf/*.pdf`) | `python3 guias-pdf/armar_guias.py` + `node guias-pdf/renderizar_pdf.mjs` | — |
| 3 | Descargas (ficha del catálogo, rutina de pedidos, mensajes listos) | `python3 descargas/armar_descargas.py` + `node guias-pdf/renderizar_pdf.mjs descargas` | — |
| 4 | 21 narraciones (3 Entradas + 18 pantallas de Aprende), 7 min | `python3 plantillas/narrar.py cursos/whatsapp-business` | Resemble |
| 4b | 3 personajes + 6 ilustraciones | `python3 plantillas/ilustrar.py cursos/whatsapp-business` | Gemini (en el hilo «Ilustraciones curso 4», sin el equipo conectado) |
| 4c | 3 videos de Entrada (31 a 33 s) | `python3 plantillas/video_entrada.py cursos/whatsapp-business` | — |
| 4d | 3 resúmenes (31 a 33 s) y bienvenida (42 s) | `python3 plantillas/video_resumen.py cursos/whatsapp-business u1-resumen` (y `u2-resumen`, `u3-resumen`, `bienvenida`) | Resemble |
| 4e | Imagen del curso 1080 × 1080 | `python3 plantillas/imagen_curso.py cursos/whatsapp-business` | — |
| 5 | Páginas, vista previa y 6 SCORM | `python3 plantillas/armar_curso.py cursos/whatsapp-business --scorm` | — |
| 6 | Respaldo .mbz con todos los medios | `python3 moodle/publicar_curso.py cursos/whatsapp-business --corto AVS-G04` | — |
| 6b | Curso nuevo en Moodle | `python3 moodle/subir_moodle.py cursos/whatsapp-business` | Moodle |

## Gasto en APIs

| Servicio | Uso | Costo |
| --- | --- | --- |
| Resemble AI (voz Jota) | Narraciones 7 min · resúmenes ≈ 1,6 min · bienvenida 0,7 min | ≈ 9,3 min de audio. El precio depende del plan. |
| Gemini 2.5 Flash Image | 14 llamadas (9 usadas, 2 escenas rehechas porque metieron gente de relleno, hojas de personaje regeneradas) | ≈ USD 0,54. Detalle en `ilustraciones/registro.json`. |

## Cambios al pipeline hechos con este curso

- `armar_curso.py`: campo opcional `receta` en `curso.json` para cambiar un paso de la receta del perfil en un solo curso (aquí, Aprende = lección narrada en vez de screencast).
- `narrar.py`: campo opcional `narracion.reemplazos` para cambiar cómo se lee un texto (por ejemplo «/domicilio» → «barra domicilio») sin tocar lo que se ve.
- Nuevo `pantallas/` (propio del curso): pantallas simplificadas de la app en HTML que el renderizador mide para poner las zonas del simulador solas.

## Pendiente en este curso

- Validar con el asesor de mercadeo digital de la Cámara los [VERIFICAR] (rutas de menú en Android y iPhone, nombres de las etiquetas, días de la bienvenida, cambio de número, redacción sobre la Ley 1581). Lista en `moodle/whatsapp-business/quitado-al-publicar.txt`.
- Si el asesor toma capturas reales del celular, reemplazar las pantallas del simulador (`piezas/uN-practica/medios/`) y ajustar las zonas.
- Enlaces directos del servicio de ayuda de WhatsApp en Profundiza (hoy van a faq.whatsapp.com).
- ~~3 fichas 1080 × 1920 para el celular (Llévatelo), en Canva.~~ Hechas el 2026-10-20 con `python3 plantillas/fichas.py cursos/whatsapp-business` (fichas/uN-ficha.jpg).
- Número de WhatsApp de la Cámara.

## Subidas a Moodle

Las agrega `moodle/subir_moodle.py`.
- 2026-10-14 23:35 UTC · nuevo en Moodle: https://portal.edunest.co/course/view.php?id=13 · respaldo-avs-g04-whatsapp-business.mbz · 26/26 actividades en su sección
- 2026-10-21 02:43 UTC · reemplazo en Moodle: https://portal.edunest.co/course/view.php?id=13 · respaldo-avs-g04-whatsapp-business.mbz · 26/26 actividades en su sección
