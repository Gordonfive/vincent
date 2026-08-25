#!/bin/sh
set -eu

fail() {
    message=$1
    {
        printf '\033c'
        echo 'VINCENT PRESEED FAILED'
        echo '======================='
        echo
        echo "$message"
        echo
        echo 'The installer will not continue with interactive fallbacks.'
        echo 'Photograph this screen and rebuild the Vincent installer.'
    } >/dev/tty1 2>/dev/null || true
    chvt 1 2>/dev/null || true
    while :; do sleep 3600; done
}

check() {
    key=$1
    expected=$2
    actual=$(debconf-get "$key" 2>/dev/null || true)
    [ "$actual" = "$expected" ] || fail "$key expected '$expected' but installer has '$actual'"
}

check passwd/root-login false
check passwd/make-user false
check netcfg/get_hostname vincent-worker
check partman-auto/method lvm
check partman-auto/choose_recipe atomic

exit 0
