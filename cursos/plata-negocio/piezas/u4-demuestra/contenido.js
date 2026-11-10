/* La plata del negocio no es la de la casa · Unidad 4 · Demuestra (cuenta para el certificado)
   Molde: componentes/leccion-interactiva usado como cuestionario: nota = aciertos ÷ preguntas.
   La posición de la respuesta correcta cambia de pregunta a pregunta. */
window.CONTENIDO = {
  "titulo": "Ventas y gastos por categoría",
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
        "enunciado": "El arriendo del local va en…",
        "opciones": [
          "Gastos variables",
          "Gastos fijos",
          "Mercancía"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: El arriendo se paga igual cada mes: es un gasto fijo.",
          "mal": "El arriendo se paga igual cada mes: es un gasto fijo."
        }
      }
    },
    {
      "titulo": "Pregunta 2 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Le debían $90.000. Fió $60.000 y le pagaron $50.000. ¿Cuánto le deben ahora?",
        "opciones": [
          "$200.000",
          "$80.000",
          "$100.000"
        ],
        "correcta": 2,
        "retro": {
          "bien": "Correcto: $90.000 + $60.000 − $50.000 = $100.000.",
          "mal": "$90.000 + $60.000 − $50.000 = $100.000."
        }
      }
    },
    {
      "titulo": "Pregunta 3 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Un cliente se llevó $30.000 fiados. ¿Cómo se anota?",
        "opciones": [
          "En la lista de fiados, hasta que pague",
          "Como entrada en el registro de hoy",
          "No se anota hasta que pague"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: El fiado es venta, pero no es plata: va en su lista hasta que paguen.",
          "mal": "El fiado es venta, pero no es plata: va en su lista hasta que paguen."
        }
      }
    },
    {
      "titulo": "Pregunta 4 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "¿Cuándo conviene tomar la foto del soporte?",
        "opciones": [
          "A fin de año",
          "El mismo día de la compra",
          "Solo si el contador la pide"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: Foto al soporte el mismo día, en la carpeta del mes.",
          "mal": "Foto al soporte el mismo día, en la carpeta del mes."
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
