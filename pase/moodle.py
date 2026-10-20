"""Alta de usuarios y cohortes en Moodle 4.3 por servicios web REST.

El conector usa su PROPIO usuario de servicio (p. ej. conector-pase) con un
servicio externo que solo tiene estas funciones:
  core_user_get_users_by_field, core_user_create_users,
  core_cohort_search_cohorts, core_cohort_add_cohort_members,
  core_cohort_delete_cohort_members
Los cursos se abren por «Sincronización de cohortes»: el conector nunca matricula
curso por curso, solo mete o saca a la persona de la cohorte.
"""
import json
import urllib.parse
import urllib.request


def _aplanar(prefijo, valor, salida):
    if isinstance(valor, dict):
        for k, v in valor.items():
            _aplanar(f"{prefijo}[{k}]" if prefijo else k, v, salida)
    elif isinstance(valor, (list, tuple)):
        for i, v in enumerate(valor):
            _aplanar(f"{prefijo}[{i}]", v, salida)
    else:
        salida.append((prefijo, valor))
    return salida


class ErrorMoodle(Exception):
    pass


class Moodle:
    def __init__(self, url, token):
        self.url, self.token = url.rstrip("/"), token
        self._cohortes = {}

    def llamar(self, funcion, **params):
        campos = [("wstoken", self.token), ("wsfunction", funcion),
                  ("moodlewsrestformat", "json")] + _aplanar("", params, [])
        datos = urllib.parse.urlencode(campos).encode()
        with urllib.request.urlopen(f"{self.url}/webservice/rest/server.php", datos, timeout=30) as r:
            res = json.loads(r.read() or b"null")
        if isinstance(res, dict) and res.get("exception"):
            raise ErrorMoodle(f"{funcion}: {res.get('errorcode')} {res.get('message')}")
        return res

    def buscar_usuario(self, correo):
        res = self.llamar("core_user_get_users_by_field", field="email", values=[correo.lower()])
        return res[0]["id"] if res else None

    def crear_usuario(self, persona):
        nombre, _, apellido = persona["nombre"].strip().partition(" ")
        res = self.llamar("core_user_create_users", users=[{
            "username": persona["correo"].lower(),
            "createpassword": 1,  # Moodle envía la contraseña por correo
            "firstname": nombre, "lastname": apellido or "-",
            "email": persona["correo"].lower(), "auth": "manual",
            "city": persona.get("municipio") or "Soacha", "country": "CO",
            "idnumber": persona["documento"],
        }])
        return res[0]["id"]

    def asegurar_usuario(self, persona):
        return self.buscar_usuario(persona["correo"]) or self.crear_usuario(persona)

    def id_cohorte(self, idnumber):
        if idnumber not in self._cohortes:
            res = self.llamar("core_cohort_search_cohorts", query=idnumber,
                              context={"contextid": 1}, includes="all")
            hallada = [c for c in res.get("cohorts", []) if c.get("idnumber") == idnumber]
            if not hallada:
                raise ErrorMoodle(f"No existe la cohorte con idnumber {idnumber!r}")
            self._cohortes[idnumber] = hallada[0]["id"]
        return self._cohortes[idnumber]

    def agregar_a_cohorte(self, usuario_id, idnumber):
        self.llamar("core_cohort_add_cohort_members", members=[{
            "cohorttype": {"type": "idnumber", "value": idnumber},
            "usertype": {"type": "id", "value": usuario_id},
        }])

    def quitar_de_cohorte(self, usuario_id, idnumber):
        self.llamar("core_cohort_delete_cohort_members", members=[{
            "cohortid": self.id_cohorte(idnumber), "userid": usuario_id,
        }])


class MoodleSimulado:
    """Mismo contrato que Moodle, en memoria. Para sandbox sin tocar portal.edunest.co."""

    def __init__(self):
        self.usuarios = {}      # correo -> id
        self.cohortes = {}      # idnumber -> set(id)
        self.llamadas = []

    def asegurar_usuario(self, persona):
        correo = persona["correo"].lower()
        if correo not in self.usuarios:
            self.usuarios[correo] = 5000 + len(self.usuarios)
            self.llamadas.append(("core_user_create_users", correo))
        return self.usuarios[correo]

    def agregar_a_cohorte(self, usuario_id, idnumber):
        self.cohortes.setdefault(idnumber, set()).add(usuario_id)
        self.llamadas.append(("core_cohort_add_cohort_members", idnumber, usuario_id))

    def quitar_de_cohorte(self, usuario_id, idnumber):
        self.cohortes.setdefault(idnumber, set()).discard(usuario_id)
        self.llamadas.append(("core_cohort_delete_cohort_members", idnumber, usuario_id))


def crear(config):
    return MoodleSimulado() if config.moodle_simulado else Moodle(config.moodle_url, config.moodle_token)
