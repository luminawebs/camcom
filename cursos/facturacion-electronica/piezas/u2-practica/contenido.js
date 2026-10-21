/* Facturación electrónica sin miedo · Unidad 2 · Practica
   Molde: componentes/arbol-decision · Perfil N · Gancho (8 min)
   ¿En qué paso de la habilitación vas? */
window.CONTENIDO = {
  titulo: "¿En qué paso vas?",
  paso: "Practica",
  unidad: "Unidad 2",
  inicio: "n1",
  datos: {},
  nodos: {
    n1: {
      pregunta: "¿Tu RUT tiene bien tu dirección, tu celular, tu correo y la actividad de tu negocio?",
      opciones: [{ texto: "Sí", ir: "n2" }, { texto: "No, o no sé", ir: "r1" }]
    },
    n2: {
      pregunta: "¿Puedes entrar al correo que pusiste en el RUT y a tu usuario de la DIAN?",
      ayuda: "Si no recuerdas la contraseña de la DIAN, la puedes recuperar con ese mismo correo.",
      opciones: [{ texto: "Sí, a los dos", ir: "n3" }, { texto: "No", ir: "r2" }]
    },
    n3: {
      pregunta: "¿Ya te registraste como facturador con el servicio gratuito y tienes tu firma?",
      opciones: [{ texto: "Sí", ir: "n4" }, { texto: "No", ir: "r3" }]
    },
    n4: {
      pregunta: "¿Ya pasaste las facturas de prueba y tienes tu numeración con prefijo?",
      opciones: [{ texto: "Sí, las dos cosas", ir: "r5" }, { texto: "Pasé las pruebas, me falta la numeración", ir: "r4" }, { texto: "No he hecho las pruebas", ir: "r6" }]
    }
  },
  resultados: {
    r1: { titulo: "Primero, pon tu RUT al día", texto: "Actualiza tu RUT en la página de la DIAN: es gratis. Revisa la dirección, el celular, el correo y la actividad. Después vuelve a este árbol.", tono: "marca" },
    r2: { titulo: "Recupera tu correo y tu usuario", texto: "Sin el correo del RUT no te llegan los códigos. Si ya no lo usas, cámbialo actualizando el RUT. Luego recupera la contraseña de la DIAN. [VERIFICAR trámite con la DIAN]", tono: "error" },
    r3: { titulo: "Regístrate y pide tu firma", texto: "Entra al portal de la DIAN, regístrate como facturador eligiendo el **servicio gratuito** y pide tu **certificado de firma**. Ponle fecha a este paso esta semana.", tono: "marca" },
    r4: { titulo: "Pide tu numeración", texto: "Pide tu rango de numeración y asócialo a un prefijo, como **FE**. Pide también un rango para contingencia. Después, ya puedes facturar.", tono: "marca" },
    r5: { titulo: "¡Ya puedes facturar!", texto: "Estás habilitado. En la Unidad 3 ves qué datos lleva tu factura y cómo hacerla sin errores.", tono: "ok" },
    r6: { titulo: "Haz las facturas de prueba", texto: "En el servicio gratuito de la DIAN busca la **habilitación** y haz las facturas de prueba. Cuando las pases, escoge la fecha desde la que vas a facturar.", tono: "marca" }
  },
  final: { titulo: "Ya sabes cuál es tu siguiente paso", texto: "Llévalo al paso Aplica: escribe tu siguiente paso con una fecha y compártelo." }
};
