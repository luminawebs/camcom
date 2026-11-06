/* La plata del negocio no es la de la casa · Unidad 6 · Demuestra (cuenta para el certificado)
   Molde: componentes/leccion-interactiva usado como cuestionario: nota = aciertos ÷ preguntas.
   La posición de la respuesta correcta cambia de pregunta a pregunta. */
window.CONTENIDO = {
  "titulo": "Demuestra: Tu utilidad real",
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
        "enunciado": "Inventario al empezar $800.000, compras $2.000.000, inventario al terminar $1.000.000. ¿Costo de lo vendido?",
        "opciones": [
          "$1.800.000",
          "$2.000.000",
          "$3.800.000"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: $800.000 + $2.000.000 − $1.000.000 = $1.800.000.",
          "mal": "$800.000 + $2.000.000 − $1.000.000 = $1.800.000."
        }
      }
    },
    {
      "titulo": "Pregunta 2 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Ventas $4.000.000; costo de lo vendido $1.800.000; fijos $700.000; variables $200.000; sueldo $1.000.000. ¿Utilidad real?",
        "opciones": [
          "$1.300.000",
          "$300.000",
          "$2.200.000"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: $4.000.000 − $1.800.000 − $700.000 − $200.000 − $1.000.000 = $300.000.",
          "mal": "$4.000.000 − $1.800.000 − $700.000 − $200.000 − $1.000.000 = $300.000."
        }
      }
    },
    {
      "titulo": "Pregunta 3 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Con utilidad de $300.000 y ventas de $4.000.000, ¿cuál es el margen?",
        "opciones": [
          "30 %",
          "13,3 %",
          "7,5 %"
        ],
        "correcta": 2,
        "retro": {
          "bien": "Correcto: $300.000 ÷ $4.000.000 × 100 = 7,5 %.",
          "mal": "$300.000 ÷ $4.000.000 × 100 = 7,5 %."
        }
      }
    },
    {
      "titulo": "Pregunta 4 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "¿Cuál de estos NO se resta para la utilidad real en este curso?",
        "opciones": [
          "La cuota del crédito de la máquina",
          "Tu sueldo",
          "Los gastos variables"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: La cuota es devolver un préstamo: va aparte de la utilidad.",
          "mal": "La cuota es devolver un préstamo: va aparte de la utilidad."
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
