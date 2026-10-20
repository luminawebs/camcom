# Conector del Pase Empresario (Wompi → Moodle)

Documento interno de EduNest · 20 de octubre de 2026 · estado: **sandbox, sin cobros reales**.
Implementa la fase A y el núcleo de la fase B de `presentaciones/requerimientos-tablero-pase.md`.

## Cómo encaja en el pipeline

```
Canal de la Cámara (?c=wa-afiliados)
   │
   ▼
Formulario EduNest  ── «Solo registro gratis» ──► Moodle: usuario + cohorte registro-gratis
   │  (autorización Ley 1581 con versión, IP y fecha)        (U1-U3 de todos los cursos)
   ▼ «Quiero el Pase»
Pantalla de pago
   ├─ Tarjeta / Nequi → token directo a Wompi → fuente de pago → primer cobro (recurrente)
   └─ PSE → Web Checkout de Wompi (renovación manual con enlace cada mes)
   │
   ▼  Wompi envía transaction.updated (firmado)
POST /webhooks/wompi ── firma OK, se guarda, responde 200 ── cola
   │
   ▼  el conector consulta GET /transactions/{id} (doble verificación de estado, monto, referencia)
APPROVED → Moodle: cohorte pase-empresario (U4-U7 y certificados) + correo a la persona,
           a la Cámara y a EduNest
   │
   ▼  tarea diaria
Cobro mensual con la fuente guardada → reintentos día 0, 3 y 7 → cancelado (sale de la
cohorte del Pase, conserva avance y cursos gratis) → si vuelve a pagar, se reactiva.
```

La página de retorno del navegador **nunca** activa el acceso: solo el evento firmado y
confirmado contra la API.

## Archivos

| Archivo | Qué hace |
|---|---|
| `config.py` | Variables de entorno; candado que impide producción sin `PASE_PERMITIR_PRODUCCION=1` y llaves `prv_prod_` |
| `wompi.py` | Firma de integridad, verificación del checksum de eventos, cliente API (comercio, fuentes de pago, cobros, enlaces, Web Checkout) |
| `moodle.py` | Alta de usuario y cohortes por REST (y un Moodle simulado para pruebas) |
| `nucleo.py` | Estados de la persona, pagos, idempotencia de eventos, cobro mensual, reintentos, cancelación, reactivación, conciliación |
| `servidor.py` | Formulario, pantalla de pago, retorno, `/webhooks/wompi`, `/estado-pago`, `/admin/resumen` |
| `tareas.py` | `cobro`, `conciliar`, `pendientes`, `resumen` para cron |
| `simulador_wompi.py` | Imita el sandbox de Wompi (tarjetas y Nequi de prueba, PSE, eventos firmados) |
| `pruebas.py` | 15 pruebas de punta a punta |
| `demo.py` | Simulador + conector para probarlo en el navegador |

Solo usa la biblioteca estándar de Python 3.9+ (SQLite). Para producción se puede pasar a
PostgreSQL sin cambiar la lógica.

## Probarlo ya (sin llaves ni red)

```
python -m unittest pase.pruebas -v     # 15 pruebas, unos 11 s
python -m pase.demo                     # abre http://localhost:8080/?c=wa-afiliados
```

En la demo: tarjeta `4242 4242 4242 4242` aprueba, `4111 1111 1111 1111` rechaza; Nequi
`3991111111` aprueba, `3992222222` rechaza; PSE muestra botones Aprobar/Rechazar.

Lo que comprueban las pruebas (criterios 1 a 5 de los requerimientos):

1. Tarjeta aprobada → cohortes `registro-gratis` y `pase-empresario` en menos de 1 s, correos a la persona, la Cámara y EduNest.
2. El mismo evento enviado dos veces no duplica pagos, historial ni llamadas a Moodle.
3. Un evento con la firma alterada («me aprobé solo») responde 401, queda registrado y no da acceso. Tampoco la página de retorno ni un monto distinto.
4. Tres cobros mensuales rechazados (días 0, 3, 7) → `cancelado`, fuera del Pase, dentro de los cursos gratis; al pagar otra vez → `reactivo`. Cobro aprobado → `activo` y corte un mes después; cancelación voluntaria al corte sin cobrar.
5. Registro gratis sin pago; inscribirse dos veces no duplica a la persona.
6. Nequi, PSE con renovación manual (enlace 5 días antes, mora, cancelación) y conciliación que recupera un evento perdido.

