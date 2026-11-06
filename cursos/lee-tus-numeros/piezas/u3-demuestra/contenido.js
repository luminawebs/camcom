/* Lee tus números · Unidad 3 · Demuestra (cuenta para el certificado)
   Molde: componentes/leccion-interactiva usado como cuestionario: nota = aciertos ÷ preguntas.
   La posición de la respuesta correcta cambia de pregunta a pregunta. */
window.CONTENIDO = {
  "titulo": "Tu estado de resultados",
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
        "enunciado": "Ventas $5.000.000 y costo de lo vendido $2.000.000. ¿Utilidad bruta?",
        "opciones": [
          "$3.000.000",
          "$7.000.000",
          "$2.000.000"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: Utilidad bruta = $5.000.000 − $2.000.000 = $3.000.000.",
          "mal": "Utilidad bruta = $5.000.000 − $2.000.000 = $3.000.000."
        }
      }
    },
    {
      "titulo": "Pregunta 2 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Utilidad bruta $3.000.000 y gastos $2.400.000 (con el sueldo de la dueña). ¿Utilidad del mes?",
        "opciones": [
          "$5.400.000",
          "$600.000",
          "$2.400.000"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: $3.000.000 − $2.400.000 = $600.000.",
          "mal": "$3.000.000 − $2.400.000 = $600.000."
        }
      }
    },
    {
      "titulo": "Pregunta 3 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Con utilidad de $600.000 y ventas de $5.000.000, ¿cuál es el margen?",
        "opciones": [
          "60 %",
          "8 %",
          "12 %"
        ],
        "correcta": 2,
        "retro": {
          "bien": "Correcto: $600.000 ÷ $5.000.000 × 100 = 12 %.",
          "mal": "$600.000 ÷ $5.000.000 × 100 = 12 %."
        }
      }
    },
    {
      "titulo": "Pregunta 4 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Si no incluyes tu sueldo en los gastos…",
        "opciones": [
          "la utilidad se ve mayor de lo que es",
          "la utilidad no cambia",
          "el margen baja"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: Sin tu sueldo, la utilidad parece mayor, pero incluye el pago de tu trabajo.",
          "mal": "Sin tu sueldo, la utilidad parece mayor, pero incluye el pago de tu trabajo."
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
