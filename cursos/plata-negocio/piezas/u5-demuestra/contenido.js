/* La plata del negocio no es la de la casa · Unidad 5 · Demuestra (cuenta para el certificado)
   Molde: componentes/leccion-interactiva usado como cuestionario: nota = aciertos ÷ preguntas.
   La posición de la respuesta correcta cambia de pregunta a pregunta. */
window.CONTENIDO = {
  "titulo": "Tu libro del mes",
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
        "enunciado": "¿Para qué sirve la columna «Medio» del libro?",
        "opciones": [
          "Para anotar el nombre del cliente",
          "Para la categoría del gasto",
          "Para cuadrar el cajón y la cuenta por separado"
        ],
        "correcta": 2,
        "retro": {
          "bien": "Correcto: El medio (efectivo, transferencia, billetera) permite cuadrar cajón y cuenta por separado.",
          "mal": "El medio (efectivo, transferencia, billetera) permite cuadrar cajón y cuenta por separado."
        }
      }
    },
    {
      "titulo": "Pregunta 2 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Saldo anterior $650.000; la línea dice: Pago de luz del local, salió $95.000. ¿Saldo?",
        "opciones": [
          "$555.000",
          "$745.000",
          "$95.000"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: $650.000 − $95.000 = $555.000.",
          "mal": "$650.000 − $95.000 = $555.000."
        }
      }
    },
    {
      "titulo": "Pregunta 3 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Las líneas de gastos variables del mes son $40.000, $25.000, $18.000 y $37.000. ¿Total?",
        "opciones": [
          "$100.000",
          "$120.000",
          "$83.000"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: $40.000 + $25.000 + $18.000 + $37.000 = $120.000.",
          "mal": "$40.000 + $25.000 + $18.000 + $37.000 = $120.000."
        }
      }
    },
    {
      "titulo": "Pregunta 4 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Si hiciste 30 ventas en efectivo en el día, ¿cuántas líneas necesitas?",
        "opciones": [
          "Treinta, una por venta",
          "Ninguna: el efectivo no se anota",
          "Basta una: «Ventas del día en efectivo»"
        ],
        "correcta": 2,
        "retro": {
          "bien": "Correcto: Las ventas del día se pueden anotar en una línea por medio de pago.",
          "mal": "Las ventas del día se pueden anotar en una línea por medio de pago."
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
