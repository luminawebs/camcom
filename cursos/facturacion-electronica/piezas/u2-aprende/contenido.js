/* Facturación electrónica sin miedo · Unidad 2 · Aprende
   Molde: componentes/leccion-interactiva · Perfil N · Gancho (5 min)
   Caso: Andrés, ferretería en Quintanares.
   Los nombres de los botones del portal de la DIAN cambian: van en "datos" para corregirlos en un solo lugar. */
window.CONTENIDO = {
  titulo: "Habilítate gratis en la DIAN",
  paso: "Aprende",
  unidad: "Unidad 2",
  notaMinima: 60,
  narracion: true,
  datos: { servicio: "Facturación Gratuita DIAN [VERIFICAR nombre actual]", resp: "52 (facturador electrónico)" },
  pantallas: [
    {
      titulo: "Un cliente semanal que pide factura",
      texto: "Un contratista le quiere comprar a Andrés materiales cada semana, pero solo si le factura. Un vendedor le dijo que el programa cuesta medio millón al año. Hay otra opción: el **servicio gratuito de la DIAN**. Vamos a ver los pasos para habilitarte.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Ilustración de Andrés en su ferretería atendiendo a un contratista de obra" }
    },
    {
      titulo: "Lo que necesitas antes de empezar",
      texto: "**1.** Tu **RUT al día**, con tu dirección, celular y actividad correctos.\n**2.** Acceso al **correo que pusiste en el RUT**: ahí te llegan los códigos.\n**3.** Tu **usuario y contraseña** de la DIAN.\n**4.** Un celular o computador con internet. No necesitas comprar nada.",
      pregunta: {
        enunciado: "¿Cuánto le cobra la DIAN a Andrés por usar su servicio de facturación?",
        opciones: ["Nada: el servicio y la firma son gratis", "Medio millón al año", "Un porcentaje de cada factura"],
        correcta: 0,
        retro: {
          bien: "Así es. El servicio de facturación de la DIAN y el certificado de firma no cuestan. [VERIFICAR con el contador]",
          mal: "El servicio de la DIAN es gratis, y la firma también. Los programas privados se pagan, pero no son obligatorios."
        }
      }
    },
    {
      titulo: "Paso 1 y 2: regístrate y pide tu firma",
      texto: "**1.** Entra al portal de la DIAN con tu usuario y busca **factura electrónica · registro como facturador**.\n**2.** Escoge el servicio gratuito: **{{servicio}}**.\n**3.** Pide tu **certificado de firma digital**. Es gratis y sirve para firmar tus facturas. [VERIFICAR pasos con el contador]",
      medio: { tipo: "imagen", src: "", nota: "Captura del portal de la DIAN: registro como facturador, con el servicio gratuito resaltado en rojo." }
    },
    {
      titulo: "Paso 3: las pruebas",
      texto: "Antes de facturar de verdad, la DIAN te pide hacer unas **facturas de prueba**. Llenas unos datos de ejemplo y el sistema revisa que salgan bien. Cuando las pasas, quedas **habilitado** y tu RUT queda con la responsabilidad **{{resp}}**. También escoges desde qué fecha vas a facturar.",
      pregunta: {
        enunciado: "Andrés pasó las facturas de prueba. ¿Qué cambia en su RUT?",
        opciones: ["Queda con la responsabilidad de facturador electrónico", "Pasa a ser responsable de IVA", "Le llega un impuesto nuevo"],
        correcta: 0,
        retro: {
          bien: "Correcto. Quedas marcado como facturador electrónico. Eso no te cambia los impuestos.",
          mal: "Habilitarte solo te marca como facturador electrónico (responsabilidad 52). No te vuelve responsable de IVA ni te crea impuestos."
        }
      }
    },
    {
      titulo: "Paso 4: tu numeración",
      texto: "Cada factura lleva un número que autoriza la DIAN. Pides un **rango**, por ejemplo de la 1 a la 1.000, y le pones un **prefijo**, unas letras que van antes del número, como **FE**. Pide también un rango para **contingencia**, por si un día se cae el sistema. Con eso, ya puedes facturar.",
      medio: { tipo: "imagen", src: "medios/ilustracion-5.jpg", alt: "Ejemplo de numeración: prefijo FE + número 1 al 1.000, con el rango de contingencia aparte" }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "Con el RUT al día y tu correo, te registras como facturador con el servicio gratuito de la DIAN, pides tu firma, haces las pruebas y pides tu numeración con su prefijo. Todo es gratis y no cambia tus impuestos."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: mira en qué paso de la habilitación vas y cuál sigue." }
};
