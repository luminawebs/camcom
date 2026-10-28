/* Lee tus números · Unidad 3 · Aprende
   Molde: componentes/leccion-interactiva · Perfil K · Gancho (5 min)
   Caso: Marisol, papelería en León XIII. Cifras del caso inventadas para enseñar. */
window.CONTENIDO = {
  titulo: "Tu estado de resultados en una hoja",
  paso: "Aprende",
  unidad: "Unidad 3",
  notaMinima: 60,
  narracion: true,
  datos: { norma: "Decreto 2420 de 2015, Anexo 3, párrafo 3.8 [VERIFICAR con el contador]" },
  pantallas: [
    {
      titulo: "Vender más no siempre es ganar más",
      texto: "En febrero Marisol vendió el doble que en un mes normal, pero casi no le quedó plata. Para entender por qué, necesita una hoja que le muestre **cuánto vendió, cuánto le costó y cuánto le quedó**. Esa hoja se llama **estado de resultados**, o también **P y G** (pérdidas y ganancias).",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Ilustración de Marisol en su papelería revisando una hoja con números" }
    },
    {
      titulo: "Las líneas del estado de resultados",
      texto: "Se lee de arriba hacia abajo, restando:\n**1. Ventas** del mes.\n**2. Menos el costo de lo vendido:** lo que te costó la mercancía o los insumos de lo que vendiste.\n**= Utilidad bruta.**\n**3. Menos los gastos:** arriendo, servicios, sueldos (el tuyo también), tóner, publicidad.\n**= Utilidad del mes.** Si da negativo, es una **pérdida**.",
      medio: { tipo: "imagen", src: "medios/ilustracion-4.jpg", alt: "Escalera que baja: ventas, menos costos, menos gastos, y abajo lo que queda" }
    },
    {
      titulo: "Hagamos el de Marisol",
      texto: "En un mes normal Marisol vende **$4.500.000**. La mercancía que vendió le costó **$2.250.000**: utilidad bruta de **$2.250.000**. Sus gastos: arriendo $700.000, servicios $200.000, tóner y mantenimiento $100.000 y su sueldo $800.000, en total **$1.800.000**. Utilidad del mes: $2.250.000 − $1.800.000 = **$450.000**.",
      pregunta: {
        enunciado: "Si Marisol no anota su sueldo, la hoja diría que ganó $1.250.000. ¿Es cierto?",
        opciones: ["No: $800.000 de eso son el pago de su trabajo", "Sí: el negocio ganó $1.250.000", "Depende del mes"],
        correcta: 0,
        retro: {
          bien: "Así es. Si no cuentas tu sueldo, la utilidad parece mayor, pero incluye el pago de tu trabajo.",
          mal: "Tu trabajo también cuesta. Si no incluyes tu sueldo, la utilidad se ve mayor, pero en realidad es el pago de tu trabajo."
        }
      }
    },
    {
      titulo: "El margen: de cada 100, ¿cuánto te queda?",
      texto: "El **margen** es la utilidad dividida entre las ventas, por 100. Te dice cuántos pesos te quedan de cada 100 que vendes.\n**Margen = Utilidad ÷ Ventas × 100.**\nEn febrero Marisol vendió $9.000.000 y le quedaron $270.000: su margen fue del **3 %**. En un mes normal es del 10 %: vendió la mitad, pero le quedó más. Compara tu margen mes a mes.",
      pregunta: {
        enunciado: "Un negocio vendió $5.000.000 y su utilidad fue $500.000. ¿Cuál es su margen?",
        opciones: ["10 %", "50 %", "5 %"],
        correcta: 0,
        retro: {
          bien: "Correcto: $500.000 ÷ $5.000.000 × 100 = 10 %. De cada $100 que vende, le quedan $10.",
          mal: "Margen = utilidad ÷ ventas × 100 = $500.000 ÷ $5.000.000 × 100 = 10 %."
        }
      }
    },
    {
      titulo: "Para qué te sirve",
      texto: "Con tu estado de resultados puedes **pedir un crédito** mostrando lo que gana tu negocio, **subir un precio** que no te deja nada y **comparar** un mes con otro. Si eres comerciante, la ley te pide llevar contabilidad, y el estado de resultados es uno de los estados que prepara una microempresa ({{norma}}). Un contador te ayuda a hacerlo oficial.",
      medio: { tipo: "imagen", src: "medios/ilustracion-5.jpg", alt: "El estado de resultados de un mes normal de Marisol, con utilidad de $450.000 y margen del 10 %" }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "**Utilidad del mes = Ventas − Costo de lo vendido − Gastos.** Incluye tu sueldo en los gastos. **Margen = Utilidad ÷ Ventas × 100.** Vender más no siempre es ganar más: mira cuánto te queda."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: calcula la utilidad del mes de una papelería con la calculadora." }
};
