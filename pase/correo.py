"""Envío de los avisos del Pase por SMTP (Brevo en smtp-relay.brevo.com:2525).

DigitalOcean bloquea los puertos 25, 465 y 587; Brevo atiende también en 2525 con STARTTLS.
La IP del droplet tiene que estar autorizada en Brevo › Seguridad › IP autorizadas.
Con HTML el mensaje va como texto + HTML, y el logo adjunto dentro (cid:logo).
"""
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

from .plantillas_correo import LOGO


class Smtp:
    """Una conexión por tanda de avisos; se usa con `with`."""

    def __init__(self, config):
        self.c = config
        self.s = None

    def __enter__(self):
        self.s = smtplib.SMTP(self.c.smtp_host, self.c.smtp_puerto, timeout=30)
        self.s.starttls(context=ssl.create_default_context())
        if self.c.smtp_usuario:
            self.s.login(self.c.smtp_usuario, self.c.smtp_clave)
        return self

    def __exit__(self, *_):
        try:
            self.s.quit()
        except smtplib.SMTPException:
            pass

    def enviar(self, para, asunto, cuerpo, html=None):
        m = EmailMessage()
        m["From"] = self.c.correo_remitente
        m["To"] = para
        m["Subject"] = asunto
        m["Date"] = formatdate(localtime=True)
        m["Message-ID"] = make_msgid(domain=self.c.correo_remitente.rsplit("@", 1)[-1].strip("> "))
        m.set_content(cuerpo)
        if html:
            m.add_alternative(html, subtype="html")
            if "cid:logo" in html:
                with open(LOGO, "rb") as f:
                    m.get_payload()[1].add_related(f.read(), "image", "png", cid="<logo>",
                                                   filename="edunest.png")
        self.s.send_message(m)
