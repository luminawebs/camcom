/* La plata del negocio no es la de la casa · Unidad 1 · Practica
   Molde: componentes/calculadora · Perfil K · Gancho: 2 ejercicios (8 min) */
window.CONTENIDO = {
  titulo: "¿Cuánta plata se fue para la casa?",
  paso: "Practica",
  unidad: "Unidad 1",
  notaMinima: 50,
  ejercicios: 2,
  tolerancia: 0.01,
  caso: "Una tienda de Soacha revisó su semana. Con estos datos, calcula cuánta plata salió de la caja sin anotarse.",
  pregunta: "¿Cuánta plata se fue sin anotar?",
  unidadRespuesta: "$",
  variables: {
    inicial: { etiqueta: "Caja el lunes", tipo: "$", min: 100000, max: 300000, paso: 10000 },
    ventas: { etiqueta: "Ventas de la semana", tipo: "$", min: 1600000, max: 2400000, paso: 50000 },
    pagos: { etiqueta: "Pagos del negocio (mercancía, servicios del local)", tipo: "$", min: 600000, max: 1100000, paso: 50000 },
    final: { etiqueta: "Caja el domingo", tipo: "$", min: 150000, max: 400000, paso: 10000 }
  },
  calcular: function (v) {
    return v.inicial + v.ventas - v.pagos - v.final;
  },
  explicar: function (v, r, f) {
    var deberia = v.inicial + v.ventas - v.pagos;
    return "Debería haber " + f(v.inicial) + " + " + f(v.ventas) + " − " + f(v.pagos) + " = " + f(deberia) +
      ". Hay " + f(v.final) + ", así que se fueron **" + f(r) + "** sin anotar.";
  },
  errores: [
    {
      calcular: function (v) { return v.ventas - v.pagos - v.final; },
      mensaje: "Te faltó la caja del lunes. La plata con la que empezaste también es del negocio."
    },
    {
      calcular: function (v) { return v.inicial + v.ventas - v.final; },
      mensaje: "Te faltó restar los pagos del negocio. Esa plata salió, pero sí está anotada: no es una fuga."
    },
    {
      calcular: function (v) { return v.inicial + v.ventas - v.pagos; },
      mensaje: "Eso es lo que debería haber en caja. Ahora réstale lo que de verdad hay el domingo."
    }
  ],
  final: { titulo: "Ejercicios terminados", texto: "Ahora hazlo con tu negocio: anota tres días lo que sacas para la casa." }
};
