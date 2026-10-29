/* IA para tu negocio desde el celular · Unidad 2 · Practica
   Molde: componentes/simulador-pantalla · lo escribe pantallas/renderizar.mjs (no editar a mano:
   cambia pantallas/armar_pantallas.py y vuelve a correr los dos scripts).
   Pantallas simplificadas, no capturas reales. */
window.CONTENIDO = {
  "titulo": "Pide la descripción de un producto y revísala",
  "paso": "Practica",
  "unidad": "Unidad 2",
  "notaMinima": 60,
  "verZonas": false,
  "pasos": [
    {
      "instruccion": "Leidy quiere la descripción del enterizo amarillo. Adjunta la foto.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-1.jpg",
        "alt": "Pantalla de práctica simplificada: Leidy quiere la descripción del enterizo amarillo. Adjunta la foto."
      },
      "zona": {
        "x": 4.3,
        "y": 92.3,
        "w": 10.8,
        "h": 5.1
      },
      "pista": "El botón para adjuntar es el «+» de la caja de texto."
    },
    {
      "instruccion": "Elige la foto del enterizo.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-2.jpg",
        "alt": "Pantalla de práctica simplificada: Elige la foto del enterizo."
      },
      "zona": {
        "x": 66.1,
        "y": 67.8,
        "w": 30.5,
        "h": 14.4
      },
      "pista": "Es la foto amarilla con el bebé."
    },
    {
      "instruccion": "Ya escribiste el pedido con tus datos reales: material, tallas, precio, para quién y cómo. Envíalo.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-3.jpg",
        "alt": "Pantalla de práctica simplificada: Ya escribiste el pedido con tus datos reales: material, tallas, precio, para quién y cómo. Envíalo."
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
      "instruccion": "Revisa la respuesta antes de usarla: toca el dato que la IA se inventó.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-4.jpg",
        "alt": "Pantalla de práctica simplificada: Revisa la respuesta antes de usarla: toca el dato que la IA se inventó."
      },
      "zona": {
        "x": 13.5,
        "y": 46.8,
        "w": 77.8,
        "h": 2.6
      },
      "pista": "Leidy nunca dijo que el enterizo fuera orgánico ni antialérgico."
    },
    {
      "instruccion": "Le pediste que quitara ese dato y lo corrigió. Copia la descripción para tu catálogo.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-5.jpg",
        "alt": "Pantalla de práctica simplificada: Le pediste que quitara ese dato y lo corrigió. Copia la descripción para tu catálogo."
      },
      "zona": {
        "x": 13.5,
        "y": 36.3,
        "w": 10.3,
        "h": 4.3
      },
      "pista": "El botón de copiar está debajo de la respuesta, a la izquierda."
    }
  ],
  "final": {
    "titulo": "¡Lo lograste!",
    "texto": "Ahora pide la descripción de 2 de tus productos y revísalas antes de publicar: eso es el paso Aplica."
  }
};
