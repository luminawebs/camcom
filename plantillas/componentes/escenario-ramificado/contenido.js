/* Escenario ramificado · paso PRACTICA (perfil R Relacional)
   Conversación tipo WhatsApp: el cliente escribe, el estudiante elige qué responder
   y ve cómo reacciona el cliente. Cada opción suma puntos (0 a 2) y lleva a otra escena.
   Una escena sin opciones es un final. */
window.CONTENIDO = {
  titulo: "[El cliente molesto]",
  paso: "Practica",
  unidad: "Unidad [n]",
  notaMinima: 60,
  cliente: "[Nombre del cliente]",
  inicio: "e1",
  escenas: {
    e1: {
      cliente: ["[Primer mensaje del cliente: la queja]"],
      opciones: [
        { texto: "[Respuesta empática y concreta]", puntos: 2, ir: "e2", nota: "[Por qué esta respuesta funciona]" },
        { texto: "[Respuesta defensiva]", puntos: 0, ir: "e3", nota: "[Qué provoca este tono]" },
        { texto: "[Respuesta correcta pero fría]", puntos: 1, ir: "e2", nota: "[Qué le falta]" }
      ]
    },
    e2: {
      cliente: ["[El cliente se calma y pide una solución]"],
      opciones: [
        { texto: "[Ofrece solución clara con fecha]", puntos: 2, ir: "f1", nota: "[Por qué funciona]" },
        { texto: "[Promete sin compromiso]", puntos: 0, ir: "f2", nota: "[Riesgo de esta respuesta]" }
      ]
    },
    e3: {
      cliente: ["[El cliente se molesta más]", "[Amenaza con dejar una mala reseña]"],
      opciones: [
        { texto: "[Pide disculpas y redirige]", puntos: 1, ir: "e2", nota: "[Cómo se recupera la conversación]" },
        { texto: "[Insiste en tener la razón]", puntos: 0, ir: "f2", nota: "[Consecuencia]" }
      ]
    },
    f1: { cliente: ["[Mensaje final positivo del cliente]"], final: "[Lo que lograste: cliente que vuelve]" },
    f2: { cliente: ["[Mensaje final negativo]"], final: "[Lo que pasó y qué respuesta habría cambiado el final]" }
  },
  final: { titulo: "Fin de la conversación" }
};
