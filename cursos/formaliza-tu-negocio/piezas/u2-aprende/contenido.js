/* Formaliza tu negocio paso a paso · Unidad 2 · Aprende
   Molde: componentes/leccion-interactiva · Perfil N · Gancho (5 min)
   Caso: Yuli, uñas y peinados a domicilio en Ciudad Latina.
   Cifras normativas en "datos" para actualizarlas cada año. */
window.CONTENIDO = {
  titulo: "Tu RUT en 15 minutos",
  paso: "Aprende",
  unidad: "Unidad 2",
  notaMinima: 60,
  narracion: true,
  datos: { anio: "2026", uvt: "$52.374", topeIva: "3.500 UVT [VERIFICAR tope con el contador]", ciiuTienda: "4711 [VERIFICAR código con la DIAN]" },
  pantallas: [
    {
      titulo: "Un trabajo fijo que espera un papel",
      texto: "A Yuli le ofrecen trabajo fijo en un salón de belleza, pero le piden el RUT para pagarle. Una vecina le dijo que cuesta plata y que hay que hacer fila. No es así: el RUT se saca **gratis** y **desde el celular**. Vamos paso a paso.",
      medio: { tipo: "imagen", src: "", nota: "Ilustración: Yuli con el celular en la mano y su maletín de manicure (4:3, máx. 150 KB)." }
    },
    {
      titulo: "Qué es el RUT",
      texto: "El RUT es el **Registro Único Tributario** de la DIAN. Dice quién eres, dónde trabajas y a qué te dedicas. Al sacarlo te dan un **NIT**: es tu número de cédula con un dígito de verificación al final. El RUT **no vence**: solo lo actualizas si cambias de dirección, celular o actividad.",
      medio: { tipo: "imagen", src: "", nota: "Ejemplo de NIT: número de cédula + guion + dígito de verificación, con flechas que explican cada parte." }
    },
    {
      titulo: "Lo que necesitas antes de empezar",
      texto: "**1.** Tu cédula y fotos claras de las dos caras.\n**2.** Una selfie.\n**3.** Un correo que revises y tu celular.\n**4.** La dirección donde trabajas.\n**5.** La actividad de tu negocio. Cada actividad tiene un código, el **CIIU**. Por ejemplo, una tienda de barrio usa el {{ciiuTienda}}. Si no sabes el tuyo, búscalo en la página de la DIAN o pregunta en la Cámara.",
      pregunta: {
        enunciado: "¿Cuánto le cobra la DIAN a Yuli por sacar su RUT?",
        opciones: ["Nada: la inscripción es gratis", "Una UVT ({{uvt}} en {{anio}})", "Depende de cuánto gane al mes"],
        correcta: 0,
        retro: {
          bien: "Así es. La DIAN no cobra por inscribirte, por las copias ni por actualizar el RUT.",
          mal: "La inscripción en el RUT es gratis. Si alguien te cobra por sacarlo, desconfía."
        }
      }
    },
    {
      titulo: "El paso a paso en línea",
      texto: "**1.** Entra a la página de la DIAN y busca **Inscripción en el RUT**.\n**2.** Elige **Persona natural** y escribe tu cédula.\n**3.** Llena tus datos, tu dirección y la actividad (CIIU).\n**4.** Sube las fotos de la cédula y la selfie.\n**5.** Escribe el código que te llega al correo.\n**6.** Descarga tu RUT en PDF y guárdalo en el celular.",
      medio: { tipo: "imagen", src: "", nota: "Seis pantallas del celular, una por paso, con el botón a tocar resaltado en rojo." }
    },
    {
      titulo: "Las responsabilidades del RUT",
      texto: "En el RUT aparecen tus **responsabilidades**: lo que la DIAN espera de ti. Muchos negocios pequeños quedan como **no responsables de IVA**, si sus ingresos del año no pasan de {{topeIva}}. Si tienes dudas sobre lo que te quedó, muéstrale tu RUT a un contador o en la Cámara de Comercio.",
      pregunta: {
        enunciado: "Yuli ya tiene RUT y se pasa a vivir a otro barrio. ¿Qué hace?",
        opciones: ["Actualiza el RUT con la nueva dirección, gratis", "Saca un RUT nuevo", "Nada: el RUT no se puede cambiar"],
        correcta: 0,
        retro: {
          bien: "Correcto. El RUT es uno solo y no vence; cuando cambian tus datos, lo actualizas.",
          mal: "Cada persona tiene un solo RUT y no vence. Si cambian tus datos, lo actualizas en línea, sin costo."
        }
      }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "El RUT se saca gratis en la página de la DIAN, con tu cédula, una selfie y tu correo. Tu NIT es tu cédula con un dígito de verificación. El RUT no vence: lo actualizas cuando cambian tus datos."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: responde unas preguntas y mira qué te toca hacer con tu RUT." }
};
