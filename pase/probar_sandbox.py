"""Prueba de punta a punta contra el sandbox real de Wompi, sin webhook (conciliación).

    python -m pase.probar_sandbox

Lee las llaves WOMPI_* del entorno (el candado de config exige llaves de sandbox) y
recorre lo que usa el conector: comercio y tokens de aceptación, token de tarjeta 4242,
token Nequi 3991111111, fuentes de pago, cobro recurrente firmado, consulta por id y por
referencia, y la URL de Web Checkout. No imprime llaves ni secretos.
"""
import sys
import time
import urllib.request
import uuid

from . import wompi as w
from .config import Config


def paso(nombre, ok, detalle=""):
    print(f"{'OK ' if ok else 'FALLA'} {nombre}{' · ' + detalle if detalle else ''}")
    return ok


def esperar_final(api, tx_id, intentos=20):
    tx = api.transaccion(tx_id)
    for _ in range(intentos):
        if tx["status"] != "PENDING":
            break
        time.sleep(3)
        tx = api.transaccion(tx_id)
    return tx


def cobrar(api, tipo, token, correo, comercio):
    fuente = api.crear_fuente_pago(tipo, token, correo, comercio["aceptacion"]["acceptance_token"],
                                   (comercio["datos_personales"] or {}).get("acceptance_token"))
    paso(f"payment_source {tipo}", fuente.get("status") == "AVAILABLE",
         f"id {fuente.get('id')} estado {fuente.get('status')}")
    ref = f"PASE-PRUEBA-{tipo}-{uuid.uuid4().hex[:8]}"
    tx = api.cobrar_fuente(fuente["id"], ref, correo, tipo)
    tx = esperar_final(api, tx["id"])
    paso(f"cobro recurrente {tipo}", tx["status"] == "APPROVED",
         f"{tx['status']} · {tx.get('payment_method_type')} · {tx['amount_in_cents']} {tx['currency']}")
    lista = api.transacciones_por_referencia(ref)
    paso(f"GET /transactions?reference {tipo}", any(t["id"] == tx["id"] for t in lista),
         f"{len(lista)} resultado(s)")
    return tx


def main():
    c = Config.desde_entorno()
    if c.entorno != "sandbox":
        sys.exit("Esta prueba solo corre en sandbox.")
    faltan = [n for n, v in (("WOMPI_LLAVE_PUBLICA", c.llave_publica), ("WOMPI_LLAVE_PRIVADA", c.llave_privada),
                             ("WOMPI_SECRETO_INTEGRIDAD", c.secreto_integridad)) if not v]
    if faltan:
        sys.exit("Faltan variables: " + ", ".join(faltan))
    api = w.Wompi(c)
    correo = "pruebas.pase@edunest.co"

    comercio = api.comercio()
    paso("GET /merchants", bool(comercio["aceptacion"].get("acceptance_token")), comercio["nombre"] or "")

    tarjeta = api._llamar("POST", "/tokens/cards", {"number": "4242424242424242", "cvc": "123",
                          "exp_month": "08", "exp_year": "30", "card_holder": "Prueba Pase"})["data"]
    paso("token tarjeta 4242", tarjeta["id"].startswith("tok_"), tarjeta.get("name", ""))
    cobrar(api, "CARD", tarjeta["id"], correo, comercio)

    nequi = api._llamar("POST", "/tokens/nequi", {"phone_number": "3991111111"})["data"]
    for _ in range(20):
        if nequi["status"] != "PENDING":
            break
        time.sleep(3)
        nequi = api._llamar("GET", f"/tokens/nequi/{nequi['id']}")["data"]
    if paso("token Nequi 3991111111", nequi["status"] == "APPROVED", nequi["status"]):
        cobrar(api, "NEQUI", nequi["id"], correo, comercio)

    url = api.url_web_checkout(f"PASE-PRUEBA-WC-{uuid.uuid4().hex[:8]}", correo, "Prueba Pase")
    with urllib.request.urlopen(url, timeout=20) as r:
        paso("Web Checkout con firma", r.status == 200, f"HTTP {r.status}")
    print("Abre esta URL en un navegador para ver el checkout y pagar con PSE de prueba:")
    print(url)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, w.ErrorWompi) as e:
        sys.exit(f"Detenido: {e}")
