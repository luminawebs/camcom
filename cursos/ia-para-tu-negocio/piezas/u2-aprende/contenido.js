/* IA para tu negocio desde el celular · Unidad 2 · Aprende
   Molde: componentes/leccion-interactiva · Perfil P (ajuste de receta en curso.json) · Gancho (5 min)
   Caso: Leidy, ropa para bebé en Terreros.
   Las pantallas del asistente son simplificadas y sin marca (pantallas/armar_pantallas.py). */
window.CONTENIDO = {
  titulo: "Mensajes y descripciones que venden",
  paso: "Aprende",
  unidad: "Unidad 2",
  notaMinima: 60,
  narracion: true,
  pantallas: [
    {
      titulo: "Hasta las once de la noche escribiendo",
      texto: "Leidy vende ropa para bebé y cada prenda nueva necesita su **descripción**. Además contesta preguntas, reclamos y cobros. Se le van las noches escribiendo. Vamos a ver cómo la IA le escribe esos textos en minutos, **sin que Leidy publique algo que no es cierto**.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Ilustración de Leidy de noche en su mesa, rodeada de ropa de bebé doblada, escribiendo cansada en el celular" }
    },
    {
      titulo: "Dale tus datos reales",
      texto: "La IA escribe bien, pero **los datos los pones tú**: qué es, **material, tallas, precio**, cuidados, si haces domicilio y para quién es. Si tu asistente deja adjuntar fotos, **mándale la foto** del producto: así describe el color y la forma. Lo que no le digas, lo va a adivinar.",
      medio: { tipo: "imagen", src: "medios/ilustracion-2.jpg", alt: "Ilustración de Leidy tomándole una foto a un enterizo de bebé junto a la ventana, con luz de día" },
      pregunta: {
        enunciado: "¿Cuál pedido le da a la IA lo que necesita para la descripción?",
        opciones: ["«Describe este enterizo»", "«Vendo ropa de bebé en Soacha. Describe este enterizo de algodón, tallas 0-3 y 3-6 meses, $38.000, para mamás primerizas. Tono cálido, 3 líneas»", "«Haz que este enterizo se venda mucho»"],
        correcta: 1,
        retro: {
          bien: "Exacto. Tiene quién es, qué necesita, los datos reales del producto, para quién y cómo lo quiere.",
          mal: "Con tan poca información la IA va a inventar el material, las tallas o el precio. Dale los datos reales."
        }
      }
    },
    {
      titulo: "La IA se puede inventar cosas",
      texto: "A veces la IA **agrega datos que suenan bien pero no son ciertos**: «orgánico», «antialérgico», «garantía de un año», «envío gratis». Lo que publicas de tu producto **tiene que ser verdad**, aunque lo haya escrito la IA, y el responsable eres tú. [VERIFICAR redacción sobre Ley 1480 con el abogado]\n**Lee todo antes de publicar** y borra lo que no sea cierto.",
      medio: { tipo: "imagen", src: "medios/ilustracion-3.jpg", alt: "Pantalla simplificada del asistente: la descripción del enterizo con la frase inventada «certificado 100 % orgánico y antialérgico» marcada en rojo" },
      pregunta: {
        enunciado: "La IA escribió: «Enterizo de algodón, tallas 0-3 y 3-6 meses, $38.000, con envío gratis a todo el país». Leidy no hace envíos gratis. ¿Qué hace?",
        opciones: ["Lo publica: así vende más", "Le pide a la IA que quite el envío gratis o lo borra ella antes de publicar", "Lo publica y si alguien pregunta, explica"],
        correcta: 1,
        retro: {
          bien: "Así es. Tú respondes por lo que publicas: corrige antes de que lo vea un cliente.",
          mal: "Publicar algo que no es cierto le trae reclamos y le quita confianza. Hay que corregirlo antes de publicar."
        }
      }
    },
    {
      titulo: "Mensajes para tus clientes",
      texto: "La IA también te ayuda con los mensajes difíciles o repetidos: **una promoción, recordar un pago, responder un reclamo con calma**. Cuéntale qué pasó y qué vas a hacer tú. Por ejemplo: «Una clienta dice que el body le llegó descosido. Escríbele una respuesta amable: le pido disculpas, se lo cambio sin costo y paso a recogerlo mañana».",
      medio: { tipo: "imagen", src: "medios/ilustracion-4.jpg", alt: "Pantalla simplificada del asistente: Leidy cuenta el reclamo y la IA escribe una respuesta amable con la solución" }
    },
    {
      titulo: "Que suene como tú",
      texto: "Pídele **tu forma de hablar**: «tuteando», «cercano, como hablamos en Soacha», «sin palabras rebuscadas», «con un emoji, no más». Cuando un pedido te funcione, **guárdalo en las notas del celular** y la próxima vez solo cambias el producto. Así cada texto te toma un minuto.",
      pregunta: {
        enunciado: "Leidy ya tiene un pedido que le sirve para sus descripciones. ¿Qué le conviene?",
        opciones: ["Guardarlo en sus notas y cambiar solo los datos de cada prenda", "Escribir uno nuevo cada vez", "Dejar que la IA decida el precio de cada prenda"],
        correcta: 0,
        retro: {
          bien: "Exacto. Un pedido guardado es una plantilla: copias, cambias los datos y listo.",
          mal: "Escribir uno nuevo cada vez le quita el tiempo que quiere ahorrar, y el precio lo pone ella. Le conviene guardar el pedido y cambiar los datos."
        }
      }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "Dale a la IA tus datos reales: precio, tallas, materiales y para quién es. La IA se puede inventar cosas, así que lee y corrige todo antes de publicar. Pídele que hable como tú y guarda los pedidos que te funcionan."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: en el simulador vas a pedir la descripción del enterizo y a encontrar el dato que la IA se inventó." }
};
