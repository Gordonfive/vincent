#!/bin/sh
set -u

log=/var/log/vincent-installer-network-preflight.log
exec >"$log" 2>&1

emit() {
    printf 'VINCENT_NET_PREFLIGHT %s\n' "$*"
    command -v logger >/dev/null 2>&1 && logger -t VINCENT_NET_PREFLIGHT -- "$*" || true
}

emit "BEGIN"
emit "DATE=$(date -u 2>/dev/null || true)"
emit "RESOLV_CONF_BEGIN"
cat /etc/resolv.conf 2>/dev/null || true
emit "RESOLV_CONF_END"

emit "ROUTES_BEGIN"
ip route 2>/dev/null || route -n 2>/dev/null || true
emit "ROUTES_END"

for host in deb.debian.org security.debian.org github.com chatgpt.com download.docker.com; do
    emit "SYSTEM_DNS host=$host"
    if command -v getent >/dev/null 2>&1; then
        getent ahosts "$host" 2>&1 || true
    elif command -v nslookup >/dev/null 2>&1; then
        nslookup "$host" 2>&1 || true
    fi
    if command -v nslookup >/dev/null 2>&1; then
        emit "DIRECT_DNS host=$host server=1.1.1.1"
        nslookup "$host" 1.1.1.1 2>&1 || true
        emit "DIRECT_DNS host=$host server=9.9.9.9"
        nslookup "$host" 9.9.9.9 2>&1 || true
    fi
done

if command -v wget >/dev/null 2>&1; then
    for url in \
        http://deb.debian.org/debian/dists/trixie/InRelease \
        http://security.debian.org/debian-security/dists/trixie-security/InRelease; do
        emit "HTTP_PROBE url=$url"
        wget -S --spider -T 15 "$url" 2>&1 || true
    done
fi

emit "END"
# Also copy the complete preflight into the installer syslog so Alt+F4 contains
# the evidence without requiring a shell login.
while IFS= read -r line; do
    command -v logger >/dev/null 2>&1 && logger -t VINCENT_NET_EVIDENCE -- "$line" || true
done <"$log"
exit 0
