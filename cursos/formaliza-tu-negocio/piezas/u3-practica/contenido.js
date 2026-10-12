/* Formaliza tu negocio paso a paso · Unidad 3 · Practica
   Molde: componentes/arbol-decision · Perfil N · Gancho (8 min)
   ¿Qué le falta a tu local? */
window.CONTENIDO = {
  titulo: "¿Qué le falta a tu local?",
  paso: "Practica",
  unidad: "Unidad 3",
  inicio: "n1",
  datos: {},
  nodos: {
    n1: {
      pregunta: "¿Atiendes a tus clientes en un local abierto al público?",
      ayuda: "Un local puede ser también el garaje o la sala de tu casa, si la gente entra a comprar.",
      opciones: [{ texto: "Sí", ir: "n2" }, { texto: "No, voy a domicilio o vendo en línea", ir: "r1" }]
    },
    n2: {
      pregunta: "¿Tienes el concepto de uso de suelo de tu local?",
      ayuda: "Es el papel de la Alcaldía que dice que tu actividad está permitida en esa dirección.",
      opciones: [{ texto: "Sí", ir: "n3" }, { texto: "No, o no sé", ir: "r2" }]
    },
    n3: {
      pregunta: "¿Tu matrícula mercantil está renovada este año?",
      opciones: [{ texto: "Sí", ir: "n4" }, { texto: "No", ir: "r3" }]
    },
    n4: {
      pregunta: "¿Pones música, radio o televisión para tus clientes?",
      opciones: [{ texto: "Sí", ir: "r4" }, { texto: "No", ir: "n5" }]
    },
    n5: {
      pregunta: "¿Vendes o preparas alimentos o bebidas?",
      opciones: [{ texto: "Sí", ir: "r5" }, { texto: "No", ir: "r6" }]
    }
  },
  resultados: {
    r1: { titulo: "Sin local, menos papeles", texto: "Si no tienes local abierto al público, no te piden los requisitos del local. Te bastan el RUT y, si es tu negocio principal, la matrícula mercantil renovada cada año. [VERIFICAR con el asesor de la Cámara]", tono: "ok" },
    r2: { titulo: "Pide el uso de suelo", texto: "Es lo primero que revisan. Pídelo en la Alcaldía de Soacha con la dirección exacta de tu local y la actividad. [VERIFICAR dependencia, costo y requisitos en Soacha]", tono: "marca" },
    r3: { titulo: "Renueva tu matrícula", texto: "Ve a la Cámara de Comercio y ponte al día. Desde ahora, anota en tu calendario: renovar cada año entre el **1 de enero y el 31 de marzo**.", tono: "marca" },
    r4: { titulo: "Paga los derechos de autor", texto: "Si la música es para tus clientes, te toca pagar derechos de autor y guardar el comprobante en el local. Pregunta en la Cámara de Comercio a quién se paga y cuánto. [VERIFICAR entidad y tarifa]", tono: "marca" },
    r5: { titulo: "Revisa el concepto sanitario", texto: "Como vendes alimentos o bebidas, también te pueden pedir el concepto sanitario de la Secretaría de Salud. No olvides avisar la apertura a la Policía de tu zona. [VERIFICAR trámite en Soacha]", tono: "marca" },
    r6: { titulo: "Tu local está casi listo", texto: "Tienes uso de suelo y matrícula al día. Revisa que hayas avisado la apertura a la Policía de tu zona y que tu local tenga extintor y salidas despejadas.", tono: "ok" }
  },
  final: { titulo: "Ya sabes qué le falta a tu local", texto: "Llévalo al paso Aplica: ponle fecha a cada pendiente." }
};
