# Conector del Pase Empresario (ePayco → Moodle)

Documento interno de EduNest · 28 de octubre de 2026 · estado: **simulador, sin cobros reales**.
Implementa la fase A y el núcleo de la fase B de `presentaciones/requerimientos-tablero-pase.md`.

El 28-oct-2026 la pasarela pasó de Wompi a **ePayco**, porque la cuenta de EduNest es de Banco
Caja Social y Wompi solo dispersa a Cuenta Wompi, Bancolombia, Occidente y Bogotá. La versión
con Wompi (validada en su sandbox el 20-oct) queda en el historial de git, PR #2.

## Cómo encaja en el pipeline

```
Canal de la Cámara (?c=wa-afiliados)
   │
   ▼
Formulario EduNest  ── «Solo registro gratis» ──► Moodle: usuario + cohorte registro-gratis
   │  (autorización Ley 1581 con versión, IP y fecha)        (U1-U3 de todos los cursos)
   ▼ «Quiero el Pase»
Pantalla de pago
   ├─ Tarjeta → token en el navegador (epayco.js) → cliente ePayco → primer cobro con token
   └─ PSE, Nequi, Daviplata → Checkout de ePayco (renovación manual con enlace cada mes)
   │
   ▼  ePayco llama a la URL de confirmación (campos x_…, x_signature con P_KEY)
POST /webhooks/epayco ── firma OK, se guarda, responde 200 ── cola
   │
   ▼  el conector consulta /validation/v1/reference/{x_ref_payco} (estado, monto, referencia, prueba)
Aceptada → Moodle: cohorte pase-empresario (U4-U7 y certificados) + correo a la persona,
           a la Cámara y a EduNest
   │
   ▼  tarea diaria
Cobro mensual con el token guardado → reintentos día 0, 3 y 7 → cancelado (sale de la
cohorte del Pase, conserva avance y cursos gratis; se borra el token) → si vuelve a pagar, se reactiva.
```

La página de retorno del navegador **nunca** activa el acceso: solo la confirmación firmada y
verificada contra la API. Ojo: la firma de ePayco cubre referencia, transacción, monto y moneda,
**no el estado**; por eso el estado siempre se toma de la API, nunca del aviso.

## Archivos

| Archivo | Qué hace |
|---|---|
| `config.py` | Variables de entorno; candado que impide producción sin `PASE_PERMITIR_PRODUCCION=1` |
| `epayco.py` | Firma de confirmaciones, estados, cliente API (login, cliente con token, cobro, validación, borrar token, datos del Checkout) |
| `moodle.py` | Alta de usuario y cohortes por REST (y un Moodle simulado para pruebas) |
| `nucleo.py` | Estados de la persona, pagos, idempotencia, cobro mensual, reintentos, cancelación, reactivación, conciliación |
| `servidor.py` | Formulario, pantalla de pago, `/checkout`, retorno, `/webhooks/epayco`, `/estado-pago`, `/admin/resumen` |
| `tareas.py` | `cobro`, `conciliar`, `pendientes`, `resumen` para cron |
| `simulador_epayco.py` | Imita ePayco en modo prueba (API, epayco.js, checkout.js y confirmaciones firmadas) |
| `pruebas.py` | 22 pruebas de punta a punta |
| `probar_sandbox.py` | Prueba contra ePayco real en modo prueba |
| `demo.py` | Simulador + conector para probarlo en el navegador |

Solo usa la biblioteca estándar de Python 3.9+ (SQLite).

## Probarlo ya (sin llaves ni red)

```
python -m unittest pase.pruebas -v     # 22 pruebas, unos 17 s
python -m pase.demo                     # abre http://localhost:8080/?c=wa-afiliados
```

En la demo: tarjeta `4575 6231 8229 0326` aprueba, `4151 6115 2758 3283` rechaza; el botón de
PSE/Nequi abre un Checkout simulado con Aprobar/Rechazar.

Lo que comprueban las pruebas:

1. Tarjeta aprobada → cohortes `registro-gratis` y `pase-empresario` en menos de 1 s, correos a la persona, la Cámara y EduNest. Solo se guardan ids de ePayco, nunca datos de la tarjeta.
2. La misma confirmación enviada dos veces no duplica pagos, historial ni llamadas a Moodle.
3. Una confirmación con el monto alterado responde 401 y queda registrada. Una con el **estado** cambiado a «Aceptada» (firma válida, porque la firma no cubre el estado) tampoco da acceso: la API dice «Rechazada». Tampoco la página de retorno, un monto distinto ni una transacción de prueba cuando el conector está en producción.
4. Tres cobros mensuales rechazados (días 0, 3, 7) → `cancelado`, fuera del Pase, dentro de los cursos gratis, token borrado en ePayco; al pagar otra vez → `reactivo`. Cobro aprobado → `activo` y corte un mes después; cancelación voluntaria al corte sin cobrar; un pago reversado vuelve a mora.
5. Registro gratis sin pago; inscribirse dos veces no duplica a la persona.
6. Checkout con renovación manual (enlace firmado 5 días antes, mora, cancelación, renovación pagada) y conciliación que recupera confirmaciones perdidas, también de Checkout gracias al `ref_payco` del retorno.

