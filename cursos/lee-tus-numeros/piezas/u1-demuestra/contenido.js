/* Lee tus números · Unidad 1 · Demuestra (cuenta para el certificado)
   Molde: componentes/leccion-interactiva usado como cuestionario: nota = aciertos ÷ preguntas.
   La posición de la respuesta correcta cambia de pregunta a pregunta. */
window.CONTENIDO = {
  "titulo": "Ingresos, costos y gastos",
  "paso": "Demuestra",
  "unidad": "Unidad 1",
  "notaMinima": 75,
  "pantallas": [
    {
      "titulo": "¿Lo lograste?",
      "texto": "Cuatro preguntas sobre la Unidad 1. Necesitas 3 de 4 bien para aprobar este paso, que cuenta para tu certificado. Si no lo logras, repásalo y vuelve a intentarlo."
    },
    {
      "titulo": "Pregunta 1 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Patricia recibió un préstamo de $4.000.000 de la cooperativa. ¿Qué es para el negocio?",
        "opciones": [
          "Un ingreso",
          "No es ingreso: es plata prestada que hay que devolver",
          "Un costo"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: Un préstamo no es venta: es plata que hay que devolver.",
          "mal": "Un préstamo no es venta: es plata que hay que devolver."
        }
      }
    },
    {
      "titulo": "Pregunta 2 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Patricia compra salchichas y pan para los perros calientes. ¿Qué es?",
        "opciones": [
          "Un gasto",
          "Un ingreso",
          "Un costo: es lo que necesita para hacer lo que vende"
        ],
        "correcta": 2,
        "retro": {
          "bien": "Correcto: Lo que necesitas para hacer lo que vendes es costo: sube y baja con las ventas.",
          "mal": "Lo que necesitas para hacer lo que vendes es costo: sube y baja con las ventas."
        }
      }
    },
    {
      "titulo": "Pregunta 3 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "El arriendo del local, que se paga vendas o no vendas, es…",
        "opciones": [
          "un gasto",
          "un costo",
          "un ingreso"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: Lo que pagas por tener el negocio abierto, vendas o no, es gasto.",
          "mal": "Lo que pagas por tener el negocio abierto, vendas o no, es gasto."
        }
      }
    },
    {
      "titulo": "Pregunta 4 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Patricia pagó el mercado de la casa desde el Nequi del negocio. ¿Dónde va?",
        "opciones": [
          "En los gastos",
          "No va: es de la casa",
          "En los costos"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: Lo de la casa no va en las cuentas del negocio.",
          "mal": "Lo de la casa no va en las cuentas del negocio."
        }
      }
    },
    {
      "titulo": "Listo",
      "texto": "Revisa tu nota. Si aprobaste, este paso queda completo para tu certificado."
    }
  ],
  "final": {
    "titulo": "Cuestionario terminado",
    "texto": "Si aprobaste, sigue con Llévatelo. Si no, repasa Aprende y vuelve a intentarlo."
  }
};
