# La plata del negocio no es la de la casa

Curso Gancho gratuito · Perfil K (Cálculo) · 3 unidades de 7 pasos con resumen en video (o audio, uno solo: `resumen_formato` en curso.json) · ≈ 1,5 h. Primer curso del catálogo.

| Archivo | Qué es |
| --- | --- |
| `curso.json` | **La ficha del curso**: caso, personas, objetivos, evidencia y los textos de Inicio, Entrada, Aplica, Llévatelo y Cierre. Se edita aquí. |
| `piezas/uN-aprende/contenido.js` | Lección interactiva de cada unidad (molde `leccion-interactiva`) |
| `piezas/uN-practica/contenido.js` | Calculadora de cada unidad (molde `calculadora`) |
| `investigacion.md` | Datos, fuentes y lo que falta validar |
| `mapas/` | Mapas mentales del curso y de cada unidad (PNG), armados por Claude desde los guiones. Fuente editable: `armar_mapas.py`; `node renderizar.mjs` los pasa a PNG |
| `guias-pdf/` | Guías de estudio de cada unidad (PDF A5 de 2 páginas, con el logo de edunest), armadas por Claude desde los guiones. Fuente editable: `armar_guias.py`; `node renderizar_pdf.mjs` las pasa a PDF |
| `notebooklm/` | Kit para NotebookLM: fuentes (ficha, guiones de las 3 unidades, bibliografía APA 7), solicitudes listas para copiar y paso a paso |
| `estructura.md` | Árbol del curso (se genera) |
| `paginas/*.html` | Fragmentos llenos para pegar en Moodle (se generan) |
| `vista-previa/` | Revisión en tamaño celular (se genera) |
| `scorm/*.zip` | Paquetes para subir a Moodle (se generan) |

Después de cambiar `curso.json` o un `contenido.js`, desde la carpeta del proyecto:

```
python3 plantillas/armar_curso.py cursos/plata-negocio --scorm
```

Los videos e infografías van en `medios/` con los nombres de `notebooklm/LEEME.md`; las imágenes de una pieza interactiva, en `piezas/<pieza>/medios/` con su `src`.
