/* Árbol de decisión · paso PRACTICA (perfil N Normativa y trámites)
   "¿Qué me toca a mí?": preguntas que llevan al caso del estudiante.
   Cada nodo tiene una pregunta y opciones que van ("ir") a otro nodo o a un resultado.
   Las cifras van en "datos" y se citan con {{dato}} para actualizarlas cada año.
   Todo dato normativo se marca [VERIFICAR] hasta que el experto lo valide. */
window.CONTENIDO = {
  titulo: "[¿Te toca facturar electrónicamente?]",
  paso: "Practica",
  unidad: "Unidad [n]",
  inicio: "n1",
  datos: { tope: "[VERIFICAR tope en UVT]" },
  nodos: {
    n1: {
      pregunta: "[Primera pregunta de clasificación]",
      ayuda: "[Aclaración corta si la pregunta tiene un término técnico]",
      opciones: [{ texto: "[Sí]", ir: "n2" }, { texto: "[No]", ir: "r1" }]
    },
    n2: {
      pregunta: "[Segunda pregunta. Puede citar cifras: ¿superas {{tope}}?]",
      opciones: [{ texto: "[Opción A]", ir: "r2" }, { texto: "[Opción B]", ir: "n3" }]
    },
    n3: {
      pregunta: "[Tercera pregunta]",
      opciones: [{ texto: "[Opción A]", ir: "r2" }, { texto: "[Opción B]", ir: "r3" }, { texto: "[No sé]", ir: "r4" }]
    }
  },
  resultados: {
    r1: { titulo: "[Resultado 1: no estás obligado]", texto: "[Qué significa y qué hacer. Fuente: VERIFICAR]", tono: "ok" },
    r2: { titulo: "[Resultado 2: sí estás obligado]", texto: "[Qué te toca, desde cuándo y el primer paso.]", tono: "marca" },
    r3: { titulo: "[Resultado 3: caso especial]", texto: "[Explicación del caso especial.]", tono: "marca" },
    r4: { titulo: "[Necesitas confirmar un dato]", texto: "[Dónde consultarlo: RUT, contador, DIAN.]", tono: "error" }
  },
  final: { titulo: "Ya sabes qué te toca", texto: "[Llévalo al paso Aplica: marca en tu checklist qué cumples.]" }
};
