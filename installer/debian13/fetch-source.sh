#!/bin/sh
set -eu

script_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$script_root/source.env"

destination=${1:-$script_root/cache}
install -d -m 0755 "$destination"

keyring=/usr/share/keyrings/debian-role-keys.gpg
if [ ! -f "$keyring" ]; then
    echo "Debian role keyring is required; install the debian-keyring package" >&2
    exit 2
fi

for file in "$DEBIAN_ISO" SHA512SUMS SHA512SUMS.sign; do
    curl --fail --location --proto '=https' --tlsv1.2 \
        --output "$destination/$file" "$DEBIAN_BASE_URL/$file"
done

gpgv --keyring "$keyring" "$destination/SHA512SUMS.sign" "$destination/SHA512SUMS"
(
    cd "$destination"
    expected=$(awk -v image="$DEBIAN_ISO" '$2 == image || $2 == "*" image {print $1}' SHA512SUMS)
    if [ -z "$expected" ]; then
        echo "ISO is absent from signed SHA512SUMS" >&2
        exit 3
    fi
    actual=$(sha512sum "$DEBIAN_ISO" | awk '{print $1}')
    [ "$actual" = "$expected" ] || {
        echo "Debian ISO checksum mismatch" >&2
        exit 4
    }
)

echo "$destination/$DEBIAN_ISO"
