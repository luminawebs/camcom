/* Vende más por WhatsApp Business · Unidad 1 · Practica
   Molde: componentes/simulador-pantalla · lo escribe pantallas/renderizar.mjs (no editar a mano:
   cambia pantallas/armar_pantallas.py y vuelve a correr los dos scripts).
   Pantallas simplificadas, no capturas reales. */
window.CONTENIDO = {
  "titulo": "Agrega un producto a tu catálogo",
  "paso": "Practica",
  "unidad": "Unidad 1",
  "notaMinima": 60,
  "verZonas": false,
  "pasos": [
    {
      "instruccion": "Abre el menú de la app (los tres puntos de arriba).",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-1.jpg",
        "alt": "Pantalla de práctica simplificada: Abre el menú de la app (los tres puntos de arriba)."
      },
      "zona": {
        "x": 87.4,
        "y": 4.4,
        "w": 10.3,
        "h": 4.9
      },
      "pista": "Busca los tres puntos en la esquina de arriba, a la derecha."
    },
    {
      "instruccion": "Entra a «Herramientas para la empresa».",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-2.jpg",
        "alt": "Pantalla de práctica simplificada: Entra a «Herramientas para la empresa»."
      },
      "zona": {
        "x": 31.8,
        "y": 4.5,
        "w": 66.4,
        "h": 8.8
      },
      "pista": "Es la primera opción del menú."
    },
    {
      "instruccion": "Abre el «Catálogo».",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-3.jpg",
        "alt": "Pantalla de práctica simplificada: Abre el «Catálogo»."
      },
      "zona": {
        "x": 0,
        "y": 23,
        "w": 100,
        "h": 8.6
      },
      "pista": "Está en la lista, debajo de «Perfil de empresa»."
    },
    {
      "instruccion": "Agrega tu primer producto.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-4.jpg",
        "alt": "Pantalla de práctica simplificada: Agrega tu primer producto."
      },
      "zona": {
        "x": 4,
        "y": 35.7,
        "w": 91.9,
        "h": 6.2
      },
      "pista": "Toca el botón verde para añadir un artículo nuevo."
    },
    {
      "instruccion": "Ya llenaste foto, nombre, precio y descripción. Guarda el producto.",
      "pantalla": {
        "tipo": "imagen",
        "src": "medios/pantalla-5.jpg",
        "alt": "Pantalla de práctica simplificada: Ya llenaste foto, nombre, precio y descripción. Guarda el producto."
      },
      "zona": {
        "x": 4,
        "y": 69.4,
        "w": 91.9,
        "h": 6.2
      },
      "pista": "El botón para guardar está debajo de los campos."
    }
  ],
  "final": {
    "titulo": "¡Lo lograste!",
    "texto": "Ahora hazlo en tu celular con tus 3 productos que más vendes: eso es el paso Aplica."
  }
};
