# Vende más por WhatsApp Business

Curso Gancho gratuito (unidades 1 a 3 del curso; las unidades 4 a 7 van con el Pase Empresario) · Perfil P (Procedimiento en herramienta) · 3 unidades de 7 pasos con resumen en video · ≈ 1,5 h. Cuarto curso del catálogo (nivel 3 · Vende más), hecho con el pipeline completo el 14 de octubre de 2026. En Moodle: AVS-G04.

| Archivo | Qué es |
| --- | --- |
| `curso.json` | La ficha del curso: caso, personas, objetivos, textos, rúbrica del reto, `narracion` (voz de Resemble y `reemplazos` de lectura) y `receta` (Aprende como lección narrada en vez de screencast) |
| `piezas/uN-aprende/` | Lección interactiva de cada unidad (`leccion-interactiva`), con `narracion: true` y sus audios e ilustraciones en `medios/` |
| `piezas/uN-practica/` | Simulador de pantalla de cada unidad (`simulador-pantalla`). Su `contenido.js` lo escribe `pantallas/renderizar.mjs` |
| `pantallas/` | Pantallas simplificadas de WhatsApp Business (HTML): `python3 armar_pantallas.py && node renderizar.mjs` arma las 15 del simulador, mide la zona que se toca y hace las 5 vistas de las lecciones |
| `investigacion.md` | Rutas de menú, fuentes y lo que falta validar con el asesor de mercadeo digital de la Cámara |
| `ilustraciones.json` | Estilo, personajes (Sandra, Camilo, Esperanza) y escenas para `plantillas/ilustrar.py` |
| `video/*.json` | Guion de la bienvenida y de los resúmenes de unidad (`plantillas/video_resumen.py`) |
| `narraciones.json` | Texto exacto de cada narración (para revisar) |
| `medios-moodle/` | Narraciones, ilustraciones y videos de Entrada, resúmenes y bienvenida |
| `mapas/`, `guias-pdf/`, `descargas/` | Mapas mentales (PNG), guías de estudio (PDF A5) y descargas de Llévatelo, cada uno con su script |
| `paginas/`, `vista-previa/`, `scorm/`, `estructura.md` | Se generan |

El orden completo de los pasos está en `plantillas/LEEME.md` y el registro de lo hecho en `registro-produccion.md`.
