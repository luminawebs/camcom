/* Formaliza tu negocio paso a paso · Unidad 3 · Aprende
   Molde: componentes/leccion-interactiva · Perfil N · Gancho (5 min)
   Caso: Wilson, taller de motos en El Danubio.
   Fechas y tarifas en "datos" para actualizarlas cada año. */
window.CONTENIDO = {
  titulo: "Matrícula mercantil y tu local",
  paso: "Aprende",
  unidad: "Unidad 3",
  notaMinima: 60,
  narracion: true,
  datos: { renovacion: "entre el 1 de enero y el 31 de marzo", tarifa: "según el valor de los activos de tu negocio [VERIFICAR tarifa 2026 en la Cámara de Comercio de Soacha]" },
  pantallas: [
    {
      titulo: "La visita al taller de Wilson",
      texto: "Wilson tiene un taller de motos en El Danubio. Sacó la matrícula mercantil hace cinco años, pero no la renueva desde hace tres. Pasó la Policía y le preguntó por la matrícula, el uso de suelo y la música del taller. En esta lección vas a ver qué te piden y cada cuánto.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Wilson en su taller hablando con un policía" }
    },
    {
      titulo: "La matrícula mercantil",
      texto: "Es el registro de tu negocio en la **Cámara de Comercio**. Se registran dos cosas: **tú**, como comerciante, y tu **establecimiento**: la tienda, el taller o el local. Se paga {{tarifa}}. En Soacha existe la **Cámara de Comercio de Soacha**, creada en 2023. [VERIFICAR dónde se hace hoy el trámite: Cámara de Soacha o sede de la Cámara de Bogotá]",
      medio: { tipo: "imagen", src: "medios/ilustracion-2.jpg", alt: "Wilson más su taller es igual a la matrícula mercantil" }
    },
    {
      titulo: "Se renueva cada año",
      texto: "La matrícula se renueva **todos los años, {{renovacion}}**. Si no la renuevas a tiempo, te pueden sancionar, y si pasan cinco años sin renovar, la matrícula se cancela. Antes de matricularte, consulta en el **RUES** que nadie más tenga el nombre que quieres para tu negocio.",
      pregunta: {
        enunciado: "Wilson no renueva su matrícula desde hace tres años. ¿Qué le conviene hacer?",
        opciones: ["Ir a la Cámara de Comercio a ponerse al día y renovar cada año antes del 31 de marzo", "Esperar: la matrícula sigue vigente aunque no la renueve", "Sacar una matrícula nueva con otro nombre"],
        correcta: 0,
        retro: {
          bien: "Así es. Ponerse al día evita sanciones y que la matrícula se cancele.",
          mal: "La matrícula hay que renovarla cada año. Sin renovar, pierde vigencia y a los cinco años se cancela; lo correcto es ponerse al día."
        }
      }
    },
    {
      titulo: "Lo que le piden a tu local",
      texto: "Para abrir y mantener un local, la ley pide (Ley 1801 de 2016, artículo 87):\n**1. Uso de suelo:** que tu actividad esté permitida en esa dirección. Se pide en la Alcaldía. [VERIFICAR dependencia en Soacha]\n**2. Matrícula mercantil al día.**\n**3. Avisar la apertura** a la estación de Policía de tu zona.\n**4. Condiciones de seguridad y sanidad** (bomberos y, si vendes comida, salud).\n**5. Derechos de autor** si pones música para tus clientes.",
      pregunta: {
        enunciado: "En el taller de Wilson suena la radio todo el día para los clientes. ¿Qué le aplica?",
        opciones: ["Pagar los derechos de autor por la música", "Nada, porque es un taller y no un bar", "Solo bajarle el volumen"],
        correcta: 0,
        retro: {
          bien: "Correcto. Si la música es para el público del local, se pagan derechos de autor, sea bar, tienda o taller.",
          mal: "Cuando pones música para los clientes de un local, se pagan derechos de autor, sin importar el tipo de negocio."
        }
      }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "La matrícula mercantil registra a la persona y a su negocio en la Cámara de Comercio, y se renueva cada año antes del 31 de marzo. Tu local necesita uso de suelo, matrícula al día y avisar la apertura a la Policía. Si pones música para los clientes, pagas derechos de autor."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: revisa paso a paso qué le falta a tu local." }
};
