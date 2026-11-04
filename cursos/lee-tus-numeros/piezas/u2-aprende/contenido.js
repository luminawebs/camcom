/* Lee tus números · Unidad 2 · Aprende
   Molde: componentes/leccion-interactiva · Perfil K · Gancho (5 min)
   Caso: Óscar, tienda de mascotas en Ciudad Verde. Cifras del caso inventadas para enseñar. */
window.CONTENIDO = {
  titulo: "Junta el mes sin contar dos veces",
  paso: "Aprende",
  unidad: "Unidad 2",
  notaMinima: 60,
  narracion: true,
  pantallas: [
    {
      titulo: "Las ventas están en todas partes",
      texto: "Óscar anota el efectivo en un cuaderno, recibe por **Nequi** y les **fía** a los vecinos del conjunto. Cuando le preguntan cuánto vendió en septiembre, no sabe qué sumar. Para leer tus números, primero hay que **juntar el mes** en un solo lugar.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Ilustración de Óscar en su tienda de mascotas con un cuaderno y el celular" }
    },
    {
      titulo: "Escoge el mes y busca tus fuentes",
      texto: "Escoge un mes que ya terminó, del 1 al último día. Reúne todo lo que tengas de ese mes: el **cuaderno** o la libreta, el **historial de Nequi, Daviplata o el banco**, los recibos del **datáfono**, las **facturas** de tus proveedores y la lista de **fiados**. No tiene que estar perfecto: con eso empiezas.",
      medio: { tipo: "imagen", src: "medios/ilustracion-2.jpg", alt: "Cuaderno, celular con pagos y recibos que se juntan en una sola hoja" }
    },
    {
      titulo: "Las ventas del mes",
      texto: "Suma **todo lo que vendiste** en el mes: el efectivo del cuaderno, lo que te pagaron por transferencia y **lo que fiaste ese mes**, aunque te lo paguen después. La venta se cuenta el día que la haces. Cuando el vecino te pague el fiado el mes siguiente, **no la vuelvas a sumar**. [VERIFICAR con el contador]",
      pregunta: {
        enunciado: "En septiembre Óscar le fió a un vecino $80.000 de concentrado, y se los pagó el 5 de octubre. ¿En qué mes cuenta esa venta?",
        opciones: ["En septiembre, cuando la hizo", "En octubre, cuando le pagaron", "En los dos meses"],
        correcta: 0,
        retro: {
          bien: "Así es. La venta se hizo en septiembre. En octubre solo le pagaron una venta que ya estaba contada.",
          mal: "La venta se cuenta el mes en que la hiciste: septiembre. Si la sumas también en octubre, la cuentas dos veces."
        }
      }
    },
    {
      titulo: "No cuentes dos veces",
      texto: "A veces Óscar pasa plata **de la caja a su Nequi** para pagarle al proveedor. Esa plata ya estaba en las ventas en efectivo: si la sumas otra vez cuando llega al Nequi, la cuentas **dos veces**. Lo mismo con un **préstamo** o la plata que **pones de tu bolsillo**: entran, pero no son ventas.",
      pregunta: {
        enunciado: "Óscar vendió $3.000.000 en efectivo y le entraron $2.000.000 al Nequi. De esos, $500.000 los pasó él mismo de la caja. ¿Cuánto vendió?",
        opciones: ["$4.500.000", "$5.000.000", "$5.500.000"],
        correcta: 0,
        retro: {
          bien: "Correcto: $3.000.000 + ($2.000.000 − $500.000) = $4.500.000. El traslado ya estaba en el efectivo.",
          mal: "Los $500.000 que pasó de la caja ya estaban en el efectivo. Ventas = $3.000.000 + $2.000.000 − $500.000 = $4.500.000."
        }
      }
    },
    {
      titulo: "Los costos y los gastos del mes",
      texto: "Haz lo mismo con lo que pagaste: suma las **compras de mercancía** que vendiste (costos) y los **pagos para tener abierto** (gastos) del mes, con las facturas y los recibos. Si pagaste algo **de dos meses** de una vez, como el arriendo, pon en cada mes solo lo que le toca. Y deja fuera lo de la casa.",
      medio: { tipo: "imagen", src: "medios/ilustracion-5.jpg", alt: "La hoja del mes de Óscar: ventas, costos y gastos de septiembre" }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "**Ventas del mes = efectivo + transferencias + fiado del mes − lo que no es venta.** Junta el mes en una sola hoja, cuenta cada venta una sola vez y separa costos y gastos. Desde hoy, anota todo en un mismo lugar: el mes siguiente será más fácil."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: calcula las ventas de un mes de Óscar sin contar nada dos veces." }
};
