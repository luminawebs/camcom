# Aula Virtual Empresarial Soacha · copia local del proyecto

Esta carpeta es un espejo del proyecto «CÁMARA DE COMERCIO» en Claude. Claude copia aquí lo que produce al terminar cada trabajo.

| Carpeta | Qué tiene |
| --- | --- |
| `artefactos/` | Manual de producción y catálogo (copias de las páginas publicadas) |
| `plantillas/` | Moldes HTML5, fragmentos para Moodle, `armar_curso.py` y `empaquetar.py` |
| `cursos/<id>/` | Un curso por carpeta: `curso.json`, piezas, páginas, vista previa, SCORM y kit de NotebookLM |
| `presentaciones/` | Presentaciones para la Cámara (HTML que se abre en el navegador; flechas para avanzar) |

La copia va en un solo sentido (proyecto → esta carpeta). Si cambias algo aquí, avísale a Claude en el proyecto para que lo recoja; si no, la próxima copia lo puede sobrescribir.

Para volver a armar un curso en tu equipo (requiere Python 3), desde esta carpeta:

```
python plantillas/armar_curso.py cursos/plata-negocio --scorm
```
