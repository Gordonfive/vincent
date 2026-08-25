#!/bin/sh
set -eu

if [ "$(id -u)" -ne 0 ]; then
    echo "installer must run as root" >&2
    exit 1
fi

source_root=${1:-}
if [ -z "$source_root" ] || [ ! -f "$source_root/pyproject.toml" ]; then
    echo "usage: install.sh /absolute/path/to/verified/platform-checkout" >&2
    exit 2
fi
case "$source_root" in
    /*) ;;
    *) echo "source checkout path must be absolute" >&2; exit 2 ;;
esac

service_user=mission-control
install_root=/opt/mission-control
configuration_root=/etc/mission-control
state_root=/var/lib/mission-control
workspace_root=/srv/codex

if ! getent passwd "$service_user" >/dev/null; then
    useradd --system --home-dir "$state_root" --shell /usr/sbin/nologin "$service_user"
fi

install -d -o root -g root -m 0755 "$install_root"
install -d -o root -g "$service_user" -m 0750 "$configuration_root"
install -d -o "$service_user" -g "$service_user" -m 0700 "$state_root" "$state_root/identity"
install -d -o "$service_user" -g "$service_user" -m 0750 "$workspace_root" "$workspace_root/worktrees"

### Debian installs the reviewed build backend as python3-setuptools. Make that
### system package visible inside the venv; otherwise pip's intentionally
### offline --no-build-isolation build cannot import setuptools.build_meta.
python3 -m venv --system-site-packages "$install_root/venv"
"$install_root/venv/bin/python" -c 'import setuptools.build_meta'
"$install_root/venv/bin/python" -m pip install --no-deps --no-build-isolation "$source_root"
ln -sfn "$install_root/venv/bin/vincent" /usr/local/bin/vincent

if [ ! -f "$configuration_root/worker.toml" ]; then
    install -o root -g "$service_user" -m 0640 \
        "$source_root/config/worker.example.toml" "$configuration_root/worker.toml"
fi

install -o root -g root -m 0644 \
    "$source_root/installer/systemd/mission-control-worker.service" \
    /etc/systemd/system/mission-control-worker.service
systemctl daemon-reload

if [ -e "$state_root/identity/identity.json" ]; then
    echo "existing identity detected; refusing implicit reuse" >&2
    echo "follow the documented recovery or replacement enrollment procedure" >&2
    exit 3
fi

runuser -u "$service_user" -- \
    "$install_root/venv/bin/mission-control-worker" \
    --identity-root "$state_root/identity" enroll

echo "installation staged; review and approve enrollment before enabling the service"
echo "service was not enabled or started"
