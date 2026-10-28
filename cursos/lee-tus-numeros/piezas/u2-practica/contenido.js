/* Lee tus números · Unidad 2 · Practica
   Molde: componentes/calculadora · Perfil K · Gancho: 2 ejercicios (8 min) */
window.CONTENIDO = {
  titulo: "¿Cuánto vendió Óscar en el mes?",
  paso: "Practica",
  unidad: "Unidad 2",
  notaMinima: 50,
  ejercicios: 2,
  tolerancia: 0.01,
  caso: "Óscar juntó septiembre en una hoja. Tiene el cuaderno, el historial de Nequi y la lista de fiados. Calcula sus ventas del mes sin contar nada dos veces.",
  pregunta: "¿Cuánto vendió en el mes?",
  unidadRespuesta: "$",
  variables: {
    efectivo: { etiqueta: "Ventas en efectivo (cuaderno)", tipo: "$", min: 2500000, max: 4000000, paso: 100000 },
    nequi: { etiqueta: "Todo lo que entró al Nequi", tipo: "$", min: 1500000, max: 2500000, paso: 100000 },
    traslado: { etiqueta: "De eso, plata que él pasó de la caja al Nequi", tipo: "$", min: 300000, max: 800000, paso: 50000 },
    prestamo: { etiqueta: "De eso, préstamo de su hermano", tipo: "$", min: 200000, max: 500000, paso: 50000 },
    fiado: { etiqueta: "Fiados de septiembre (aún sin pagar)", tipo: "$", min: 150000, max: 400000, paso: 10000 }
  },
  calcular: function (v) {
    return v.efectivo + (v.nequi - v.traslado - v.prestamo) + v.fiado;
  },
  explicar: function (v, r, f) {
    var ventasNequi = v.nequi - v.traslado - v.prestamo;
    return "Ventas por Nequi = " + f(v.nequi) + " − " + f(v.traslado) + " − " + f(v.prestamo) + " = " + f(ventasNequi) +
      ". Ventas del mes = " + f(v.efectivo) + " + " + f(ventasNequi) + " + " + f(v.fiado) + " = **" + f(r) + "**.";
  },
  errores: [
    {
      calcular: function (v) { return v.efectivo + v.nequi + v.fiado; },
      mensaje: "Sumaste todo el Nequi. Quita lo que él mismo pasó de la caja (ya estaba en el efectivo) y el préstamo (no es venta)."
    },
    {
      calcular: function (v) { return v.efectivo + (v.nequi - v.prestamo) + v.fiado; },
      mensaje: "Contaste dos veces la plata que pasó de la caja al Nequi. Ya estaba en el efectivo."
    },
    {
      calcular: function (v) { return v.efectivo + (v.nequi - v.traslado) + v.fiado; },
      mensaje: "Te faltó quitar el préstamo del hermano. Entró al Nequi, pero no es una venta."
    },
    {
      calcular: function (v) { return v.efectivo + (v.nequi - v.traslado - v.prestamo); },
      mensaje: "Te faltaron los fiados. La venta se cuenta el mes en que la hiciste, aunque te paguen después."
    }
  ],
  final: { titulo: "Ejercicios terminados", texto: "Ahora junta tu último mes con la hoja de Llévatelo." }
};
