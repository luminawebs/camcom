/* La plata del negocio no es la de la casa · Unidad 4 · Practica (tramo del Pase)
   Molde: componentes/calculadora · Perfil K */
window.CONTENIDO = {
  titulo: "Separa los gastos fijos del mes",
  paso: "Practica",
  unidad: "Unidad 4",
  notaMinima: 50,
  ejercicios: 2,
  tolerancia: 0.01,
  caso: "Una tienda de barrio anotó todos los pagos del mes en una sola lista. Algunos son gastos fijos y otros no.",
  pregunta: "¿Cuánto suman los gastos fijos del mes?",
  unidadRespuesta: "$",
  variables: {
    arriendo: { etiqueta: "Arriendo del local", tipo: "$", min: 600000, max: 1200000, paso: 50000 },
    servicios: { etiqueta: "Luz y agua del local", tipo: "$", min: 80000, max: 200000, paso: 10000 },
    internet: { etiqueta: "Internet y celular del negocio", tipo: "$", min: 60000, max: 120000, paso: 5000 },
    mercancia: { etiqueta: "Compras de mercancía", tipo: "$", min: 1500000, max: 3500000, paso: 100000 },
    bolsas: { etiqueta: "Bolsas y empaques", tipo: "$", min: 40000, max: 120000, paso: 5000 },
    sueldo: { etiqueta: "Sueldo de la dueña", tipo: "$", min: 1000000, max: 1600000, paso: 100000 }
  },
  calcular: function (v) {
    return v.arriendo + v.servicios + v.internet;
  },
  explicar: function (v, r, f) {
    return "Gastos fijos = arriendo " + f(v.arriendo) + " + servicios " + f(v.servicios) + " + internet y celular " + f(v.internet) + " = **" + f(r) + "**. La mercancía, las bolsas y el sueldo de la dueña van en sus propias categorías.";
  },
  errores: [
    {
      calcular: function (v) { return v.arriendo + v.servicios + v.internet + v.bolsas; },
      mensaje: "Sumaste las bolsas. Las bolsas suben o bajan con las ventas: son un gasto variable."
    },
    {
      calcular: function (v) { return v.arriendo + v.servicios + v.internet + v.sueldo; },
      mensaje: "Sumaste el sueldo de la dueña. En este curso tu sueldo va en su propia categoría para verlo claro."
    },
    {
      calcular: function (v) { return v.arriendo + v.servicios + v.internet + v.mercancia; },
      mensaje: "Sumaste la mercancía. Lo que compras para vender va en «Mercancía o insumos», no en gastos fijos."
    }
  ],
  final: { titulo: "Ejercicios terminados", texto: "Ahora anota tu propia semana por categorías y lleva tu lista de fiados." }
};
