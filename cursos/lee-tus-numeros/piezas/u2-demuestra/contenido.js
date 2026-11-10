/* Lee tus números · Unidad 2 · Demuestra (cuenta para el certificado)
   Molde: componentes/leccion-interactiva usado como cuestionario: nota = aciertos ÷ preguntas.
   La posición de la respuesta correcta cambia de pregunta a pregunta. */
window.CONTENIDO = {
  "titulo": "El mes en números",
  "paso": "Demuestra",
  "unidad": "Unidad 2",
  "notaMinima": 75,
  "pantallas": [
    {
      "titulo": "¿Lo lograste?",
      "texto": "Cuatro preguntas sobre la Unidad 2. Necesitas 3 de 4 bien para aprobar este paso, que cuenta para tu certificado. Si no lo logras, repásalo y vuelve a intentarlo."
    },
    {
      "titulo": "Pregunta 1 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Óscar vendió $2.000.000 en efectivo, $1.500.000 por Nequi y fió $300.000. ¿Ventas del mes?",
        "opciones": [
          "$3.500.000",
          "$3.800.000",
          "$3.200.000"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: $2.000.000 + $1.500.000 + $300.000 = $3.800.000: lo fiado también es venta del mes.",
          "mal": "$2.000.000 + $1.500.000 + $300.000 = $3.800.000: lo fiado también es venta del mes."
        }
      }
    },
    {
      "titulo": "Pregunta 2 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Óscar pasó $500.000 de la caja a su Nequi para pagarle al proveedor. ¿Es venta?",
        "opciones": [
          "No: es un traslado, esa plata ya estaba en las ventas",
          "Sí, porque entró al Nequi",
          "Solo la mitad"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: Pasar plata de la caja al Nequi es un traslado: contarla otra vez sería contar dos veces.",
          "mal": "Pasar plata de la caja al Nequi es un traslado: contarla otra vez sería contar dos veces."
        }
      }
    },
    {
      "titulo": "Pregunta 3 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "¿Cuál de estos SÍ es venta del mes?",
        "opciones": [
          "La devolución de un proveedor",
          "Lo que fiaste este mes a un vecino",
          "Plata que pusiste de tu bolsillo"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: Lo fiado es venta del mes; la devolución y tu aporte no son ventas.",
          "mal": "Lo fiado es venta del mes; la devolución y tu aporte no son ventas."
        }
      }
    },
    {
      "titulo": "Pregunta 4 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Efectivo $1.800.000, transferencias $1.200.000, fiado $200.000 y un aporte tuyo de $300.000. ¿Ventas?",
        "opciones": [
          "$3.500.000",
          "$3.000.000",
          "$3.200.000"
        ],
        "correcta": 2,
        "retro": {
          "bien": "Correcto: $1.800.000 + $1.200.000 + $200.000 = $3.200.000. Tu aporte no es venta.",
          "mal": "$1.800.000 + $1.200.000 + $200.000 = $3.200.000. Tu aporte no es venta."
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
