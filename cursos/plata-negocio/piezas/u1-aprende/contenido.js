/* La plata del negocio no es la de la casa · Unidad 1 · Aprende
   Molde: componentes/leccion-interactiva · Perfil K · Gancho (5 min)
   Caso hilo: Luz Dary, miscelánea y papelería en León XIII (Soacha). */
window.CONTENIDO = {
  titulo: "¿Dónde está la plata del negocio?",
  paso: "Aprende",
  unidad: "Unidad 1",
  notaMinima: 60,
  datos: {},
  pantallas: [
    {
      titulo: "Vendes todos los días, pero no sabes si ganas",
      texto: "Luz Dary vende cerca de **$300.000 al día** en su miscelánea. Al final del mes casi nunca le queda plata para surtir. No es que venda poco: la plata sale del cajón por muchos lados y nadie la anota. En esta lección vas a ver por dónde se va.",
      medio: { tipo: "imagen", src: "", nota: "Ilustración: Luz Dary detrás del mostrador mirando el cajón casi vacío (4:3, máx. 150 KB)." }
    },
    {
      titulo: "Las 4 fugas más comunes",
      texto: "**1. El cajón para la casa:** sacas para el mercado, el arriendo o las onces sin anotarlo.\n**2. Pagos cruzados:** pagas la luz de la casa con la plata del negocio, o la mercancía con tu tarjeta personal.\n**3. Lo que consumes:** el cuaderno, la gaseosa o el regalo que tomas del negocio.\n**4. El celular personal:** los clientes te pagan al mismo Nequi o Daviplata donde te llega la plata de la familia.",
      medio: { tipo: "imagen", src: "", nota: "Infografía vertical con las 4 fugas e íconos (cajón, factura, producto, celular)." }
    },
    {
      titulo: "Una venta no es una ganancia",
      texto: "Si vendes un cuaderno en $5.000 y te costó $3.500, solo **$1.500** son ganancia. Los otros $3.500 son del proveedor: los necesitas para volver a surtir. Cuando sacas la venta completa para la casa, te estás gastando la plata de la mercancía.",
      pregunta: {
        enunciado: "Luz Dary vende un bloc en $8.000. Le costó $5.000. ¿Cuánto puede llevarse para la casa sin dañar el negocio?",
        opciones: ["Máximo $3.000, que es la ganancia", "Los $8.000, porque ya lo vendió", "$5.000, porque es lo que pagó"],
        correcta: 0,
        retro: {
          bien: "Exacto. Los $5.000 tienen que volver a la mercancía; solo la ganancia es tuya.",
          mal: "Lo que pagaste por el producto tiene que volver al negocio para surtir. Lo tuyo es la diferencia: $8.000 − $5.000 = $3.000."
        }
      }
    },
    {
      titulo: "Cómo medir la fuga en una semana",
      texto: "No necesitas contador para saber cuánto se fue. Anota cuánto había en caja el lunes, suma lo que vendiste y resta lo que pagaste del negocio. Eso es lo que **debería** haber. Lo que falta para llegar ahí se fue sin anotar.\n\n**Se fue = caja inicial + ventas − pagos del negocio − caja final**",
      medio: { tipo: "imagen", src: "", nota: "La fórmula con el ejemplo de Luz Dary: $200.000 + $1.800.000 − $1.100.000 − $350.000 = $550.000 que se fueron sin anotar." }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "La plata del negocio tiene dueño: el negocio. Lo que vendes no es todo tuyo: una parte es para volver a surtir. Si no anotas lo que sacas, no puedes saber si estás ganando."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: vas a calcular cuánta plata se fue del cajón en la semana de otros negocios." }
};
