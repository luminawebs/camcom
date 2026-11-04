/* Lee tus números · Unidad 3 · Practica
   Molde: componentes/calculadora · Perfil K · Gancho: 2 ejercicios (8 min) */
window.CONTENIDO = {
  titulo: "¿Cuánto le quedó a la papelería?",
  paso: "Practica",
  unidad: "Unidad 3",
  notaMinima: 50,
  ejercicios: 2,
  tolerancia: 0.01,
  caso: "Estos son los números de un mes de una papelería de León XIII. Arma su estado de resultados y calcula la utilidad del mes.",
  pregunta: "¿Cuál fue la utilidad del mes?",
  unidadRespuesta: "$",
  variables: {
    ventas: { etiqueta: "Ventas del mes", tipo: "$", min: 4800000, max: 6000000, paso: 100000 },
    costo: { etiqueta: "Costo de la mercancía vendida", tipo: "$", min: 1600000, max: 2400000, paso: 50000 },
    arriendo: { etiqueta: "Arriendo del local", tipo: "$", min: 600000, max: 800000, paso: 50000 },
    servicios: { etiqueta: "Servicios e internet", tipo: "$", min: 150000, max: 300000, paso: 10000 },
    toner: { etiqueta: "Tóner y mantenimiento", tipo: "$", min: 80000, max: 200000, paso: 10000 },
    sueldo: { etiqueta: "Sueldo de la dueña", tipo: "$", min: 600000, max: 900000, paso: 50000 }
  },
  calcular: function (v) {
    return v.ventas - v.costo - v.arriendo - v.servicios - v.toner - v.sueldo;
  },
  explicar: function (v, r, f) {
    var bruta = v.ventas - v.costo, gastos = v.arriendo + v.servicios + v.toner + v.sueldo;
    return "Utilidad bruta = " + f(v.ventas) + " − " + f(v.costo) + " = " + f(bruta) +
      ". Gastos = " + f(gastos) + ". Utilidad del mes = " + f(bruta) + " − " + f(gastos) + " = **" + f(r) + "** (margen " +
      Math.round(r / v.ventas * 100) + " %).";
  },
  errores: [
    {
      calcular: function (v) { return v.ventas - v.costo; },
      mensaje: "Esa es la utilidad bruta. Ahora réstale los gastos: arriendo, servicios, tóner y el sueldo de la dueña."
    },
    {
      calcular: function (v) { return v.ventas - v.costo - v.arriendo - v.servicios - v.toner; },
      mensaje: "Te faltó el sueldo de la dueña. Su trabajo también es un gasto del negocio."
    },
    {
      calcular: function (v) { return v.ventas - v.arriendo - v.servicios - v.toner - v.sueldo; },
      mensaje: "Te faltó restar el costo de la mercancía que vendió."
    }
  ],
  final: { titulo: "Ejercicios terminados", texto: "Ahora arma tu estado de resultados con la plantilla de Llévatelo." }
};
