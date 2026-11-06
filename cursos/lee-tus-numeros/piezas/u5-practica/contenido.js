/* Lee tus números · Unidad 5 · Practica (tramo del Pase)
   Molde: componentes/calculadora · Perfil K */
window.CONTENIDO = {
  titulo: "¿Con cuánto termina el mes?",
  paso: "Practica",
  unidad: "Unidad 5",
  notaMinima: 50,
  ejercicios: 2,
  tolerancia: 0.01,
  caso: "Estos son los movimientos de plata de un mes de una tienda de mascotas. Ese mes también fió $400.000 que todavía no le han pagado.",
  pregunta: "¿Con cuánta plata terminó el mes?",
  unidadRespuesta: "$",
  variables: {
    inicio: { etiqueta: "Saldo al empezar el mes (caja + Nequi)", tipo: "$", min: 300000, max: 800000, paso: 50000 },
    contado: { etiqueta: "Ventas de contado (efectivo y Nequi)", tipo: "$", min: 3500000, max: 4500000, paso: 100000 },
    cobros: { etiqueta: "Cobros de fiados del mes pasado", tipo: "$", min: 300000, max: 800000, paso: 50000 },
    compras: { etiqueta: "Pago de concentrado y accesorios", tipo: "$", min: 2000000, max: 2800000, paso: 100000 },
    gastos: { etiqueta: "Arriendo y servicios", tipo: "$", min: 800000, max: 1100000, paso: 50000 },
    sueldo: { etiqueta: "Sueldo del dueño", tipo: "$", min: 700000, max: 1000000, paso: 50000 },
    cuota: { etiqueta: "Cuota del préstamo", tipo: "$", min: 200000, max: 400000, paso: 50000 }
  },
  calcular: function (v) {
    return v.inicio + v.contado + v.cobros - v.compras - v.gastos - v.sueldo - v.cuota;
  },
  explicar: function (v, r, f) {
    var ent = v.contado + v.cobros, sal = v.compras + v.gastos + v.sueldo + v.cuota;
    return "Entradas = " + f(v.contado) + " + " + f(v.cobros) + " = " + f(ent) + ". Salidas = " + f(sal) +
      ". Saldo al terminar = " + f(v.inicio) + " + " + f(ent) + " − " + f(sal) + " = **" + f(r) + "**. Los $400.000 fiados no entran hasta que los paguen.";
  },
  errores: [
    {
      calcular: function (v) { return v.inicio + v.contado + v.cobros + 400000 - v.compras - v.gastos - v.sueldo - v.cuota; },
      mensaje: "Sumaste los $400.000 que fió. Esa plata todavía no ha entrado: no va en el flujo hasta que la paguen."
    },
    {
      calcular: function (v) { return v.inicio + v.contado + v.cobros - v.compras - v.gastos - v.sueldo; },
      mensaje: "Te faltó la cuota del préstamo: es plata que sale del negocio."
    },
    {
      calcular: function (v) { return v.contado + v.cobros - v.compras - v.gastos - v.sueldo - v.cuota; },
      mensaje: "Te faltó sumar el saldo con el que empezó el mes."
    }
  ],
  final: { titulo: "Ejercicios terminados", texto: "Ahora arma el flujo de tus próximas 4 semanas con la plantilla de Llévatelo." }
};
