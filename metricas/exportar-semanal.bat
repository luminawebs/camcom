@echo off
rem Exporta las metricas de la semana anterior a la carpeta compartida del negocio.
rem Lo corre el Programador de tareas de Windows cada lunes (ver metricas\LEEME.md).
rem Las llaves (MOODLE_URL, MOODLE_TOKEN, PASE_METRICAS_TOKEN) van como variables de usuario de Windows, no aqui.
cd /d "%~dp0.."
git pull --quiet
python -m metricas.exportar --salida "D:\30 Cam de comercio de Soacha\negocio\datos" >> "D:\30 Cam de comercio de Soacha\negocio\datos\estado\exportar.log" 2>&1
