# Exportador semanal de métricas

`python -m metricas.exportar` junta las cifras de la semana anterior (lunes a domingo, hora Colombia) desde Moodle y desde el servidor del Pase, y las deja en la carpeta `negocio/datos/` que leen los proyectos de Investigación y Marketing. Solo exporta conteos y sumas: ningún nombre, correo ni documento.

## Qué escribe

| Archivo | Contenido |
|---|---|
| `metricas-AAAA-Wss.md` | Resumen legible de la semana: las 6 métricas, tabla por curso y por canal, y notas de lo que faltó |
| `metricas-semanales.csv` | Una fila por semana (si se vuelve a correr la misma semana, se reemplaza) |
| `metricas-cursos.csv` | Una fila por curso y semana |
| `estado/moodle-vistos.json` | Ids internos de Moodle ya vistos por curso, para contar matrículas nuevas |

Lee además `gasto-marketing.csv` (lo llena Marketing: `semana,canal,gasto_cop,nota`) para calcular el costo por suscriptor.

## Las 6 métricas

Definiciones completas en `negocio/metricas.md`.

1. **Matrículas nuevas por semana**: estudiantes que aparecen en un curso y no estaban en la exportación anterior. La primera corrida es la línea base. Si se salta una semana, la siguiente trae las dos juntas.
2. **% que termina la U3**: estudiantes que completaron todas las actividades con seguimiento de la Unidad 3 de al menos un curso, sobre el total de estudiantes (acumulado).
3. **Conversión U3 → Pase**: de quienes terminaron una U3, cuántos están en el grupo `pase-empresario` (acumulado).
4. **Pagos**: aprobados en la semana (Pases nuevos y renovaciones), rechazados, recaudo y 25 % de la Cámara.
5. **Cancelaciones**: pedidas y efectivas en la semana; tasa = efectivas ÷ (activos + efectivas).
6. **Costo por suscriptor**: gasto de marketing de la semana ÷ Pases nuevos, total y por canal.

## Lo que necesita para funcionar

| Fuente | Qué hace falta | Si falta |
|---|---|---|
| Moodle | `MOODLE_URL` y `MOODLE_TOKEN` (servicio Claude Aula). Para la métrica 2 y 3, agregar al servicio la función `core_completion_get_activities_completion_status` | Sin datos de Moodle, o sin U3 y conversión |
| Pase | Desplegar en pase.edunest.co la versión con `/metricas` y poner `PASE_METRICAS_TOKEN` (cadena larga al azar, `openssl rand -hex 32`) en `/etc/pase/pase.env` y en el equipo que exporta | Sin pagos ni cancelaciones |
| Marketing | `gasto-marketing.csv` en la carpeta de datos | Sin costo por suscriptor |

Cuentas de prueba que no deben contar: `METRICAS_EXCLUIR=201,205` (ids de Moodle separados por coma).

Mientras el Pase siga en modo prueba, el informe lo dice arriba: esos pagos no son ventas reales.

## Rutina semanal (equipo de David)

1. Clonar el repositorio en el equipo e instalar Python 3.
2. Poner como variables de usuario de Windows (Configuración › Sistema › Información › Configuración avanzada › Variables de entorno): `MOODLE_URL`, `MOODLE_TOKEN`, `PASE_METRICAS_TOKEN` y, si hace falta, `METRICAS_EXCLUIR`.
3. Programador de tareas › Crear tarea básica › Semanal, lunes 7:00 › Iniciar un programa: `metricas\exportar-semanal.bat`. En la pestaña Configuración marcar «Ejecutar la tarea lo antes posible si no se ejecutó a la hora programada».

Para probar a mano: `python -m metricas.exportar --semana 2026-W45 --salida "D:\30 Cam de comercio de Soacha\negocio\datos"`.

Pruebas: `python -m unittest metricas.pruebas`.
