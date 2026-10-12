/* Formaliza tu negocio paso a paso · Unidad 1 · Practica
   Molde: componentes/arbol-decision · Perfil N · Gancho (8 min)
   ¿En qué paso de la ruta de formalización estás? */
window.CONTENIDO = {
  titulo: "¿En qué paso de la ruta vas?",
  paso: "Practica",
  unidad: "Unidad 1",
  inicio: "n1",
  datos: {},
  nodos: {
    n1: {
      pregunta: "¿Tu negocio tiene RUT?",
      ayuda: "El RUT es el Registro Único Tributario de la DIAN. Si alguna vez lo sacaste, tienes un documento con tu número de NIT.",
      opciones: [{ texto: "Sí", ir: "n2" }, { texto: "No", ir: "r1" }, { texto: "No sé", ir: "r1" }]
    },
    n2: {
      pregunta: "¿Vendes productos o prestas servicios todos los días, como tu trabajo principal?",
      ayuda: "Por ejemplo: una tienda, un taller, una peluquería, venta de comida o de ropa.",
      opciones: [{ texto: "Sí, es mi negocio", ir: "n3" }, { texto: "No, es algo ocasional", ir: "r2" }]
    },
    n3: {
      pregunta: "¿Tu negocio tiene matrícula mercantil en la Cámara de Comercio?",
      opciones: [{ texto: "Sí, y la renové este año", ir: "n4" }, { texto: "Sí, pero no la he renovado", ir: "r3" }, { texto: "No", ir: "r4" }]
    },
    n4: {
      pregunta: "¿Atiendes en un local abierto al público?",
      opciones: [{ texto: "Sí", ir: "r5" }, { texto: "No, voy a domicilio o vendo en línea", ir: "r6" }]
    }
  },
  resultados: {
    r1: { titulo: "Tu primer paso: el RUT", texto: "Empieza por el RUT. Es gratis y lo sacas en línea con tu cédula. En la **Unidad 2** lo haces paso a paso.", tono: "marca" },
    r2: { titulo: "Puede que no necesites matrícula", texto: "Si solo vendes de vez en cuando y no es tu trabajo principal, puede que no te toque la matrícula mercantil. Confírmalo con la Cámara de Comercio. Igual, tener RUT te sirve para que te paguen. [VERIFICAR con el asesor de la Cámara]", tono: "ok" },
    r3: { titulo: "Te toca renovar la matrícula", texto: "La matrícula mercantil se renueva cada año entre el **1 de enero y el 31 de marzo**. Si llevas años sin renovar, ve a la Cámara de Comercio a ponerte al día. En la **Unidad 3** ves cómo.", tono: "marca" },
    r4: { titulo: "Tu siguiente paso: la matrícula mercantil", texto: "Ya tienes RUT. Ahora registra tu negocio en la Cámara de Comercio con la matrícula mercantil. En la **Unidad 3** ves qué llevar y cuándo se renueva.", tono: "marca" },
    r5: { titulo: "Revisa los requisitos de tu local", texto: "Tienes RUT y matrícula al día. Te falta revisar que tu local cumpla: uso de suelo, aviso de apertura a la Policía y, si pones música, derechos de autor. Lo ves en la **Unidad 3**.", tono: "ok" },
    r6: { titulo: "¡Vas muy bien!", texto: "Tienes RUT y matrícula al día. Como no atiendes en local, no te piden los requisitos del local. Recuerda renovar la matrícula antes del 31 de marzo de cada año.", tono: "ok" }
  },
  final: { titulo: "Ya sabes en qué paso vas", texto: "Llévalo al paso Aplica: cuéntale al grupo en qué paso estás y qué te frena." }
};
