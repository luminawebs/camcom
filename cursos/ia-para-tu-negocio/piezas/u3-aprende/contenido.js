/* IA para tu negocio desde el celular · Unidad 3 · Aprende
   Molde: componentes/leccion-interactiva · Perfil P (ajuste de receta en curso.json) · Gancho (5 min)
   Caso: Yaneth, peluquería y uñas en Rincón de Santa Fe.
   Lo normativo (Ley 1581 de 2012, Circular Externa 002 de 2024 de la SIC) va marcado [VERIFICAR] para el abogado de la Cámara. */
window.CONTENIDO = {
  titulo: "Lo que no le cuentas a la IA",
  paso: "Aprende",
  unidad: "Unidad 3",
  notaMinima: 60,
  narracion: true,
  pantallas: [
    {
      titulo: "La lista que Yaneth iba a pegar",
      texto: "Yaneth quería mensajes de cumpleaños para sus clientas y ya tenía copiada la lista con **nombre, cédula, celular y a quién le da alergia el tinte**. Su hija la frenó a tiempo. En esta lección vas a ver qué datos no le cuentas a la IA y cómo pedirle lo mismo **sin ellos**.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Ilustración de Yaneth en su salón de belleza con un cuaderno de clientas en una mano y el celular en la otra, dudando" }
    },
    {
      titulo: "Lo que escribes puede quedar guardado",
      texto: "Lo que le escribes a un asistente de IA **viaja a los computadores de la empresa que lo hace** y puede quedar guardado. Algunas lo usan para mejorar su sistema, según cómo tengas los ajustes. [VERIFICAR políticas de las apps más usadas]\nUna regla sencilla: **no le escribas a la IA nada que no publicarías en una cartelera**.",
      pregunta: {
        enunciado: "¿Qué pasa con lo que escribes en un asistente de IA?",
        opciones: ["Se borra apenas cierras la app", "Puede quedar guardado en los servidores de la empresa que hace el asistente", "Solo lo puedes ver tú, siempre"],
        correcta: 1,
        retro: {
          bien: "Así es. Por eso lo que no publicarías tampoco va en la IA.",
          mal: "No se borra solo ni es siempre privado: puede quedar guardado en los servidores de la empresa del asistente."
        }
      }
    },
    {
      titulo: "El semáforo de datos",
      texto: "**Rojo, nunca:** cédulas, claves, números de cuenta o tarjeta, fotos de documentos y **datos de salud** de tus clientes, como una alergia, que la ley llama **datos sensibles**. [VERIFICAR con el abogado: Ley 1581 de 2012, art. 5]\n**Amarillo, quítalos antes:** nombres, celulares y direcciones de clientes.\n**Verde, tranquilo:** lo público de tu negocio: productos, precios, horario, barrio.",
      medio: { tipo: "imagen", src: "medios/ilustracion-3.jpg", alt: "Ilustración de un semáforo: en rojo una cédula, una llave y una tarjeta; en amarillo una libreta de contactos; en verde una tienda y una etiqueta de precio" },
      pregunta: {
        enunciado: "¿Cuál de estos datos va en rojo: nunca a la IA?",
        opciones: ["El horario de la peluquería", "El precio del manicure", "Que una clienta es alérgica al tinte"],
        correcta: 2,
        retro: {
          bien: "Exacto. Es un dato de salud de una persona: es sensible y no va en la IA.",
          mal: "El horario y los precios son públicos: van en verde. La alergia de una clienta es un dato de salud, sensible: nunca va."
        }
      }
    },
    {
      titulo: "Pide lo mismo, sin datos personales",
      texto: "La IA no necesita saber **quién** es la clienta para escribir un buen mensaje. Cambia los nombres por **«Clienta 1»** o deja **[nombre]** para ponerlo tú al enviarlo. Yaneth pidió: «Tengo una peluquería en Soacha. Escribe un mensaje de cumpleaños corto y cariñoso para una clienta que viene cada mes a arreglarse las uñas. Deja [nombre] para ponerlo yo». El resultado fue igual de bueno.",
      medio: { tipo: "imagen", src: "medios/ilustracion-4.jpg", alt: "Pantalla simplificada del asistente: el pedido de Yaneth sin datos personales y un mensaje de cumpleaños con el espacio [nombre]" },
      pregunta: {
        enunciado: "¿Cuál pedido es seguro?",
        opciones: ["«Escribe un saludo para María Pérez, cédula 1.012…, celular 310…»", "«Escribe un saludo de cumpleaños para una clienta que viene cada mes. Deja [nombre] para ponerlo yo»", "«Te paso la lista de mis clientas para que les escribas a todas»"],
        correcta: 1,
        retro: {
          bien: "Así es. No dice quién es la clienta y el mensaje sale igual de bueno.",
          mal: "Ese pedido le entrega a la IA datos personales de tus clientas. Cámbialos por [nombre] o «Clienta 1»."
        }
      }
    },
    {
      titulo: "Revisa los ajustes y cuida a tus clientes",
      texto: "Entra a los **ajustes** de tu asistente y busca la opción de **no usar tus chats para mejorar el modelo**; en cada app se llama distinto. [VERIFICAR rutas en cada app] Borra los chats que tengan datos de clientes.\nY recuerda: los datos de tus clientes los usas **solo para lo que ellos te autorizaron**. Antes de mandarles saludos o promociones, pregúntales si los quieren recibir. [VERIFICAR con el abogado: Ley 1581 de 2012 y Circular Externa 002 de 2024 de la SIC]",
      medio: { tipo: "imagen", src: "medios/ilustracion-5.jpg", alt: "Pantalla simplificada de los ajustes de un asistente de IA: controles de datos con la opción de mejorar el modelo apagada" }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "Lo que escribes en la IA puede quedar guardado: no pongas nada que no publicarías. Nunca pongas cédulas, claves, números de cuenta ni datos de salud de tus clientes. Cambia nombres y números por «Clienta 1» o [nombre]: la IA te ayuda igual."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: en el simulador vas a revisar los ajustes de privacidad del asistente y a elegir el pedido seguro de Yaneth." }
};
