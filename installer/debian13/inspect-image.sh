#!/bin/sh
set -eu

image=${1:-}
[ -n "$image" ] && [ -f "$image" ] || { echo "usage: inspect-image.sh /path/to/installer.iso" >&2; exit 2; }
script_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
build_number=$(tr -d '\r\n' <"$script_root/BUILD_NUMBER")
expected_volume="VINCENT_B${build_number}"
case "$(basename -- "$image")" in *"build-${build_number}"*) ;; *) echo "image filename does not contain build-${build_number}" >&2; exit 3;; esac

inspection_root=$(mktemp -d)
trap 'rm -rf "$inspection_root"' EXIT HUP INT TERM

for required in \
    /preseed.cfg \
    /vincent/platform.tar.gz \
    /vincent/expected-commit \
    /vincent/build-number \
    /vincent/first-boot.sh \
    /vincent/self-test.sh \
    /vincent/console-status.sh \
    /vincent/codex-console.sh \
    /vincent/vincent-first-boot.service \
    /vincent/vincent-console-status.service \
    /vincent/vincent-codex-console.service \
    /isolinux/mission-control.cfg; do
    extracted="$inspection_root/$(basename -- "$required")"
    xorriso -osirrox on -indev "$image" -extract "$required" "$extracted" >/dev/null 2>&1 || { echo "missing installer payload: $required" >&2; exit 3; }
    [ -s "$extracted" ] || { echo "empty installer payload: $required" >&2; exit 3; }
done

tar -tzf "$inspection_root/platform.tar.gz" >/dev/null
[ "$(tr -d '\r\n' <"$inspection_root/build-number")" = "$build_number" ] || { echo "embedded build number mismatch" >&2; exit 3; }
volume=$(xorriso -indev "$image" -pvd_info 2>/dev/null | sed -n "s/^Volume id    : '\(.*\)'$/\1/p" | head -n1)
[ "$volume" = "$expected_volume" ] || { echo "volume id mismatch: expected $expected_volume got $volume" >&2; exit 3; }

grep -F 'passwd/make-user boolean false' "$inspection_root/preseed.cfg" >/dev/null
grep -F 'in-target passwd -l root' "$inspection_root/preseed.cfg" >/dev/null
if grep -E 'partman-auto/(method|choose_recipe|disk)|partman-auto-lvm' "$inspection_root/preseed.cfg" >/dev/null; then
    echo "Vincent-specific forced partitioning detected" >&2
    exit 3
fi
grep -F 'BUILD:' "$inspection_root/console-status.sh" >/dev/null
grep -F 'runuser -u "$service_user"' "$inspection_root/codex-console.sh" >/dev/null

if grep -a -E 'BEGIN (OPENSSH|RSA|EC) PRIVATE KEY' "$image" >/dev/null; then echo "private key material detected" >&2; exit 4; fi

echo "BUILD_NUMBER=$build_number"
echo "VOLUME_ID=$volume"
echo "INSTALLER_INSPECTION=PASS"
