# Kit para NotebookLM · Formaliza tu negocio paso a paso

En este curso NotebookLM produce **solo los 4 videos**: la bienvenida y el resumen de cada unidad (video de 60 s). Lo demás ya sale del pipeline:

| Medio | Quién lo hace | Dónde queda |
| --- | --- | --- |
| Video de bienvenida | Tú, en NotebookLM (solicitud 1) | `medios-moodle/bienvenida.mp4` |
| Resúmenes de unidad (3) | Tú, en NotebookLM (solicitud 2) | `medios-moodle/u1-resumen.mp4` … `u3-resumen.mp4` |
| Narración del caso de cada Entrada (3) | Claude, con Resemble AI (voz Jota) | `medios-moodle/uN-entrada-narracion.mp3` |
| Narración de cada pantalla de Aprende (16) | Claude, con Resemble AI (voz Jota) | `piezas/uN-aprende/medios/narracion-K.mp3` (dentro del SCORM) |
| Mapas mentales | Claude | `mapas/` |
| Guías de estudio PDF | Claude | `guias-pdf/` |
| Descargas (lista del RUT, checklist) | Claude | `descargas/` |

## 1. Crear el cuaderno

Nombre: **Aula Soacha · Formaliza tu negocio**.

## 2. Cargar las fuentes

**Archivos de este kit** (Agregar fuente → Subir; si no acepta .md, copia el texto y usa "Texto copiado"):

| Archivo | Qué es |
| --- | --- |
| `fuentes/00-ficha-del-curso.md` | Público, tono, caso hilo y reglas. Va marcada en todas las solicitudes. |
| `fuentes/u1-guion.md` | Guion de la Unidad 1 + guion del resumen en video |
| `fuentes/u2-guion.md` | Ídem Unidad 2 |
| `fuentes/u3-guion.md` | Ídem Unidad 3 |
| `fuentes/bibliografia.md` | Referencias APA 7 |

**Fuentes web** (Agregar fuente → Sitio web):

1. https://www.dane.gov.co/files/operaciones/EMICRON/bol-EMICRON-2024.pdf
2. https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=257376
3. https://leyes.co/codigo_nacional_de_seguridad_y_convivencia_ciudadana/87.htm
4. https://www.cronista.com/colombia/finanzas-y-economia/registro-unico-tributario-rut-2026-como-sacarlo-por-internet-paso-a-paso/
5. https://www.ambitojuridico.com/sites/default/files/2025-05/DOCUMENTO-Mincomercio-2025%28Porquerenovaroportunamentesumatriculamercantil%29.pdf

## 3. Generar

Abre `solicitudes.md` y sigue los bloques 1 y 2. Para cada uno: marca solo las fuentes que indica, pega la solicitud y genera.

## 4. Revisar y guardar

1. Mira cada video completo: NotebookLM escribe su propio texto y puede decir cosas que no están en el guion.
2. El asesor de la Cámara revisa con la lista de [VERIFICAR] de la vista previa.
3. MP4 vertical liviano (≈ 2–3 MB), con subtítulos, sin textos en inglés y sin silencio al final.
4. Guarda los 4 videos en `cursos/formaliza-tu-negocio/medios/` (o en la carpeta del curso en tu equipo) y avísale a Claude: los convierte, los pone en `medios-moodle/` y vuelve a armar el respaldo.
