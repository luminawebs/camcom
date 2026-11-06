/* Lee tus números · Unidad 4 · Aprende (tramo del Pase)
   Molde: componentes/leccion-interactiva · Perfil K
   Caso: Patricia, comidas rápidas en La Despensa. Cifras del caso inventadas para enseñar. */
window.CONTENIDO = {
  titulo: "Tu balance general",
  paso: "Aprende",
  unidad: "Unidad 4",
  notaMinima: 60,
  narracion: true,
  pantallas: [
    {
      titulo: "Una foto, no una película",
      texto: "En la cooperativa le pidieron a Patricia el **balance general**. No es lo mismo que el estado de resultados: el estado de resultados es la **película del mes** (ventas, costos y gastos); el balance es la **foto de un día**, por ejemplo el 31 de octubre: lo que el negocio tiene, lo que debe y lo que es de ella.",
      medio: { tipo: "imagen", src: "medios/ilustracion-1.jpg", alt: "Ilustración de Patricia frente a su carro de comidas haciendo una lista" }
    },
    {
      titulo: "Las tres partes del balance",
      texto: "**Lo que tiene (activos):** la plata en la caja y en Nequi, la mercancía y los insumos, lo que te deben los clientes y los equipos.\n**Lo que debe (pasivos):** a los proveedores, los préstamos, los impuestos por pagar.\n**Lo que es tuyo (patrimonio):** lo que queda si con lo que tienes pagas todo lo que debes.\n**Patrimonio = lo que tiene − lo que debe.**",
      medio: { tipo: "imagen", src: "medios/ilustracion-2.jpg", alt: "Balanza: a un lado lo que el negocio tiene; al otro, lo que debe y lo que es del dueño" }
    },
    {
      titulo: "El balance de Patricia",
      texto: "Al 31 de octubre Patricia tiene: caja $300.000, Nequi $500.000, mercancía e insumos $600.000 y equipos (plancha, freidora, nevera y carro) $5.200.000. **Total: $6.600.000.** Debe: al proveedor de gaseosas $400.000 y a la cooperativa $1.200.000 de la freidora. **Total: $1.600.000.**",
      pregunta: {
        enunciado: "¿Cuál es el patrimonio de Patricia?",
        opciones: ["$5.000.000", "$8.200.000", "$6.600.000"],
        correcta: 0,
        retro: {
          bien: "Correcto: $6.600.000 − $1.600.000 = $5.000.000. Eso es lo que de verdad es de ella.",
          mal: "Patrimonio = lo que tiene − lo que debe = $6.600.000 − $1.600.000 = $5.000.000."
        }
      }
    },
    {
      titulo: "Tres reglas para no enredarte",
      texto: "**1. Solo lo del negocio.** La moto de la familia, el televisor o la tarjeta de crédito de la casa no van.\n**2. Todo con la misma fecha.** Cuenta la plata, la mercancía y las deudas el mismo día.\n**3. Los equipos a su valor de hoy:** lo que te costaron menos el desgaste por los años de uso.\nLos **fiados que te deben sí van**: es plata que vas a recibir.",
      pregunta: {
        enunciado: "Patricia usa la moto de la familia los domingos para ir al mercado. ¿Va en el balance del negocio?",
        opciones: ["Sí, como un equipo", "No: es de la casa; si se usa para las dos cosas, se decide con el contador", "Sí, como una deuda"],
        correcta: 1,
        retro: {
          bien: "Así es. El balance lleva solo lo del negocio; lo que se usa en las dos cosas se decide con el contador.",
          mal: "La moto es de la familia: no va. Si un bien se usa en el negocio y en la casa, decídelo con el contador."
        }
      }
    },
    {
      titulo: "Para qué te sirve",
      texto: "Con el balance ves si el negocio **crece de un año a otro** (si sube tu patrimonio), **cuánto debes** comparado con lo que tienes y qué podrías dar como **respaldo** de un crédito. La cooperativa lo mira junto con tu estado de resultados."
    },
    {
      titulo: "Lo que debes recordar",
      texto: "El balance es la **foto de un día**. **Patrimonio = lo que tiene − lo que debe.** Solo cosas del negocio, todo con la misma fecha y los equipos a su valor de hoy."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: calcula el patrimonio de un negocio con la calculadora." }
};
