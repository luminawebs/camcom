/* Lee tus números · Unidad 6 · Aprende (tramo del Pase)
   Molde: componentes/leccion-interactiva · Perfil K
   Caso: Patricia en la cooperativa. Cifras del caso inventadas para enseñar. */
window.CONTENIDO = {
  titulo: "Presenta tus números al banco o al contador",
  paso: "Aprende",
  unidad: "Unidad 6",
  notaMinima: 60,
  narracion: true,
  pantallas: [
    {
      titulo: "La cita del jueves",
      texto: "Patricia tiene cita en la cooperativa para pedir **$4.000.000** para la plancha. Ya tiene su estado de resultados y su balance. Le falta saber **qué más llevar**, **cómo explicar sus números** en pocos minutos y **si la cuota le cabe**.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Ilustración de Patricia frente a una asesora de la cooperativa con una carpeta" }
    },
    {
      titulo: "La carpeta del crédito",
      texto: "Lo que suelen pedir a un micronegocio (cada entidad pide distinto, pregunta antes):\n**Cédula y RUT.**\n**Certificado de matrícula mercantil** de la Cámara de Comercio, si eres comerciante formal.\n**Estado de resultados** de los últimos meses y **balance general** a la fecha.\n**Extractos** de Nequi, Daviplata o el banco de los últimos 3 a 6 meses.\n**Facturas o recibos** de las ventas y las compras grandes.",
      medio: { tipo: "imagen", src: "medios/ilustracion-2.jpg", alt: "Una carpeta abierta con documentos ordenados y separadores" }
    },
    {
      titulo: "Tus números en tres frases",
      texto: "La asesora tiene poco tiempo. Patricia lo lleva dicho así:\n**1.** «Mi negocio vende en promedio **$6.000.000** al mes.»\n**2.** «Después de pagar todo, incluido mi sueldo, le quedan **$700.000**.»\n**3.** «Cada mes me sobran **$900.000** de plata para pagar una cuota.»\nLas dos primeras salen del estado de resultados; la tercera, del flujo de efectivo.",
      pregunta: {
        enunciado: "¿De dónde sale «cada mes me sobran $900.000 para pagar una cuota»?",
        opciones: ["Del balance general", "Del flujo de efectivo: entradas menos salidas de cada mes", "De las ventas del mes"],
        correcta: 1,
        retro: {
          bien: "Correcto: es la plata que de verdad te queda cada mes, sin contar la cuota nueva.",
          mal: "Sale del flujo de efectivo: lo que entra menos lo que sale cada mes, sin la cuota nueva."
        }
      }
    },
    {
      titulo: "¿Te cabe la cuota?",
      texto: "**Peso de la cuota = cuota nueva ÷ lo que te sobra al mes × 100.**\nA 12 meses la cuota de Patricia sería de unos **$380.000** (con una tasa de ejemplo). A 24 meses, unos **$210.000**. Mientras más bajo el peso, más tranquila: si la cuota se lleva más de la mitad de lo que te sobra, un mes malo te deja sin con qué pagar.",
      pregunta: {
        enunciado: "Con la cuota de $380.000 y $900.000 que le sobran al mes, ¿cuál es el peso de la cuota?",
        opciones: ["42 %", "24 %", "58 %"],
        correcta: 0,
        retro: {
          bien: "Correcto: $380.000 ÷ $900.000 × 100 = 42 %. Cerca de la mitad: a 24 meses bajaría a 23 %.",
          mal: "$380.000 ÷ $900.000 × 100 = 42 %."
        }
      }
    },
    {
      titulo: "Antes de firmar y con el contador",
      texto: "Pregunta siempre la **tasa efectiva anual** y el **valor total** que vas a pagar, no solo la cuota. Con el **contador**, lleva la carpeta del mes (ventas, compras con factura, gastos con soporte y extractos) y pregúntale: ¿debo llevar contabilidad?, ¿qué estados necesito y con qué firma?, ¿qué impuestos me tocan?"
    },
    {
      titulo: "Lo que debes recordar",
      texto: "Lleva la carpeta completa y ordenada. Di tus números en **tres frases**: cuánto vendes, cuánto te queda y cuánto te sobra. **Peso de la cuota = cuota ÷ lo que te sobra × 100.** Pregunta la tasa efectiva anual y el total a pagar."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: calcula el peso de la cuota de un préstamo con la calculadora." }
};
