#!/bin/sh
set -eu

image=${1:-}
target_by_id=${2:-}
confirmation=${3:-}

if [ -z "$image" ] || [ -z "$target_by_id" ]; then
    echo "usage: sudo flash-usb.sh IMAGE.iso /dev/disk/by-id/usb-DEVICE 'ERASE:usb-DEVICE'" >&2
    exit 2
fi
if [ ! -f "$image" ]; then
    echo "installer image does not exist" >&2
    exit 2
fi
case "$target_by_id" in
    /dev/disk/by-id/usb-*) ;;
    *) echo "target must use a /dev/disk/by-id/usb-* path" >&2; exit 3 ;;
esac
expected="ERASE:$(basename -- "$target_by_id")"
if [ "$confirmation" != "$expected" ]; then
    echo "destructive confirmation mismatch; expected: $expected" >&2
    exit 3
fi
if [ ! -b "$target_by_id" ]; then
    echo "target is not a block device" >&2
    exit 3
fi

target=$(readlink -f "$target_by_id")
type=$(lsblk -dn -o TYPE "$target")
transport=$(lsblk -dn -o TRAN "$target")
removable=$(lsblk -dn -o RM "$target")
if [ "$type" != "disk" ] || [ "$transport" != "usb" ] || [ "$removable" != "1" ]; then
    echo "target is not a removable whole USB disk" >&2
    exit 3
fi
if lsblk -nr -o MOUNTPOINTS "$target" | grep -q '[^[:space:]]'; then
    echo "target or one of its partitions is mounted" >&2
    exit 3
fi

image_size=$(stat -c %s "$image")
device_size=$(lsblk -bdn -o SIZE "$target")
if [ "$image_size" -gt "$device_size" ]; then
    echo "installer image is larger than target USB" >&2
    exit 3
fi

echo "ERASING $target_by_id ($target) with $image"
dd if="$image" of="$target" bs=16M status=progress conv=fsync
sync
cmp -n "$image_size" "$image" "$target"
echo "USB_FLASH_VERIFICATION=PASS"
