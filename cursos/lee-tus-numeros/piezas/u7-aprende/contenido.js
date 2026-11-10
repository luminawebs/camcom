/* Lee tus números · Unidad 7 · Aprende (tramo del Pase)
   Molde: componentes/leccion-interactiva · Perfil K
   Caso: Marisol, papelería en León XIII. Cifras del caso inventadas para enseñar. */
window.CONTENIDO = {
  titulo: "3 indicadores para vigilar cada mes",
  paso: "Aprende",
  unidad: "Unidad 7",
  notaMinima: 60,
  narracion: true,
  pantallas: [
    {
      titulo: "Que no se repita febrero",
      texto: "Marisol ya sabe por qué su mejor mes en ventas fue el que menos le dejó. Ahora quiere darse cuenta **a tiempo**. Con **tres números**, una vez al mes y en 10 minutos, lo logra: el **margen**, el **punto de equilibrio** y el **colchón de caja**.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Ilustración de Marisol mirando un tablero con tres indicadores en su papelería" }
    },
    {
      titulo: "1. El margen",
      texto: "**Margen = utilidad del mes ÷ ventas × 100.** Cuántos pesos te quedan de cada 100 que vendes.\nEn un mes normal Marisol tiene utilidad de $450.000 con ventas de $4.500.000: margen del **10 %**. En febrero fue del 3 %. Si el margen baja, revisa precios y costos antes de vender más."
    },
    {
      titulo: "2. El punto de equilibrio",
      texto: "Lo **mínimo que tienes que vender** al mes para no perder.\n**Punto de equilibrio = gastos fijos ÷ (1 − costo de lo vendido ÷ ventas).**\nGastos fijos de Marisol: **$1.800.000** (arriendo, servicios, tóner y su sueldo). Su costo de lo vendido es la **mitad** de las ventas.",
      medio: { tipo: "imagen", src: "medios/ilustracion-2.jpg", alt: "Una línea que sube cruza otra línea plana: el punto donde se cruzan es el equilibrio" },
      pregunta: {
        enunciado: "¿Cuál es el punto de equilibrio de Marisol?",
        opciones: ["$900.000", "$3.600.000", "$1.800.000"],
        correcta: 1,
        retro: {
          bien: "Correcto: $1.800.000 ÷ (1 − 0,5) = $3.600.000. Si vende menos, pierde; cada peso por encima le deja ganancia.",
          mal: "$1.800.000 ÷ (1 − 0,5) = $1.800.000 ÷ 0,5 = $3.600.000."
        }
      }
    },
    {
      titulo: "3. El colchón de caja",
      texto: "Cuántos meses aguantas pagando los gastos fijos si un mes no vendes nada.\n**Colchón de caja = plata disponible ÷ gastos fijos del mes.**\nMarisol tiene **$900.000** entre caja y banco, y gastos fijos de $1.800.000.",
      pregunta: {
        enunciado: "¿Cuánto es el colchón de caja de Marisol?",
        opciones: ["2 meses", "0,5 meses (unos 15 días)", "1 mes"],
        correcta: 1,
        retro: {
          bien: "Correcto: $900.000 ÷ $1.800.000 = 0,5 meses. Una meta razonable para ella es llegar a un mes.",
          mal: "$900.000 ÷ $1.800.000 = 0,5 meses, unos 15 días."
        }
      }
    },
    {
      titulo: "Tu tablero de 3 indicadores",
      texto: "Una hoja con **12 filas** (una por mes) y **3 columnas**: margen, punto de equilibrio y colchón. El mismo día de cada mes, después de tu estado de resultados y tu flujo, anota los tres y **compara con el mes anterior**: ¿subió?, ¿bajó? No hay un número «bueno» para todos los negocios: **compárate contigo mismo**."
    },
    {
      titulo: "Lo que debes recordar",
      texto: "**Margen:** de cada 100 pesos, cuánto te queda. **Punto de equilibrio:** lo mínimo que tienes que vender. **Colchón:** cuántos meses aguantas. Anótalos cada mes y mira hacia dónde van."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: calcula el punto de equilibrio de una papelería con la calculadora." }
};
