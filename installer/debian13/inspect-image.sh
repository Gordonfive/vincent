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
    /mission-control/preseed-assert.sh \
    /mission-control/platform.tar.gz \
    /mission-control/expected-commit \
    /mission-control/first-boot.sh \
    /mission-control/self-test.sh \
    /mission-control/console-status.sh \
    /mission-control/mission-control-first-boot.service \
    /mission-control/vincent-console-status.service \
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
grep -F 'preseed/early_command string /bin/sh /cdrom/mission-control/preseed-assert.sh' "$inspection_root/preseed.cfg" >/dev/null
grep -F 'passwd/make-user boolean false' "$inspection_root/preseed.cfg" >/dev/null
grep -F 'netcfg/get_hostname string vincent-worker' "$inspection_root/preseed.cfg" >/dev/null
grep -F 'partman-auto/init_automatically_partition select 60some_device_lvm__________lvm' "$inspection_root/preseed.cfg" >/dev/null
grep -F 'partman-auto/method string lvm' "$inspection_root/preseed.cfg" >/dev/null
grep -F 'partman-auto-lvm/new_vg_name string vincent-vg' "$inspection_root/preseed.cfg" >/dev/null
grep -F 'partman-auto/choose_recipe select atomic' "$inspection_root/preseed.cfg" >/dev/null
grep -F 'https://github.com/Gordonfive/vincent.git' "$inspection_root/first-boot.sh" >/dev/null
grep -F 'expected-commit' "$inspection_root/first-boot.sh" >/dev/null

expected_commit=$(cat "$inspection_root/expected-commit")
printf '%s' "$expected_commit" | grep -E '^[0-9a-f]{40}$' >/dev/null

if grep -a -E 'BEGIN (OPENSSH|RSA|EC) PRIVATE KEY' "$image" >/dev/null; then
    echo "private key material detected" >&2
    exit 4
fi

echo "INSTALLER_INSPECTION=PASS"