## Pasar al sandbox real de Wompi (lo que falta de David)

1. **Llaves de sandbox** del comercio EduNest en Wompi (panel › Desarrolladores): llave pública `pub_test_…`, llave privada `prv_test_…`, secreto de integridad y secreto de eventos. Van como variables del entorno en la nube (`WOMPI_LLAVE_PUBLICA`, `WOMPI_LLAVE_PRIVADA`, `WOMPI_SECRETO_INTEGRIDAD`, `WOMPI_SECRETO_EVENTOS`), nunca en el chat.
2. **Dominios permitidos** en el entorno: `sandbox.wompi.co`, `checkout.wompi.co` y `docs.wompi.co` (hoy están bloqueados, por eso se usó el simulador y los campos de la API salen de la documentación conocida: hay que confirmarlos).
3. **Dónde vive el conector**: un subdominio con HTTPS (propuesto `pase.edunest.co`) en DigitalOcean, separado del Moodle, para que Wompi pueda llamar a `https://pase.edunest.co/webhooks/wompi`. Esa URL se pone en el panel de Wompi como URL de eventos del sandbox.
4. **Moodle** (primero en un curso de prueba):
   - Cohortes de sistema con idnumber `registro-gratis` y `pase-empresario`.
   - En cada curso: método «Sincronización de cohortes» con `registro-gratis` (rol Estudiante) y otro con `pase-empresario` que **agrega al grupo «Pase»**; U4-U7, la Demuestra de U1-U3 y el certificado se restringen a ese grupo (modelo de dos tramos aprobado el 14-oct).
   - Como en estos cursos la persona sigue matriculada por `registro-gratis`, la instancia del Pase puede usar «Dar de baja» al salir de la cohorte: así se quita el grupo «Pase» y el avance se conserva. Con «Desactivar», Moodle podría dejarle el grupo y por tanto el acceso: **verificarlo en el curso de prueba** antes de decidir.
   - Usuario de servicio `conector-pase` (no ClaudeBot) con un servicio externo que solo tenga: `core_user_get_users_by_field`, `core_user_create_users`, `core_cohort_search_cohorts`, `core_cohort_add_cohort_members`, `core_cohort_delete_cohort_members`. Su token va como `PASE_MOODLE_TOKEN` y se pone `PASE_MOODLE_SIMULADO=0`.

## Variables de entorno

| Variable | Ejemplo / valor por defecto |
|---|---|
| `WOMPI_ENTORNO` | `sandbox` (o `produccion`, bloqueado sin `PASE_PERMITIR_PRODUCCION=1`) |
| `WOMPI_LLAVE_PUBLICA`, `WOMPI_LLAVE_PRIVADA` | `pub_test_…`, `prv_test_…` |
| `WOMPI_SECRETO_INTEGRIDAD`, `WOMPI_SECRETO_EVENTOS` | del panel de Wompi |
| `PASE_PRECIO_CENTAVOS` | `2900000` ($29.000) |
| `PASE_URL_PUBLICA` | `https://pase.edunest.co` |
| `PASE_MOODLE_URL`, `PASE_MOODLE_TOKEN`, `PASE_MOODLE_SIMULADO` | `https://portal.edunest.co`, token de `conector-pase`, `1` |
| `PASE_REINTENTOS_DIAS` | `0,3,7` |
| `PASE_AVISOS_CORREO` | correos de la Cámara y de EduNest, separados por coma |
| `PASE_ADMIN_TOKEN` | protege `/admin/resumen` |
| `PASE_SECRETO_SESION` | firma los enlaces de pago de cada persona |

Cron sugerido: `cobro` y `conciliar` una vez al día (6:00), `pendientes` cada hora.

## Por hacer después del sandbox

- Envío real de correos (hoy quedan en la tabla `avisos`) y WhatsApp (fase C).
- Tablero compartido Cámara/EduNest sobre esta misma base, liquidación del 25 % (falta decidir base bruta o neta) y conciliación contra el reporte de Wompi.
- Pase para organizaciones (varios usuarios por pago).
- Confirmar con Wompi: tarifa vigente, Nequi como fuente recurrente, campo `recurrent` y política de reintentos de eventos.
- Texto final de la autorización de datos (hoy es un borrador v1) revisado por el abogado junto con el convenio.
