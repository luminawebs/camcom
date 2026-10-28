/* Vende más por WhatsApp Business · Unidad 1 · Aprende
   Molde: componentes/leccion-interactiva · Perfil P (ajuste de receta en curso.json) · Gancho (5 min)
   Caso: Sandra, tortas por encargo en Hogares Soacha.
   Las pantallas de la app son simplificadas (pantallas/armar_pantallas.py): la app real puede verse distinta. */
window.CONTENIDO = {
  titulo: "Tu vitrina: perfil y catálogo",
  paso: "Aprende",
  unidad: "Unidad 1",
  notaMinima: 60,
  narracion: true,
  pantallas: [
    {
      titulo: "Diez clientes, la misma pregunta",
      texto: "A Sandra le escriben todos los días para preguntar **qué tortas tiene, cuánto valen y si hace domicilio**. Ella busca las fotos en la galería y las manda una por una, entre los chats de la familia. Así se le van las horas y los clientes. Vamos a ver cómo WhatsApp Business le muestra todo eso al cliente sin que Sandra tenga que escribirlo cada vez.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Ilustración de Sandra en su cocina con tortas, mirando el celular lleno de mensajes" }
    },
    {
      titulo: "WhatsApp Business: tu negocio aparte",
      texto: "**WhatsApp Business** es una app **gratis**, distinta del WhatsApp normal, hecha para negocios pequeños. Tiene **perfil de empresa, catálogo, etiquetas y mensajes automáticos**. Puedes usarla con un número nuevo solo para el negocio, o pasar a ella tu número de siempre: al instalarla en el mismo celular, la app te ofrece traer tus chats. [VERIFICAR pasos de cambio de número en la app actual]",
      pregunta: {
        enunciado: "Sandra quiere separar sus pedidos de los chats de la familia. ¿Qué le conviene?",
        opciones: ["Usar WhatsApp Business para el negocio", "Crear un grupo con todos sus clientes", "Pagar una página web antes de vender"],
        correcta: 0,
        retro: {
          bien: "Así es. WhatsApp Business es gratis y le da perfil de empresa, catálogo y herramientas para atender a sus clientes aparte.",
          mal: "No hace falta pagar nada ni meter a todos los clientes en un grupo. WhatsApp Business es gratis y separa el negocio de lo personal."
        }
      }
    },
    {
      titulo: "Tu perfil de empresa",
      texto: "Es lo primero que ve el cliente cuando toca tu nombre. Llénalo completo:\n**1.** **Nombre** del negocio y **foto** (tu logo o tu mejor producto).\n**2.** **Categoría** y una **descripción** corta: qué vendes y para quién.\n**3.** **Dirección** o zona de domicilio y **horario**.\n**4.** Un **correo** o tu página, si tienes.",
      medio: { tipo: "imagen", src: "medios/ilustracion-3.jpg", alt: "Pantalla simplificada del perfil de empresa de Dulce Sandra: foto, categoría Repostería, descripción, dirección y horario" }
    },
    {
      titulo: "Tu catálogo es tu vitrina",
      texto: "En el **catálogo** subes cada producto con **foto, nombre, precio y descripción**. El cliente lo abre desde tu perfil y ve todo sin preguntarte. Tú también puedes mandar un producto o el catálogo completo dentro de un chat, con el clip de adjuntar. Empieza por **tus 5 productos que más se venden**.",
      medio: { tipo: "imagen", src: "medios/ilustracion-4.jpg", alt: "Pantalla simplificada del catálogo de Dulce Sandra con tortas, cada una con foto, nombre y precio" }
    },
    {
      titulo: "Fotos y textos que venden",
      texto: "Toma la foto con **luz de día**, cerca de una ventana, sobre un **fondo limpio** y con **un solo producto**. En el nombre di qué es y para cuántos: «Torta de chocolate para 12». En la descripción, lo que el cliente pregunta: **tamaño, sabor, con cuánto tiempo pedir y si llevas a domicilio**. Y siempre el **precio**.",
      medio: { tipo: "imagen", src: "medios/ilustracion-5.jpg", alt: "Ilustración: a la izquierda una foto oscura y desordenada de una torta, a la derecha la misma torta con luz natural y fondo limpio" },
      pregunta: {
        enunciado: "¿Cuál de estos productos está mejor en el catálogo?",
        opciones: ["«Torta de chocolate para 12 · $65.000 · Pídela con 2 días. Domicilio en Soacha»", "«Torta rica · Pregunta el precio»", "«Torta · $65.000»"],
        correcta: 0,
        retro: {
          bien: "Exacto. Dice qué es, para cuántos, el precio y lo que el cliente iba a preguntar. Así compra sin escribirte.",
          mal: "Al cliente le falta información y te va a escribir para preguntar. Pon qué es, para cuántos, el precio y las condiciones."
        }
      }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "WhatsApp Business es gratis y separa tu negocio de lo personal. Completa tu perfil de empresa: qué vendes, dónde y a qué hora. Arma tu catálogo con foto clara, nombre, precio y descripción de cada producto, empezando por los que más vendes."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: en el simulador vas a agregar un producto al catálogo, paso a paso." }
};
