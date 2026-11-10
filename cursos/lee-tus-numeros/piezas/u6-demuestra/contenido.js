/* Lee tus números · Unidad 6 · Demuestra (cuenta para el certificado)
   Molde: componentes/leccion-interactiva usado como cuestionario: nota = aciertos ÷ preguntas.
   La posición de la respuesta correcta cambia de pregunta a pregunta. */
window.CONTENIDO = {
  "titulo": "Presenta tus números",
  "paso": "Demuestra",
  "unidad": "Unidad 6",
  "notaMinima": 75,
  "pantallas": [
    {
      "titulo": "¿Lo lograste?",
      "texto": "Cuatro preguntas sobre la Unidad 6. Necesitas 3 de 4 bien para aprobar este paso, que cuenta para tu certificado. Si no lo logras, repásalo y vuelve a intentarlo."
    },
    {
      "titulo": "Pregunta 1 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Cuota nueva de $300.000 y te sobran $1.000.000 al mes. ¿Peso de la cuota?",
        "opciones": [
          "33 %",
          "30 %",
          "70 %"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: $300.000 ÷ $1.000.000 × 100 = 30 %.",
          "mal": "$300.000 ÷ $1.000.000 × 100 = 30 %."
        }
      }
    },
    {
      "titulo": "Pregunta 2 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "¿De dónde sale «cada mes me sobran $900.000 para una cuota»?",
        "opciones": [
          "Del balance general",
          "De las ventas",
          "Del flujo de efectivo"
        ],
        "correcta": 2,
        "retro": {
          "bien": "Correcto: Es lo que entra menos lo que sale cada mes, sin la cuota nueva.",
          "mal": "Es lo que entra menos lo que sale cada mes, sin la cuota nueva."
        }
      }
    },
    {
      "titulo": "Pregunta 3 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Antes de firmar un crédito, ¿qué debes preguntar además de la cuota?",
        "opciones": [
          "La tasa efectiva anual y el total que vas a pagar",
          "Solo el plazo",
          "El color del formulario"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: La cuota sola no dice cuánto te cuesta el préstamo: pide la tasa efectiva anual y el total.",
          "mal": "La cuota sola no dice cuánto te cuesta el préstamo: pide la tasa efectiva anual y el total."
        }
      }
    },
    {
      "titulo": "Pregunta 4 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Si la cuota se lleva más de la mitad de lo que te sobra al mes…",
        "opciones": [
          "no hay problema",
          "un mes malo te puede dejar sin con qué pagar",
          "el banco te la baja solo"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: Mientras más bajo el peso de la cuota, más tranquilo.",
          "mal": "Mientras más bajo el peso de la cuota, más tranquilo."
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
