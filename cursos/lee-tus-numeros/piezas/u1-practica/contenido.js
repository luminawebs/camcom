/* Lee tus números · Unidad 1 · Practica
   Molde: componentes/calculadora · Perfil K · Gancho: 2 ejercicios (8 min) */
window.CONTENIDO = {
  titulo: "¿Cuánto fueron los costos del mes?",
  paso: "Practica",
  unidad: "Unidad 1",
  notaMinima: 50,
  ejercicios: 2,
  tolerancia: 0.01,
  caso: "Estos son los movimientos de un mes del negocio de comidas rápidas de Patricia. Separa lo que es costo (lo que necesita para hacer lo que vende) de lo demás.",
  pregunta: "¿Cuánto suman los costos del mes?",
  unidadRespuesta: "$",
  variables: {
    ventas: { etiqueta: "Ventas del mes", tipo: "$", min: 5000000, max: 7000000, paso: 100000 },
    insumos: { etiqueta: "Salchichas, carne, pan y papa", tipo: "$", min: 1800000, max: 2600000, paso: 50000 },
    empaques: { etiqueta: "Salsas, empaques y servilletas", tipo: "$", min: 300000, max: 500000, paso: 10000 },
    arriendo: { etiqueta: "Arriendo del local", tipo: "$", min: 800000, max: 1000000, paso: 50000 },
    servicios: { etiqueta: "Gas, luz y agua del local", tipo: "$", min: 250000, max: 400000, paso: 10000 },
    casa: { etiqueta: "Mercado de la casa (pagado con el Nequi del negocio)", tipo: "$", min: 200000, max: 350000, paso: 10000 }
  },
  calcular: function (v) {
    return v.insumos + v.empaques;
  },
  explicar: function (v, r, f) {
    return "Costos = insumos " + f(v.insumos) + " + empaques " + f(v.empaques) + " = **" + f(r) + "**. El arriendo y los servicios son gastos; el mercado de la casa no va; y las ventas son el ingreso.";
  },
  errores: [
    {
      calcular: function (v) { return v.insumos + v.empaques + v.arriendo + v.servicios; },
      mensaje: "Sumaste también el arriendo y los servicios. Esos son gastos: los pagas aunque no vendas."
    },
    {
      calcular: function (v) { return v.insumos + v.empaques + v.casa; },
      mensaje: "Metiste el mercado de la casa. Aunque sea comida, no es para vender: no va en el negocio."
    },
    {
      calcular: function (v) { return v.insumos; },
      mensaje: "Te faltaron las salsas y los empaques. También los necesitas para entregar lo que vendes."
    },
    {
      calcular: function (v) { return v.insumos + v.empaques + v.arriendo + v.servicios + v.casa; },
      mensaje: "Sumaste todo lo que salió. Solo es costo lo que necesitas para hacer lo que vendes."
    }
  ],
  final: { titulo: "Ejercicios terminados", texto: "Ahora hazlo con tu negocio: clasifica 10 movimientos de esta semana en la tabla de Llévatelo." }
};
