#!/bin/sh
set -eu

# ADR-0004: remove only the active installer medium from Debian's disk
# enumeration. Do not select, rank, or otherwise prefer any remaining disk.
media_source=$(awk '$2 == "/cdrom" { print $1; exit }' /proc/mounts)
case "$media_source" in
    /dev/*) ;;
    *) echo "unable to identify active installer media mounted at /cdrom" >&2; exit 1 ;;
esac

media_name=${media_source#/dev/}
sys_path=/sys/class/block/$media_name
[ -e "$sys_path" ] || { echo "installer media block device not found in sysfs: $media_source" >&2; exit 1; }
resolved=$(readlink -f "$sys_path")
if [ -f "$sys_path/partition" ]; then
    parent_name=$(basename "$(dirname "$resolved")")
else
    parent_name=$(basename "$resolved")
fi
installer_disk=/dev/$parent_name
printf '%s\n' "$installer_disk" >/run/vincent-installer-disk

# Debian partman-base 237 (Debian 13 / trixie) builds its partitioner device
# tree from parted_devices, not from list-devices. Filter parted_devices first so
# the active installer disk never enters /var/lib/partman/devices.
parted_devices=$(command -v parted_devices)
[ -n "$parted_devices" ] || { echo "parted_devices not found" >&2; exit 1; }
real_parted_devices=${parted_devices}.vincent-real

if [ ! -x "$real_parted_devices" ]; then
    mv "$parted_devices" "$real_parted_devices"
    cat >"$parted_devices" <<EOF
#!/bin/sh
real='$real_parted_devices'
exclude_file=/run/vincent-installer-disk
if [ ! -s "\$exclude_file" ]; then
    exec "\$real" "\$@"
fi
exclude=\$(cat "\$exclude_file")
"\$real" "\$@" | while IFS= read -r line; do
    set -- \$line
    device=\${1:-}
    [ "\$device" = "\$exclude" ] || printf '%s\\n' "\$line"
done
EOF
    chmod 0755 "$parted_devices"
fi

# Keep list-devices filtered as defense-in-depth for installer components that
# use it independently of partman.
list_devices=$(command -v list-devices)
[ -n "$list_devices" ] || { echo "list-devices not found" >&2; exit 1; }
real_list_devices=${list_devices}.vincent-real

if [ ! -x "$real_list_devices" ]; then
    mv "$list_devices" "$real_list_devices"
    cat >"$list_devices" <<EOF
#!/bin/sh
real='$real_list_devices'
exclude_file=/run/vincent-installer-disk
if [ "\${1:-}" != disk ] || [ ! -s "\$exclude_file" ]; then
    exec "\$real" "\$@"
fi
exclude=\$(cat "\$exclude_file")
"\$real" "\$@" | while IFS= read -r device; do
    [ "\$device" = "\$exclude" ] || printf '%s\\n' "\$device"
done
EOF
    chmod 0755 "$list_devices"
fi

# Also make accidental direct writes to the active installer disk fail closed.
blockdev --setro "$installer_disk" 2>/dev/null || true

echo "Vincent installer media excluded from target disk enumeration: $installer_disk" >&2
