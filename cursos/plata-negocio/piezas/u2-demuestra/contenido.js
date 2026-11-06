/* La plata del negocio no es la de la casa · Unidad 2 · Demuestra (cuenta para el certificado)
   Molde: componentes/leccion-interactiva usado como cuestionario: nota = aciertos ÷ preguntas. Solo con el Pase: en las unidades 1 a 3 este paso lo ve quien tiene el Pase.
   La posición de la respuesta correcta cambia de pregunta a pregunta. */
window.CONTENIDO = {
  "titulo": "Tu sueldo",
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
        "enunciado": "Las ganancias de tres meses fueron $1.800.000, $2.100.000 y $1.500.000. ¿Cuál es el promedio?",
        "opciones": [
          "$2.100.000",
          "$5.400.000",
          "$1.800.000"
        ],
        "correcta": 2,
        "retro": {
          "bien": "Correcto: ($1.800.000 + $2.100.000 + $1.500.000) ÷ 3 = $1.800.000.",
          "mal": "($1.800.000 + $2.100.000 + $1.500.000) ÷ 3 = $1.800.000."
        }
      }
    },
    {
      "titulo": "Pregunta 2 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "Con un promedio de $1.800.000 y un colchón del 20 %, ¿cuánto es el sueldo?",
        "opciones": [
          "$1.440.000",
          "$1.800.000",
          "$360.000"
        ],
        "correcta": 0,
        "retro": {
          "bien": "Correcto: $1.800.000 × (1 − 0,20) = $1.440.000.",
          "mal": "$1.800.000 × (1 − 0,20) = $1.440.000."
        }
      }
    },
    {
      "titulo": "Pregunta 3 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "¿Con qué mes conviene calcular tu sueldo?",
        "opciones": [
          "Con el mejor mes",
          "Con el promedio de 3 meses",
          "Con el mes de diciembre"
        ],
        "correcta": 1,
        "retro": {
          "bien": "Correcto: El promedio de 3 meses evita pagarte de más en los meses buenos.",
          "mal": "El promedio de 3 meses evita pagarte de más en los meses buenos."
        }
      }
    },
    {
      "titulo": "Pregunta 4 de 4",
      "texto": "",
      "pregunta": {
        "enunciado": "¿Qué es un sueldo fijo?",
        "opciones": [
          "Lo que necesite ese mes",
          "Lo que quede en el cajón el día 30",
          "La misma cifra en la misma fecha"
        ],
        "correcta": 2,
        "retro": {
          "bien": "Correcto: Sueldo fijo: la misma cifra, en fecha fija, como a un trabajador.",
          "mal": "Sueldo fijo: la misma cifra, en fecha fija, como a un trabajador."
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
