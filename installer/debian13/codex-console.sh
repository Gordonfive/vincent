#!/bin/sh
set -eu

service_home=/var/lib/mission-control
service_config=$service_home/.config
service_cache=$service_home/.cache
service_data=$service_home/.local/share

while :; do
    printf '\033c'
    echo 'VINCENT INTERACTIVE CODEX CONSOLE'
    echo '================================='
    echo
    echo 'This console runs Codex as the locked Vincent service account.'
    echo 'It does not provide a root shell or local login account.'
    echo 'Alt+F1 returns to the Vincent status dashboard.'
    echo

    if ! getent passwd mission-control >/dev/null 2>&1; then
        echo 'Vincent service account is not available yet.'
        echo 'Waiting for bootstrap...'
        sleep 5
        continue
    fi
    if [ ! -x /usr/local/bin/codex ]; then
        echo 'Codex is not installed yet.'
        echo 'Waiting for bootstrap...'
        sleep 5
        continue
    fi

    echo 'Press Enter to launch Codex, or Alt+F1 to return to status.'
    IFS= read -r _
    printf '\033c'
    set +e
    runuser -u mission-control -- env \
        HOME="$service_home" \
        USER=mission-control \
        LOGNAME=mission-control \
        XDG_CONFIG_HOME="$service_config" \
        XDG_CACHE_HOME="$service_cache" \
        XDG_DATA_HOME="$service_data" \
        PATH=/usr/local/bin:/usr/bin:/bin \
        /usr/local/bin/codex
    rc=$?
    set -e
    echo
    echo "Codex exited with status $rc."
    echo 'Press Enter to relaunch, or Alt+F1 to return to status.'
    IFS= read -r _
done
