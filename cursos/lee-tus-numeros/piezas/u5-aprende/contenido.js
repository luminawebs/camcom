/* Lee tus números · Unidad 5 · Aprende (tramo del Pase)
   Molde: componentes/leccion-interactiva · Perfil K
   Caso: Óscar, tienda de mascotas en Ciudad Verde. Cifras del caso inventadas para enseñar. */
window.CONTENIDO = {
  titulo: "Tu flujo de efectivo",
  paso: "Aprende",
  unidad: "Unidad 5",
  notaMinima: 60,
  narracion: true,
  pantallas: [
    {
      titulo: "Ganó, pero no le alcanzó",
      texto: "El estado de resultados de octubre le dio utilidad a Óscar. Pero el 15 de noviembre no tenía con qué pagarle al proveedor de concentrado. La respuesta está en el **flujo de efectivo**: la cuenta de **la plata que de verdad entra y sale**.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Ilustración de Óscar en su tienda de mascotas mirando un calendario" }
    },
    {
      titulo: "Ganancia no es lo mismo que plata",
      texto: "**Lo que fiaste** este mes es venta, pero todavía no es plata.\n**Lo que te pagaron de fiados** del mes pasado es plata, pero no es venta de este mes.\n**La cuota del préstamo** saca plata del negocio.\n**Un equipo nuevo** saca mucha plata de una vez, aunque te sirva muchos meses.",
      medio: { tipo: "imagen", src: "medios/ilustracion-2.jpg", alt: "Un tubo por donde entra y sale plata, con un tanque que muestra cuánto queda" }
    },
    {
      titulo: "El flujo de Óscar en octubre",
      texto: "Empezó el mes con **$500.000** entre caja y Nequi. **Entradas:** ventas de contado $3.800.000 y cobros de fiados de septiembre $600.000: **$4.400.000**. **Salidas:** concentrado y accesorios $2.400.000, arriendo $800.000, servicios $150.000, su sueldo $900.000 y la cuota del préstamo $300.000: **$4.550.000**.",
      pregunta: {
        enunciado: "¿Con cuánto terminó Óscar el mes?",
        opciones: ["$350.000", "−$150.000", "$850.000"],
        correcta: 0,
        retro: {
          bien: "Correcto: $500.000 + $4.400.000 − $4.550.000 = $350.000.",
          mal: "Saldo al terminar = saldo al empezar + entradas − salidas = $500.000 + $4.400.000 − $4.550.000 = $350.000."
        }
      }
    },
    {
      titulo: "La fórmula del flujo",
      texto: "**Saldo al terminar = saldo al empezar + entradas − salidas.**\nLas ventas de octubre de Óscar fueron $4.200.000: $3.800.000 de contado y $400.000 que fió. Pero esos $400.000 **no entran al flujo** hasta que se los paguen.",
      pregunta: {
        enunciado: "Óscar le fió $120.000 de concentrado a un vecino hasta la quincena. ¿Cuándo entra al flujo?",
        opciones: ["El día que se lo fió", "El día que el vecino le pague", "Nunca"],
        correcta: 1,
        retro: {
          bien: "Así es. Es venta del día que lo fió, pero entra al flujo el día que le pagan.",
          mal: "El flujo solo cuenta la plata que entra: el fiado entra el día que te lo pagan."
        }
      }
    },
    {
      titulo: "Mira hacia adelante",
      texto: "El flujo sirve más si lo haces **antes**. Anota semana por semana lo que esperas que entre y lo que tienes que pagar en las **próximas 4 semanas**. Así ves la semana en que se juntan el arriendo y el proveedor, y puedes **cobrar fiados con fecha fija**, **pedir plazo** al proveedor o **no hacer una compra grande** esa semana. Y guarda un colchón para un mes malo."
    },
    {
      titulo: "Lo que debes recordar",
      texto: "El flujo cuenta solo la plata que entra y sale. **Saldo al terminar = saldo al empezar + entradas − salidas.** Hazlo también hacia adelante, semana por semana, para ver venir los huecos."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: calcula el saldo al terminar el mes de una tienda con la calculadora." }
};
