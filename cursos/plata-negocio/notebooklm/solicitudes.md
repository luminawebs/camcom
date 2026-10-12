# Solicitudes para NotebookLM · La plata del negocio no es la de la casa

Cada bloque es una solicitud lista para copiar en el cuadro de personalización ("Personalizar" o "Customize") de la herramienta indicada en el panel Studio. Antes, el cuaderno debe tener cargadas todas las fuentes (ver LEEME.md).

Todo lo que salga de aquí lo revisa el contador antes de subirlo a Moodle.

---

## 1. Bienvenida del curso · Resumen en video

- **Herramienta:** Resumen en video · formato breve · idioma español.
- **Fuentes a marcar:** 00-ficha-del-curso, u1-guion, u2-guion, u3-guion.
- **Dónde va:** INICIO · Bienvenida (H5P · Video interactivo) y cabecera del curso.

```
Video de bienvenida de 60 segundos para dueños de pequeños negocios de Soacha, Colombia. Tutea, en español de Colombia, frases cortas. Empieza con Luz Dary, que vende todos los días en su miscelánea de León XIII pero a fin de mes no tiene para surtir. Presenta las tres unidades: por dónde se va la plata, págate un sueldo, y una cuenta y un registro para el negocio. Termina invitando a empezar. No uses cifras que no estén en las fuentes. Video vertical de unos 60 segundos. Todos los textos en pantalla en español.
```

---

## 2. Resumen de cada unidad · video O audio, solo uno

Cada unidad lleva **un solo resumen**: video de 60 s **o** audio de 5 min, nunca los dos. El formato está en `curso.json` (`resumen_formato`, o `resumen.formato` dentro de una unidad). **En este curso: video** (los tres resúmenes ya están hechos en video, con subtítulos). Usa solo el bloque 2A; el 2B queda por si una unidad pasa a audio.

### 2A. Si el resumen es en video (60 s)

- **Herramienta:** Resumen en video · formato breve · español · estilo pizarra o clásico. Usa el mismo estilo en las tres unidades.
- **Fuentes a marcar:** 00-ficha-del-curso y el guion de la unidad (solo ese).
- **Dónde va:** arriba de la sección de la unidad, «Resumen en video» (H5P).
- **Al revisar:** que ningún texto en pantalla salga en inglés y que diga las cifras del guion. Recorta el final si queda en silencio.

**Unidad 1**
```
Resumen de 60 segundos de la Unidad 1 "Por qué se mezcla la plata". Sigue el "Guion del resumen en video" de la fuente u1-guion, en ese orden: el caso de Luz Dary, las 4 fugas, venta no es ganancia (cuaderno de $5.000 que costó $3.500) y la fórmula de lo que se fue. Tutea, español de Colombia, sin regaños. Solo cifras de la fuente. Todos los textos en pantalla en español.
```

**Unidad 2**
```
Resumen de 60 segundos de la Unidad 2 "Págate un sueldo". Sigue el "Guion del resumen en video" de la fuente u2-guion: el caso de Luz Dary, sueldo fijo en fecha fija, ganancia del mes, promedio de 3 meses y colchón del 20 % (aclara que es una regla práctica del curso). Ejemplo: promedio $2.100.000, sueldo $1.680.000. Tutea, español de Colombia. Todos los textos en pantalla en español.
```

**Unidad 3**
```
Resumen de 60 segundos de la Unidad 3 "Una cuenta y un registro para el negocio". Sigue el "Guion del resumen en video" de la fuente u3-guion: el Nequi mezclado de Luz Dary, una cuenta solo para el negocio, las 3 reglas de la plata y el registro diario con la fórmula del saldo. No recomiendes bancos ni billeteras. No digas el valor en pesos del 4x1000. Di el ejemplo $400.000 + $350.000 − $120.000 = $630.000. Tutea, español de Colombia. Todos los textos en pantalla en español.
```

### 2B. Si el resumen es en audio (5 min)

- **Herramienta:** Resumen de audio · formato "Breve" (o "A fondo" si sale de menos de 4 min) · idioma español.
- **Fuentes a marcar:** 00-ficha-del-curso y el guion de la unidad.
- **Dónde va:** arriba de la sección de la unidad, «Resumen en audio» (Página con audio, MP3 mono 64 kbps).
- **Después:** descarga, pasa a MP3 y genera la transcripción (NotebookLM no la da; puedes pegar el audio en Descript o pedirla a Claude con el archivo). La transcripción va en la misma Página.

