/* Lección interactiva · paso APRENDE (perfiles K Cálculo y N Normativa)
   Ejemplo resuelto que el estudiante avanza a su ritmo.
   Reemplaza lo que está entre [ ]. Un medio con src vacío se muestra como espacio por llenar.
   {{dato}} toma el valor de "datos": las cifras normativas (UVT, plazos) se cambian
   aquí cada año sin rehacer la pieza. Marca [VERIFICAR] lo que deba revisar el experto. */
window.CONTENIDO = {
  titulo: "[Título de la lección]",
  paso: "Aprende",
  unidad: "Unidad [n]",
  notaMinima: 60,
  datos: { valorUVT: "[VERIFICAR valor UVT del año]", anio: "[año]" },
  pantallas: [
    {
      titulo: "[Pregunta que abre la lección · máx. 10 palabras]",
      texto: "[Texto corto de entrada: 40 a 60 palabras, tuteando, con el caso del negocio de Soacha que sigue todo el curso.]",
      medio: { tipo: "video", src: "", nota: "Video corto de 1 a 2 min o ilustración del caso. Con subtítulos." }
    },
    {
      titulo: "[Paso 1 del ejemplo resuelto]",
      texto: "[Explica una sola idea. Máx. 60 palabras.]\n\nEjemplo con cifra editable: el valor de la UVT en {{anio}} es **{{valorUVT}}**.",
      medio: { tipo: "imagen", src: "", nota: "Esquema o tabla del paso 1 (vertical, legible en celular)." }
    },
    {
      titulo: "[Paso 2 del ejemplo resuelto]",
      texto: "[Explica la segunda idea. Máx. 60 palabras.]",
      pregunta: {
        enunciado: "[Pregunta de comprobación sobre el paso 2]",
        opciones: ["[Opción correcta]", "[Distractor 1: error común]", "[Distractor 2: error común]"],
        correcta: 0,
        retro: {
          bien: "[Por qué es correcta, en una frase]",
          mal: "[Qué se confundió y cuál es la idea correcta]"
        }
      }
    },
    {
      titulo: "[Paso 3 del ejemplo resuelto]",
      texto: "[Cierra el ejemplo con el resultado final del caso.]",
      medio: { tipo: "imagen", src: "", nota: "Resultado del caso: fórmula o resumen visual." }
    },
    {
      titulo: "[Lo que debes recordar]",
      texto: "[Resumen en 3 frases cortas. Esto se repite en el paso Llévatelo.]"
    }
  ],
  final: { titulo: "Lección terminada", texto: "[Frase que invita al siguiente paso: Practica.]" }
};
