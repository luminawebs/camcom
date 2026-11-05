"""Pruebas del exportador: python -m unittest metricas.pruebas"""
import datetime as dt
import json
import pathlib
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest import mock

from . import exportar as ex


class MoodleFalso:
    """Curso 10: U3 = actividades 31 y 32. Estudiantes 1 (termina U3, con Pase), 2 (termina, sin Pase),
    3 (no termina) y un profesor que no cuenta."""

    def __init__(self, finalizacion=True, estudiantes=(1, 2, 3)):
        self.finalizacion, self.estudiantes = finalizacion, estudiantes

    def llamar(self, funcion, **p):
        if funcion == "core_course_get_courses":
            return [{"fullname": "La plata del negocio"}]
        if funcion == "core_course_get_contents":
            return [{"section": 0, "name": "INICIO", "modules": [{"id": 1, "completion": 2}]},
                    {"section": 3, "name": "Unidad 3 · Una cuenta", "modules": [
                        {"id": 31, "completion": 2}, {"id": 32, "completion": 2}, {"id": 33, "completion": 0}]}]
        if funcion == "core_enrol_get_enrolled_users":
            pase = [{"name": "pase-empresario cohort"}]
            return [{"id": u, "roles": [{"shortname": "student"}], "groups": pase if u == 1 else [],
                     "firstaccess": ex.epoca(dt.date(2026, 11, 3)) if u == 3 else 0} for u in self.estudiantes] + \
                   [{"id": 99, "roles": [{"shortname": "editingteacher"}], "groups": []}]
        if funcion == "core_completion_get_activities_completion_status":
            if not self.finalizacion:
                raise ex.ErrorMoodle("accessexception")
            hechas = {1: [31, 32], 2: [31, 32, 33], 3: [31]}[p["userid"]]
            return {"statuses": [{"cmid": c, "state": 1} for c in hechas]}
        raise AssertionError(funcion)


class Pruebas(unittest.TestCase):
    def test_semana(self):
        self.assertEqual(ex.semana_iso(hoy=dt.date(2026, 11, 5))[0], "2026-W44")
        etiqueta, lunes, sig = ex.semana_iso("2026-W45")
        self.assertEqual((etiqueta, lunes, sig), ("2026-W45", dt.date(2026, 11, 2), dt.date(2026, 11, 9)))

    def test_moodle_u3_conversion_y_linea_base(self):
        vistos = {}
        lunes, sig = dt.date(2026, 11, 2), dt.date(2026, 11, 9)
        total, filas, notas = ex.medir_moodle(MoodleFalso(estudiantes=(1, 2)), {10: "AVS-G01"}, lunes, sig, vistos, set())
        self.assertEqual(total["matriculas_nuevas"], "")  # línea base
        total, filas, notas = ex.medir_moodle(MoodleFalso(), {10: "AVS-G01"}, lunes, sig, vistos, set())
        self.assertEqual(total["estudiantes_total"], 3)
        self.assertEqual(total["matriculas_nuevas"], 1)
        self.assertEqual(total["primer_ingreso_semana"], 1)
        self.assertEqual((total["terminaron_u3"], total["pct_termina_u3"]), (2, 66.7))
        self.assertEqual((total["terminaron_u3_con_pase"], total["conversion_u3_pase"]), (1, 50.0))
        self.assertEqual(notas, [])

    def test_sin_permiso_de_finalizacion_sigue(self):
        total, filas, notas = ex.medir_moodle(MoodleFalso(False), {10: "X"}, dt.date(2026, 11, 2),
                                              dt.date(2026, 11, 9), {}, set())
        self.assertNotIn("pct_termina_u3", total)
        self.assertTrue(any("core_completion" in n for n in notas))

    def test_exportacion_completa(self):
        recibido = {}

        class Pase(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                recibido["ruta"], recibido["llave"] = self.path, self.headers.get("Authorization")
                cuerpo = json.dumps({"entorno": "sandbox", "inscritos_nuevos": 4, "pases_nuevos": 2,
                                     "renovaciones": 1, "pagos_aprobados": 3, "pagos_rechazados": 1,
                                     "recaudo_cop": 87000, "camara_25_cop": 21750, "cancelaciones_pedidas": 1,
                                     "cancelaciones_efectivas": 1, "pases_activos_hoy": 9, "en_mora_hoy": 0,
                                     "por_canal": {"curso-avs-g01": {"inscritos_nuevos": 4, "pases_nuevos": 2,
                                                                     "recaudo_cop": 58000}}}).encode()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(cuerpo)

        srv = ThreadingHTTPServer(("127.0.0.1", 0), Pase)
        self.addCleanup(srv.server_close)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        with tempfile.TemporaryDirectory() as tmp:
            datos = pathlib.Path(tmp)
            (datos / "gasto-marketing.csv").write_text(
                "semana,canal,gasto_cop,nota\n2026-W45,curso-avs-g01,50.000,pauta\n2026-W44,otro,9\n",
                encoding="utf-8")
            entorno = {"PASE_METRICAS_TOKEN": "k" * 20, "PASE_URL": f"http://127.0.0.1:{srv.server_address[1]}",
                       "MOODLE_URL": "", "MOODLE_TOKEN": ""}
            with mock.patch.dict("os.environ", entorno), mock.patch("builtins.print"):
                fila = ex.main(["--semana", "2026-W45", "--salida", tmp])
                ex.main(["--semana", "2026-W45", "--salida", tmp])  # repetir no duplica
            srv.shutdown()
            self.assertEqual(recibido["ruta"], "/metricas?desde=2026-11-02&hasta=2026-11-09")
            self.assertEqual(recibido["llave"], "Bearer " + "k" * 20)
            self.assertEqual((fila["gasto_marketing_cop"], fila["costo_por_suscriptor_cop"]), (50000, 25000))
            self.assertEqual(fila["tasa_cancelacion"], 10.0)
            filas = (datos / "metricas-semanales.csv").read_text(encoding="utf-8-sig").splitlines()
            self.assertEqual(len(filas), 2)
            md = (datos / "metricas-2026-W45.md").read_text(encoding="utf-8")
            self.assertIn("modo prueba", md)
            self.assertIn("| curso-avs-g01 | 4 | 2 | $58.000 | $50.000 | $25.000 |", md)


if __name__ == "__main__":
    unittest.main()