## Pasar a ePayco real en modo prueba (lo que falta de David)

1. **Cuenta ePayco** de EduNest con la cuenta de Banco Caja Social inscrita para retiros.
2. **Credenciales** (panel › Integraciones › Llaves API): `P_CUST_ID_CLIENTE`, `P_KEY`, `PUBLIC_KEY`, `PRIVATE_KEY`. Van como `EPAYCO_CLIENTE`, `EPAYCO_P_KEY`, `EPAYCO_LLAVE_PUBLICA`, `EPAYCO_LLAVE_PRIVADA` en el entorno de la nube y en `/etc/pase/pase.env`, nunca en el chat.
3. **Dominios permitidos** en el entorno de la nube: `epayco.com`, `docs.epayco.com`, `secure.epayco.co`, `apify.epayco.co`, `checkout.epayco.co`, `api.secure.payco.co`, `secure.payco.co`. Con eso: `python -m pase.probar_sandbox`.
4. **Servidor**: actualizar pase.edunest.co (ver «Pasar el servidor de Wompi a ePayco» en `despliegue/DESPLIEGUE.md`) y poner `https://pase.edunest.co/webhooks/epayco` como URL de confirmación en el panel.
5. **Moodle**: igual que antes (`despliegue/MOODLE.md`): cohortes, usuario `conector-pase`, curso de prueba.

## Variables de entorno

| Variable | Ejemplo / valor por defecto |
|---|---|
| `EPAYCO_ENTORNO` | `sandbox` = modo prueba (o `produccion`, bloqueado sin `PASE_PERMITIR_PRODUCCION=1`) |
| `EPAYCO_CLIENTE`, `EPAYCO_P_KEY` | del panel de ePayco (firma de confirmaciones) |
| `EPAYCO_LLAVE_PUBLICA`, `EPAYCO_LLAVE_PRIVADA` | del panel de ePayco (API, epayco.js y Checkout) |
| `EPAYCO_API_URL`, `EPAYCO_VALIDACION_URL`, `EPAYCO_CHECKOUT_JS`, `EPAYCO_TOKEN_JS` | solo si ePayco cambia sus direcciones |
| `PASE_PRECIO_CENTAVOS` | `2900000` ($29.000; ePayco cobra en pesos enteros) |
| `PASE_URL_PUBLICA` | `https://pase.edunest.co` |
| `PASE_MOODLE_URL`, `PASE_MOODLE_TOKEN`, `PASE_MOODLE_SIMULADO` | `https://portal.edunest.co`, token de `conector-pase`, `1` |
| `PASE_REINTENTOS_DIAS` | `0,3,7` |
| `PASE_AVISOS_CORREO` | correos de la Cámara y de EduNest, separados por coma |
| `PASE_ADMIN_TOKEN` | protege `/admin/resumen` |
| `PASE_SECRETO_SESION` | firma los enlaces de pago de cada persona |

## Supuestos por verificar en el modo prueba real

La documentación de ePayco no se pudo abrir desde la nube (dominios bloqueados). Rutas y campos
salen del SDK oficial `epayco-sdk-node` 1.4.4 (septiembre de 2025) y de la guía pública de la
página de confirmación:

- Login `POST api.secure.payco.co/v1/auth/login`; cliente `/payment/v1/customer/create`; cobro `/payment/v1/charge/create`; borrar token `/v1/remove/token`.
- Validación `GET secure.epayco.co/validation/v1/reference/{ref_payco}`.
- `epayco.js` (tokenización en el navegador, usa jQuery) y `checkout.js` con `ePayco.checkout.configure({key, test}).open({...})`. ePayco tiene un Checkout más nuevo que puede pedir crear una sesión antes; si es así se ajusta `pantalla_checkout`.
- Tarjetas de prueba 4575 6231 8229 0326 (aprobada) y 4151 6115 2758 3283 (rechazada).
- Nequi y Daviplata como pago recurrente: por ahora no; van por Checkout con renovación manual.

## Por hacer después

- Envío real de correos (hoy quedan en la tabla `avisos`) y WhatsApp (fase C).
- Tablero compartido Cámara/EduNest y liquidación del 25 %. ePayco tiene **pagos divididos (split payment)**, que podrían girar ese 25 % en cada pago: preguntarlo al abrir la cuenta.
- Pase para organizaciones (varios usuarios por pago).
- Confirmar con ePayco: tarifa vigente, retiros a Caja Social, cobro con token habilitado.
- Texto final de la autorización de datos (hoy es un borrador v1) revisado por el abogado junto con el convenio.
