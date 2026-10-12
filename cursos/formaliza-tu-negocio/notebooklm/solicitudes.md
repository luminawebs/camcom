# Solicitudes para NotebookLM · Formaliza tu negocio paso a paso

Cada bloque es una solicitud lista para copiar en el cuadro de personalización ("Personalizar") de la herramienta indicada en el panel Studio. Antes, el cuaderno debe tener cargadas todas las fuentes (ver LEEME.md).

En este curso NotebookLM hace **solo los videos**: la bienvenida y los tres resúmenes de unidad. Las narraciones de las Entradas y de las lecciones Aprende las genera Claude con Resemble AI (voz Jota), los mapas y las guías también los arma Claude.

Todo lo que salga de aquí lo revisa el asesor de formalización de la Cámara antes de subirlo a Moodle.

---

## 1. Bienvenida del curso · Resumen en video

- **Herramienta:** Resumen en video · formato breve · idioma español.
- **Fuentes a marcar:** 00-ficha-del-curso, u1-guion, u2-guion, u3-guion.
- **Dónde va:** INICIO · Bienvenida y portada del curso. Guárdalo como `medios-moodle/bienvenida.mp4`.

```
Video de bienvenida de 60 segundos para dueños de pequeños negocios de Soacha, Colombia. Tutea, en español de Colombia, frases cortas, sin asustar. Empieza con Édgar, que tiene una tienda en Compartir hace ocho años y no puede comprar a crédito porque no tiene RUT ni matrícula mercantil, y cree que formalizarse es pagar más impuestos. Presenta las tres unidades: qué es estar formal y qué ganas, el RUT gratis desde el celular, y la matrícula mercantil y el local en regla. Termina invitando a empezar. No digas tarifas ni cifras que no estén en las fuentes. Video vertical de unos 60 segundos. Todos los textos en pantalla en español.
```

---

## 2. Resumen de cada unidad · video (60 s)

- **Herramienta:** Resumen en video · formato breve · español · el mismo estilo en las tres unidades.
- **Fuentes a marcar:** 00-ficha-del-curso y el guion de la unidad (solo ese).
- **Dónde va:** arriba de cada unidad, «Resumen en video». Guárdalos como `medios-moodle/u1-resumen.mp4`, `u2-resumen.mp4`, `u3-resumen.mp4`.
- **Al revisar:** que ningún texto en pantalla salga en inglés, que no diga tarifas ni que el RUT cobra impuestos, y recorta el silencio del final.

**Unidad 1**
```
Resumen de 60 segundos de la Unidad 1 "Formal no es pagar más: es poder crecer". Sigue el "Guion del resumen en video" de la fuente u1-guion, en ese orden: el caso de Édgar y el distribuidor, los 3 pasos (RUT en la DIAN, matrícula mercantil en la Cámara de Comercio, local en regla), el RUT no es un impuesto y lo que se gana al estar formal. Tutea, español de Colombia, sin regaños. Solo datos de la fuente. Todos los textos en pantalla en español.
```

**Unidad 2**
```
Resumen de 60 segundos de la Unidad 2 "El RUT, gratis y desde el celular". Sigue el "Guion del resumen en video" de la fuente u2-guion: el caso de Yuli, el RUT es gratis y en línea, lo que necesitas (cédula, selfie, correo, dirección, código CIIU), el paso a paso en la página de la DIAN, el NIT y que el RUT no vence. No menciones tramitadores ni cobros. Tutea, español de Colombia. Todos los textos en pantalla en español.
```

**Unidad 3**
```
Resumen de 60 segundos de la Unidad 3 "Matrícula mercantil y tu local en regla". Sigue el "Guion del resumen en video" de la fuente u3-guion: el caso de Wilson y la visita de la Policía, la matrícula mercantil y su renovación del 1 de enero al 31 de marzo, los requisitos del local (uso de suelo, matrícula al día, aviso de apertura a la Policía, condiciones sanitarias y derechos de autor por la música). No digas tarifas. Tutea, español de Colombia. Todos los textos en pantalla en español.
```

---

## 3 y 4. Mapas mentales y guías de estudio · no se piden en NotebookLM

Los arma Claude: `mapas/` (PNG) y `guias-pdf/` (PDF A5). Los números se dejan vacíos para mantener la numeración del manual.

---

## 5. Borrador de la ficha de Llévatelo · Infografía

- **Herramienta:** Infografía · vertical. **Fuentes:** el guion de la unidad.
- **Uso:** solo borrador; la ficha final se arma en Canva con la plantilla de la marca.

```
Infografía vertical para guardar en el celular con lo que hay que recordar de la Unidad [n]: [la ruta RUT, matrícula y local | el RUT en 6 pasos | el calendario de la matrícula y los requisitos del local]. Pocas palabras, letra grande, en español.
```

---

## 6. Normas y fechas para revisar · Tabla de datos

- **Herramienta:** Tabla de datos (exportar a Google Sheets). **Fuentes:** todas las fuentes web.
- **Uso interno:** se entrega al asesor de la Cámara para validar cada dato contra la fuente oficial.

```
Tabla con cada norma, fecha o cifra que aparece en las fuentes sobre RUT, matrícula mercantil y requisitos de establecimientos: dato, valor, año, fuente, artículo o página. Incluye: plazo de renovación de la matrícula, cancelación por no renovar, requisitos del artículo 87 de la Ley 1801 de 2016, decreto de creación de la Cámara de Comercio de Soacha, valor de la UVT 2026 y porcentaje de micronegocios con RUT.
```

---

## Qué NO se genera con NotebookLM en este curso

- Las narraciones (Resemble AI, `plantillas/narrar.py`).
- Las lecciones y los árboles de decisión (plantillas HTML5).
- Los mapas, las guías y las descargas en PDF (los arma Claude).
