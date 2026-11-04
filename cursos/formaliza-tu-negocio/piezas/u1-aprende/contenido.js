/* Formaliza tu negocio paso a paso · Unidad 1 · Aprende
   Molde: componentes/leccion-interactiva · Perfil N · Gancho (5 min)
   Caso hilo: Édgar, tienda de barrio en Compartir (Soacha).
   narracion: true -> cada pantalla tiene su audio en medios/narracion-N.mp3 (plantillas/narrar.py, Resemble AI). */
window.CONTENIDO = {
  titulo: "¿Qué es estar formal?",
  paso: "Aprende",
  unidad: "Unidad 1",
  notaMinima: 60,
  narracion: true,
  datos: {},
  pantallas: [
    {
      titulo: "Édgar quiere crecer, pero le piden papeles",
      texto: "Édgar tiene una tienda en Compartir hace ocho años. Un distribuidor le ofrece surtir **a crédito**, pero le pide RUT y matrícula mercantil. Édgar no tiene ninguno y cree que registrarse es empezar a pagar impuestos. En esta lección vas a ver qué es de verdad estar formal.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Édgar en el mostrador de su tienda hablando con el distribuidor" }
    },
    {
      titulo: "Los 3 pasos de la formalización",
      texto: "**1. RUT, en la DIAN:** dice quién eres para los impuestos. Es gratis.\n**2. Matrícula mercantil, en la Cámara de Comercio:** registra a la persona y a su negocio. Se renueva cada año.\n**3. Requisitos del local, ante la Alcaldía y la Policía:** que tu local pueda funcionar donde está.",
      medio: { tipo: "imagen", src: "medios/ilustracion-2.jpg", alt: "La ruta: documento, edificio de la Cámara y local" }
    },
    {
      titulo: "El RUT no es un impuesto",
      texto: "Tener RUT **no** significa pagar impuestos al mes siguiente. El RUT es un registro: dice quién eres y a qué te dedicas. Si te toca declarar o cobrar IVA depende de cuánto vendes y cuánto ganas, no de tener RUT. Para tu caso, pregúntale a un contador.",
      pregunta: {
        enunciado: "Édgar saca su RUT hoy. ¿Qué pasa con los impuestos?",
        opciones: ["Nada cambia por tener RUT: depende de cuánto vende y gana", "Empieza a pagar IVA desde el mes siguiente", "Tiene que pagar por inscribirse en la DIAN"],
        correcta: 0,
        retro: {
          bien: "Exacto. El RUT es un registro gratis; los impuestos dependen de tus ventas y ganancias.",
          mal: "El RUT no cobra nada ni crea impuestos por sí solo. Lo que te toca pagar depende de cuánto vendes y ganas."
        }
      }
    },
    {
      titulo: "Lo que ganas al estar formal",
      texto: "Con RUT y matrícula puedes **comprar a crédito** a distribuidores, **venderle a empresas** que piden factura o RUT, **pedir un crédito en un banco** y no en el gota a gota, y entrar a programas de la Cámara de Comercio. En Colombia, solo **22,4 %** de los micronegocios tiene RUT (DANE, EMICRON 2024).",
      medio: { tipo: "imagen", src: "medios/ilustracion-4.jpg", alt: "Crédito con proveedor, empresa cliente, banco y programas de la Cámara" }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "Estar formal es tener tres cosas: RUT, matrícula mercantil y el local en regla. El RUT es gratis y no es un impuesto. Formal, tu negocio puede comprar a crédito, venderle a empresas y pedir crédito en un banco."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: responde unas preguntas y mira en qué paso de la ruta está tu negocio." }
};
