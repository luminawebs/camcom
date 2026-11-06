/* La plata del negocio no es la de la casa · Unidad 7 · Aprende (tramo del Pase)
   Molde: componentes/leccion-interactiva · Perfil K */
window.CONTENIDO = {
  titulo: "Cierra el mes en 20 minutos",
  paso: "Aprende",
  unidad: "Unidad 7",
  notaMinima: 60,
  pantallas: [
    {
      titulo: "El día 30 de Luz Dary",
      texto: "Ya tiene cuenta del negocio, sueldo fijo, libro y lista de fiados. Pero el día 30 llega cansada y no sabe por dónde empezar. Jhon Fredy le muestra su lista: **5 pasos, una alarma en el celular y 20 minutos con un tinto**.",
      medio: { tipo: "imagen", src: "", nota: "Alarma en el celular: «Cierre del mes · 20 min»." }
    },
    {
      titulo: "Los 5 pasos del cierre",
      texto: "**1. Cuadra** (5 min): el libro contra la cuenta y el cajón.\n**2. Suma** (5 min): totales por categoría y lo que te deben.\n**3. Cuenta** (5 min): el inventario a precio de compra.\n**4. Calcula** (3 min): utilidad real y margen.\n**5. Decide** (2 min): compara con el mes pasado y escoge **una** acción.",
      medio: { tipo: "imagen", src: "", nota: "Los 5 pasos del cierre en una tarjeta vertical para guardar." }
    },
    {
      titulo: "Cuando no cuadra",
      texto: "**Diferencia = saldo del libro − (saldo de la cuenta + efectivo en el cajón)**\n\nSi es positiva, **falta** plata: algo salió sin anotar (un retiro para la casa, una comisión). Si es negativa, **sobra**: una venta sin anotar o un fiado que pagaron. Búscala en los movimientos antes de ajustar.",
      pregunta: {
        enunciado: "El libro dice $1.450.000. En la cuenta hay $980.000 y en el cajón $390.000. ¿Cuál es la diferencia?",
        opciones: ["Faltan $80.000", "Sobran $80.000", "Cuadra exacto"],
        correcta: 0,
        retro: {
          bien: "Correcto: $1.450.000 − ($980.000 + $390.000) = $80.000. Es positiva: falta plata.",
          mal: "$980.000 + $390.000 = $1.370.000. $1.450.000 − $1.370.000 = $80.000 positivos: **faltan** $80.000."
        }
      }
    },
    {
      titulo: "Una acción por mes",
      texto: "El paso 5 es el que cambia tu negocio. Una sola acción, concreta y que puedas medir: «cobrar $100.000 de fiados antes del 15», «bajar el internet a un plan más barato», «surtir la mitad de lo que no rotó».",
      pregunta: {
        enunciado: "¿Cuál es una buena acción para el mes siguiente?",
        opciones: ["Cobrar $100.000 de fiados antes del día 15", "Tratar de vender más", "Organizarme mejor"],
        correcta: 0,
        retro: {
          bien: "Correcto: dice qué, cuánto y para cuándo. Así sabes si la cumpliste.",
          mal: "Una buena acción dice qué, cuánto y para cuándo: «cobrar $100.000 de fiados antes del 15»."
        }
      }
    },
    {
      titulo: "Tu hoja de cierre",
      texto: "Al final llenas una hoja con: ventas, costo de lo vendido, gastos, tu sueldo, utilidad real, margen, lo que te deben y el inventario. Mes a mes, esa hoja muestra si vas mejorando. Es lo que llevas al banco o al contador.",
      medio: { tipo: "imagen", src: "", nota: "Hoja de cierre del mes de Luz Dary con los 8 datos." }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "Una alarma el último día. Cuadra, suma, cuenta, calcula, decide. Una acción por mes. La hoja de cierre es la historia de tu negocio."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: encuentra la diferencia del cierre de otros negocios." }
};
