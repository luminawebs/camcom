/* Vende más por WhatsApp Business · Unidad 2 · Aprende
   Molde: componentes/leccion-interactiva · Perfil P (ajuste de receta en curso.json) · Gancho (5 min)
   Caso: Camilo, accesorios para celular a domicilio en Ducales. */
window.CONTENIDO = {
  titulo: "Ningún pedido se pierde",
  paso: "Aprende",
  unidad: "Unidad 2",
  notaMinima: 60,
  narracion: true,
  pantallas: [
    {
      titulo: "Tres pedidos pagos que nadie despachó",
      texto: "Camilo tiene **más de 200 chats** abiertos. Unos clientes preguntan, otros ya le pagaron por Nequi y otros solo saludan. Un viernes se le olvidó despachar **tres pedidos que ya estaban pagos**, y uno de esos clientes lo contó en el grupo del conjunto. El problema no es vender poco: es que no sabe **en qué va cada cliente**.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Ilustración de Camilo con una caja de domicilios, mirando preocupado el celular lleno de chats" }
    },
    {
      titulo: "Qué es una etiqueta",
      texto: "Una **etiqueta** es un **color con nombre** que le pones a un chat, como un papelito pegado en una carpeta. WhatsApp Business ya trae algunas, como **Nuevo cliente, Nuevo pedido, Pago pendiente y Pagado**, y puedes cambiarles el nombre o crear las tuyas. [VERIFICAR nombres de las etiquetas que trae la app] Después tocas una etiqueta y ves **solo los chats que la tienen**.",
      medio: { tipo: "imagen", src: "medios/ilustracion-2.jpg", alt: "Pantalla simplificada de la lista de chats de Camilo, cada chat con una etiqueta de color: Nuevo pedido, Pago pendiente, Pagado" }
    },
    {
      titulo: "Las etiquetas de tus pedidos",
      texto: "No necesitas muchas. Usa las **etapas de un pedido**, en orden:\n**1.** **Nuevo pedido**: el cliente ya dijo qué quiere.\n**2.** **Pago pendiente**: le mandaste el valor y falta que pague.\n**3.** **Pagado**: ya pagó y falta entregar.\n**4.** **Entregado**: listo. Cuando el cliente avanza, le cambias la etiqueta.",
      medio: { tipo: "imagen", src: "medios/ilustracion-3.jpg", alt: "Ilustración: cuatro cajas de pedido en fila con etiquetas de colores, de un pedido nuevo hasta uno entregado" },
      pregunta: {
        enunciado: "Un cliente de Camilo le mandó el comprobante de Nequi, pero todavía no le ha llevado el cargador. ¿Qué etiqueta le pone?",
        opciones: ["Pagado", "Nuevo pedido", "Entregado"],
        correcta: 0,
        retro: {
          bien: "Correcto. Ya pagó y falta entregar: «Pagado». Así aparece en la lista de despachos del día.",
          mal: "Ya pagó, pero todavía no le ha entregado. Esa etapa es «Pagado»: así no se le olvida despacharlo."
        }
      }
    },
    {
      titulo: "Cómo poner una etiqueta",
      texto: "**Mantén presionado** el chat del cliente, toca el **ícono de etiqueta** y elige la que va. Puedes ponerle etiqueta también a un **mensaje** importante, como el del comprobante de pago. Para ver los chats de una etiqueta, tócala en la parte de arriba de tus chats o búscala en el menú de etiquetas. [VERIFICAR ruta en Android y iPhone]"
    },
    {
      titulo: "Tu rutina de 10 minutos",
      texto: "Al cerrar el día, Camilo hace dos cosas:\n**1.** Filtra **Pago pendiente**: les escribe a los que no han pagado. Ahí está **su plata por cobrar**.\n**2.** Filtra **Pagado**: arma los despachos de mañana. Ahí está **lo que no se le puede olvidar**.\nCuando entrega, cambia la etiqueta a **Entregado**.",
      pregunta: {
        enunciado: "Camilo quiere saber a quién cobrarle hoy. ¿Qué etiqueta filtra?",
        opciones: ["Pago pendiente", "Entregado", "Nuevo cliente"],
        correcta: 0,
        retro: {
          bien: "Así es. En «Pago pendiente» están los clientes que ya pidieron y todavía no pagan.",
          mal: "Los que deben están en «Pago pendiente»: ya pidieron y les mandaste el valor, pero no han pagado."
        }
      }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "Una etiqueta es un color con nombre que le pones a un chat. Usa pocas, en el orden del pedido: nuevo pedido, pago pendiente, pagado y entregado. Cada día filtra «Pago pendiente» para cobrar y «Pagado» para despachar. Así ningún pedido se pierde."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: en el simulador vas a ponerle la etiqueta a un cliente que ya pagó." }
};
