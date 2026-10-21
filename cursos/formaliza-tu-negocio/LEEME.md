# Formaliza tu negocio paso a paso

Curso Gancho gratuito · Perfil N (Normativa y trámites) · 3 unidades de 7 pasos con resumen en video · ≈ 1,5 h. Segundo curso del catálogo y primero hecho de punta a punta con el pipeline (12 de octubre de 2026). En Moodle: AVS-G02.

| Archivo | Qué es |
| --- | --- |
| `curso.json` | La ficha del curso: caso, personas, objetivos, textos, rúbrica del reto y `narracion` (voz de Resemble). Se edita aquí. |
| `piezas/uN-aprende/` | Lección interactiva de cada unidad (`leccion-interactiva`), con `narracion: true` y sus audios en `medios/` |
| `piezas/uN-practica/` | Árbol de decisión de cada unidad (`arbol-decision`) |
| `investigacion.md` | Datos, normas, fuentes y lo que falta validar con el asesor de la Cámara |
| `narraciones.json` | Texto exacto de cada narración (para revisar) |
| `medios-moodle/` | Narraciones de las Entradas (Resemble). Aquí van también `bienvenida.mp4` y `uN-resumen.mp4` cuando estén |
| `mapas/`, `guias-pdf/`, `descargas/` | Mapas mentales (PNG), guías de estudio (PDF A5) y descargas de Llévatelo (lista del RUT, checklist), cada uno con su script |
| `notebooklm/` | Kit para los 4 videos que se hacen a mano en NotebookLM |
| `paginas/`, `vista-previa/`, `scorm/`, `estructura.md` | Se generan |

Para volver a armar todo, desde la carpeta del proyecto:

```
python3 plantillas/narrar.py cursos/formaliza-tu-negocio          # solo rehace los audios cuyo texto cambió (necesita RESEMBLE_API_KEY)
python3 plantillas/armar_curso.py cursos/formaliza-tu-negocio --scorm
python3 moodle/publicar_curso.py cursos/formaliza-tu-negocio --corto AVS-G02
```

Pendiente: los 4 videos de NotebookLM, las ilustraciones de las Entradas y de las lecciones y la revisión del asesor (lista de [VERIFICAR] en la vista previa).
