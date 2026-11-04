# Investigación · Vende más por WhatsApp Business

Datos, rutas de menú y fuentes que usa el curso, y lo que falta validar con el asesor de mercadeo digital de la Cámara. Consultado el 14 de octubre de 2026.

El servicio de ayuda oficial de WhatsApp (faq.whatsapp.com) no se pudo abrir desde el entorno donde se produjo el curso. Las rutas de menú y los nombres de las opciones salen de guías de terceros (Leadsales, Tiendanube, Semrush, El Diario) que coinciden entre sí, pero cambian según la versión de la app y entre Android y iPhone. Por eso las pantallas del curso son **simplificadas** (dibujadas en `pantallas/armar_pantallas.py`, con la marca «Pantalla de práctica»), no capturas reales, y lo que depende de la versión lleva **[VERIFICAR]**.

## Cifras

| Dato | Valor | Fuente | Estado |
| --- | --- | --- | --- |
| Personas en Colombia que usan WhatsApp | 91,1 % | Infobip, citado por Portafolio | Solo contexto; el curso no lo usa |
| Tiendas en línea colombianas que usan WhatsApp para vender | 84,1 % | Tiendanube, NubeCommerce Colombia 2026 | Solo contexto; fuente comercial |
| Etiquetas posibles | hasta 20 | Leadsales | [VERIFICAR]; el curso no da el número |
| Descripción del perfil | ≈ 139 caracteres (una sola fuente) | Eazybe | [VERIFICAR]; el curso solo dice «corta» |
| Catálogo | hasta 10 fotos o videos por artículo; revisión de Meta antes de mostrarse | Tiendanube, Brevo | [VERIFICAR]; el curso no da números |

El curso no usa cifras de mercado: el caso de Sandra, Camilo y Esperanza es inventado para enseñar.

## Funciones y rutas (Android)

- **Cambio a WhatsApp Business:** app gratuita aparte. Al instalarla en el mismo celular ofrece usar el número del WhatsApp normal y traer los chats. **[VERIFICAR]** pasos y si se conserva el historial en iPhone.
- **Perfil de empresa:** nombre, foto, categoría, descripción, dirección, horario (abierto en horario, siempre abierto o con cita), correo y sitio web. Menú ⋮ › Herramientas para la empresa › Perfil de empresa. **[VERIFICAR]** nombre del menú («Herramientas para la empresa» en las guías; en algunas versiones «Herramientas comerciales»).
- **Catálogo:** Herramientas para la empresa › Catálogo › Añadir artículo nuevo: foto, nombre, precio (opcional), descripción (opcional), enlace y código del artículo. Se comparte el catálogo o un artículo desde el chat con el clip. Algunas guías dicen que la app pide el país de origen y que los artículos pasan por revisión. **[VERIFICAR]**.
- **Etiquetas:** predeterminadas Nuevo cliente, Nuevo pedido, Pago pendiente, Pagado y Pedido finalizado (el curso usa «Entregado» como nombre propio de la última etapa). Se crean y renombran; se le pone etiqueta a un chat (mantener presionado › ícono de etiqueta) o a un mensaje; se filtra por etiqueta desde la lista de chats o el menú Etiquetas. **[VERIFICAR]** nombres y ruta del filtro, que cambió en 2024 con los filtros de chats.
- **Mensaje de bienvenida:** sale solo la primera vez que alguien escribe o tras un tiempo sin conversación (las guías dicen 14 días). Destinatarios: todos, quien no está en la agenda, todos excepto, solo enviar a. **[VERIFICAR]** días.
- **Mensaje de ausencia:** siempre, en horario personalizado o fuera del horario comercial (este último requiere el horario en el perfil). **[VERIFICAR]**.
- **Respuestas rápidas:** mensaje guardado con atajo; en el chat se escribe «/» y se elige. No se envían solas. **[VERIFICAR]** número máximo (las guías dicen 50).

## Normas

- **Datos personales (Ley 1581 de 2012 y Decreto 1377 de 2013):** el número y el nombre del cliente son datos personales; para mandar promociones hace falta su autorización. El curso solo dice «pide permiso antes de mandar promociones». **[VERIFICAR]** redacción con el asesor. Se profundiza en el curso 19 del catálogo («Datos de tus clientes sin problemas legales»).
- No se mencionan sanciones ni montos.

## Decisiones del curso

- **Perfil P con ajuste:** la receta P pide un screencast en Aprende. Se cambió por una lección interactiva narrada con pantallas simplificadas (`receta` en `curso.json`): pesa poco con datos limitados, usa el mismo pipeline de narración que los cursos 2 y 3 y no depende de grabar la app real. Practica sí es el simulador de pantalla de la receta.
- **Pantallas dibujadas, no capturas:** el simulador y las vistas de Aprende son pantallas HTML con los nombres de los menús, sin el logo ni la marca de WhatsApp. Si el asesor toma capturas reales del celular, se reemplazan las imágenes en `piezas/uN-practica/medios/` y se ajustan las zonas.
- No se recomienda ninguna herramienta pagada ni la API de WhatsApp Business (es para empresas grandes); el tramo del Pase verá cobros con link de pago, Nequi y Daviplata.
- Caso hilo: Sandra (tortas por encargo, Hogares Soacha). Personas: Camilo (accesorios para celular, Ducales) y Esperanza (frutas y verduras a domicilio, El Altico). Nombres, negocios y precios inventados para enseñar.

## Fuentes consultadas

- https://www.tiendanube.com/blog/como-hacer-un-catalogo-en-whatsapp
- https://leadsales.io/blog/etiquetas-de-whatsapp-business-organizacion-en-tus-chats/
- https://leadsales.io/blog/como-tener-respuestas-automaticas-en-whatsapp/
- https://es.semrush.com/blog/whatsapp-business/
- https://eldiario.com/2025/08/23/whatsapp-herramienta-de-trabajo-version-business/
- https://eazybe.com/es/blog/ejemplos-de-descripciones-de-empresa-para-whatsapp
- https://platzi.com/cursos/whatsapp-for-business/maneja-el-caos-con-etiquetas/
- https://www.brevo.com/es/blog/crear-catalogo-whatsapp/
- https://www.portafolio.co/tecnologia/whatsapp-se-consolida-como-aliado-clave-del-comercio-electronico-en-colombia-segun-informe-de-e-commerce-489757
- https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=49981 (Ley 1581 de 2012)
