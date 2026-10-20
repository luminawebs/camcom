# Registro de producción · Lee tus números (AVS-G05)

Curso 5 del Aula Virtual Empresarial Soacha (nivel 2 · Entiende tus números). Gancho gratuito (unidades 1 a 3 del curso; las 4 a 7 van con el Pase), perfil K, ≈ 1,5 horas. Propuesto el 20 de octubre de 2026, aprobado por David ese día y producido ese mismo día.
Respaldo: `moodle/lee-tus-numeros/respaldo-avs-g05-lee-tus-numeros.mbz` (≈ 14 MB, 26 actividades, 5 secciones).

## Qué se hizo y con qué comando

| Paso | Qué produce | Comando | API |
| --- | --- | --- | --- |
| 1 | `investigacion.md` y `curso.json` (caso, personas, objetivos, textos) | a mano, con Claude | búsqueda web |
| 2 | `piezas/uN-aprende` y `uN-practica` (`contenido.js`) | a mano, con Claude | — |
| 3 | Mapas mentales (`mapas/*.png`) | `python3 mapas/armar_mapas.py` + `node mapas/renderizar.mjs` | — |
| 3 | Guías de estudio A5 (`guias-pdf/*.pdf`) | `python3 guias-pdf/armar_guias.py` + `node guias-pdf/renderizar_pdf.mjs` | — |
| 3 | Descargas (clasificar movimientos, hoja del mes, estado de resultados en PDF y Excel) | `python3 descargas/armar_descargas.py` + `node guias-pdf/renderizar_pdf.mjs descargas` (el .xlsx con openpyxl) | — |
| 4 | 21 narraciones (3 Entradas + 18 pantallas de Aprende), 7 min | `python3 plantillas/narrar.py cursos/lee-tus-numeros` | Resemble |
| 4b | 3 personajes + 6 ilustraciones | `python3 plantillas/ilustrar.py cursos/lee-tus-numeros` | Gemini (en el hilo «Ilustraciones curso 5», sin el equipo conectado) |
| 4b | 2 hojas de ejemplo (hoja del mes de Óscar, estado de resultados de Marisol) | HTML en `ilustraciones/hojas/` → JPG con Playwright | — |
| 4c | 3 videos de Entrada (32 a 33 s) | `python3 plantillas/video_entrada.py cursos/lee-tus-numeros` | — |
| 4d | 3 resúmenes (29 a 30 s) y bienvenida (44 s) | `python3 plantillas/video_resumen.py cursos/lee-tus-numeros u1-resumen` (y `u2-resumen`, `u3-resumen`, `bienvenida`) | Resemble |
| 4e | Imagen del curso 1080 × 1080 | `python3 plantillas/imagen_curso.py cursos/lee-tus-numeros` | — |
| 5 | Páginas, vista previa y 6 SCORM | `python3 plantillas/armar_curso.py cursos/lee-tus-numeros --scorm` | — |
| 6 | Respaldo .mbz con todos los medios | `python3 moodle/publicar_curso.py cursos/lee-tus-numeros --corto AVS-G05` | — |
| 6b | Curso nuevo en Moodle (curso 14) | `python3 moodle/subir_moodle.py cursos/lee-tus-numeros` | Moodle |

## Gasto en APIs

| Servicio | Uso | Costo |
| --- | --- | --- |
| Resemble AI (voz Jota) | Narraciones 7 min · resúmenes ≈ 1,5 min · bienvenida 0,7 min | ≈ 9,2 min de audio. El precio depende del plan. |
| Gemini 2.5 Flash Image | 15 llamadas (9 usadas; las 3 infografías se rehicieron porque salieron con gente o con palabras en inglés) | ≈ USD 0,58. Detalle en `ilustraciones/registro.json`. |

## Pendiente en este curso

- Validación del contador de la Cámara de los [VERIFICAR] (`investigacion.md` y `moodle/lee-tus-numeros/quitado-al-publicar.txt`): criterio de la venta fiada, sueldo del dueño como gasto, Anexo 3 del Decreto 2420 de 2015, cifra ponderada de EMICRON.
- 3 fichas 1080 × 1920 para el celular (Llévatelo), en Canva.
- Número de WhatsApp de la Cámara y portada del siguiente curso (igual que en los cursos anteriores).
- Tramo del Pase (U4 a U7): balance general, flujo de efectivo, presentar los números al banco o al contador, 3 indicadores.

## Subidas a Moodle

- 2026-10-20 22:20 UTC · nuevo en Moodle: https://portal.edunest.co/course/view.php?id=14 · 26/26 actividades en su sección
- 2026-10-20 22:24 UTC · reemplazo (mismo curso, recién creado y sin estudiantes) para incluir las dos hojas de ejemplo de U2 y U3 · 26/26 actividades, 46 archivos con HTTP 200
