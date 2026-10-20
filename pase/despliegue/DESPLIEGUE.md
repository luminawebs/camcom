# Publicar el conector del Pase en un droplet

Para un droplet Ubuntu que ya tiene otro proyecto. El conector queda **aislado**: usuario
`pase` sin shell, código en `/opt/pase`, datos en `/var/lib/pase`, configuración en
`/etc/pase/pase.env`, un sitio nginx propio (`/etc/nginx/sites-available/pase`) y servicios
`pase*.service`. No modifica sitios, puertos ni servicios existentes.

## 0. Antes (David)

- Registro DNS **A** `pase` → IP del droplet en el administrador de DNS de edunest.co.
- En Wompi, sandbox: URL de eventos `https://pase.edunest.co/webhooks/wompi` (después del paso 3).

## 1. Revisar (solo lectura)

```
ssh <droplet> 'bash -s' < pase/despliegue/revisar.sh
```

Muestra sistema, puertos ocupados, sitios nginx, certificados, contenedores y servicios.
Con eso se elige un puerto libre (por defecto 8091) y se confirma que nginx es el que
atiende el 80/443. Si el servidor usa Caddy, Traefik o Docker en esos puertos, este kit se
adapta antes de instalar.

## 2. Instalar

```
scp -r pase <droplet>:/tmp/pase
ssh <droplet> 'sudo bash /tmp/pase/despliegue/instalar.sh /tmp/pase pase.edunest.co 8091'
```

La primera vez crea `/etc/pase/pase.env` desde `pase.env.ejemplo` y **no arranca** el
servicio. Se completan las llaves de sandbox de Wompi y los dos secretos de sesión
(`openssl rand -hex 32`) directamente en el servidor:

```
sudo nano /etc/pase/pase.env
sudo bash /tmp/pase/despliegue/instalar.sh /tmp/pase pase.edunest.co 8091
```

El script corre las pruebas en el servidor, arranca `pase.service` y los temporizadores
(`cobro` 6:00, `conciliar` 6:30 hora Colombia, `pendientes` cada hora) y consulta `/salud`.

## 3. HTTPS

Cuando `pase.edunest.co` ya resuelva a la IP del droplet:

```
sudo certbot --nginx -d pase.edunest.co --redirect -m <correo> --agree-tos -n
curl https://pase.edunest.co/salud
```

## Operación

| Qué | Comando |
|---|---|
| Estado | `systemctl status pase` · `systemctl list-timers 'pase*'` |
| Registros | `journalctl -u pase -f` · `/var/log/nginx/pase.*.log` |
| Resumen | `curl -H "Authorization: Bearer $PASE_ADMIN_TOKEN" http://127.0.0.1:8091/admin/resumen` (solo desde el servidor) |
| Actualizar | copiar el nuevo `pase/` y volver a correr `instalar.sh` (guarda la versión anterior en `/opt/pase/pase.anterior`) |
| Volver atrás | `sudo mv /opt/pase/pase /opt/pase/pase.malo && sudo mv /opt/pase/pase.anterior /opt/pase/pase && sudo systemctl restart pase` |
| Respaldo | `sqlite3 /var/lib/pase/pase.db ".backup /var/lib/pase/respaldo-$(date +%F).db"` |
| Quitar todo | `systemctl disable --now pase pase-cobro.timer pase-conciliar.timer pase-pendientes.timer; rm /etc/nginx/sites-enabled/pase; systemctl reload nginx` |

Mientras `PASE_MOODLE_SIMULADO=1`, las cohortes se simulan en memoria y no se toca
portal.edunest.co. Producción de Wompi sigue bloqueada sin `PASE_PERMITIR_PRODUCCION=1`.
