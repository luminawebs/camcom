/* Lee tus números · Unidad 4 · Practica (tramo del Pase)
   Molde: componentes/calculadora · Perfil K */
window.CONTENIDO = {
  titulo: "¿Cuánto es del dueño?",
  paso: "Practica",
  unidad: "Unidad 4",
  notaMinima: 50,
  ejercicios: 2,
  tolerancia: 0.01,
  caso: "Este es el balance de una tienda de mascotas el último día del mes. Calcula el patrimonio: lo que es del dueño.",
  pregunta: "¿Cuál es el patrimonio del negocio?",
  unidadRespuesta: "$",
  variables: {
    plata: { etiqueta: "Plata en caja y Nequi", tipo: "$", min: 400000, max: 1200000, paso: 50000 },
    mercancia: { etiqueta: "Mercancía (concentrado y accesorios)", tipo: "$", min: 1500000, max: 3000000, paso: 100000 },
    fiados: { etiqueta: "Fiados por cobrar a los vecinos", tipo: "$", min: 200000, max: 600000, paso: 50000 },
    equipos: { etiqueta: "Equipos (estantes, nevera, báscula)", tipo: "$", min: 1500000, max: 3000000, paso: 100000 },
    proveedor: { etiqueta: "Deuda con el proveedor", tipo: "$", min: 500000, max: 1200000, paso: 50000 },
    prestamo: { etiqueta: "Saldo del préstamo", tipo: "$", min: 800000, max: 2000000, paso: 100000 }
  },
  calcular: function (v) {
    return v.plata + v.mercancia + v.fiados + v.equipos - v.proveedor - v.prestamo;
  },
  explicar: function (v, r, f) {
    var tiene = v.plata + v.mercancia + v.fiados + v.equipos, debe = v.proveedor + v.prestamo;
    return "Lo que tiene = " + f(v.plata) + " + " + f(v.mercancia) + " + " + f(v.fiados) + " + " + f(v.equipos) + " = " + f(tiene) +
      ". Lo que debe = " + f(v.proveedor) + " + " + f(v.prestamo) + " = " + f(debe) + ". Patrimonio = " + f(tiene) + " − " + f(debe) + " = **" + f(r) + "**.";
  },
  errores: [
    {
      calcular: function (v) { return v.plata + v.mercancia + v.equipos - v.proveedor - v.prestamo; },
      mensaje: "Te faltaron los fiados por cobrar: es plata que te van a pagar, así que es algo que el negocio tiene."
    },
    {
      calcular: function (v) { return v.plata + v.mercancia + v.fiados + v.equipos; },
      mensaje: "Ese es el total de lo que tiene. Ahora réstale lo que debe: el proveedor y el préstamo."
    },
    {
      calcular: function (v) { return v.plata + v.mercancia + v.fiados + v.equipos + v.proveedor + v.prestamo; },
      mensaje: "Las deudas se restan, no se suman: patrimonio = lo que tiene − lo que debe."
    }
  ],
  final: { titulo: "Ejercicios terminados", texto: "Ahora haz el balance de tu negocio con la plantilla de Llévatelo." }
};
