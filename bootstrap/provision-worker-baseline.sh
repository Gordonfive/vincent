#!/bin/sh
set -eu

status_root=/var/lib/vincent-install
service_user=vincent
service_home=/var/lib/vincent
service_config=$service_home/.config
service_cache=$service_home/.cache
service_data=$service_home/.local/share
codex_root=/opt/vincent-codex

# systemd services do not guarantee a login-style root environment.
export HOME=/root USER=root LOGNAME=root
export XDG_CONFIG_HOME=/root/.config XDG_CACHE_HOME=/root/.cache XDG_DATA_HOME=/root/.local/share
install -d -m 0700 "$HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME" "$XDG_DATA_HOME"

install -d -o root -g "$service_user" -m 0750 "$status_root"
install -d -o "$service_user" -g "$service_user" -m 0700 \
    "$service_home" "$service_config" "$service_cache" "$service_data" "$service_home/.local/bin"

service_run() {
    runuser -u "$service_user" -- env \
        HOME="$service_home" USER="$service_user" LOGNAME="$service_user" \
        XDG_CONFIG_HOME="$service_config" XDG_CACHE_HOME="$service_cache" \
        XDG_DATA_HOME="$service_data" PATH=/usr/local/bin:/usr/bin:/bin "$@"
}

apt-get update
apt-get install -y ca-certificates curl gpg jq gh git network-manager iw wpasupplicant rfkill bubblewrap
install -m 0755 -d /etc/apt/keyrings

curl --fail --location --proto '=https' --tlsv1.2 https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
cat >/etc/apt/sources.list.d/docker.sources <<'EOF'
Types: deb
URIs: https://download.docker.com/linux/debian
Suites: trixie
Components: stable
Architectures: amd64
Signed-By: /etc/apt/keyrings/docker.asc
EOF

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
systemctl enable --now docker NetworkManager
usermod -aG docker "$service_user"

# Run the official Codex installer from Vincent's own protected cache. The
# root-owned status directory is intentionally not used as an executable path
# for the non-login service account.
codex_installer=$service_cache/codex-install.sh
curl --fail --location --proto '=https' --tlsv1.2 https://chatgpt.com/codex/install.sh -o "$codex_installer"
chown "$service_user:$service_user" "$codex_installer"
chmod 0700 "$codex_installer"
sha256sum "$codex_installer" >"$status_root/codex-install.sh.sha256"
service_run sh "$codex_installer"

# Codex now ships companion executables used by tool-backed sessions. Do not
# copy only the top-level `codex` binary into /usr/local/bin: Codex resolves
# codex-code-mode-host relative to its own executable directory. Preserve the
# required companion next to the root-owned runtime copy.
codex_binary=$service_home/.local/bin/codex
[ -x "$codex_binary" ] || { echo "official Codex installer did not create expected binary" >&2; exit 1; }
codex_host=$(find "$service_home" -type f -name codex-code-mode-host -perm -u+x -print -quit 2>/dev/null || true)
[ -n "$codex_host" ] || { echo "official Codex installer did not create codex-code-mode-host" >&2; exit 1; }
install -d -o root -g root -m 0755 "$codex_root/bin"
install -o root -g root -m 0755 "$codex_binary" "$codex_root/bin/codex"
install -o root -g root -m 0755 "$codex_host" "$codex_root/bin/codex-code-mode-host"
ln -sfn "$codex_root/bin/codex" /usr/local/bin/codex
ln -sfn "$codex_root/bin/codex-code-mode-host" /usr/local/bin/codex-code-mode-host

docker version
docker info
docker run --rm hello-world
service_run docker info
gh --version
bwrap --version
codex --version
codex-code-mode-host --help >/dev/null 2>&1 || true
service_run /usr/local/bin/codex --version
nmcli --version

python3 - "$status_root/toolchain.json" <<'PY'
import json, subprocess, sys
from pathlib import Path

def output(*command):
    return subprocess.run(command, text=True, capture_output=True, check=True).stdout.strip()

payload = {
    "schema_version": 1,
    "docker": output("docker", "--version"),
    "github_cli": output("gh", "--version").splitlines()[0],
    "codex": output("codex", "--version"),
    "bubblewrap": output("bwrap", "--version"),
    "codex_code_mode_host": str(Path("/usr/local/bin/codex-code-mode-host").resolve()),
    "network_manager": output("nmcli", "--version"),
    "codex_installer_sha256": Path("/var/lib/vincent-install/codex-install.sh.sha256").read_text().split()[0],
}
Path(sys.argv[1]).write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
PY
chmod 0600 "$status_root/toolchain.json"
