/* Lienzo interactivo · paso PRACTICA (perfil E Estrategia)
   El estudiante completa bloques; cada bloque recibe retroalimentación al momento.
   La revisión es simple y no reemplaza al tutor: largo mínimo y palabras clave.
   "claves" acepta variantes; con que aparezca una cuenta. */
window.CONTENIDO = {
  titulo: "[Lienzo: tu cliente ideal]",
  paso: "Practica",
  unidad: "Unidad [n]",
  ejemplo: "[Caso guía: así lo llenó Doña Marta, de la panadería del barrio …]",
  bloques: [
    {
      titulo: "[Bloque 1: ¿Quién es?]",
      ayuda: "[Pregunta guía y un ejemplo corto]",
      minPalabras: 8,
      claves: ["[palabra clave 1]", "[edad]", "[barrio]"],
      retro: { bien: "[Qué hizo bien]", corto: "[Pide más detalle: describe edad, barrio, ocupación]", sinClave: "[Le falta mencionar …]" }
    },
    {
      titulo: "[Bloque 2: ¿Qué problema tiene?]",
      ayuda: "[Pregunta guía]",
      minPalabras: 8,
      claves: [],
      retro: { bien: "[Qué hizo bien]", corto: "[Pide más detalle]", sinClave: "" }
    },
    {
      titulo: "[Bloque 3: ¿Por qué te elegiría a ti?]",
      ayuda: "[Pregunta guía]",
      minPalabras: 8,
      claves: [],
      retro: { bien: "[Qué hizo bien]", corto: "[Pide más detalle]", sinClave: "" }
    },
    {
      titulo: "[Bloque 4: ¿Dónde lo encuentras?]",
      ayuda: "[Pregunta guía: canales]",
      minPalabras: 5,
      claves: ["whatsapp", "instagram", "facebook", "tienda", "google"],
      retro: { bien: "[Qué hizo bien]", corto: "[Pide más detalle]", sinClave: "[Nombra al menos un canal concreto]" }
    }
  ],
  final: { titulo: "Tu lienzo está listo", texto: "Cópialo y guárdalo. Lo vas a entregar en el paso Aplica." }
};
