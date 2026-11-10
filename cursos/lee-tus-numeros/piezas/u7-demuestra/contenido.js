/* Lee tus números · Unidad 7 · Demuestra (cuenta para el certificado)
   Molde: componentes/leccion-interactiva usado como cuestionario: nota = aciertos ÷ preguntas.
   La posición de la respuesta correcta cambia de pregunta a pregunta. */
window.CONTENIDO = {
  "titulo": "3 indicadores",
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
        "enunciado": "Gastos fijos $2.000.000 y costo de lo vendido del 60 % de las ventas. ¿Punto de equilibrio?",
        "opciones": [
          "$3.333.333",
          "$5.000.000",
          "$1.200.000"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: $2.000.000 ÷ (1 − 0,6) = $2.000.000 ÷ 0,4 = $5.000.000.",
          "mal": "$2.000.000 ÷ (1 − 0,6) = $2.000.000 ÷ 0,4 = $5.000.000."
        }
      }
    },
    {
      "titulo": "Pregunta 2 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Plata disponible $1.500.000 y gastos fijos $1.000.000. ¿Colchón de caja?",
        "opciones": [
          "1,5 meses",
          "0,7 meses",
          "15 meses"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: $1.500.000 ÷ $1.000.000 = 1,5 meses.",
          "mal": "$1.500.000 ÷ $1.000.000 = 1,5 meses."
        }
      }
    },
    {
      "titulo": "Pregunta 3 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "El margen de tu negocio bajó de 10 % a 4 %. ¿Qué haces primero?",
        "opciones": [
          "Vender más sin mirar nada",
          "Revisar precios y costos",
          "Nada, es normal"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: Si el margen baja, revisa precios y costos antes de vender más.",
          "mal": "Si el margen baja, revisa precios y costos antes de vender más."
        }
      }
    },
    {
      "titulo": "Pregunta 4 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "¿Con qué comparas tus 3 indicadores cada mes?",
        "opciones": [
          "Con un número igual para todos los negocios",
          "Con el de tu vecino",
          "Con tus propios meses anteriores"
        ],
        "correcta": 2,
        "retro": {
          "bien": "Correcto: No hay un número bueno para todos: compárate contigo mismo.",
          "mal": "No hay un número bueno para todos: compárate contigo mismo."
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
