/* La plata del negocio no es la de la casa · Unidad 3 · Demuestra (cuenta para el certificado)
   Molde: componentes/leccion-interactiva usado como cuestionario: nota = aciertos ÷ preguntas. Solo con el Pase: en las unidades 1 a 3 este paso lo ve quien tiene el Pase.
   La posición de la respuesta correcta cambia de pregunta a pregunta. */
window.CONTENIDO = {
  "titulo": "Demuestra: Tu cuenta y tu registro",
  "paso": "Demuestra",
  "unidad": "Unidad 3",
  "notaMinima": 75,
  "pantallas": [
    {
      "titulo": "¿Lo lograste?",
      "texto": "Cuatro preguntas sobre la Unidad 3. Necesitas 3 de 4 bien para aprobar este paso, que cuenta para tu certificado. Si no lo logras, repásalo y vuelve a intentarlo."
    },
    {
      "titulo": "Pregunta 1 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Empezó el día con $500.000, vendió $420.000 y pagó $180.000. ¿Saldo al cerrar?",
        "opciones": [
          "$740.000",
          "$920.000",
          "$320.000"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: $500.000 + $420.000 − $180.000 = $740.000.",
          "mal": "$500.000 + $420.000 − $180.000 = $740.000."
        }
      }
    },
    {
      "titulo": "Pregunta 2 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Según las 3 reglas de la plata, ¿qué va a la casa?",
        "opciones": [
          "Lo que sobre del día",
          "Solo tu sueldo, en tu fecha fija",
          "Las ventas en efectivo"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: A la casa solo va tu sueldo, en tu fecha fija.",
          "mal": "A la casa solo va tu sueldo, en tu fecha fija."
        }
      }
    },
    {
      "titulo": "Pregunta 3 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "El efectivo que vendiste en el día, ¿dónde va?",
        "opciones": [
          "Al bolsillo, porque es efectivo",
          "No se anota",
          "A la cuenta del negocio y al registro"
        ],
        "correcta": 2,
        "retro": {
          "bien": "Correcto: Todo lo que vendes, también el efectivo, entra a la cuenta del negocio.",
          "mal": "Todo lo que vendes, también el efectivo, entra a la cuenta del negocio."
        }
      }
    },
    {
      "titulo": "Pregunta 4 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "El saldo del registro no cuadra con la cuenta y el cajón. ¿Qué quiere decir?",
        "opciones": [
          "Que algo se fue o entró sin anotar",
          "Que el negocio está perdiendo",
          "Que hay que cambiar de banco"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: Si no cuadra, algo se movió sin anotar.",
          "mal": "Si no cuadra, algo se movió sin anotar."
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
