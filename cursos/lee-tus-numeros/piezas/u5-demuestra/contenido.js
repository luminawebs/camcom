/* Lee tus números · Unidad 5 · Demuestra (cuenta para el certificado)
   Molde: componentes/leccion-interactiva usado como cuestionario: nota = aciertos ÷ preguntas.
   La posición de la respuesta correcta cambia de pregunta a pregunta. */
window.CONTENIDO = {
  "titulo": "Tu flujo de efectivo",
  "paso": "Demuestra",
  "unidad": "Unidad 5",
  "notaMinima": 75,
  "pantallas": [
    {
      "titulo": "¿Lo lograste?",
      "texto": "Cuatro preguntas sobre la Unidad 5. Necesitas 3 de 4 bien para aprobar este paso, que cuenta para tu certificado. Si no lo logras, repásalo y vuelve a intentarlo."
    },
    {
      "titulo": "Pregunta 1 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Saldo al empezar $400.000, entradas $3.000.000, salidas $3.100.000. ¿Saldo al terminar?",
        "opciones": [
          "$300.000",
          "$500.000",
          "−$100.000"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: $400.000 + $3.000.000 − $3.100.000 = $300.000.",
          "mal": "$400.000 + $3.000.000 − $3.100.000 = $300.000."
        }
      }
    },
    {
      "titulo": "Pregunta 2 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Fiaste $250.000 este mes. ¿Entran al flujo de este mes?",
        "opciones": [
          "Sí, el día que fiaste",
          "No, entran cuando te paguen",
          "Solo la mitad"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: El flujo cuenta la plata que de verdad entra: el fiado entra cuando te pagan.",
          "mal": "El flujo cuenta la plata que de verdad entra: el fiado entra cuando te pagan."
        }
      }
    },
    {
      "titulo": "Pregunta 3 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "¿Cuál de estos SÍ sale en el flujo de efectivo?",
        "opciones": [
          "Lo que te fiaron tus clientes",
          "La cuota del préstamo",
          "Las ventas fiadas"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: La cuota del préstamo saca plata del negocio.",
          "mal": "La cuota del préstamo saca plata del negocio."
        }
      }
    },
    {
      "titulo": "Pregunta 4 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "¿Para qué sirve hacer el flujo de las próximas 4 semanas?",
        "opciones": [
          "Para ver antes en qué semana te va a faltar plata",
          "Para pagar menos impuestos",
          "Para saber el patrimonio"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: Hacerlo hacia adelante te deja ver los huecos antes de que pasen.",
          "mal": "Hacerlo hacia adelante te deja ver los huecos antes de que pasen."
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
