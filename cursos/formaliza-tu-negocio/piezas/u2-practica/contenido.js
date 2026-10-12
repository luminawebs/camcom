/* Formaliza tu negocio paso a paso · Unidad 2 · Practica
   Molde: componentes/arbol-decision · Perfil N · Gancho (8 min)
   ¿Qué hago con mi RUT? */
window.CONTENIDO = {
  titulo: "¿Qué hago con mi RUT?",
  paso: "Practica",
  unidad: "Unidad 2",
  inicio: "n1",
  datos: {},
  nodos: {
    n1: {
      pregunta: "¿Ya tienes RUT?",
      opciones: [{ texto: "Sí", ir: "n3" }, { texto: "No", ir: "n2" }, { texto: "No sé", ir: "r5" }]
    },
    n2: {
      pregunta: "¿Tienes cédula de ciudadanía colombiana?",
      ayuda: "Si tienes cédula de extranjería o Permiso por Protección Temporal (PPT), el trámite cambia un poco.",
      opciones: [{ texto: "Sí", ir: "r1" }, { texto: "No, soy extranjero", ir: "r2" }]
    },
    n3: {
      pregunta: "Desde que lo sacaste, ¿cambió tu dirección, tu celular, tu correo o tu actividad?",
      opciones: [{ texto: "Sí, algo cambió", ir: "r3" }, { texto: "No, todo sigue igual", ir: "n4" }]
    },
    n4: {
      pregunta: "En tu RUT, ¿la actividad económica es la de tu negocio?",
      ayuda: "Mira el código de actividad (CIIU) en tu RUT y su nombre. Por ejemplo, si tienes una tienda y dice otra cosa, no coincide.",
      opciones: [{ texto: "Sí, coincide", ir: "r4" }, { texto: "No, o no sé", ir: "r3" }]
    }
  },
  resultados: {
    r1: { titulo: "Sácalo hoy en línea", texto: "Entra a la página de la DIAN, elige **Inscripción en el RUT · Persona natural** y ten a la mano tu cédula, una selfie, tu correo y la dirección donde trabajas. Es gratis y toma unos 15 minutos.", tono: "marca" },
    r2: { titulo: "Haz el pre-RUT y pide cita", texto: "Con documento extranjero haces el pre-RUT en línea y terminas el trámite en una oficina de la DIAN, con cita. También es gratis. [VERIFICAR pasos actuales con la DIAN]", tono: "marca" },
    r3: { titulo: "Actualiza tu RUT", texto: "Entra a la DIAN con tu usuario y actualiza los datos que cambiaron, o la actividad de tu negocio. Es gratis. Descarga el RUT nuevo y guárdalo en el celular.", tono: "marca" },
    r4: { titulo: "Tu RUT está al día", texto: "Descárgalo en PDF y guárdalo en el celular: te lo van a pedir proveedores, clientes y bancos. Tu siguiente paso es la matrícula mercantil (Unidad 3).", tono: "ok" },
    r5: { titulo: "Primero averigua si ya lo tienes", texto: "Puede que lo hayas sacado para un trabajo o un crédito. Consúltalo en la página de la DIAN con tu cédula, o pregunta en la Cámara de Comercio. Si no lo tienes, sácalo en línea. [VERIFICAR nombre de la consulta en la DIAN]", tono: "error" }
  },
  final: { titulo: "Ya sabes qué hacer con tu RUT", texto: "Llévalo al paso Aplica: saca o revisa tu RUT y cuéntale al grupo cómo te fue." }
};
