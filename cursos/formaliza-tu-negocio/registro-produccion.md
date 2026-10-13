# Registro de producción · Formaliza tu negocio paso a paso (AVS-G02)

Curso 2 del Aula Virtual Empresarial Soacha. Gancho, perfil N, 3 unidades, ≈ 1,5 horas.
Producido el 12 y 13 de octubre de 2026. Respaldo: `moodle/formaliza-tu-negocio/respaldo-avs-g02-formaliza-tu-negocio.mbz` (≈ 13 MB, 26 actividades, 5 secciones). Todavía no está restaurado en Moodle.

## Qué se hizo y con qué comando

Orden en que se corre el pipeline (detalle de cada paso en `plantillas/LEEME.md`):

| Paso | Qué produce | Comando | API |
| --- | --- | --- | --- |
| 1 | `curso.json` (caso, personas, objetivos, textos de cada paso) | a mano, con Claude | — |
| 2 | `piezas/uN-aprende` y `uN-practica` (`contenido.js`) | a mano, con Claude | — |
| 3 | Mapas mentales (`mapas/*.png`) | `python3 mapas/armar_mapas.py` + `node mapas/renderizar.mjs` | — |
| 3 | Guías de estudio A5 (`guias-pdf/*.pdf`) | `python3 guias-pdf/armar_guias.py` + `node guias-pdf/renderizar_pdf.mjs` | — |
| 3 | Descargas (lista del RUT, checklist) | `python3 descargas/armar_descargas.py` | — |
| 4 | 19 narraciones (3 Entradas + 16 pantallas de Aprende) | `python3 plantillas/narrar.py cursos/formaliza-tu-negocio` | Resemble |
| 4b | 3 personajes + 7 ilustraciones | `python3 plantillas/ilustrar.py cursos/formaliza-tu-negocio` | Gemini |
| 4c | 3 videos de Entrada (25 a 28 s) | `python3 plantillas/video_entrada.py cursos/formaliza-tu-negocio` | — |
| 4d | Bienvenida (47 s) y 3 resúmenes (≈ 40 s) | `python3 plantillas/video_resumen.py cursos/formaliza-tu-negocio bienvenida` (y `u1-resumen`, `u2-resumen`, `u3-resumen`) | Resemble |
| 5 | Páginas, vista previa y 6 SCORM | `python3 plantillas/armar_curso.py cursos/formaliza-tu-negocio --scorm` | — |
| 6 | Respaldo .mbz con todos los medios | `python3 moodle/publicar_curso.py cursos/formaliza-tu-negocio --corto AVS-G02` | — |

## Gasto en APIs

| Servicio | Uso | Costo |
| --- | --- | --- |
| Gemini 2.5 Flash Image | 12 imágenes (10 usadas, 2 repetidas porque salieron mal) | ≈ USD 0,47, estimado con los tokens de la API y el precio de lista (USD 0,039 por imagen). Detalle por imagen en `ilustraciones/registro.json`. |
| Resemble AI (voz Jota) | Narraciones 6,1 min · resúmenes 2 min · bienvenida 0,8 min · pruebas ≈ 1 min | ≈ 10 min de audio. El precio depende del plan: ver Billing en la cuenta de Resemble. |
| Claude | — | Se ve en la configuración de uso de claude.ai. |

Los videos de Entrada no gastan nada: reutilizan la ilustración y la narración que ya existían.

## Aviso de seguridad (13 oct, 02:07)

Google suspendió el proyecto de Google Cloud «Salle» (gen-lang-client-0760543233) por credenciales filtradas; puede ser el de la clave de Gemini. Se revisó que la clave no aparece en ningún archivo del proyecto, del repositorio (incluido su historial) ni en la copia de D:. No se volvió a llamar a Gemini después del aviso. Antes de seguir usando `ilustrar.py` hay que rotar la clave y poner la nueva en la variable `GEMINI_API_KEY` del entorno.

## Pendiente en este curso

**Medios**
- 6 capturas reales del trámite del RUT en la DIAN (Unidad 2, Aprende, pantalla 4). No se hacen con IA para no inventar la página.
- 3 fichas 1080 × 1920 para el celular (Llévatelo de cada unidad), en Canva.
- Portada del siguiente curso (Cierre), cuando se defina cuál sigue.

**Validación con el asesor de la Cámara** (18 marcas [VERIFICAR]; `publicar_curso.py` las quita del respaldo pero el texto queda sin validar; lista en `moodle/formaliza-tu-negocio/quitado-al-publicar.txt`)
- Tarifa de la matrícula 2026 y dónde se hace hoy el trámite (Cámara de Soacha o sede de la Cámara de Bogotá).
- Dependencias de la Alcaldía de Soacha (uso de suelo, requisitos del local).
- Pasos actuales del RUT en la DIAN, código CIIU de ejemplo y tope de ingresos para no responsable de IVA.
- Número de WhatsApp de la Cámara, texto del formulario de datos y logo de la constancia.

**Moodle**
- Restaurar el .mbz como curso nuevo, poner el número de ID (AVS-G02-formaliza-tu-negocio) y revisar con REST que cada actividad quedó en su sección.

## Pendiente en el pipeline para los siguientes cursos

- Rotar la clave de Gemini (ver arriba) antes de ilustrar otro curso.
- `curso.json`, `contenido.js`, `ilustraciones.json` y `video/*.json` se escriben con Claude a partir de la investigación y los guiones; no hay un paso que los genere solo.
- Las fichas de Canva, las capturas de pantalla reales y la revisión del experto siguen siendo manuales.
- El curso 1 (La plata del negocio) usa los videos de NotebookLM que hizo David; el curso 2 es el primero con todos los videos automáticos.
