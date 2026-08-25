#!/bin/sh
set -eu

status_root=/var/lib/mission-control-install
### The service account executes the saved Codex installer, while root retains
### ownership of the installer evidence directory and downloaded artifact.
install -d -o root -g mission-control -m 0750 "$status_root"

apt-get update
apt-get install -y ca-certificates curl gpg jq gh git
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

curl --fail --location --proto '=https' --tlsv1.2 https://pkg.ddev.com/apt/gpg.key -o /etc/apt/keyrings/ddev.asc
chmod a+r /etc/apt/keyrings/ddev.asc
cat >/etc/apt/sources.list.d/ddev.sources <<'EOF'
Types: deb
URIs: https://pkg.ddev.com/apt/
Suites: *
Components: *
Signed-By: /etc/apt/keyrings/ddev.asc
EOF

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin ddev
systemctl enable --now docker
usermod -aG docker mission-control

codex_installer=$status_root/codex-install.sh
curl --fail --location --proto '=https' --tlsv1.2 https://chatgpt.com/codex/install.sh -o "$codex_installer"
chown root:mission-control "$codex_installer"
chmod 0750 "$codex_installer"
sha256sum "$codex_installer" >"$status_root/codex-install.sh.sha256"
runuser -u mission-control -- env HOME=/var/lib/mission-control sh "$codex_installer"

codex_binary=/var/lib/mission-control/.local/bin/codex
if [ ! -x "$codex_binary" ]; then
    echo "official Codex installer did not create expected binary" >&2
    exit 1
fi
### Do not symlink into the service account's mode-0700 home: the owner must
### be able to type `vincent` and launch this global CLI from the console.
install -o root -g root -m 0755 "$codex_binary" /usr/local/bin/codex

docker version
docker info
docker run --rm hello-world
runuser -u mission-control -- docker info
ddev version
gh --version
codex --version
runuser -u nobody -- /usr/local/bin/codex --version

python3 - "$status_root/toolchain.json" <<'PY'
import json, subprocess, sys
from pathlib import Path

def output(*command):
    return subprocess.run(command, text=True, capture_output=True, check=True).stdout.strip()

payload = {
    "schema_version": 1,
    "docker": output("docker", "--version"),
    "ddev": output("ddev", "version"),
    "github_cli": output("gh", "--version").splitlines()[0],
    "codex": output("codex", "--version"),
    "codex_installer_sha256": Path("/var/lib/mission-control-install/codex-install.sh.sha256").read_text().split()[0],
}
Path(sys.argv[1]).write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
PY
chmod 0600 "$status_root/toolchain.json"
