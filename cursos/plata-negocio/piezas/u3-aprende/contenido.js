/* La plata del negocio no es la de la casa · Unidad 3 · Aprende
   Molde: componentes/leccion-interactiva · Perfil K · Gancho (5 min)
   Cifras normativas en "datos": revisar cada año y antes de publicar. */
window.CONTENIDO = {
  titulo: "Una cuenta y un registro para el negocio",
  paso: "Aprende",
  unidad: "Unidad 3",
  notaMinima: 60,
  datos: {
    topeGMF: "350 UVT al mes [VERIFICAR valor en pesos del año]",
    normaGMF: "Estatuto Tributario, art. 879 num. 1 y art. 881-1 [VERIFICAR]"
  },
  pantallas: [
    {
      titulo: "Un lugar solo para la plata del negocio",
      texto: "A Luz Dary los clientes le pagan al mismo Nequi donde su hija le manda plata. Al final del mes no sabe qué es de quién. La solución es simple: **una cuenta o billetera que se use solo para el negocio**. Puede ser una cuenta de ahorros o una billetera digital distinta a la tuya personal.",
      medio: { tipo: "imagen", src: "", nota: "Dos celulares: uno con la billetera personal y otro con la del negocio (o dos tarjetas). Sin logos de marcas." }
    },
    {
      titulo: "Las 3 reglas de la plata",
      texto: "**1.** Todo lo que vendes entra a la cuenta del negocio, también el efectivo al final del día.\n**2.** Todo gasto del negocio sale de esa cuenta.\n**3.** A la casa solo va tu sueldo, por transferencia, en tu fecha fija.\n\nSobre el 4x1000: las cuentas de ahorro tienen una exención hasta **{{topeGMF}}**, sumando todas tus cuentas de ahorro ({{normaGMF}}).",
      medio: { tipo: "imagen", src: "", nota: "Las 3 reglas en una tarjeta vertical para guardar." }
    },
    {
      titulo: "El registro: 5 minutos al día",
      texto: "Al cerrar, anota en un cuaderno, en Excel o en una app: **fecha, qué fue, entró, salió y saldo**. El saldo de hoy es el de ayer más lo que entró menos lo que salió. Si el saldo del cuaderno no cuadra con la cuenta y el cajón, algo se fue sin anotar.",
      pregunta: {
        enunciado: "Luz Dary empezó el día con $400.000. Vendió $350.000 y pagó $120.000 al proveedor. ¿Cuál es su saldo al cerrar?",
        opciones: ["$630.000", "$870.000", "$230.000"],
        correcta: 0,
        retro: {
          bien: "Correcto: $400.000 + $350.000 − $120.000 = $630.000.",
          mal: "Saldo de ayer + lo que entró − lo que salió: $400.000 + $350.000 − $120.000 = $630.000."
        }
      }
    },
    {
      titulo: "Tu registro también abre puertas",
      texto: "Con una cuenta y un registro ordenados puedes mostrar cuánto vende tu negocio cuando pidas un crédito en un banco y no en el gota a gota. Si estás inscrito como comerciante, la ley te pide llevar contabilidad [VERIFICAR con el contador: Código de Comercio art. 19]. Este registro es el primer paso.",
      medio: { tipo: "imagen", src: "", nota: "Ejemplo de una semana del registro de Luz Dary en el cuaderno." }
    },
    {
      titulo: "Lo que debes recordar",
      texto: "Una cuenta solo para el negocio. Todo entra ahí y todo sale de ahí; a la casa va solo tu sueldo. Cinco minutos al día de registro te dicen si estás ganando."
    }
  ],
  final: { titulo: "Lección terminada", texto: "Ahora practica: cuadra el registro de un día de otros negocios." }
};
