/* Calculadora con retroalimentación · paso PRACTICA (perfil K Cálculo)
   Cada intento genera cifras distintas dentro de los rangos de "variables".
   "calcular" devuelve la respuesta correcta y "explicar" el procedimiento.
   El ejemplo usa el caso del manual (precio de venta con margen); cámbialo por el de tu curso. */
window.CONTENIDO = {
  titulo: "[¿A cuánto vendes tu producto?]",
  paso: "Practica",
  unidad: "Unidad [n]",
  notaMinima: 60,
  ejercicios: 3,
  tolerancia: 0.02, /* 2 % de margen de error por redondeos */
  caso: "[Contexto del caso: quién, qué vende y qué necesita saber. Máx. 30 palabras.]",
  pregunta: "[Pregunta que responde el estudiante] ¿A qué precio debe vender?",
  unidadRespuesta: "$",
  variables: {
    ingredientes: { etiqueta: "Ingredientes", tipo: "$", min: 800, max: 2000, paso: 50 },
    empaque: { etiqueta: "Empaque", tipo: "$", min: 100, max: 300, paso: 50 },
    margen: { etiqueta: "Margen que quieres", tipo: "%", min: 25, max: 45, paso: 5 }
  },
  calcular: function (v) {
    return (v.ingredientes + v.empaque) / (1 - v.margen / 100);
  },
  explicar: function (v, r, f) {
    var costo = v.ingredientes + v.empaque;
    return "Costo = " + f(v.ingredientes) + " + " + f(v.empaque) + " = " + f(costo) +
      ". Precio = costo ÷ (1 − " + (v.margen / 100).toFixed(2).replace(".", ",") + ") = **" + f(r) + "**.";
  },
  /* Errores frecuentes: si la respuesta coincide con uno, se muestra su explicación */
  errores: [
    {
      calcular: function (v) { return (v.ingredientes + v.empaque) * (1 + v.margen / 100); },
      mensaje: "Sumaste el margen sobre el costo. El margen se calcula sobre el precio de venta, por eso se divide."
    },
    {
      calcular: function (v) { return v.ingredientes / (1 - v.margen / 100); },
      mensaje: "Olvidaste el empaque. Todo lo que gastas para vender el producto es parte del costo."
    }
  ],
  final: { titulo: "Ejercicios terminados", texto: "[Frase que conecta con el paso Aplica: ahora hazlo con tus productos.]" }
};
