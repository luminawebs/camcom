/* Lee tus números · Unidad 1 · Aprende
   Molde: componentes/leccion-interactiva · Perfil K · Gancho (5 min)
   Caso: Patricia, comidas rápidas en La Despensa. Cifras del caso inventadas para enseñar. */
window.CONTENIDO = {
  titulo: "Ingreso, costo o gasto",
  paso: "Aprende",
  unidad: "Unidad 1",
  notaMinima: 60,
  narracion: true,
  pantallas: [
    {
      titulo: "Todo mezclado en un solo Nequi",
      texto: "La cooperativa le pide a Patricia el **estado de resultados** de su negocio para prestarle para una plancha nueva. Ella mira su Nequi: entran las ventas, salen las salchichas, el pan, el arriendo, el gas y el mercado de la casa. Para saber cuánto gana, primero hay que poner cada peso en su lugar.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Ilustración de Patricia en su puesto de comidas rápidas mirando el celular" }
    },
    {
      titulo: "Ingreso: lo que vendes",
      texto: "Un **ingreso** es la plata que entra porque **vendiste** algo: cada perro caliente, cada hamburguesa, cada domicilio. No son ingresos un **préstamo**, la plata que tú pones de tu bolsillo ni la que te manda un familiar. Esa plata entra, pero no la ganó el negocio vendiendo.",
      pregunta: {
        enunciado: "La cooperativa le presta a Patricia $4.000.000. ¿Es un ingreso del negocio?",
        opciones: ["No: es un préstamo que tiene que devolver", "Sí: es plata que entra al negocio", "Solo si lo usa para el negocio"],
        correcta: 0,
        retro: {
          bien: "Así es. El préstamo entra, pero no lo ganaste vendiendo: lo debes. No va en las ventas.",
          mal: "Un préstamo entra a la cuenta, pero no es una venta: es plata que debes devolver. No es ingreso."
        }
      }
    },
    {
      titulo: "Costo: lo que te cuesta lo que vendes",
      texto: "El **costo** es lo que pagas para **hacer o comprar lo que vendes**: salchichas, pan, papa, salsas, empaques. Si vendes más, compras más; si vendes menos, compras menos. Por eso el costo **sube y baja con las ventas**.",
      medio: { tipo: "imagen", src: "medios/ilustracion-3.jpg", alt: "Tres cajas: lo que entra, lo que cuesta lo que vendes y lo que cuesta tener abierto el negocio" }
    },
    {
      titulo: "Gasto: lo que pagas por estar abierto",
      texto: "El **gasto** es lo que pagas por **tener el negocio abierto**, vendas mucho o poco: arriendo del local, luz, agua, gas de la cocina, internet, el sueldo de quien te ayuda **y tu propio sueldo**. Un mes flojo, el arriendo es el mismo.",
      pregunta: {
        enunciado: "Patricia paga $900.000 de arriendo del local cada mes. ¿Qué es?",
        opciones: ["Un gasto: lo paga aunque no venda", "Un costo: lo necesita para vender", "No es del negocio"],
        correcta: 0,
        retro: {
          bien: "Correcto. El arriendo es el mismo en un mes bueno o malo: es un gasto.",
          mal: "El arriendo no sube ni baja con las ventas: lo pagas por tener el local abierto. Es un gasto."
        }
      }
    },
    {
      titulo: "Lo que no es del negocio",
      texto: "El **mercado de la casa**, la cuota del colegio de los hijos o la recarga de tu celular personal **no van** en las cuentas del negocio. Si los metes, el negocio parece ganar menos de lo que gana. Si sacas plata para la casa, eso sale de **tu sueldo**, no es un gasto más del negocio. Lo viste en el curso «La plata del negocio no es la de la casa».",
      pregunta: {
        enunciado: "Patricia pagó con el Nequi del negocio $250.000 del mercado de la casa. ¿Dónde va?",
        opciones: ["No va en las cuentas del negocio", "Es un gasto del negocio", "Es un costo, porque es comida"],
        correcta: 0,
        retro: {
          bien: "Bien. Es plata de la casa: no va ni en costos ni en gastos del negocio.",
          mal: "Aunque sea comida, es de la casa, no para vender. No va en las cuentas del negocio."
        }
      }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "**¿Lo vendí?** Ingreso. **¿Lo necesito para hacer lo que vendo?** Costo. **¿Lo pago aunque no venda?** Gasto. **¿Es de la casa?** No va. Con cada peso en su lugar, ya puedes saber cuánto gana tu negocio."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: clasifica los movimientos de un mes de Patricia y calcula sus costos." }
};
