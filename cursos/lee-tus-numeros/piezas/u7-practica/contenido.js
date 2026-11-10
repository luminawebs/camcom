/* Lee tus números · Unidad 7 · Practica (tramo del Pase)
   Molde: componentes/calculadora · Perfil K */
window.CONTENIDO = {
  titulo: "¿Cuánto tiene que vender para no perder?",
  paso: "Practica",
  unidad: "Unidad 7",
  notaMinima: 50,
  ejercicios: 2,
  tolerancia: 0.01,
  caso: "Estos son los números de un mes de una papelería. Calcula su punto de equilibrio: lo mínimo que tiene que vender al mes para no perder.",
  pregunta: "¿Cuál es el punto de equilibrio?",
  unidadRespuesta: "$",
  variables: {
    ventas: { etiqueta: "Ventas del mes", tipo: "$", min: 4000000, max: 6000000, paso: 500000 },
    costo: { etiqueta: "Costo de lo vendido (40 % a 60 % de las ventas)", tipo: "%", min: 40, max: 60, paso: 5 },
    fijos: { etiqueta: "Gastos fijos (arriendo, servicios, sueldos)", tipo: "$", min: 1500000, max: 2200000, paso: 100000 }
  },
  calcular: function (v) {
    return v.fijos / (1 - v.costo / 100);
  },
  explicar: function (v, r, f) {
    var c = v.costo / 100;
    return "El costo es el " + v.costo + " % de las ventas. Punto de equilibrio = " + f(v.fijos) + " ÷ (1 − " + c.toLocaleString("es-CO") + ") = **" + f(Math.round(r)) +
      "**. Con ventas de " + f(v.ventas) + (v.ventas >= r ? " el negocio está por encima: gana." : " está por debajo: pierde.");
  },
  errores: [
    {
      calcular: function (v) { return v.fijos / (v.costo / 100); },
      mensaje: "Dividiste entre el costo. Se divide entre lo que queda de cada peso vendido: 1 menos el costo."
    },
    {
      calcular: function (v) { return v.fijos; },
      mensaje: "Ese son solo los gastos fijos. Divídelos entre (1 − costo ÷ ventas)."
    },
    {
      calcular: function (v) { return v.fijos * (1 - v.costo / 100); },
      mensaje: "Multiplicaste. Los gastos fijos se dividen entre (1 − costo ÷ ventas)."
    }
  ],
  final: { titulo: "Ejercicios terminados", texto: "Ahora calcula tus 3 indicadores en el tablero de Llévatelo." }
};
