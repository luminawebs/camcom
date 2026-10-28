/* Facturación electrónica sin miedo · Unidad 1 · Practica
   Molde: componentes/arbol-decision · Perfil N · Gancho (8 min)
   ¿Me toca facturar? Orienta; la respuesta final la confirma un contador. */
window.CONTENIDO = {
  titulo: "¿Me toca facturar?",
  paso: "Practica",
  unidad: "Unidad 1",
  inicio: "n1",
  datos: {},
  nodos: {
    n1: {
      pregunta: "¿Vendes productos o prestas servicios de forma habitual, como negocio?",
      ayuda: "Por ejemplo: una tienda, una panadería, un taller, una peluquería o ventas por catálogo.",
      opciones: [{ texto: "Sí", ir: "n2" }, { texto: "No, fue una venta ocasional", ir: "r4" }]
    },
    n2: {
      pregunta: "¿Tienes RUT?",
      opciones: [{ texto: "Sí", ir: "n3" }, { texto: "No", ir: "r5" }]
    },
    n3: {
      pregunta: "En tu RUT, ¿dice que eres responsable de IVA o que estás en el Régimen Simple?",
      ayuda: "Mírala en la casilla de responsabilidades del RUT. Si dice «No responsable de IVA», escoge No.",
      opciones: [{ texto: "Sí", ir: "r1" }, { texto: "No", ir: "n4" }, { texto: "No sé leerlo", ir: "r3" }]
    },
    n4: {
      pregunta: "Este año o el año pasado, ¿vendiste más de 3.500 UVT, o tienes más de un local o una franquicia?",
      ayuda: "La UVT de 2026 es $52.374. Si no tienes claras tus ventas del año, escoge No sé. [VERIFICAR condiciones con el contador]",
      opciones: [{ texto: "Sí, alguna de esas", ir: "r1" }, { texto: "No, ninguna", ir: "r2" }, { texto: "No sé", ir: "r3" }]
    }
  },
  resultados: {
    r1: { titulo: "Te toca facturar", texto: "Tienes que hacer factura electrónica en cada venta. La buena noticia: la DIAN tiene un servicio **gratis** para hacerlo. En la Unidad 2 ves cómo habilitarte.", tono: "marca" },
    r2: { titulo: "Puede que no te toque, pero te conviene", texto: "Podrías ser **no obligado a facturar**, si cumples todas las condiciones de la ley. Confírmalo con un contador o en la Cámara. Aunque no te toque, facturar es gratis y te abre la puerta a clientes grandes.", tono: "ok" },
    r3: { titulo: "Confírmalo con un contador", texto: "Lleva tu RUT y una idea de cuánto vendiste este año a un contador o a la Cámara de Comercio. Con eso te dicen en cinco minutos si te toca facturar.", tono: "error" },
    r4: { titulo: "Por una venta ocasional, normalmente no", texto: "Si vendiste algo personal una vez, como tu moto, no estás facturando como negocio. Si empiezas a vender seguido, vuelve a hacer este árbol. [VERIFICAR con el contador]", tono: "ok" },
    r5: { titulo: "Primero saca tu RUT", texto: "Para facturar necesitas RUT. Se saca **gratis** en la página de la DIAN, con tu cédula, una selfie y tu correo. Lo ves paso a paso en el curso «Formaliza tu negocio».", tono: "marca" }
  },
  final: { titulo: "Ya sabes si te toca facturar", texto: "Llévalo al paso Aplica: cuéntale al grupo qué te salió y qué te frena." }
};
