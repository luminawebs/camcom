/* La plata del negocio no es la de la casa · Unidad 7 · Demuestra (cuenta para el certificado)
   Molde: componentes/leccion-interactiva usado como cuestionario: nota = aciertos ÷ preguntas.
   La posición de la respuesta correcta cambia de pregunta a pregunta. */
window.CONTENIDO = {
  "titulo": "Tu cierre del mes",
  "paso": "Demuestra",
  "unidad": "Unidad 7",
  "notaMinima": 75,
  "pantallas": [
    {
      "titulo": "¿Lo lograste?",
      "texto": "Cuatro preguntas sobre la Unidad 7. Necesitas 3 de 4 bien para aprobar este paso, que cuenta para tu certificado. Si no lo logras, repásalo y vuelve a intentarlo."
    },
    {
      "titulo": "Pregunta 1 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Libro $1.200.000; cuenta $850.000; cajón $300.000. ¿Diferencia?",
        "opciones": [
          "Sobran $50.000",
          "Faltan $50.000",
          "Cuadra exacto"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: $1.200.000 − ($850.000 + $300.000) = $50.000 positivos: faltan.",
          "mal": "$1.200.000 − ($850.000 + $300.000) = $50.000 positivos: faltan."
        }
      }
    },
    {
      "titulo": "Pregunta 2 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "¿Cuál es el orden de los 5 pasos del cierre?",
        "opciones": [
          "Decide, cuenta, suma, cuadra, calcula",
          "Suma, decide, cuadra, calcula, cuenta",
          "Cuadra, suma, cuenta, calcula, decide"
        ],
        "correcta": 2,
        "retro": {
          "bien": "Correcto: Cuadra, suma, cuenta, calcula y decide.",
          "mal": "Cuadra, suma, cuenta, calcula y decide."
        }
      }
    },
    {
      "titulo": "Pregunta 3 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "La diferencia del cierre es negativa. ¿Qué es lo más probable?",
        "opciones": [
          "Una venta o un pago de fiado sin anotar",
          "Un retiro para la casa sin anotar",
          "Que el negocio perdió plata"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: Si sobra plata, entró algo sin anotar.",
          "mal": "Si sobra plata, entró algo sin anotar."
        }
      }
    },
    {
      "titulo": "Pregunta 4 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "¿Cuántas acciones conviene escoger para el mes siguiente?",
        "opciones": [
          "Todas las que se te ocurran",
          "Una, concreta y medible",
          "Ninguna: solo revisar"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: Una sola acción por mes, concreta y medible.",
          "mal": "Una sola acción por mes, concreta y medible."
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
