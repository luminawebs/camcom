/* IA para tu negocio desde el celular · Unidad 1 · Practica
   Molde: componentes/simulador-pantalla · lo escribe pantallas/renderizar.mjs (no editar a mano:
   cambia pantallas/armar_pantallas.py y vuelve a correr los dos scripts).
   Pantallas simplificadas, no capturas reales. */
window.CONTENIDO = {
  "titulo": "Pídele a la IA el aviso de Nelson",
  "paso": "Practica",
  "unidad": "Unidad 1",
  "notaMinima": 60,
  "verZonas": false,
  "pasos": [
    {
      "instruccion": "Nelson abrió el asistente. Empieza una conversación nueva.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-1.jpg",
        "alt": "Pantalla de práctica simplificada: Nelson abrió el asistente. Empieza una conversación nueva."
      },
      "zona": {
        "x": 86.3,
        "y": 3.8,
        "w": 11.9,
        "h": 5.7
      },
      "pista": "Busca el lápiz arriba, a la derecha."
    },
    {
      "instruccion": "Nelson guardó tres pedidos en sus notas. Pega el que tiene las 4 partes: quién es, qué necesita, para quién y cómo lo quiere.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-2.jpg",
        "alt": "Pantalla de práctica simplificada: Nelson guardó tres pedidos en sus notas. Pega el que tiene las 4 partes: quién es, qué necesita, para quién y cómo lo quiere."
      },
      "zona": {
        "x": 3.5,
        "y": 71.9,
        "w": 93.1,
        "h": 17.5
      },
      "pista": "Es el que dice que es una ferretería en Quintanares."
    },
    {
      "instruccion": "El pedido quedó escrito. Envíalo.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-3.jpg",
        "alt": "Pantalla de práctica simplificada: El pedido quedó escrito. Envíalo."
      },
      "zona": {
        "x": 84.9,
        "y": 92.3,
        "w": 10.8,
        "h": 5.1
      },
      "pista": "El botón de enviar es la flecha negra."
    },
    {
      "instruccion": "El aviso está bien, pero es largo para el grupo del barrio. Pídele un ajuste: toca la sugerencia que lo deja corto.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-4.jpg",
        "alt": "Pantalla de práctica simplificada: El aviso está bien, pero es largo para el grupo del barrio. Pídele un ajuste: toca la sugerencia que lo deja corto."
      },
      "zona": {
        "x": 31.5,
        "y": 86.1,
        "w": 45.8,
        "h": 4.6
      },
      "pista": "Busca la sugerencia que habla de 4 líneas."
    },
    {
      "instruccion": "Quedó listo. Copia el aviso para pegarlo en el grupo del barrio.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-5.jpg",
        "alt": "Pantalla de práctica simplificada: Quedó listo. Copia el aviso para pegarlo en el grupo del barrio."
      },
      "zona": {
        "x": 13.5,
        "y": 35.6,
        "w": 10.3,
        "h": 4.3
      },
      "pista": "El botón de copiar está debajo de la respuesta, a la izquierda."
    }
  ],
  "final": {
    "titulo": "¡Lo lograste!",
    "texto": "Ahora hazlo en tu celular con algo que necesites escribir esta semana: eso es el paso Aplica."
  }
};
