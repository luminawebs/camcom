/* La plata del negocio no es la de la casa · Unidad 6 · Aprende (tramo del Pase)
   Molde: componentes/leccion-interactiva · Perfil K */
window.CONTENIDO = {
  titulo: "Cuánto ganas de verdad: tu utilidad real",
  paso: "Aprende",
  unidad: "Unidad 6",
  notaMinima: 60,
  pantallas: [
    {
      titulo: "«Gané $900.000… ¿o no?»",
      texto: "Marleny vendió $5.000.000 y pagó $4.100.000. Pero compró tela para todo diciembre y su sueldo no aparece. Restar «lo que pagué» falla cuando compras mercancía para varios meses: un mes parece que perdiste y el siguiente que ganaste mucho.",
      medio: { tipo: "imagen", src: "", nota: "Marleny en su taller entre rollos de tela, con una calculadora." }
    },
    {
      titulo: "Lo que compraste no es lo que vendiste",
      texto: "Lo justo es restar solo **la mercancía que salió vendida**:\n\n**Costo de lo vendido = inventario al empezar + compras del mes − inventario al terminar**\n\nNo tiene que ser perfecto: cuenta lo que tienes y ponle el precio al que lo compraste. Una vez al mes, el mismo día.",
      pregunta: {
        enunciado: "Marleny empezó noviembre con tela por $600.000, compró $2.400.000 y terminó con $1.200.000. ¿Cuál es su costo de lo vendido?",
        opciones: ["$1.800.000", "$2.400.000", "$3.000.000"],
        correcta: 0,
        retro: {
          bien: "Correcto: $600.000 + $2.400.000 − $1.200.000 = $1.800.000.",
          mal: "Inventario al empezar + compras − inventario al terminar: $600.000 + $2.400.000 − $1.200.000 = $1.800.000."
        }
      }
    },
    {
      titulo: "La utilidad real",
      texto: "**Utilidad real = ventas − costo de lo vendido − gastos fijos − gastos variables − tu sueldo**\n\nTu sueldo **sí** se resta: si no, el negocio parece ganar más de lo que gana. Las cuotas de un crédito y las máquinas **no** van aquí: la cuota es devolver un préstamo y la máquina sirve muchos meses. [VERIFICAR con el contador cómo explicar intereses y depreciación.]",
      pregunta: {
        enunciado: "Ventas $5.000.000; costo de lo vendido $1.800.000; fijos $900.000; variables $300.000; sueldo de Marleny $1.200.000. ¿Utilidad real?",
        opciones: ["$800.000", "$2.000.000", "$900.000"],
        correcta: 0,
        retro: {
          bien: "Correcto: $5.000.000 − $1.800.000 − $900.000 − $300.000 − $1.200.000 = $800.000.",
          mal: "Resta todo, también el sueldo: $5.000.000 − $1.800.000 − $900.000 − $300.000 − $1.200.000 = $800.000."
        }
      }
    },
    {
      titulo: "Utilidad no es plata en la cuenta",
      texto: "Puedes tener utilidad y no tener plata: si fiaste mucho, si compraste inventario o si pagaste una cuota grande. Y puedes tener plata sin utilidad: si te prestaron. Mira las dos cada mes.\n\n**Margen = utilidad real ÷ ventas × 100.** Marleny: $800.000 ÷ $5.000.000 = **16 %**. De cada $100.000 que vende, le quedan $16.000 después de su sueldo.",
      medio: { tipo: "imagen", src: "", nota: "Dos columnas: «Utilidad» y «Plata en la cuenta», con fiados e inventario en el medio." }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "Resta lo que vendiste, no lo que compraste. Cuenta tu sueldo como un gasto. Las cuotas y las máquinas van aparte. Utilidad y plata en la cuenta son cosas distintas."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: calcula la utilidad real de otros negocios con su inventario." }
};
