/* La plata del negocio no es la de la casa · Unidad 3 · Practica
   Molde: componentes/calculadora · Perfil K · Gancho: 2 ejercicios (8 min) */
window.CONTENIDO = {
  titulo: "Cuadra el registro del día",
  paso: "Practica",
  unidad: "Unidad 3",
  notaMinima: 50,
  ejercicios: 2,
  tolerancia: 0.01,
  caso: "Un taller de confección de San Mateo anotó su día. Hoy también fue la fecha de pago del sueldo de la dueña.",
  pregunta: "¿Cuál es el saldo del negocio al cerrar?",
  unidadRespuesta: "$",
  variables: {
    ayer: { etiqueta: "Saldo de ayer", tipo: "$", min: 800000, max: 1500000, paso: 50000 },
    efectivo: { etiqueta: "Ventas en efectivo", tipo: "$", min: 200000, max: 500000, paso: 10000 },
    digital: { etiqueta: "Ventas por transferencia", tipo: "$", min: 200000, max: 600000, paso: 10000 },
    proveedor: { etiqueta: "Pago de tela al proveedor", tipo: "$", min: 100000, max: 400000, paso: 10000 },
    sueldo: { etiqueta: "Sueldo de la dueña (quincena)", tipo: "$", min: 400000, max: 700000, paso: 50000 }
  },
  calcular: function (v) {
    return v.ayer + v.efectivo + v.digital - v.proveedor - v.sueldo;
  },
  explicar: function (v, r, f) {
    return "Saldo = " + f(v.ayer) + " + " + f(v.efectivo) + " + " + f(v.digital) + " − " + f(v.proveedor) + " − " + f(v.sueldo) + " = **" + f(r) + "**.";
  },
  errores: [
    {
      calcular: function (v) { return v.ayer + v.efectivo + v.digital - v.proveedor; },
      mensaje: "Te faltó restar el sueldo. Tu sueldo sale de la cuenta del negocio y también se anota."
    },
    {
      calcular: function (v) { return v.ayer + v.digital - v.proveedor - v.sueldo; },
      mensaje: "Te faltaron las ventas en efectivo. El efectivo también es del negocio y se anota."
    },
    {
      calcular: function (v) { return v.efectivo + v.digital - v.proveedor - v.sueldo; },
      mensaje: "Te faltó el saldo de ayer. El registro siempre arranca de lo que había."
    }
  ],
  final: { titulo: "Ejercicios terminados", texto: "Ahora lleva tu propio registro durante una semana." }
};
