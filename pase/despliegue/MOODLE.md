# Conectar el Pase con Moodle (portal.edunest.co, Moodle 4.3)

Lo hace David con su cuenta de **administrador** (la cuenta Gestor de Claude no puede
crear cohortes, usuarios ni tokens). Unos 15 minutos. Los nombres en cursiva son los de la
interfaz en español.

## 1. Activar la sincronización de cohortes

*Administración del sitio › Extensiones › Matriculaciones › Gestionar extensiones de
matriculación* → el ojo de **Sincronización de cohortes** debe estar abierto.

## 2. Crear las dos cohortes

*Administración del sitio › Usuarios › Cuentas › Cohortes › Añadir nueva cohorte*, dos veces:

| Nombre | ID de cohorte (exacto) | Contexto |
|---|---|---|
| Registro gratis | `registro-gratis` | Sistema |
| Pase Empresario | `pase-empresario` | Sistema |

## 3. Usuario de servicio `conector-pase`

*Administración del sitio › Usuarios › Cuentas › Añadir usuario*:
nombre de usuario `conector-pase`, método de autenticación **Servicios web**, nombre
«Conector», apellido «Pase», correo de EduNest (no recibe correos del aula).

## 4. Rol con lo justo

*Administración del sitio › Usuarios › Permisos › Definir roles › Añadir un nuevo rol*
(arquetipo: ninguno). Nombre «Conector Pase», nombre corto `conectorpase`, contexto
**Sistema**. Permitir solo:

- `webservice/rest:use`
- `moodle/user:create`, `moodle/user:update`, `moodle/user:viewdetails`, `moodle/user:viewhiddendetails`
- `moodle/cohort:view`, `moodle/cohort:assign`

Luego *Usuarios › Permisos › Asignar roles de sistema › Conector Pase* → agregar a `conector-pase`.

## 5. Servicio externo

*Administración del sitio › Servidor › Servicios web › Servicios externos › Agregar*:
nombre «Conector Pase», **Habilitado**, **Solo usuarios autorizados**. Guardar y en
*Funciones › Agregar funciones*:

```
core_webservice_get_site_info
core_user_get_users_by_field
core_user_create_users
core_cohort_search_cohorts
core_cohort_add_cohort_members
core_cohort_delete_cohort_members
```

En *Usuarios autorizados* agregar `conector-pase`.

## 6. Token y conexión (en el servidor, nunca en el chat)

*Servidor › Servicios web › Gestionar tokens › Crear token*: usuario `conector-pase`,
servicio «Conector Pase». Copiar el token y, en el droplet:

```
nano /etc/pase/pase.env
#   PASE_MOODLE_SIMULADO=0
#   PASE_MOODLE_URL=https://portal.edunest.co
#   PASE_MOODLE_TOKEN=<el token>

# El pago de prueba quedó con un usuario de Moodle simulado: se archiva esa base
systemctl stop pase
mv /var/lib/pase/pase.db /var/lib/pase/pase-sandbox-simulado.db
systemctl start pase

# Prueba (solo lectura): debe listar la cohorte «Pase Empresario»
set -a; . /etc/pase/pase.env
curl -s "$PASE_MOODLE_URL/webservice/rest/server.php" -d moodlewsrestformat=json \
  -d wstoken="$PASE_MOODLE_TOKEN" -d wsfunction=core_cohort_search_cohorts \
  -d query=pase -d 'context[contextid]=1' -d includes=all; echo
```

## 7. Curso de prueba (dos tramos)

En un curso de prueba (p. ej. «Curso Muestra Cam Comercio»), *Participantes › Métodos de
matriculación › Añadir método › Sincronización de cohortes*, dos veces:

| Cohorte | Rol | Agregar al grupo |
|---|---|---|
| Registro gratis | Estudiante | Ninguno |
| Pase Empresario | Estudiante | **Crear nuevo grupo** (queda «Pase Empresario cohort») |

Restringir las unidades 4 a 7 (y la Demuestra y el certificado) con *Restricciones de acceso
› Grupo › Pase Empresario cohort*.

Luego, un pago de prueba nuevo en `https://pase.edunest.co/?c=prueba` y verificar:

1. La persona aparece en las dos cohortes y ve U1-U7.
2. Se cancela el Pase de prueba: debe seguir viendo U1-U3, **dejar de ver U4-U7** y
   conservar su avance. Si el grupo no se le quita, se cambia la acción de baja externa del
   método «Pase Empresario» a *Dar de baja* (la persona sigue matriculada por el gratis).
