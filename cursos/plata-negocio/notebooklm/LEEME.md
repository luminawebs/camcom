# Kit para NotebookLM · La plata del negocio no es la de la casa

Todo lo que hay que cargar y pedir en NotebookLM para producir los resúmenes de este curso, según la sección NotebookLM del manual de producción. Cada unidad lleva un solo resumen, en video o en audio; en este curso es **video**. Los mapas mentales y las guías de estudio no salen de NotebookLM: los arma Claude en `mapas/` y `guias-pdf/`.

## 1. Crear el cuaderno

Nombre: **Aula Soacha · La plata del negocio**. Un cuaderno por curso.

## 2. Cargar las fuentes (en este orden)

**Archivos de este kit** (Agregar fuente → Subir; si no acepta .md, abre el archivo, copia todo y usa "Texto copiado"):

| Archivo | Qué es |
| --- | --- |
| `fuentes/00-ficha-del-curso.md` | Público, tono, caso hilo y reglas. Va marcada en todas las solicitudes. |
| `fuentes/u1-guion.md` | Guion completo de la Unidad 1 + guiones de sus resúmenes |
| `fuentes/u2-guion.md` | Ídem Unidad 2 |
| `fuentes/u3-guion.md` | Ídem Unidad 3 |
| `fuentes/bibliografia.md` | Referencias APA 7 del curso |

**Fuentes web** (Agregar fuente → Sitio web, una por una; los PDF se pueden subir descargados si el enlace falla):

1. https://www.dane.gov.co/files/operaciones/EMICRON/bol-EMICRON-2024.pdf
2. https://bancadelasoportunidades.gov.co/sites/default/files/2021-03/Reporte%20micronegocios%20final.pdf
3. https://www.portafolio.co/negocios/empresas/microempresas-mas-de-la-mitad-carece-de-registros-financieros-formales-643178
4. http://www.secretariasenado.gov.co/senado/basedoc/codigo_comercio.html
5. http://www.secretariasenado.gov.co/senado/basedoc/estatuto_tributario_pr035.html
6. https://www.gerencie.com/exencion-gmf.html
7. https://www.banrep.gov.co/es/bre-b/preguntas-frecuentes/que-es-la-llave-en-bre-b-y-para-que-se-necesita
8. https://www.siigo.com/blog/empresario/7-tips-para-separar-tu-dinero-del-de-tu-negocio/

Son 13 fuentes en total. Carga las mismas en el Proyecto de Claude si vas a pedirle cambios al curso, así los dos trabajan con lo mismo.

## 3. Generar

Abre `solicitudes.md` y sigue los bloques en orden. Para cada uno: marca solo las fuentes que indica, pega la solicitud en el cuadro de personalización y genera.

| # | Salida | Cantidad | Va en Moodle |
| --- | --- | --- | --- |
| 1 | Video de bienvenida | 1 | INICIO · Bienvenida |
| 2A | Resumen en video, 60 s (el 2B, audio, solo si una unidad cambia de formato) | 3 | Arriba de cada unidad |
| — | Mapas mentales: los arma Claude en `mapas/`, no NotebookLM | 1 + 3 | INICIO y Llévatelo |
| — | Guías de estudio en PDF: las arma Claude en `guias-pdf/`, no NotebookLM | 3 | Llévatelo (PDF) |
| 5 | Infografía (borrador) | 3 | Base para la ficha de Canva |
| 6 | Tabla de datos | 1 | Uso interno, para el contador |

## 4. Revisar antes de subir

1. Escucha y mira cada resumen completo. NotebookLM escribe su propio diálogo y puede cambiar cifras: compáralas con el guion.
2. El contador revisa todo con la lista de [VERIFICAR] de la vista previa del curso.
3. Video (bienvenida y resúmenes): vertical, MP4 liviano (≈ 2–3 MB por resumen), con subtítulos, sin textos en inglés y sin silencio al final. Audio (solo si una unidad cambia a audio): MP3 mono 64 kbps, con transcripción.
4. Aviso visible en cada resumen: "Resumen generado con inteligencia artificial y revisado por un contador público" (enfoque legal del manual).
5. Antes de vender cursos con estos audios y videos, confirma la política de Google sobre uso comercial (pendiente en el manual).

## 5. Guardar

Pon los archivos finales en `cursos/plata-negocio/medios/` con estos nombres, para tenerlos ordenados al montar en Moodle:

```
bienvenida.mp4
u1-resumen.mp4   u1-infografia.png
u2-resumen.mp4   u2-infografia.png
u3-resumen.mp4   u3-infografia.png
```

Los mapas (`mapa-curso.png`, `uN-mapa.png`) y las guías (`uN-guia.pdf`) no van en `medios/`: están en `mapas/` y `guias-pdf/`. Si una unidad pasa a audio, su resumen se guarda como `uN-resumen.mp3` con su transcripción `uN-resumen.txt`.
