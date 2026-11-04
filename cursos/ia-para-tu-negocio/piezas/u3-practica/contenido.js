/* IA para tu negocio desde el celular · Unidad 3 · Practica
   Molde: componentes/simulador-pantalla · lo escribe pantallas/renderizar.mjs (no editar a mano:
   cambia pantallas/armar_pantallas.py y vuelve a correr los dos scripts).
   Pantallas simplificadas, no capturas reales. */
window.CONTENIDO = {
  "titulo": "Cuida tus datos y pide sin datos personales",
  "paso": "Practica",
  "unidad": "Unidad 3",
  "notaMinima": 60,
  "verZonas": false,
  "pasos": [
    {
      "instruccion": "Antes de pedir, Yaneth revisa la privacidad. Abre el menú del asistente.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-1.jpg",
        "alt": "Pantalla de práctica simplificada: Antes de pedir, Yaneth revisa la privacidad. Abre el menú del asistente."
      },
      "zona": {
        "x": 1.8,
        "y": 3.8,
        "w": 11.9,
        "h": 5.7
      },
      "pista": "El menú son las tres rayas, arriba a la izquierda."
    },
    {
      "instruccion": "Entra a «Ajustes».",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-2.jpg",
        "alt": "Pantalla de práctica simplificada: Entra a «Ajustes»."
      },
      "zona": {
        "x": 0,
        "y": 92,
        "w": 78.2,
        "h": 6.1
      },
      "pista": "Está al final del menú."
    },
    {
      "instruccion": "Entra a «Controles de datos».",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-3.jpg",
        "alt": "Pantalla de práctica simplificada: Entra a «Controles de datos»."
      },
      "zona": {
        "x": 0,
        "y": 34.3,
        "w": 100,
        "h": 9.1
      },
      "pista": "Es la opción del escudo."
    },
    {
      "instruccion": "Apaga la opción que deja usar tus chats para entrenar el asistente.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-4.jpg",
        "alt": "Pantalla de práctica simplificada: Apaga la opción que deja usar tus chats para entrenar el asistente."
      },
      "zona": {
        "x": 81.8,
        "y": 13.7,
        "w": 13.6,
        "h": 3.8
      },
      "pista": "Es el primer interruptor: «Mejorar el modelo para todos»."
    },
    {
      "instruccion": "Ahora sí: pega el pedido seguro para los mensajes de cumpleaños.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-5.jpg",
        "alt": "Pantalla de práctica simplificada: Ahora sí: pega el pedido seguro para los mensajes de cumpleaños."
      },
      "zona": {
        "x": 3.5,
        "y": 69.6,
        "w": 93.1,
        "h": 17.5
      },
      "pista": "El seguro no tiene nombres, cédulas, celulares ni datos de salud."
    }
  ],
  "final": {
    "titulo": "¡Lo lograste!",
    "texto": "Ahora revisa los ajustes de tu asistente y reescribe un pedido sin datos de clientes: eso es el paso Aplica."
  }
};
