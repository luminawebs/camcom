#!/usr/bin/env python3
"""Arma moodle/aula-en-head.html (Appearance > Additional HTML > Within HEAD): aula.css + portada.css + portada.js, minificado y sin BOM."""
import os, subprocess, tempfile
aqui = os.path.dirname(os.path.abspath(__file__))
raiz = os.path.dirname(aqui)
css = open(os.path.join(raiz, "plantillas/comun/aula.css"), encoding="utf-8").read() + "\n" + open(os.path.join(aqui, "portada.css"), encoding="utf-8").read()
with tempfile.NamedTemporaryFile("w", suffix=".scss", delete=False, encoding="utf-8") as f:
    f.write(css)
mini = subprocess.run(["npx", "--yes", "sass@1.77.8", "--no-source-map", "--style=compressed", f.name], capture_output=True, text=True, check=True).stdout
mini = mini.replace("﻿", "").replace("@charset \"UTF-8\";", "").strip()
js = " ".join(l.strip() for l in open(os.path.join(aqui, "portada.js"), encoding="utf-8") if l.strip() and not l.strip().startswith("/*"))
salida = ("<style>\n/* Aula Virtual Empresarial Soacha: estilos (plantillas/comun/aula.css + moodle/portada.css) */\n" + mini +
          "\n</style>\n<script>\n/* Aula Virtual Empresarial Soacha: portada del curso (moodle/portada.js) */\n" + js + "\n</script>\n")
open(os.path.join(aqui, "aula-en-head.html"), "w", encoding="utf-8").write(salida)
print("aula-en-head.html", len(salida.encode()), "bytes")
