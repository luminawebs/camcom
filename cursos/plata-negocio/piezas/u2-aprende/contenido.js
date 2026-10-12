/* La plata del negocio no es la de la casa · Unidad 2 · Aprende
   Molde: componentes/leccion-interactiva · Perfil K · Gancho (5 min)
   El "colchón" del 20 % es una regla práctica del curso, no una norma: [VALIDAR con el contador]. */
window.CONTENIDO = {
  titulo: "Págate un sueldo",
  paso: "Aprende",
  unidad: "Unidad 2",
  notaMinima: 60,
  datos: { colchon: "20 %" },
  pantallas: [
    {
      titulo: "Tú también trabajas en tu negocio",
      texto: "Luz Dary saca \"lo que necesita\": un mes $2.500.000, otro $600.000. En diciembre no tuvo para surtir los útiles de enero. Si tú atiendes el negocio, eres su trabajadora más importante, y a una trabajadora se le paga **un sueldo fijo, en una fecha fija**.",
      medio: { tipo: "imagen", src: "", nota: "Ilustración: calendario con dos fechas de pago marcadas (15 y 30)." }
    },
    {
      titulo: "Primero: ¿cuánto gana el negocio?",
      texto: "Ganancia del mes = **ventas − todo lo que pagaste para el negocio** (mercancía, arriendo del local, servicios del local, transporte de mercancía).\n\nUn solo mes engaña: hay meses buenos y malos. Por eso usa el **promedio de los últimos 3 meses**.",
      medio: { tipo: "imagen", src: "", nota: "Tabla vertical: ganancia de agosto, septiembre y octubre de Luz Dary y su promedio." }
    },
    {
      titulo: "Segundo: deja un colchón",
      texto: "No te pagues toda la ganancia. Deja una parte en el negocio para los meses malos y para crecer. En este curso usamos un colchón de **{{colchon}}** como punto de partida.\n\n**Sueldo = promedio de ganancia de 3 meses × (1 − colchón)**",
      pregunta: {
        enunciado: "Luz Dary ganó $2.400.000, $1.800.000 y $2.100.000 en tres meses. Con un colchón del 20 %, ¿cuál es su sueldo?",
        opciones: ["$1.680.000", "$2.400.000", "$2.100.000"],
        correcta: 0,
        retro: {
          bien: "Así es. Promedio $2.100.000 × 0,80 = $1.680.000.",
          mal: "Primero saca el promedio: ($2.400.000 + $1.800.000 + $2.100.000) ÷ 3 = $2.100.000. Luego deja el colchón: × 0,80 = $1.680.000."
        }
      }
    },
    {
      titulo: "¿Y si no alcanza para la casa?",
      texto: "Si el sueldo que puede pagar tu negocio es menor que lo que necesita tu casa, no es culpa tuya: es una **señal**. Ahora la ves con números. Puedes vender más, revisar precios o bajar costos. Lo que no sirve es seguir sacando sin anotar, porque el negocio se va quedando sin plata para surtir.",
      medio: { tipo: "imagen", src: "", nota: "Tres caminos con íconos: vender más, revisar precios, bajar costos." }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "Págate un sueldo fijo en fecha fija, no \"lo que necesites\". Calcúlalo con el promedio de 3 meses, no con el mejor mes. Deja un colchón en el negocio."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: calcula el sueldo de otros dueños de negocio de Soacha." }
};
