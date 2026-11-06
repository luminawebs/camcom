"""Códigos de canal del Pase (`?c=`), decisión D-05 del 2026-11-06 (issue #15).

Dos clases de código:

- **Canal de origen**: por dónde llegó la persona al registro gratis (campañas de la Cámara,
  de EduNest, aliados). Se guarda la primera vez en `personas.canal_origen` y no se pisa.
- **Enlace de curso** (`curso-avs-gNN`): el botón de compra al final de la U3. No es un canal:
  dice desde qué curso se compró el Pase y se guarda aparte (`suscripciones.curso`).

Un código que no está en la lista se guarda igual (para no perder datos de un enlace mal
escrito) y el tablero lo marca como «no reconocido». Para agregar un canal: una línea en CANALES.
"""
import re

SIN_CANAL = "sin-canal"

CANALES = {
    "camara-whatsapp": "WhatsApp de la Cámara a afiliados (difusión, estados, grupos)",
    "camara-correo": "Correo de la Cámara a afiliados",
    "camara-redes": "Redes de la Cámara (Facebook, Instagram)",
    "camara-evento": "Charla o taller presencial con la Cámara (QR)",
    "brevo-registrados": "Correo de EduNest (Brevo) a registrados que autorizaron",
    "wa-edunest": "WhatsApp Business de EduNest",
    "ig-organico": "Instagram orgánico de EduNest",
    "fb-organico": "Facebook orgánico de EduNest",
    "meta-ads": "Anuncios en Meta (Facebook/Instagram) segmentados a Soacha",
    "qr-impreso": "Impresos con QR (afiches o volantes)",
}
# Uno por aliado (gremios, contadores, asociaciones): aliado-01, aliado-02…
ALIADO = re.compile(r"aliado-\d{2,3}")
CURSO = re.compile(r"curso-[a-z0-9-]+")
FORMATO = re.compile(r"[a-z0-9][a-z0-9-]{0,39}")


def normalizar(codigo):
    """Código limpio en minúsculas, o SIN_CANAL si viene vacío o con caracteres raros."""
    c = (codigo or "").strip().lower()
    return c if FORMATO.fullmatch(c) else SIN_CANAL


def es_curso(codigo):
    return bool(codigo) and bool(CURSO.fullmatch(codigo))


def es_origen(codigo):
    """Cualquier código que cuente como canal de origen (conocido o no), no un enlace de curso."""
    return bool(codigo) and codigo != SIN_CANAL and not es_curso(codigo) and bool(FORMATO.fullmatch(codigo))


def reconocido(codigo):
    return codigo in CANALES or bool(ALIADO.fullmatch(codigo or "")) or es_curso(codigo)


def descripcion(codigo):
    if codigo in CANALES:
        return CANALES[codigo]
    if ALIADO.fullmatch(codigo or ""):
        return "Aliado " + codigo.split("-")[1]
    if es_curso(codigo):
        return "Enlace de compra al final de la U3"
    if codigo == SIN_CANAL:
        return "Sin código (entró directo)"
    return "No reconocido: revisar el enlace"
