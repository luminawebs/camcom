/* IA para tu negocio desde el celular · Unidad 1 · Aprende
   Molde: componentes/leccion-interactiva · Perfil P (ajuste de receta en curso.json) · Gancho (5 min)
   Caso: Nelson, ferretería en Quintanares.
   Las pantallas del asistente son simplificadas y sin marca (pantallas/armar_pantallas.py): cada app real se ve distinta. */
window.CONTENIDO = {
  titulo: "Pídele bien a la IA",
  paso: "Aprende",
  unidad: "Unidad 1",
  notaMinima: 60,
  narracion: true,
  pantallas: [
    {
      titulo: "«Eso no sirve para mi negocio»",
      texto: "Nelson escribió **«haz un aviso»** y la inteligencia artificial le devolvió un texto largo, con palabras raras y una oferta que él no tiene. No es que la IA no sirva: es que **no sabía nada de su ferretería**. En esta lección vas a ver qué decirle para que te responda algo que de verdad puedas usar.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Ilustración de Nelson detrás del mostrador de su ferretería, mirando el celular con desconfianza" }
    },
    {
      titulo: "Un asistente que escribe contigo",
      texto: "Un **asistente de IA** es una app con la que conversas por escrito o por voz: le pides un aviso, un mensaje o una idea y te responde en segundos. Hay versiones **gratis** para el celular, como ChatGPT, Gemini, Copilot o Meta AI dentro de WhatsApp. [VERIFICAR versiones gratis disponibles en Colombia]\nDos cosas claras: **no conoce tu negocio** si no se lo cuentas, y **se puede equivocar**.",
      pregunta: {
        enunciado: "¿Qué es cierto sobre un asistente de IA?",
        opciones: ["Sabe todo sobre tu negocio desde que lo instalas", "Escribe rápido, pero solo sabe lo que tú le cuentas y se puede equivocar", "Solo sirve para empresas grandes con computador"],
        correcta: 1,
        retro: {
          bien: "Así es. Te ahorra tiempo escribiendo, pero tú le das los datos y tú revisas lo que responde.",
          mal: "La IA no conoce tu negocio ni es solo para empresas grandes: funciona en el celular, pero solo sabe lo que tú le cuentas y se puede equivocar."
        }
      }
    },
    {
      titulo: "Por qué el aviso de Nelson salió mal",
      texto: "«Haz un aviso» son tres palabras. La IA no sabía **qué vende Nelson, dónde queda, para quién era el aviso ni dónde lo iba a publicar**. Entonces rellenó con lo que suena a publicidad: palabras grandes y ofertas inventadas. Cuando la IA no tiene tus datos, **adivina**.",
      medio: { tipo: "imagen", src: "medios/ilustracion-2.jpg", alt: "Pantalla simplificada de un asistente de IA: el pedido «haz un aviso» y una respuesta larga y genérica con una oferta inventada" }
    },
    {
      titulo: "Las 4 partes de un buen pedido",
      texto: "**1. Quién eres:** «Tengo una ferretería en Quintanares, Soacha».\n**2. Qué necesitas:** «Escribe un aviso para el grupo de WhatsApp del barrio».\n**3. Para quién:** «Para vecinos que arreglan la casa el fin de semana».\n**4. Cómo lo quieres:** «Corto, 4 líneas, amable, con el horario del sábado de 7 a. m. a 6 p. m.».",
      medio: { tipo: "imagen", src: "medios/ilustracion-3.jpg", alt: "Pantalla simplificada del asistente: el pedido de Nelson con las 4 partes y un aviso corto y claro para el barrio" },
      pregunta: {
        enunciado: "Nelson pidió: «Escribe un aviso de pintura para vecinos de Quintanares, corto y amable». ¿Qué parte le falta?",
        opciones: ["Para quién es", "Cómo lo quiere", "Quién es él: su ferretería y qué vende"],
        correcta: 2,
        retro: {
          bien: "Exacto. Sin decir que es una ferretería ni qué tiene, la IA va a inventar marcas, precios o productos.",
          mal: "Ya dice para quién (vecinos de Quintanares) y cómo (corto y amable). Le falta contar quién es: su ferretería y qué vende."
        }
      }
    },
    {
      titulo: "Conversa: la primera respuesta no es la última",
      texto: "Si la respuesta no te gusta, **no empieces de cero: pídele cambios**. «Más corto». «Más cercano, como hablamos en Soacha». «Dame tres opciones». «Ahora para Facebook». También puedes hablarle con el micrófono mientras atiendes. Cada ajuste toma segundos y ahí está el tiempo que te ahorras.",
      medio: { tipo: "imagen", src: "medios/ilustracion-4.jpg", alt: "Ilustración de Nelson tranquilo en su ferretería, hablándole al celular mientras organiza la vitrina" },
      pregunta: {
        enunciado: "A Nelson el aviso le salió bien, pero muy largo para el grupo del barrio. ¿Qué hace?",
        opciones: ["Le pide en el mismo chat: «Hazlo más corto, en 4 líneas»", "Borra todo y escribe el aviso a mano", "Lo publica así, aunque sea largo"],
        correcta: 0,
        retro: {
          bien: "Eso es. La IA recuerda la conversación: con un ajuste corto tienes el aviso como lo necesitas.",
          mal: "No hace falta empezar de cero ni publicar algo que no te sirve. Pídele el ajuste en el mismo chat: «Hazlo más corto»."
        }
      }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "La IA escribe por ti, pero solo sabe de tu negocio lo que tú le cuentas. Un buen pedido tiene 4 partes: quién eres, qué necesitas, para quién y cómo lo quieres. Y si la respuesta no te sirve, conversa: pídele que la cambie."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: en el simulador vas a pedirle a la IA el aviso de Nelson, paso a paso." }
};
