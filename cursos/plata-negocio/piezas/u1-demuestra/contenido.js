/* La plata del negocio no es la de la casa · Unidad 1 · Demuestra (cuenta para el certificado)
   Molde: componentes/leccion-interactiva usado como cuestionario: nota = aciertos ÷ preguntas. Solo con el Pase: en las unidades 1 a 3 este paso lo ve quien tiene el Pase.
   La posición de la respuesta correcta cambia de pregunta a pregunta. */
window.CONTENIDO = {
  "titulo": "Demuestra: Las fugas de la plata",
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
        "enunciado": "Luz Dary empezó con $200.000 en el cajón, vendió $500.000, pagó $150.000 al proveedor y al cerrar tiene $380.000. ¿Cuánto se fue sin anotar?",
        "opciones": [
          "$350.000",
          "$170.000",
          "$120.000"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: $200.000 + $500.000 − $150.000 − $380.000 = $170.000.",
          "mal": "$200.000 + $500.000 − $150.000 − $380.000 = $170.000."
        }
      }
    },
    {
      "titulo": "Pregunta 2 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "¿Cuál de estas NO es una de las 4 fugas de la plata?",
        "opciones": [
          "Sacar del cajón para el mercado de la casa",
          "Recibir pagos del negocio en el celular personal",
          "Pagar el arriendo del local desde la cuenta del negocio"
        ],
        "correcta": 2,
        "retro": {
          "bien": "Correcto: Pagar el arriendo del local es un gasto del negocio, no una fuga.",
          "mal": "Pagar el arriendo del local es un gasto del negocio, no una fuga."
        }
      }
    },
    {
      "titulo": "Pregunta 3 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Lo que vendes en el día, ¿es todo tuyo?",
        "opciones": [
          "No: una parte es para volver a surtir",
          "Sí: si lo vendí, es ganancia",
          "Solo si fue en efectivo"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: Una parte de cada venta es para volver a comprar la mercancía.",
          "mal": "Una parte de cada venta es para volver a comprar la mercancía."
        }
      }
    },
    {
      "titulo": "Pregunta 4 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "¿Por qué conviene anotar lo que sacas para la casa?",
        "opciones": [
          "Porque lo exige la DIAN cada día",
          "Porque sin anotarlo no sabes si el negocio gana",
          "No conviene: es plata tuya"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: Si no anotas lo que sacas, no puedes saber si estás ganando.",
          "mal": "Si no anotas lo que sacas, no puedes saber si estás ganando."
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
