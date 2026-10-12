/* ¿Cuál funciona mejor? · paso PRACTICA (perfil H Habilidad creativa)
   Pares de ejemplos (foto o video vertical). El estudiante elige el mejor y ve por qué.
   El orden de A y B se mezcla en cada intento. */
window.CONTENIDO = {
  titulo: "[¿Cuál foto vende más?]",
  paso: "Practica",
  unidad: "Unidad [n]",
  notaMinima: 60,
  pares: [
    {
      pregunta: "[¿Cuál foto tiene mejor luz?]",
      buena: { tipo: "imagen", src: "", alt: "[Descripción]", nota: "Foto bien hecha (luz natural de ventana)", etiqueta: "[Foto 1]" },
      mala: { tipo: "imagen", src: "", alt: "[Descripción]", nota: "Foto con el error a identificar (flash directo)", etiqueta: "[Foto 2]" },
      explicacion: "[Por qué la buena funciona: qué mirar en la luz, el fondo o el encuadre.]"
    },
    {
      pregunta: "[¿Cuál tiene mejor fondo?]",
      buena: { tipo: "imagen", src: "", alt: "", nota: "Ejemplo correcto", etiqueta: "[Foto 1]" },
      mala: { tipo: "imagen", src: "", alt: "", nota: "Ejemplo con error", etiqueta: "[Foto 2]" },
      explicacion: "[Explicación del par 2]"
    },
    {
      pregunta: "[¿Cuál video engancha en los primeros 3 segundos?]",
      buena: { tipo: "vertical", src: "", nota: "Video vertical correcto, máx. 15 s", etiqueta: "[Video 1]" },
      mala: { tipo: "vertical", src: "", nota: "Video vertical con error", etiqueta: "[Video 2]" },
      explicacion: "[Explicación del par 3]"
    }
  ],
  final: { titulo: "Ya tienes buen ojo", texto: "[Ahora sube tu propia foto en el paso Aplica.]" }
};
