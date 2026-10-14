/* Facturación electrónica sin miedo · Unidad 3 · Aprende
   Molde: componentes/leccion-interactiva · Perfil N · Gancho (5 min)
   Caso: Doris, almuerzos corrientes en el centro de Soacha. */
window.CONTENIDO = {
  titulo: "Tu primera factura, sin errores",
  paso: "Aprende",
  unidad: "Unidad 3",
  notaMinima: 60,
  narracion: true,
  datos: { consumidorFinal: "222222222222" },
  pantallas: [
    {
      titulo: "Un NIT mal escrito",
      texto: "Doris le hizo su primera factura a una empresa de vigilancia, pero escribió mal el NIT. La contadora se la devolvió. Doris no sabe si borrarla, hacer otra o pagar una multa. Vamos a ver qué lleva una factura y qué hacer si te equivocas.",
      medio: { tipo: "imagen", src: "", nota: "Ilustración de Doris en su restaurante revisando una factura en el celular." }
    },
    {
      titulo: "Los datos que pides antes de facturar",
      texto: "**1.** El **nombre completo** o la razón social de tu cliente.\n**2.** Su **NIT o cédula**. Si es empresa, pídele el RUT.\n**3.** Su **correo**: ahí le llega la factura.\n**4.** Si no te quiere dar sus datos, factura a **consumidor final** con el número **{{consumidorFinal}}**.",
      pregunta: {
        enunciado: "Un señor compra un almuerzo y no quiere dar sus datos. ¿Cómo factura Doris?",
        opciones: ["A «consumidor final», con el número {{consumidorFinal}}", "No puede venderle", "Inventa un nombre y una cédula"],
        correcta: 0,
        retro: {
          bien: "Así es. Cuando el cliente no da sus datos, la factura va a consumidor final con ese número.",
          mal: "Nunca inventes datos. Si el cliente no da sus datos, facturas a consumidor final con el número {{consumidorFinal}}."
        }
      }
    },
    {
      titulo: "Lo que lleva tu factura",
      texto: "Tu factura dice **factura electrónica de venta** y lleva: **tus datos** y tu NIT, **los del cliente**, tu **número autorizado** con el prefijo, la **fecha y la hora**, **lo que vendiste** con cantidad y valor, los impuestos si te toca cobrarlos, la **forma de pago**, y el **código único (CUFE) con el QR**, que pone el sistema. [VERIFICAR lista con el contador]",
      medio: { tipo: "imagen", src: "", nota: "Factura de ejemplo con cada parte señalada en rojo: datos, numeración, detalle, total, CUFE y QR." }
    },
    {
      titulo: "Si te equivocas: nota crédito",
      texto: "Una factura **no se borra**. Si te equivocaste en un dato o en el valor, haces una **nota crédito** que anula la factura (o la parte que estaba mal) y después una **factura nueva** con los datos correctos. Hazlo apenas te des cuenta: si el cliente ya aceptó la factura, ya no se puede corregir así. [VERIFICAR con el contador]",
      pregunta: {
        enunciado: "Doris escribió mal el NIT de la empresa. ¿Qué hace?",
        opciones: ["Hace una nota crédito y una factura nueva con el NIT bien", "Borra la factura del sistema", "Paga una multa a la DIAN"],
        correcta: 0,
        retro: {
          bien: "Correcto. La nota crédito anula la factura con el error y la nueva queda bien. No hay multa por corregir a tiempo.",
          mal: "Las facturas no se borran. Se anulan con una nota crédito y se hace una nueva con los datos correctos."
        }
      }
    },
    {
      titulo: "Si se cae el sistema",
      texto: "Si un día no hay internet o falla el servicio, no dejes de vender: usa tu **factura de contingencia**, con el rango que pediste para eso. Cuando vuelva el sistema, la pasas a la DIAN. Y recuerda: no facturar estando obligado puede traer el **cierre del negocio**. [VERIFICAR plazos con el contador]",
      medio: { tipo: "imagen", src: "", nota: "Talonario de contingencia junto al celular sin señal." }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "Antes de facturar, pide el nombre, el NIT o la cédula y el correo de tu cliente; si no te los da, factura a consumidor final. Tu factura lleva tu numeración, la fecha, lo que vendiste, el valor y el código único con el QR. Si te equivocas, haces una nota crédito y una factura nueva."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: revisa una factura y mira si está lista para enviar." }
};