**Unidad 1**
```
Conversación de unos 5 minutos para dueños de pequeños negocios de Soacha. Sigue la estructura del "Guion de referencia del resumen en audio" de la fuente u1-guion: apertura, el caso de Luz Dary, las 4 fugas, venta no es ganancia, cómo medir la fuga ($550.000 en la semana) y el reto de anotar tres días. Español de Colombia, cálido y sencillo, sin tecnicismos. No inventes cifras ni recomiendes marcas.
```

**Unidad 2**
```
Conversación de unos 5 minutos. Una de las voces hace de Jhon Fredy, peluquero de Ciudad Verde que se paga un sueldo fijo. Sigue el "Guion de referencia del resumen en audio" de la fuente u2-guion. Explica el cálculo completo hasta $1.680.000 y aclara que el colchón del 20 % es una regla práctica, no una ley. Español de Colombia, sencillo. No hables de salario mínimo ni de impuestos.
```

**Unidad 3**
```
Conversación de unos 5 minutos. Una de las voces hace de Marleny, del taller de confección en San Mateo. Sigue el "Guion de referencia del resumen en audio" de la fuente u3-guion: cuenta aparte, las 3 reglas, registro diario ($400.000 + $350.000 − $120.000 = $630.000) y el registro como puerta al crédito formal. No recomiendes bancos ni billeteras y no digas el valor en pesos del 4x1000. Español de Colombia.
```

---

## 3. Mapa mental · ya no se pide en NotebookLM

NotebookLM solo deja ver el mapa mental como enlace y no se puede descargar. Los mapas los arma Claude desde los guiones, con los colores de la marca: `mapas/mapa-curso.png` (INICIO) y `mapas/u1-mapa.png` a `u3-mapa.png` (Llévatelo). Para cambiarlos, edita `mapas/armar_mapas.py` y pide a Claude que los vuelva a generar. El número 3 se deja vacío para no cambiar la numeración de las demás solicitudes.

---

## 4. Guía de estudio · ya no se pide en NotebookLM

Las guías de estudio de cada unidad las arma Claude desde los guiones, con el logo de edunest y diagramación propia: `guias-pdf/u1-guia.pdf` a `u3-guia.pdf` (A5, 2 páginas, van en Llévatelo). Para cambiarlas, edita `guias-pdf/armar_guias.py` y pide a Claude que las vuelva a generar. El número 4 se deja vacío para no cambiar la numeración de las demás solicitudes.

---

## 5. Borrador de la ficha de Llévatelo · Infografía

- **Herramienta:** Infografía · orientación vertical.
- **Fuentes a marcar:** el guion de la unidad.
- **Uso:** solo como borrador. La ficha final se arma en Canva con la plantilla de la marca (blanco, rojo #c8102e, negro y grises), porque la infografía trae marca de agua y el texto puede salir con errores.

```
Infografía vertical para guardar en el celular con lo que hay que recordar de la Unidad [n]: [las 4 fugas | tu sueldo en 3 pasos | las 3 reglas de la plata] y la fórmula de la unidad. Pocas palabras, letra grande.
```

---

## 6. Cifras para revisar · Tabla de datos

- **Herramienta:** Tabla de datos (exportar a Google Sheets).
- **Fuentes a marcar:** todas las fuentes web de la bibliografía (DANE, Banca de las Oportunidades, Estatuto Tributario, Gerencie).
- **Uso interno:** se entrega al contador para validar cada cifra contra la fuente oficial. Lo validado pasa a `datos` del componente U3 Aprende.

```
Tabla con cada cifra o norma que aparece en las fuentes sobre micronegocios y el 4x1000: dato, valor, año, fuente, página o artículo. Incluye: porcentaje sin registros contables, porcentaje con RUT, porcentaje que acude al gota a gota, tope de la exención del GMF en UVT y el artículo que lo establece.
```

---

## Qué NO se genera con NotebookLM en este curso

- Las lecciones interactivas y las calculadoras (las hace Claude con las plantillas HTML5).
- El cuestionario: el gancho no tiene Demuestra. El diagnóstico de 3 preguntas ya está escrito en `curso.json`.
- Tarjetas didácticas: no se pueden incrustar en Moodle y el gancho no las necesita.
