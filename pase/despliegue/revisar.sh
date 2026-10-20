#!/usr/bin/env bash
# Revisión de SOLO LECTURA del droplet antes de instalar el conector del Pase.
# No cambia nada. Uso: ssh <droplet> 'bash -s' < pase/despliegue/revisar.sh
set -u
t() { echo; echo "=== $* ==="; }

t "Sistema"
. /etc/os-release 2>/dev/null && echo "$PRETTY_NAME"; uname -r; uptime
t "Recursos"
nproc; free -h | sed -n 1,2p; df -h / | tail -1
t "Python"
command -v python3 && python3 --version
t "Puertos en escucha"
(ss -ltnp 2>/dev/null || netstat -ltnp 2>/dev/null) | sed 's/users:.*//' | sort -u
t "Servidores web y proxys"
for s in nginx apache2 caddy traefik haproxy docker; do
  printf '%-8s ' "$s"; systemctl is-active "$s" 2>/dev/null || echo "-"
done
t "Sitios nginx"
ls -1 /etc/nginx/sites-enabled /etc/nginx/conf.d 2>/dev/null
grep -rhoE 'server_name[^;]+' /etc/nginx/sites-enabled /etc/nginx/conf.d 2>/dev/null | sort -u
t "Certificados"
command -v certbot && certbot certificates 2>/dev/null | grep -E 'Certificate Name|Domains|Expiry' || echo "sin certbot"
t "Contenedores"
command -v docker >/dev/null && docker ps --format '{{.Names}}  {{.Image}}  {{.Ports}}' 2>/dev/null || echo "sin docker"
t "Servicios propios (systemd, no del sistema)"
systemctl list-units --type=service --state=running --no-legend 2>/dev/null \
  | awk '{print $1}' | grep -vE '^(systemd|dbus|cron|ssh|rsyslog|polkit|udisks|snapd|getty|serial|unattended|multipathd|networkd|ModemManager|packagekit|fwupd|irqbalance|atd|chrony|qemu|droplet|do-agent|user@)' || true
t "Firewall"
ufw status 2>/dev/null | head -20 || echo "sin ufw"
t "¿Ya existe algo del Pase?"
id pase 2>/dev/null || echo "usuario pase: no existe"
ls -d /opt/pase /etc/pase 2>/dev/null || echo "carpetas /opt/pase y /etc/pase: no existen"
t "DNS de pase.edunest.co"
getent hosts pase.edunest.co || echo "pase.edunest.co aún no resuelve"
curl -s -m 5 https://api.ipify.org && echo " (IP pública de este droplet)"
