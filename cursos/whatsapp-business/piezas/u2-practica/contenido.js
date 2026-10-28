/* Vende más por WhatsApp Business · Unidad 2 · Practica
   Molde: componentes/simulador-pantalla · lo escribe pantallas/renderizar.mjs (no editar a mano:
   cambia pantallas/armar_pantallas.py y vuelve a correr los dos scripts).
   Pantallas simplificadas, no capturas reales. */
window.CONTENIDO = {
  "titulo": "Ponle la etiqueta a un cliente que ya pagó",
  "paso": "Practica",
  "unidad": "Unidad 2",
  "notaMinima": 60,
  "verZonas": false,
  "pasos": [
    {
      "instruccion": "Laura ya le pagó a Camilo por Nequi. Selecciona su chat (mantenlo presionado).",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-1.jpg",
        "alt": "Pantalla de práctica simplificada: Laura ya le pagó a Camilo por Nequi. Selecciona su chat (mantenlo presionado)."
      },
      "zona": {
        "x": 0,
        "y": 16.6,
        "w": 100,
        "h": 9.6
      },
      "pista": "Es el primer chat de la lista: «Ya te pagué por Nequi»."
    },
    {
      "instruccion": "Toca el ícono de etiqueta.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-2.jpg",
        "alt": "Pantalla de práctica simplificada: Toca el ícono de etiqueta."
      },
      "zona": {
        "x": 60.7,
        "y": 4.4,
        "w": 10.3,
        "h": 4.9
      },
      "pista": "Está arriba, en la barra verde, junto al alfiler."
    },
    {
      "instruccion": "Elige la etiqueta que va: ya pagó, pero falta entregar.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-3.jpg",
        "alt": "Pantalla de práctica simplificada: Elige la etiqueta que va: ya pagó, pero falta entregar."
      },
      "zona": {
        "x": 0,
        "y": 77.4,
        "w": 100,
        "h": 6.4
      },
      "pista": "Si ya pagó y no le ha entregado, la etapa es «Pagado»."
    },
    {
      "instruccion": "Guarda la etiqueta.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-4.jpg",
        "alt": "Pantalla de práctica simplificada: Guarda la etiqueta."
      },
      "zona": {
        "x": 4,
        "y": 91.9,
        "w": 91.9,
        "h": 6.2
      },
      "pista": "El botón para guardar está al final de la lista."
    },
    {
      "instruccion": "Es hora de cobrar. Muestra solo los clientes que todavía no han pagado.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-5.jpg",
        "alt": "Pantalla de práctica simplificada: Es hora de cobrar. Muestra solo los clientes que todavía no han pagado."
      },
      "zona": {
        "x": 47.5,
        "y": 11.6,
        "w": 34.3,
        "h": 4.1
      },
      "pista": "Busca el filtro arriba de los chats."
    }
  ],
  "final": {
    "titulo": "¡Lo lograste!",
    "texto": "Ahora ponle etiqueta a todos los chats de clientes de esta semana: eso es el paso Aplica."
  }
};
