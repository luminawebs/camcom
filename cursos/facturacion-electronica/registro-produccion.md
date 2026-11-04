# Registro de producción · Facturación electrónica sin miedo (AVS-G03)

Curso 3 del Aula Virtual Empresarial Soacha. Gancho gratuito (unidades 1 a 3 del curso; las 4 a 7 van con el Pase), perfil N, ≈ 1,5 horas. Pedido de David el 14 de octubre de 2026 y producido ese mismo día.
Respaldo: `moodle/facturacion-electronica/respaldo-avs-g03-facturacion-electronica.mbz` (≈ 8 MB, 26 actividades, 5 secciones). En Moodle como curso 12 (AVS-G03), creado con `moodle/subir_moodle.py`.

## Qué se hizo y con qué comando

| Paso | Qué produce | Comando | API |
| --- | --- | --- | --- |
| 1 | `investigacion.md` y `curso.json` (caso, personas, objetivos, textos) | a mano, con Claude | búsqueda web |
| 2 | `piezas/uN-aprende` y `uN-practica` (`contenido.js`) | a mano, con Claude | — |
| 3 | Mapas mentales (`mapas/*.png`) | `python3 mapas/armar_mapas.py` + `node mapas/renderizar.mjs` | — |
| 3 | Guías de estudio A5 (`guias-pdf/*.pdf`) | `python3 guias-pdf/armar_guias.py` + `node guias-pdf/renderizar_pdf.mjs` | — |
| 3 | Descargas (lista para habilitarte, chequeo de la factura) | `python3 descargas/armar_descargas.py` + `node guias-pdf/renderizar_pdf.mjs descargas` | — |
| 4 | 21 narraciones (3 Entradas + 18 pantallas de Aprende), 6,5 min | `python3 plantillas/narrar.py cursos/facturacion-electronica` | Resemble |
| 4b | 3 personajes + 8 ilustraciones | `python3 plantillas/ilustrar.py cursos/facturacion-electronica` | Gemini (en un hilo aparte, sin el equipo conectado) |
| 4c | 3 videos de Entrada (25 a 28 s) | `python3 plantillas/video_entrada.py cursos/facturacion-electronica` | — |
| 4d | 3 resúmenes (30 a 35 s) y bienvenida (46 s) | `python3 plantillas/video_resumen.py cursos/facturacion-electronica u1-resumen` (y `u2-resumen`, `u3-resumen`, `bienvenida`) | Resemble |
| 5 | Páginas, vista previa y 6 SCORM | `python3 plantillas/armar_curso.py cursos/facturacion-electronica --scorm` | — |
| 6 | Respaldo .mbz con todos los medios | `python3 moodle/publicar_curso.py cursos/facturacion-electronica --corto AVS-G03` | — |
| 6b | Curso nuevo en Moodle (curso 12) | `python3 moodle/subir_moodle.py cursos/facturacion-electronica` | Moodle |

## Gasto en APIs

| Servicio | Uso | Costo |
| --- | --- | --- |
| Resemble AI (voz Jota) | Narraciones 6,5 min · resúmenes ≈ 1,6 min · bienvenida 0,8 min | ≈ 8 min de audio. El precio depende del plan (Billing en Resemble). |
| Gemini 2.5 Flash Image | 18 imágenes (11 usadas y 7 rehechas: la prueba inicial, Gloria se veía joven, Andrés salió con otras personas y letreros, la factura salió con palabras en inglés) | ≈ USD 0,70. Detalle en `ilustraciones/registro.json`. |

## Ilustraciones desde otro hilo

La sesión que produjo el curso estaba conectada al computador de David, y con esa conexión el entorno solo deja enviar datos a los dominios de su lista; Gemini respondió «request blocked». Las ilustraciones se hicieron en el hilo «Ilustraciones curso 3», sin el equipo conectado. David no ha rotado la clave de Gemini después del aviso de Google del 13 de octubre y autorizó usarla igual (14 de octubre).

## Pendiente en este curso

**Medios**
- Captura real del registro como facturador en el portal de la DIAN (Unidad 2, Aprende, pantalla 3). No se hace con IA para no inventar la página.
- ~~3 fichas 1080 × 1920 para el celular (Llévatelo), en Canva.~~ Hechas el 2026-10-20 con `python3 plantillas/fichas.py cursos/facturacion-electronica` (fichas/uN-ficha.jpg).

**Validación con el contador de la Cámara** (marcas [VERIFICAR]; `publicar_curso.py` las quita del respaldo pero el texto queda sin validar; lista en `moodle/facturacion-electronica/quitado-al-publicar.txt`)
- Quién debe facturar y las condiciones de los no obligados (Resolución 000165 de 2023, art. 7; Decreto 1625 de 2016, art. 1.6.1.4.3).
- Nombre actual del servicio gratuito, pasos de habilitación y vigencia del certificado de firma.
- Lista de requisitos de la factura, nota crédito, aceptación tácita y contingencia.
- Número de WhatsApp de la Cámara.

## Subidas a Moodle

Las agrega `moodle/subir_moodle.py`.
- 2026-10-14 · nuevo en Moodle: https://portal.edunest.co/course/view.php?id=12 · respaldo-avs-g03-facturacion-electronica.mbz · 26/26 actividades en su sección (sin ilustraciones ni videos de Entrada)
- 2026-10-14 21:55 UTC · reemplazo en Moodle: https://portal.edunest.co/course/view.php?id=12 · respaldo-avs-g03-facturacion-electronica.mbz · 26/26 actividades en su sección
- 2026-10-21 02:42 UTC · reemplazo en Moodle: https://portal.edunest.co/course/view.php?id=12 · respaldo-avs-g03-facturacion-electronica.mbz · 26/26 actividades en su sección
