/* Vende más por WhatsApp Business · Unidad 3 · Aprende
   Molde: componentes/leccion-interactiva · Perfil P (ajuste de receta en curso.json) · Gancho (5 min)
   Caso: Esperanza, frutas y verduras a domicilio en El Altico. */
window.CONTENIDO = {
  titulo: "Responde rápido sin vivir pegado al celular",
  paso: "Aprende",
  unidad: "Unidad 3",
  notaMinima: 60,
  narracion: true,
  pantallas: [
    {
      titulo: "Las mismas preguntas, todos los días",
      texto: "A Esperanza le llegan **unos 40 mensajes al día**: hasta qué hora atiende, si lleva a domicilio, cuánto vale el aguacate, si recibe Nequi. En la madrugada está comprando en la plaza y no alcanza a contestar. WhatsApp Business tiene tres herramientas para eso: **mensaje de bienvenida, mensaje de ausencia y respuestas rápidas**.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Ilustración de Esperanza en la plaza de mercado, con cajas de frutas y el celular sonando en el bolsillo" }
    },
    {
      titulo: "El mensaje de bienvenida",
      texto: "Sale **solo** cuando alguien te escribe **por primera vez**, o cuando vuelve a escribir después de un tiempo sin hablarte. [VERIFICAR cuántos días de inactividad usa la app] Úsalo para saludar y decir lo básico: **qué vendes, tu horario y cómo pedir**. Ejemplo: «¡Hola! Soy Esperanza, frutas y verduras a domicilio en El Altico. Mira el catálogo y dime qué necesitas.»",
      medio: { tipo: "imagen", src: "medios/ilustracion-2.jpg", alt: "Pantalla simplificada de un chat: el cliente escribe «Buenas» y llega solo el mensaje de bienvenida de Esperanza" }
    },
    {
      titulo: "El mensaje de ausencia",
      texto: "Sale **solo** cuando te escriben y **no puedes atender**: fuera de tu horario, o en las horas que tú escojas. Dice **cuándo vuelves**, para que el cliente no se vaya: «Estoy en la plaza comprando lo más fresco. Te respondo desde las 7 a. m.». Para que salga fuera de tu horario, el horario tiene que estar en tu **perfil de empresa**.",
      medio: { tipo: "imagen", src: "medios/ilustracion-3.jpg", alt: "Ilustración: un reloj y una luna junto a un celular que responde solo mientras la vendedora está ocupada" },
      pregunta: {
        enunciado: "Esperanza está en la plaza de 3 a 7 de la mañana. ¿Qué le sirve para que el cliente no se vaya?",
        opciones: ["Un mensaje de ausencia en ese horario, que diga a qué hora vuelve", "Apagar el celular", "Un mensaje de bienvenida con todo el catálogo"],
        correcta: 0,
        retro: {
          bien: "Así es. El mensaje de ausencia sale solo en ese horario y le dice al cliente cuándo le van a responder.",
          mal: "La bienvenida solo sale la primera vez. Para las horas en que no puede atender, el que sirve es el mensaje de ausencia."
        }
      }
    },
    {
      titulo: "Respuestas rápidas",
      texto: "Son **mensajes guardados** con un **atajo**. En el chat escribes **/** y eliges el que necesitas, por ejemplo **/domicilio** o **/pagos**, y lo envías en segundos. A diferencia de la bienvenida y la ausencia, **no salen solas**: tú decides cuándo mandarlas. Haz una por cada pregunta que te repiten.",
      medio: { tipo: "imagen", src: "medios/ilustracion-4.jpg", alt: "Pantalla simplificada de un chat: al escribir / aparecen las respuestas rápidas /domicilio, /horario y /pagos" }
    },
    {
      titulo: "Rápido, pero como persona",
      texto: "Escribe como si el cliente estuviera en tu mostrador: **corto, amable y con lo que necesita saber**. Saluda, usa su nombre cuando puedas y termina con una pregunta: «¿Te lo llevo hoy?». Y para mandar **promociones**, pide permiso primero: los datos de tus clientes están protegidos por la ley. [VERIFICAR con el asesor: autorización de datos, Ley 1581 de 2012]",
      pregunta: {
        enunciado: "¿Cuál respuesta rápida está mejor escrita?",
        opciones: ["«¡Hola! Llevamos a domicilio en Soacha de 7 a. m. a 6 p. m. El envío vale $3.000. ¿Qué te mandamos hoy?»", "«DOMICILIOS SOLO CON PEDIDO MINIMO»", "«Sí»"],
        correcta: 0,
        retro: {
          bien: "Exacto. Saluda, responde todo lo que el cliente iba a preguntar y lo invita a pedir.",
          mal: "Una respuesta muy corta o en mayúsculas suena brava y deja preguntas. Saluda, da los datos completos y cierra con una pregunta."
        }
      }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "La bienvenida saluda solo al cliente nuevo. La ausencia le dice cuándo vuelves si no puedes atender. Las respuestas rápidas guardan lo que más te preguntan: escribes la barra y eliges. Escribe corto, amable y con los datos completos, y pide permiso antes de mandar promociones."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: en el simulador vas a crear una respuesta rápida y a usarla en un chat." }
};
