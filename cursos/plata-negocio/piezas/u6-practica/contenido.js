/* La plata del negocio no es la de la casa · Unidad 6 · Practica (tramo del Pase)
   Molde: componentes/calculadora · Perfil K */
window.CONTENIDO = {
  titulo: "Calcula la utilidad real del mes",
  paso: "Practica",
  unidad: "Unidad 6",
  notaMinima: 50,
  ejercicios: 2,
  tolerancia: 0.01,
  caso: "Una miscelánea cerró el mes. Contó su inventario el primer y el último día, y tiene los totales de su libro.",
  pregunta: "¿Cuál es la utilidad real del mes?",
  unidadRespuesta: "$",
  variables: {
    ventas: { etiqueta: "Ventas del mes", tipo: "$", min: 7000000, max: 9000000, paso: 100000 },
    invInicial: { etiqueta: "Inventario al empezar", tipo: "$", min: 1500000, max: 2000000, paso: 100000 },
    compras: { etiqueta: "Compras de mercancía", tipo: "$", min: 3000000, max: 4000000, paso: 100000 },
    invFinal: { etiqueta: "Inventario al terminar", tipo: "$", min: 1600000, max: 2400000, paso: 100000 },
    fijos: { etiqueta: "Gastos fijos", tipo: "$", min: 700000, max: 900000, paso: 50000 },
    variables: { etiqueta: "Gastos variables", tipo: "$", min: 150000, max: 350000, paso: 10000 },
    sueldo: { etiqueta: "Sueldo de la dueña", tipo: "$", min: 1000000, max: 1300000, paso: 100000 }
  },
  calcular: function (v) {
    return v.ventas - (v.invInicial + v.compras - v.invFinal) - v.fijos - v.variables - v.sueldo;
  },
  explicar: function (v, r, f) {
    var costo = v.invInicial + v.compras - v.invFinal;
    return "Costo de lo vendido = " + f(v.invInicial) + " + " + f(v.compras) + " − " + f(v.invFinal) + " = " + f(costo) + ". Utilidad real = " + f(v.ventas) + " − " + f(costo) + " − " + f(v.fijos) + " − " + f(v.variables) + " − " + f(v.sueldo) + " = **" + f(r) + "**.";
  },
  errores: [
    {
      calcular: function (v) { return v.ventas - v.compras - v.fijos - v.variables - v.sueldo; },
      mensaje: "Restaste las compras, no el costo de lo vendido. Usa el inventario: al empezar + compras − al terminar."
    },
    {
      calcular: function (v) { return v.ventas - (v.invInicial + v.compras - v.invFinal) - v.fijos - v.variables; },
      mensaje: "Te faltó restar el sueldo de la dueña. Su trabajo también es un gasto del negocio."
    },
    {
      calcular: function (v) { return v.ventas - (v.invInicial + v.compras + v.invFinal) - v.fijos - v.variables - v.sueldo; },
      mensaje: "El inventario al terminar se resta, no se suma: es mercancía que todavía no vendiste."
    }
  ],
  final: { titulo: "Ejercicios terminados", texto: "Ahora cuenta tu inventario y calcula tu propia utilidad real." }
};
