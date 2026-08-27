#!/bin/sh
set -eu

output=${1:-}
[ -n "$output" ] || { echo "usage: prepare-offline-packages.sh OUTPUT.tar.gz" >&2; exit 2; }

for command in apt-get dpkg tar sha256sum; do
    command -v "$command" >/dev/null || { echo "missing required command: $command" >&2; exit 2; }
done

arch=$(dpkg --print-architecture)
[ "$arch" = "amd64" ] || { echo "offline installer bundle currently requires amd64 builder" >&2; exit 2; }

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT HUP INT TERM
state="$work/state"
cache="$work/cache"
log="$work/log"
mkdir -p "$state/lists/partial" "$cache/archives/partial" "$log"
: >"$state/status"

packages='sudo git curl ca-certificates gpg jq gh rsync openssh-client openssh-server python3 python3-venv python3-pip python3-setuptools build-essential xz-utils network-manager iw wpasupplicant rfkill bubblewrap'

apt_opts="-o Debug::NoLocking=1 -o Dir::State=$state -o Dir::State::status=$state/status -o Dir::Cache=$cache -o Dir::Cache::archives=$cache/archives -o Dir::Log=$log -o APT::Architecture=amd64"

# Use the builder's configured Debian sources, but an empty package-status DB,
# so apt downloads the complete dependency closure rather than assuming the
# builder's already-installed packages will exist in the target system.
# shellcheck disable=SC2086
apt-get $apt_opts update
# shellcheck disable=SC2086
apt-get $apt_opts --download-only --no-install-recommends -y install $packages

set -- "$cache"/archives/*.deb
[ -e "$1" ] || { echo "offline package bundle is empty" >&2; exit 3; }

manifest="$work/offline-packages.manifest"
(
    cd "$cache/archives"
    sha256sum ./*.deb | sort
) >"$manifest"

mkdir -p "$(dirname -- "$output")"
tar -C "$cache/archives" -czf "$output" ./*.deb
cp "$manifest" "${output}.manifest"

echo "offline_bundle=$output"
echo "offline_bundle_sha256=$(sha256sum "$output" | awk '{print $1}')"
echo "offline_package_count=$(wc -l <"$manifest" | tr -d ' ')"
