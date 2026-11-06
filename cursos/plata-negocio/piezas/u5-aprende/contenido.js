/* La plata del negocio no es la de la casa · Unidad 5 · Aprende (tramo del Pase)
   Molde: componentes/leccion-interactiva · Perfil K */
window.CONTENIDO = {
  titulo: "Tu libro sencillo del negocio",
  paso: "Aprende",
  unidad: "Unidad 5",
  notaMinima: 60,
  narracion: true,
  pantallas: [
    {
      titulo: "Tres cuadernos y ninguno cuadra",
      texto: "Jhon Fredy tiene un cuaderno para los servicios, una libreta para el proveedor y los pantallazos de Nequi en el celular. Su contador le pidió «el libro del mes» y no supo qué entregarle. La solución: **un solo libro por mes**.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Cuaderno, libreta y celular con pantallazos sobre el mostrador de la peluquería" }
    },
    {
      titulo: "Un libro, siete columnas",
      texto: "En cuaderno, Excel o app, una línea por movimiento, en orden de fecha:\n**Fecha · Qué fue · Categoría · Medio · Entró · Salió · Saldo**\n\n**Categoría:** las 5 de la Unidad 4, o «Venta». **Medio:** efectivo, transferencia o billetera; así cuadras el cajón y la cuenta por separado.",
      medio: { tipo: "imagen", src: "medios/ilustracion-2.jpg", alt: "Libro del mes con siete columnas y un total subrayado en rojo" }
    },
    {
      titulo: "Las ventas del día, en pocas líneas",
      texto: "Si un día hiciste 40 servicios, no hacen falta 40 líneas. Basta una línea «Ventas del día en efectivo» y otra «Ventas del día por transferencia».",
      pregunta: {
        enunciado: "El saldo de la línea anterior es $820.000. La nueva línea dice: Ventas del día por transferencia, entró $310.000. ¿Qué saldo va en esa línea?",
        opciones: ["$1.130.000", "$510.000", "$310.000"],
        correcta: 0,
        retro: {
          bien: "Correcto: saldo anterior + lo que entró = $820.000 + $310.000 = $1.130.000.",
          mal: "Cada línea arranca del saldo anterior: $820.000 + $310.000 = $1.130.000."
        }
      }
    },
    {
      titulo: "Los totales del mes",
      texto: "El último día sumas las líneas de cada categoría.\n\n**Total de una categoría = suma de todas sus líneas del mes**\n\nJhon Fredy en noviembre: ventas $4.200.000; insumos $780.000; fijos $1.350.000; variables $210.000; su sueldo $1.400.000; cuota de la silla $250.000.",
      pregunta: {
        enunciado: "En una semana, las líneas de insumos son $120.000, $65.000 y $95.000. ¿Cuál es el total de insumos?",
        opciones: ["$280.000", "$185.000", "$215.000"],
        correcta: 0,
        retro: {
          bien: "Correcto: $120.000 + $65.000 + $95.000 = $280.000.",
          mal: "Se suman todas las líneas de la categoría: $120.000 + $65.000 + $95.000 = $280.000."
        }
      }
    },
    {
      titulo: "¿Y la ley qué pide?",
      texto: "Si estás inscrito como comerciante, el Código de Comercio (art. 19) dice que debes llevar contabilidad; para microempresas hay una contabilidad simplificada. Quien no está obligado a llevar contabilidad y no es responsable de IVA debe llevar un libro fiscal de operaciones diarias (Estatuto Tributario, art. 616). [VERIFICAR con el contador: a quién aplica cada cosa y cómo decirlo sin asustar.] Este libro sencillo no reemplaza la contabilidad, pero es la base que tu contador necesita."
    },
    {
      titulo: "Lo que debes recordar",
      texto: "Un solo libro por mes, siete columnas, una línea por movimiento. El último día, totales por categoría. Si el saldo del libro no cuadra con el cajón y la cuenta, algo falta por anotar."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: saca el total de una categoría en el libro de una peluquería." }
};
