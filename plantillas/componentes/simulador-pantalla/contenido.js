/* Simulador de pantalla · paso PRACTICA (perfil P Procedimiento en herramienta)
   El estudiante toca el lugar correcto de una captura del celular.
   Para cada paso: captura vertical (9:19) y la zona correcta en porcentajes
   de la pantalla (x, y = esquina superior izquierda; w, h = ancho y alto).
   Activa "verZonas: true" mientras ajustas las zonas; apágalo al publicar. */
window.CONTENIDO = {
  titulo: "[Configura tu catálogo en WhatsApp Business]",
  paso: "Practica",
  unidad: "Unidad [n]",
  notaMinima: 60,
  verZonas: true,
  pasos: [
    {
      instruccion: "[Paso 1: qué debe tocar. Ej.: Abre los ajustes de la app.]",
      pantalla: { tipo: "imagen", src: "", alt: "[Descripción de la captura]", nota: "Captura del celular, paso 1 (1080 × 2280 px)" },
      zona: { x: 78, y: 4, w: 18, h: 6 },
      pista: "[Pista si se equivoca: dónde mirar]"
    },
    {
      instruccion: "[Paso 2: qué debe tocar]",
      pantalla: { tipo: "imagen", src: "", alt: "[Descripción de la captura]", nota: "Captura del celular, paso 2" },
      zona: { x: 6, y: 30, w: 88, h: 8 },
      pista: "[Pista del paso 2]"
    },
    {
      instruccion: "[Paso 3: qué debe tocar]",
      pantalla: { tipo: "imagen", src: "", alt: "[Descripción de la captura]", nota: "Captura del celular, paso 3" },
      zona: { x: 60, y: 86, w: 34, h: 8 },
      pista: "[Pista del paso 3]"
    }
  ],
  final: { titulo: "¡Lo lograste!", texto: "[Ahora hazlo en tu propio celular: eso es el paso Aplica.]" }
};
