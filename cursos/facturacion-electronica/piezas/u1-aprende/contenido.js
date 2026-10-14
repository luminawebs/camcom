/* Facturación electrónica sin miedo · Unidad 1 · Aprende
   Molde: componentes/leccion-interactiva · Perfil N · Gancho (5 min)
   Caso: Gloria, panadería en San Mateo.
   Cifras normativas en "datos" para actualizarlas cada año. */
window.CONTENIDO = {
  titulo: "¿Qué es una factura electrónica?",
  paso: "Aprende",
  unidad: "Unidad 1",
  notaMinima: 60,
  narracion: true,
  datos: { anio: "2026", uvt: "$52.374", topeIva: "3.500 UVT [VERIFICAR tope con el contador]" },
  pantallas: [
    {
      titulo: "Una venta grande que pide un papel",
      texto: "Un colegio le quiere comprar a Gloria los refrigerios de todos los días, pero solo le paga con **factura electrónica**. Gloria cree que necesita un programa caro y un contador de planta. No es así. Vamos a ver qué es una factura electrónica y si a tu negocio le toca.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Ilustración de Gloria en el mostrador de la panadería con la rectora del colegio" }
    },
    {
      titulo: "Qué es una factura electrónica",
      texto: "Es la factura de siempre, pero hecha en el celular o el computador. Antes de llegarle a tu cliente, la **DIAN la revisa y la valida**. Cada factura lleva un **código único (CUFE)** y un **código QR** para comprobar que es real. Le llega a tu cliente al correo. No hay papel que se pierda.",
      medio: { tipo: "imagen", src: "medios/ilustracion-2.jpg", alt: "Esquema: el negocio hace la factura, la DIAN la valida y le llega al correo del cliente" }
    },
    {
      titulo: "Facturar no es pagar más impuestos",
      texto: "La factura es una **constancia de lo que vendiste**. Los impuestos dependen de lo que te quedó en el RUT y de cuánto vendes, no de si facturas. Con factura puedes **venderle a empresas, a colegios y al Estado**, que solo pagan con factura, y tienes tus ventas en orden para pedir un crédito.",
      pregunta: {
        enunciado: "Si Gloria empieza a facturar, ¿qué le pasa con los impuestos?",
        opciones: ["Nada cambia por facturar: sus impuestos dependen de su RUT y de cuánto vende", "Empieza a pagar IVA en cada factura", "Paga una multa por no haber facturado antes"],
        correcta: 0,
        retro: {
          bien: "Así es. Facturar es dejar constancia de la venta. Lo que debes de impuestos no cambia por hacer la factura.",
          mal: "Facturar no crea impuestos nuevos: deja constancia de lo que vendes. Si tienes dudas sobre tus impuestos, muéstrale tu RUT a un contador."
        }
      }
    },
    {
      titulo: "¿A quién le toca facturar?",
      texto: "**1.** A los **comerciantes**: quien compra y vende o presta servicios como negocio.\n**2.** A quien es **responsable de IVA** o está en el **Régimen Simple**.\n**3.** A los **profesionales** que cobran honorarios.\nHay excepciones, los **no obligados a facturar**. Por ejemplo, algunas personas que no son responsables de IVA y cumplen todas las condiciones de la ley, como vender menos de {{topeIva}} al año. [VERIFICAR con el contador]",
      medio: { tipo: "imagen", src: "medios/ilustracion-4.jpg", alt: "Tres íconos: tienda (comerciante), recibo con IVA y maletín (profesional)" }
    },
    {
      titulo: "Si no te toca, igual te puede convenir",
      texto: "Si eres **no obligado a facturar**, la empresa que te compra hace un **documento soporte** para poder descontar la compra. Pero muchas empresas prefieren comprarle a quien factura. Y facturar es **gratis** con el servicio de la DIAN. Si no sabes si te toca, muéstrale tu RUT a un contador o pregunta en la Cámara.",
      pregunta: {
        enunciado: "Andrés tiene una ferretería, es comerciante y es responsable de IVA. ¿Le toca facturar?",
        opciones: ["Sí: es comerciante y responsable de IVA", "No: solo facturan las empresas grandes", "Solo si el cliente se lo pide"],
        correcta: 0,
        retro: {
          bien: "Correcto. A los comerciantes y a los responsables de IVA les toca facturar cada venta.",
          mal: "No depende del tamaño ni de que el cliente la pida: a los comerciantes y a los responsables de IVA les toca facturar."
        }
      }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "La factura electrónica la valida la DIAN y le llega a tu cliente al correo, con un código único y un QR. Facturar no es pagar más impuestos. A los comerciantes y a los responsables de IVA les toca, salvo excepciones: confirma tu caso con un contador."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: responde unas preguntas sobre tu negocio y mira si te toca facturar." }
};
