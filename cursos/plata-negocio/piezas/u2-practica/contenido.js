/* La plata del negocio no es la de la casa · Unidad 2 · Practica
   Molde: componentes/calculadora · Perfil K · Gancho: 2 ejercicios (8 min) */
window.CONTENIDO = {
  titulo: "¿Cuánto te puedes pagar?",
  paso: "Practica",
  unidad: "Unidad 2",
  notaMinima: 50,
  ejercicios: 2,
  tolerancia: 0.01,
  caso: "Un peluquero de Ciudad Verde quiere pagarse un sueldo fijo. Estas fueron las ganancias de su negocio en los últimos tres meses.",
  pregunta: "¿Cuál debe ser su sueldo mensual?",
  unidadRespuesta: "$",
  variables: {
    mes1: { etiqueta: "Ganancia mes 1", tipo: "$", min: 1200000, max: 3000000, paso: 100000 },
    mes2: { etiqueta: "Ganancia mes 2", tipo: "$", min: 1200000, max: 3000000, paso: 100000 },
    mes3: { etiqueta: "Ganancia mes 3", tipo: "$", min: 1200000, max: 3000000, paso: 100000 },
    colchon: { etiqueta: "Colchón para el negocio", tipo: "%", min: 10, max: 25, paso: 5 }
  },
  calcular: function (v) {
    return (v.mes1 + v.mes2 + v.mes3) / 3 * (1 - v.colchon / 100);
  },
  explicar: function (v, r, f) {
    var prom = (v.mes1 + v.mes2 + v.mes3) / 3;
    return "Promedio = (" + f(v.mes1) + " + " + f(v.mes2) + " + " + f(v.mes3) + ") ÷ 3 = " + f(prom) +
      ". Sueldo = " + f(prom) + " × (1 − " + (v.colchon / 100).toFixed(2).replace(".", ",") + ") = **" + f(r) + "**.";
  },
  errores: [
    {
      calcular: function (v) { return (v.mes1 + v.mes2 + v.mes3) / 3; },
      mensaje: "Ese es el promedio, pero te faltó dejar el colchón para el negocio."
    },
    {
      calcular: function (v) { return Math.max(v.mes1, v.mes2, v.mes3) * (1 - v.colchon / 100); },
      mensaje: "Usaste el mejor mes. Usa el promedio de los tres, porque también vienen meses malos."
    },
    {
      calcular: function (v) { return (v.mes1 + v.mes2 + v.mes3) * (1 - v.colchon / 100); },
      mensaje: "Sumaste los tres meses pero no dividiste entre 3. El sueldo es mensual."
    }
  ],
  final: { titulo: "Ejercicios terminados", texto: "Ahora calcula tu propio sueldo con los números de tus últimos tres meses." }
};
