/* La plata del negocio no es la de la casa · Unidad 5 · Practica (tramo del Pase)
   Molde: componentes/calculadora · Perfil K */
window.CONTENIDO = {
  titulo: "Saca el total de una categoría",
  paso: "Practica",
  unidad: "Unidad 5",
  notaMinima: 50,
  ejercicios: 2,
  tolerancia: 0.01,
  caso: "Estas son las salidas de una semana del libro de una peluquería. Hay líneas de insumos (productos para los servicios) y de otras categorías.",
  pregunta: "¿Cuánto suman las salidas de la categoría Insumos en la semana?",
  unidadRespuesta: "$",
  variables: {
    tinte: { etiqueta: "Lunes · Tintes (Insumos)", tipo: "$", min: 60000, max: 180000, paso: 5000 },
    champu: { etiqueta: "Miércoles · Champú y crema (Insumos)", tipo: "$", min: 40000, max: 120000, paso: 5000 },
    cuchillas: { etiqueta: "Viernes · Cuchillas y talco (Insumos)", tipo: "$", min: 20000, max: 70000, paso: 5000 },
    luz: { etiqueta: "Martes · Recibo de luz del local (Fijos)", tipo: "$", min: 80000, max: 160000, paso: 5000 },
    domicilio: { etiqueta: "Jueves · Domicilio del proveedor (Variables)", tipo: "$", min: 8000, max: 20000, paso: 1000 }
  },
  calcular: function (v) {
    return v.tinte + v.champu + v.cuchillas;
  },
  explicar: function (v, r, f) {
    return "Insumos = " + f(v.tinte) + " + " + f(v.champu) + " + " + f(v.cuchillas) + " = **" + f(r) + "**. La luz es un gasto fijo y el domicilio, un gasto variable.";
  },
  errores: [
    {
      calcular: function (v) { return v.tinte + v.champu + v.cuchillas + v.domicilio; },
      mensaje: "Sumaste el domicilio. El transporte del proveedor es un gasto variable, no un insumo."
    },
    {
      calcular: function (v) { return v.tinte + v.champu + v.cuchillas + v.luz; },
      mensaje: "Sumaste la luz. El recibo del local es un gasto fijo."
    },
    {
      calcular: function (v) { return v.tinte + v.champu + v.cuchillas + v.luz + v.domicilio; },
      mensaje: "Sumaste todas las salidas. El total de una categoría suma solo sus propias líneas."
    }
  ],
  final: { titulo: "Ejercicios terminados", texto: "Ahora pasa una semana de tu registro al libro y saca tus totales." }
};
