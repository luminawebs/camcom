/* La plata del negocio no es la de la casa · Unidad 4 · Aprende (tramo del Pase)
   Molde: componentes/leccion-interactiva · Perfil K */
window.CONTENIDO = {
  titulo: "Registra tus ventas y gastos sin enredos",
  paso: "Aprende",
  unidad: "Unidad 4",
  notaMinima: 60,
  narracion: true,
  pantallas: [
    {
      titulo: "Todo dice «pago»",
      texto: "Luz Dary ya anota cada día lo que entra y lo que sale. Pero al final de la semana no sabe **en qué** se le fue la plata: todo dice «pago». Para decidir, no basta con saber cuánto salió; hay que saber **para qué** fue.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Cuaderno con muchas líneas iguales y una bolsa de útiles que se llevan fiada" }
    },
    {
      titulo: "Cada salida tiene su cajón",
      medio: { tipo: "imagen", src: "medios/ilustracion-2.jpg", alt: "Cinco cajas: mercancía, gastos fijos, gastos variables, tu sueldo y deudas" },
      texto: "Con 5 categorías alcanza para casi todo negocio pequeño:\n**1. Mercancía o insumos:** lo que compras para vender o producir.\n**2. Gastos fijos:** arriendo del local, servicios del local, internet, sueldo de un ayudante.\n**3. Gastos variables:** bolsas, empaques, transporte de mercancía, comisiones.\n**4. Tu sueldo:** lo que te pagas en tu fecha fija.\n**5. Deudas e inversiones:** cuotas de un crédito, una vitrina, una máquina.",
      pregunta: {
        enunciado: "Luz Dary pagó $45.000 de bolsas y empaques para las ventas de la semana. ¿En qué categoría va?",
        opciones: ["Gastos variables", "Gastos fijos", "Mercancía"],
        correcta: 0,
        retro: {
          bien: "Correcto: las bolsas suben o bajan con lo que vendes. Son un gasto variable.",
          mal: "Las bolsas suben o bajan con lo que vendes y no se revenden: son un **gasto variable**."
        }
      }
    },
    {
      titulo: "El fiado se anota aparte",
      texto: "Una venta fiada **es una venta**, pero no es plata en la cuenta. Anótala en una lista de fiados: fecha, quién, qué llevó, cuánto debe y cuándo paga. Cuando te pague, entra al registro y se tacha de la lista.\n\n**Te deben = fiados de antes + fiados nuevos − lo que te pagaron**",
      pregunta: {
        enunciado: "Le debían $120.000 de fiado. Esta semana fió $85.000 y le pagaron $40.000. ¿Cuánto le deben ahora?",
        opciones: ["$165.000", "$245.000", "$205.000"],
        correcta: 0,
        retro: {
          bien: "Correcto: $120.000 + $85.000 − $40.000 = $165.000.",
          mal: "Fiados de antes + nuevos − lo que pagaron: $120.000 + $85.000 − $40.000 = $165.000."
        }
      }
    },
    {
      titulo: "El soporte en 1 minuto",
      texto: "Cada compra deja un papel o un pantallazo: la factura del proveedor, el recibo del arriendo, el comprobante de la transferencia. Tómale foto el mismo día y guárdala en una carpeta del celular por mes, por ejemplo «Negocio · noviembre». [VERIFICAR con el contador: qué soportes guardar y por cuánto tiempo.]",
      medio: { tipo: "imagen", src: "medios/ilustracion-4.jpg", alt: "Manos tomando foto a un recibo con el celular" }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "Cada salida con su categoría. El fiado en su lista, no en la caja. Foto al soporte el mismo día. Así a fin de mes sabes en qué se fue la plata y no solo cuánto."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: separa los gastos fijos de un mes con pagos mezclados." }
};
