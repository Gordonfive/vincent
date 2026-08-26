#!/bin/sh
set -eu

script_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repository_root=$(CDPATH= cd -- "$script_root/../.." && pwd)
. "$script_root/source.env"

source_iso=${1:-}
[ -n "$source_iso" ] && [ -f "$source_iso" ] || { echo "usage: build-image.sh /path/to/verified-debian.iso [output.iso]" >&2; exit 2; }

build_number=$(tr -d '\r\n' <"$script_root/BUILD_NUMBER")
case "$build_number" in *[!0-9]*|'') echo "invalid BUILD_NUMBER" >&2; exit 2;; esac
output_iso=${2:-$repository_root/dist/vincent-debian-${DEBIAN_VERSION}-${DEBIAN_ARCH}-build-${build_number}.iso}
case "$(basename -- "$output_iso")" in *"build-${build_number}"*) ;; *) echo "output filename must contain build-${build_number}" >&2; exit 2;; esac
[ ! -e "$output_iso" ] || { echo "refusing to overwrite or append to existing output: $output_iso" >&2; exit 3; }

for command in git xorriso tar sha256sum python3; do command -v "$command" >/dev/null || { echo "required build command is missing: $command" >&2; exit 2; }; done
tracked_dirty=$(git -C "$repository_root" status --porcelain --untracked-files=no)
[ -z "$tracked_dirty" ] || { echo "installer builds require a clean tracked Git checkout" >&2; exit 3; }
commit=$(git -C "$repository_root" rev-parse HEAD)
source_date_epoch=$(git -C "$repository_root" show -s --format=%ct HEAD)
volume_id="VINCENT_B${build_number}"

work_root=$(mktemp -d)
trap 'rm -rf "$work_root"' EXIT HUP INT TERM
payload_root=$work_root/payload
install -d "$payload_root" "$(dirname -- "$output_iso")"

git -C "$repository_root" archive --format=tar.gz --output="$payload_root/platform.tar.gz" HEAD
printf '%s\n' "$commit" >"$payload_root/expected-commit"
printf '%s\n' "$build_number" >"$payload_root/build-number"
install -m 0644 "$script_root/preseed.cfg" "$payload_root/preseed.cfg"
install -m 0755 "$script_root/first-boot.sh" "$payload_root/first-boot.sh"
install -m 0755 "$script_root/self-test.sh" "$payload_root/self-test.sh"
install -m 0755 "$script_root/console-status.sh" "$payload_root/console-status.sh"
install -m 0755 "$script_root/codex-console.sh" "$payload_root/codex-console.sh"
install -m 0644 "$script_root/vincent-first-boot.service" "$payload_root/vincent-first-boot.service"
install -m 0644 "$script_root/vincent-console-status.service" "$payload_root/vincent-console-status.service"
install -m 0644 "$script_root/vincent-codex-console.service" "$payload_root/vincent-codex-console.service"
install -m 0644 "$script_root/isolinux-mission-control.cfg" "$payload_root/isolinux-mission-control.cfg"
install -m 0644 "$script_root/grub-mission-control.cfg" "$payload_root/grub-mission-control.cfg"

xorriso -osirrox on -indev "$source_iso" -extract /isolinux/menu.cfg "$work_root/menu.cfg" >/dev/null 2>&1
xorriso -osirrox on -indev "$source_iso" -extract /boot/grub/grub.cfg "$work_root/grub.cfg" >/dev/null 2>&1
chmod u+w "$work_root/menu.cfg" "$work_root/grub.cfg"
printf '\ninclude mission-control.cfg\n' >>"$work_root/menu.cfg"
cat "$payload_root/grub-mission-control.cfg" >>"$work_root/grub.cfg"
find "$payload_root" "$work_root/menu.cfg" "$work_root/grub.cfg" -exec touch -d "@$source_date_epoch" {} +

xorriso \
    -indev "$source_iso" \
    -outdev "$output_iso" \
    -volid "$volume_id" \
    -boot_image any replay \
    -map "$payload_root/preseed.cfg" /preseed.cfg \
    -map "$payload_root/platform.tar.gz" /vincent/platform.tar.gz \
    -map "$payload_root/expected-commit" /vincent/expected-commit \
    -map "$payload_root/build-number" /vincent/build-number \
    -map "$payload_root/first-boot.sh" /vincent/first-boot.sh \
    -map "$payload_root/self-test.sh" /vincent/self-test.sh \
    -map "$payload_root/console-status.sh" /vincent/console-status.sh \
    -map "$payload_root/codex-console.sh" /vincent/codex-console.sh \
    -map "$payload_root/vincent-first-boot.service" /vincent/vincent-first-boot.service \
    -map "$payload_root/vincent-console-status.service" /vincent/vincent-console-status.service \
    -map "$payload_root/vincent-codex-console.service" /vincent/vincent-codex-console.service \
    -map "$payload_root/isolinux-mission-control.cfg" /isolinux/mission-control.cfg \
    -map "$work_root/menu.cfg" /isolinux/menu.cfg \
    -map "$work_root/grub.cfg" /boot/grub/grub.cfg \
    -commit >/dev/null

source_sha256=$(sha256sum "$source_iso" | awk '{print $1}')
output_sha256=$(sha256sum "$output_iso" | awk '{print $1}')
manifest=${output_iso}.manifest.json
python3 - "$manifest" "$commit" "$build_number" "$volume_id" "$DEBIAN_VERSION" "$DEBIAN_ARCH" "$source_iso" "$source_sha256" "$output_iso" "$output_sha256" <<'PY'
import json, sys
from pathlib import Path
manifest, commit, build, volume, version, architecture, source, source_hash, output, output_hash = sys.argv[1:]
data = {
 "schema_version":1,"platform_commit":commit,"build_number":build,"volume_id":volume,
 "debian_version":version,"architecture":architecture,"source_iso":Path(source).name,"source_sha256":source_hash,
 "output_iso":Path(output).name,"output_sha256":output_hash,"partitioning_mode":"debian_installer_interactive",
 "human_login_account":False,"service_account":"vincent","runtime_source":"public_git_exact_commit",
 "runtime_repository":"https://github.com/Gordonfive/vincent.git","persistent_console_status":True,
 "interactive_codex_console":"tty2_non_root","unattended_self_test":True,"embedded_secrets":False
}
Path(manifest).write_text(json.dumps(data, sort_keys=True, indent=2)+"\n")
PY

if grep -a -E 'BEGIN (OPENSSH|RSA|EC) PRIVATE KEY' "$output_iso" >/dev/null; then echo "private key material detected in installer image" >&2; exit 5; fi
printf '%s  %s\n' "$output_sha256" "$(basename -- "$output_iso")" >"${output_iso}.sha256"
printf 'build_number=%s\nvolume_id=%s\nimage=%s\nmanifest=%s\nsha256=%s\n' "$build_number" "$volume_id" "$output_iso" "$manifest" "$output_sha256"
