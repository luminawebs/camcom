/* Lee tus números · Unidad 4 · Demuestra (cuenta para el certificado)
   Molde: componentes/leccion-interactiva usado como cuestionario: nota = aciertos ÷ preguntas.
   La posición de la respuesta correcta cambia de pregunta a pregunta. */
window.CONTENIDO = {
  "titulo": "Tu balance general",
  "paso": "Demuestra",
  "unidad": "Unidad 4",
  "notaMinima": 75,
  "pantallas": [
    {
      "titulo": "¿Lo lograste?",
      "texto": "Cuatro preguntas sobre la Unidad 4. Necesitas 3 de 4 bien para aprobar este paso, que cuenta para tu certificado. Si no lo logras, repásalo y vuelve a intentarlo."
    },
    {
      "titulo": "Pregunta 1 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "¿Qué muestra el balance general?",
        "opciones": [
          "Lo que pasó en todo un mes",
          "Cómo está el negocio un día: lo que tiene, lo que debe y lo que es tuyo",
          "Solo las ventas"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: El balance es la foto de un día; el estado de resultados es la película del mes.",
          "mal": "El balance es la foto de un día; el estado de resultados es la película del mes."
        }
      }
    },
    {
      "titulo": "Pregunta 2 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Tiene $7.000.000 y debe $2.500.000. ¿Patrimonio?",
        "opciones": [
          "$9.500.000",
          "$2.500.000",
          "$4.500.000"
        ],
        "correcta": 2,
        "retro": {
          "bien": "Correcto: Patrimonio = $7.000.000 − $2.500.000 = $4.500.000.",
          "mal": "Patrimonio = $7.000.000 − $2.500.000 = $4.500.000."
        }
      }
    },
    {
      "titulo": "Pregunta 3 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Los fiados que te deben los clientes, ¿van en el balance?",
        "opciones": [
          "Sí, en lo que el negocio tiene",
          "No, porque no es plata",
          "Sí, en lo que debe"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: Son plata que vas a recibir: van en lo que el negocio tiene.",
          "mal": "Son plata que vas a recibir: van en lo que el negocio tiene."
        }
      }
    },
    {
      "titulo": "Pregunta 4 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "La tarjeta de crédito personal con la que pagas cosas de la casa, ¿va en el balance del negocio?",
        "opciones": [
          "Sí, como deuda",
          "No: es de la casa",
          "Sí, como patrimonio"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: El balance lleva solo lo del negocio.",
          "mal": "El balance lleva solo lo del negocio."
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
