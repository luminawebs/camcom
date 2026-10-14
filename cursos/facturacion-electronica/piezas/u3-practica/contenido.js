/* Facturación electrónica sin miedo · Unidad 3 · Practica
   Molde: componentes/arbol-decision · Perfil N · Gancho (8 min)
   ¿Mi factura está lista? */
window.CONTENIDO = {
  titulo: "¿Tu factura está lista?",
  paso: "Practica",
  unidad: "Unidad 3",
  inicio: "n1",
  datos: {},
  nodos: {
    n1: {
      pregunta: "¿La factura ya fue enviada al cliente?",
      opciones: [{ texto: "No, la estoy haciendo", ir: "n2" }, { texto: "Sí, y encontré un error", ir: "n5" }]
    },
    n2: {
      pregunta: "¿Tienes el nombre, el NIT o la cédula y el correo de tu cliente?",
      opciones: [{ texto: "Sí, los tres", ir: "n3" }, { texto: "No me los quiere dar", ir: "r2" }, { texto: "Me falta el correo", ir: "r3" }]
    },
    n3: {
      pregunta: "¿Revisaste el NIT contra el RUT del cliente, número por número?",
      ayuda: "El error más común es un número cambiado o el dígito de verificación.",
      opciones: [{ texto: "Sí", ir: "n4" }, { texto: "No", ir: "r4" }]
    },
    n4: {
      pregunta: "¿Pusiste lo que vendiste, la cantidad, el valor y la forma de pago (contado o crédito)?",
      opciones: [{ texto: "Sí", ir: "r1" }, { texto: "Me falta algo", ir: "r5" }]
    },
    n5: {
      pregunta: "¿El cliente ya aceptó la factura o pasaron más de tres días hábiles desde que recibió el pedido?",
      ayuda: "Si no sabes, pregúntale al cliente o mira el estado de la factura en el servicio de la DIAN. [VERIFICAR con el contador]",
      opciones: [{ texto: "No, todavía no", ir: "r6" }, { texto: "Sí, o no sé", ir: "r7" }]
    }
  },
  resultados: {
    r1: { titulo: "Lista para enviar", texto: "Tu factura tiene los datos completos. Cuando la generes, el sistema le pone el **código único (CUFE) y el QR** y se la envía al correo del cliente.", tono: "ok" },
    r2: { titulo: "Factura a consumidor final", texto: "Si el cliente no da sus datos, pon «consumidor final» y el número **222222222222**. Nunca inventes datos.", tono: "marca" },
    r3: { titulo: "Pide el correo antes de facturar", texto: "La factura le llega al cliente por correo. Pídeselo antes de generarla; si es una empresa, pregunta por el correo de facturación.", tono: "marca" },
    r4: { titulo: "Revisa el NIT antes de enviar", texto: "Pide el RUT del cliente y compara el NIT número por número, con el dígito de verificación. Un minuto de revisión te ahorra una nota crédito.", tono: "error" },
    r5: { titulo: "Completa el detalle", texto: "Escribe qué vendiste, cuántos, el valor de cada uno y si es de contado o a crédito. Revisa también los impuestos si te toca cobrarlos. [VERIFICAR con el contador]", tono: "marca" },
    r6: { titulo: "Haz una nota crédito y una factura nueva", texto: "Anula la factura con una **nota crédito** asociada a ella y haz una **factura nueva** con los datos correctos. Avísale al cliente.", tono: "marca" },
    r7: { titulo: "Habla con tu cliente y con un contador", texto: "Si la factura ya fue aceptada, ya no se corrige con una nota crédito de la forma normal. Cuéntale al cliente y pide ayuda a un contador o en la Cámara. [VERIFICAR con el contador]", tono: "error" }
  },
  final: { titulo: "Ya sabes revisar tu factura", texto: "Llévalo al paso Aplica: haz tu factura de práctica y revísala con la lista de chequeo." }
};
