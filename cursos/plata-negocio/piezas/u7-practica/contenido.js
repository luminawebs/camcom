/* La plata del negocio no es la de la casa · Unidad 7 · Practica (tramo del Pase)
   Molde: componentes/calculadora · Perfil K */
window.CONTENIDO = {
  titulo: "Encuentra la diferencia del cierre",
  paso: "Practica",
  unidad: "Unidad 7",
  notaMinima: 50,
  ejercicios: 2,
  tolerancia: 0.01,
  caso: "Es el último día del mes en un puesto de comidas rápidas. La dueña revisa su libro, la billetera del negocio y el cajón.",
  pregunta: "¿Cuánta plata falta según el cierre?",
  unidadRespuesta: "$",
  variables: {
    libro: { etiqueta: "Saldo según el libro", tipo: "$", min: 1900000, max: 2100000, paso: 10000 },
    cuenta: { etiqueta: "Saldo de la billetera del negocio", tipo: "$", min: 1200000, max: 1400000, paso: 10000 },
    cajon: { etiqueta: "Efectivo en el cajón", tipo: "$", min: 300000, max: 450000, paso: 10000 }
  },
  calcular: function (v) {
    return v.libro - (v.cuenta + v.cajon);
  },
  explicar: function (v, r, f) {
    return "Diferencia = " + f(v.libro) + " − (" + f(v.cuenta) + " + " + f(v.cajon) + ") = **" + f(r) + "**. " +
      (r > 0 ? "Es positiva: falta plata. Busca un retiro o una comisión sin anotar." : r < 0 ? "Es negativa: sobra plata. Busca una venta o un pago de fiado sin anotar." : "Cuadra exacto.");
  },
  errores: [
    {
      calcular: function (v) { return v.libro - v.cuenta; },
      mensaje: "Te faltó el cajón. El efectivo también es plata del negocio."
    },
    {
      calcular: function (v) { return (v.cuenta + v.cajon) - v.libro; },
      mensaje: "Lo restaste al revés. Arranca del libro: saldo del libro − (cuenta + cajón)."
    }
  ],
  final: { titulo: "Ejercicios terminados", texto: "Ahora haz el cierre de tu propio mes con los 5 pasos." }
};
