/* Lee tus números · Unidad 6 · Practica (tramo del Pase)
   Molde: componentes/calculadora · Perfil K */
window.CONTENIDO = {
  titulo: "¿Le cabe la cuota?",
  paso: "Practica",
  unidad: "Unidad 6",
  notaMinima: 50,
  ejercicios: 2,
  tolerancia: 0.02,
  caso: "Una dueña de un puesto de comidas va a pedir un préstamo. Estas son sus entradas y salidas de un mes normal (ya incluyen su sueldo) y la cuota que le ofrecen.",
  pregunta: "¿Cuál es el peso de la cuota sobre lo que le sobra al mes?",
  unidadRespuesta: "%",
  variables: {
    entradas: { etiqueta: "Entradas de plata de un mes normal", tipo: "$", min: 6000000, max: 7000000, paso: 100000 },
    salidas: { etiqueta: "Salidas de plata de un mes normal (con su sueldo)", tipo: "$", min: 4800000, max: 5400000, paso: 100000 },
    cuota: { etiqueta: "Cuota del préstamo nuevo", tipo: "$", min: 200000, max: 450000, paso: 10000 }
  },
  calcular: function (v) {
    return v.cuota / (v.entradas - v.salidas) * 100;
  },
  explicar: function (v, r, f) {
    var sobra = v.entradas - v.salidas;
    return "Le sobran " + f(v.entradas) + " − " + f(v.salidas) + " = " + f(sobra) + " al mes. Peso de la cuota = " + f(v.cuota) + " ÷ " + f(sobra) +
      " × 100 = **" + (Math.round(r * 10) / 10).toLocaleString("es-CO") + " %**" + (r > 50 ? ". Pasa de la mitad: conviene un plazo más largo o un préstamo menor." : ".");
  },
  errores: [
    {
      calcular: function (v) { return v.cuota / v.entradas * 100; },
      mensaje: "Dividiste entre las entradas. La cuota se compara con lo que te sobra: entradas menos salidas."
    },
    {
      calcular: function (v) { return (v.entradas - v.salidas) / v.cuota * 100; },
      mensaje: "Lo dividiste al revés: es la cuota dividida entre lo que te sobra, por 100."
    }
  ],
  final: { titulo: "Ejercicios terminados", texto: "Ahora arma tus tres frases y tu carpeta con la lista de Llévatelo." }
};
