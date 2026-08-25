#!/bin/sh
set -eu

image=${1:-}
if [ -z "$image" ] || [ ! -f "$image" ]; then
    echo "usage: inspect-image.sh /path/to/installer.iso" >&2
    exit 2
fi

inspection_root=$(mktemp -d)
trap 'rm -rf "$inspection_root"' EXIT HUP INT TERM

for required in \
    /preseed.cfg \
    /mission-control/platform.tar.gz \
    /mission-control/first-boot.sh \
    /mission-control/mission-control-first-boot.service \
    /isolinux/mission-control.cfg; do
    extracted="$inspection_root/$(basename -- "$required")"
    xorriso -osirrox on -indev "$image" -extract "$required" "$extracted" >/dev/null 2>&1 || {
        echo "missing installer payload: $required" >&2
        exit 3
    }
    if [ ! -s "$extracted" ]; then
        echo "empty installer payload: $required" >&2
        exit 3
    fi
done

tar -tzf "$inspection_root/platform.tar.gz" >/dev/null
grep -F 'mission-control/first-boot.sh' "$inspection_root/preseed.cfg" >/dev/null

if grep -a -E 'BEGIN (OPENSSH|RSA|EC) PRIVATE KEY' "$image" >/dev/null; then
    echo "private key material detected" >&2
    exit 4
fi

echo "INSTALLER_INSPECTION=PASS"
