#!/usr/bin/env bash
# Instala o actualiza el conector del Pase en un droplet Ubuntu con nginx.
# Todo queda aparte de lo que ya corre: usuario «pase», /opt/pase, /etc/pase, un sitio
# nginx propio y servicios systemd con prefijo pase-. Se puede correr varias veces.
#
#   sudo bash instalar.sh <carpeta con el código pase/> [dominio] [puerto]
#   sudo bash instalar.sh /tmp/pase pase.edunest.co 8091
set -euo pipefail

ORIGEN=${1:?Falta la carpeta con el código pase/}
DOMINIO=${2:-pase.edunest.co}
PUERTO=${3:-8091}
APP=/opt/pase
DATOS=/var/lib/pase
ENVF=/etc/pase/pase.env
AQUI=$(cd "$(dirname "$0")" && pwd)

[ "$(id -u)" = 0 ] || { echo "Correr con sudo"; exit 1; }
command -v python3 >/dev/null || { echo "Falta python3"; exit 1; }
python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))' || { echo "Se necesita Python 3.9+"; exit 1; }
command -v nginx >/dev/null || { echo "Falta nginx (apt install nginx)"; exit 1; }
if ss -ltn | awk '{print $4}' | grep -qE "[:.]$PUERTO\$" && ! systemctl is-active -q pase; then
  echo "El puerto $PUERTO ya está en uso por otro servicio: elige otro"; exit 1
fi

echo "› Usuario y carpetas"
id pase >/dev/null 2>&1 || useradd --system --home "$DATOS" --shell /usr/sbin/nologin pase
install -d -o pase -g pase -m 750 "$DATOS"
install -d -o root -g pase -m 750 /etc/pase
install -d -o root -g root -m 755 "$APP"

echo "› Código"
rm -rf "$APP/pase.nuevo"
cp -r "$ORIGEN" "$APP/pase.nuevo"
rm -rf "$APP/pase.nuevo/__pycache__" "$APP/pase.nuevo"/*.db
[ -d "$APP/pase" ] && rm -rf "$APP/pase.anterior" && mv "$APP/pase" "$APP/pase.anterior"
mv "$APP/pase.nuevo" "$APP/pase"
chown -R root:root "$APP"

echo "› Configuración"
if [ ! -f "$ENVF" ]; then
  sed -e "s#__DOMINIO__#$DOMINIO#g" -e "s#__PUERTO__#$PUERTO#g" "$AQUI/pase.env.ejemplo" > "$ENVF"
  echo "  Creado $ENVF: completa las llaves y vuelve a correr este script."
fi
chown root:pase "$ENVF"; chmod 640 "$ENVF"

echo "› Servicios systemd"
for f in "$AQUI"/systemd/*; do
  sed -e "s#__APP__#$APP#g" -e "s#__DATOS__#$DATOS#g" -e "s#__ENV__#$ENVF#g" "$f" \
    > "/etc/systemd/system/$(basename "$f")"
done
systemctl daemon-reload

echo "› Sitio nginx ($DOMINIO → 127.0.0.1:$PUERTO)"
SITIO=/etc/nginx/sites-available/pase
sed -e "s#__DOMINIO__#$DOMINIO#g" -e "s#__PUERTO__#$PUERTO#g" "$AQUI/nginx-pase.conf" > "$SITIO"
ln -sf "$SITIO" /etc/nginx/sites-enabled/pase
nginx -t && systemctl reload nginx

echo "› Pruebas del código en el servidor"
(cd "$APP" && PASE_LOG=0 sudo -u pase -H python3 -m unittest pase.pruebas 2>&1 | tail -3)

if grep -qE '^WOMPI_LLAVE_PRIVADA=prv_(test|prod)_.+' "$ENVF"; then
  echo "› Arranque"
  systemctl enable --now pase.service pase-cobro.timer pase-conciliar.timer pase-pendientes.timer
  systemctl restart pase.service
  sleep 2; curl -fsS "http://127.0.0.1:$PUERTO/salud" && echo
else
  echo "› Faltan llaves en $ENVF: el servicio NO se arrancó."
fi

if [ ! -d "/etc/letsencrypt/live/$DOMINIO" ]; then
  echo
  echo "Para el HTTPS, cuando $DOMINIO ya apunte a este droplet:"
  echo "  certbot --nginx -d $DOMINIO --redirect -m <correo> --agree-tos -n"
fi
echo "Listo."
