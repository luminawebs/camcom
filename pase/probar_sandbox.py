"""Prueba de punta a punta contra ePayco en modo prueba, sin URL de confirmación (consulta).

    python -m pase.probar_sandbox

Lee las variables EPAYCO_* del entorno (con EPAYCO_ENTORNO=sandbox: las transacciones van
con test=TRUE) y recorre lo que usa el conector: acceso a la API, token de la tarjeta de
prueba (aquí por API, en el sitio lo hace epayco.js en el navegador), cliente, cobro con
token, consulta por x_ref_payco, firma de la confirmación, borrado del token y sesión del
Smart Checkout v2.
No imprime llaves ni secretos.
"""
import sys
import time
import uuid

from . import epayco as ep
from .config import Config


def paso(nombre, ok, detalle=""):
    print(f"{'OK ' if ok else 'FALLA'} {nombre}{' · ' + detalle if detalle else ''}")
    return ok


def esperar_final(api, ref_payco, intentos=20):
    tx = api.transaccion(ref_payco)
    for _ in range(intentos):
        if tx["status"] != "PENDING":
            break
        time.sleep(3)
        tx = api.transaccion(ref_payco)
    return tx


def main():
    c = Config.desde_entorno()
    if not c.pruebas:
        sys.exit("Esta prueba solo corre con EPAYCO_ENTORNO=sandbox.")
    faltan = [n for n, v in (("EPAYCO_CLIENTE", c.cliente_id), ("EPAYCO_P_KEY", c.p_key),
                             ("EPAYCO_LLAVE_PUBLICA", c.llave_publica),
                             ("EPAYCO_LLAVE_PRIVADA", c.llave_privada)) if not v]
    if faltan:
        sys.exit("Faltan variables: " + ", ".join(faltan))
    if "localhost" in c.url_publica or "127.0.0.1" in c.url_publica:
        c.url_publica = "https://pase.edunest.co"
    api = ep.Epayco(c)
    persona = {"nombre": "Prueba Pase", "correo": "pruebas.pase@edunest.co", "documento": "1000000001",
               "tipo_doc": "CC", "whatsapp": "3001234567", "municipio": "Soacha"}

    paso("POST /v1/auth/login", bool(api._token_api()))

    # Tarjetas de docs.epayco.com/docs/medios-de-pruebas-1 (vencen 12/2027, CVV 123)
    for numero, esperado in (("4575623182290326", "APPROVED"), ("4151611527583283", "DECLINED"),
                             ("5170394490379427", "ERROR")):
        r = api._api("POST", "/v1/tokens", {"card[number]": numero, "card[exp_year]": "2027",
                                            "card[exp_month]": "12", "card[cvc]": "123", "hasCvv": True})
        token = r.get("id") or (r.get("data") or {}).get("id")
        if not paso(f"token tarjeta {numero[-4:]}", bool(token)):
            print(r)
            continue
        fuente = api.crear_cliente(token, persona)
        paso("cliente con token", bool(fuente["cliente"]), fuente["cliente"])
        ref = f"PASE-PRUEBA-{uuid.uuid4().hex[:8]}"
        tx = api.cobrar_tarjeta(fuente, ref, persona, "190.0.0.1")
        paso("cobro con token", bool(tx["id"]), f"x_ref_payco {tx['id']}")
        tx = esperar_final(api, tx["id"])
        paso(f"validación por x_ref_payco ({esperado})", tx["status"] == esperado and tx["reference"] == ref,
             f"{tx['status']} · {tx['amount_in_cents']} {tx['currency']} · ref {tx['reference']}")
        paso("marcada como prueba", tx["prueba"] is True)
        datos = api._http("GET", f"{c.restpagos_epayco}/restpagos/transaction/response.json?"
                                 f"ref_payco={tx['id']}&public_key={c.llave_publica}")["data"]
        if "x_signature" in datos:
            paso("x_signature con P_KEY", ep.confirmacion_valida(datos, c.cliente_id, c.p_key))
        r = api.quitar_tarjeta(fuente)
        paso("borrar token del cliente", r.get("ya_no_existe") or r.get("status") is not False, str(r)[:120])

    sesion = api.datos_checkout(f"PASE-PRUEBA-{uuid.uuid4().hex[:8]}", persona)
    paso("sesión Smart Checkout v2 (Apify)", bool(sesion["sessionId"]), sesion["sessionId"])
    print("Para pagar con PSE, Nequi o Daviplata, inscríbete en el sitio en modo prueba y usa el "
          "botón de PSE: la confirmación llega a /webhooks/epayco.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, ep.ErrorEpayco) as e:
        sys.exit(f"Detenido: {e}")
