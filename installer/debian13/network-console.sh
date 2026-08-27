#!/bin/sh
set -u

run_diagnostics() {
    systemctl start vincent-diagnostics.service >/dev/null 2>&1 || true
}

show_unique_wifi() {
    nmcli -t -f SSID,SIGNAL,SECURITY device wifi list ifname "$wifi_device" 2>/dev/null |
        awk -F: '
            $1 != "" {
                ssid=$1; signal=$2; security=$3
                if (!(ssid in best) || signal+0 > best[ssid]+0) {
                    best[ssid]=signal
                    sec[ssid]=security
                }
            }
            END {
                printf "%-32s %6s  %s\n", "SSID", "SIGNAL", "SECURITY"
                for (ssid in best)
                    printf "%-32s %6s  %s\n", ssid, best[ssid], sec[ssid]
            }
        ' | sort -k2,2nr
}

while :; do
    clear
    echo "VINCENT NETWORK CONFIGURATION"
    echo "============================="
    echo
    nmcli -f DEVICE,TYPE,STATE,CONNECTION device status 2>/dev/null || true
    echo

    if nmcli -t -f TYPE,STATE device status 2>/dev/null | grep -q '^ethernet:connected$'; then
        echo "Ethernet is connected. Vincent will prefer it."
        echo
        echo "Alt+F1: status   Alt+F2: Codex   Alt+F3: network   Alt+F4: diagnostics"
        sleep 10
        continue
    fi

    if nmcli -t -f TYPE,STATE device status 2>/dev/null | grep -q '^wifi:connected$'; then
        echo "Wi-Fi is connected."
        echo
        echo "Alt+F1: status   Alt+F2: Codex   Alt+F3: network   Alt+F4: diagnostics"
        sleep 10
        continue
    fi

    wifi_device=$(nmcli -t -f DEVICE,TYPE device status 2>/dev/null | awk -F: '$2=="wifi" {print $1; exit}')
    if [ -z "$wifi_device" ]; then
        echo "No Wi-Fi NIC detected. Retrying..."
        sleep 10
        continue
    fi

    echo "Ethernet is unavailable and Wi-Fi is disconnected."
    echo "Trying saved Wi-Fi profiles first..."
    nmcli radio wifi on >/dev/null 2>&1 || true

    nmcli -t -f NAME,TYPE connection show 2>/dev/null |
        awk -F: '$2=="802-11-wireless" {print $1}' |
        while IFS= read -r profile; do
            [ -n "$profile" ] || continue
            nmcli connection up "$profile" >/dev/null 2>&1 && break
        done

    if nmcli -t -f TYPE,STATE device status 2>/dev/null | grep -q '^wifi:connected$'; then
        run_diagnostics
        continue
    fi

    echo
    echo "Available wireless networks:"
    nmcli device wifi rescan ifname "$wifi_device" >/dev/null 2>&1 || true
    show_unique_wifi
    echo
    printf 'SSID (blank to rescan): '
    IFS= read -r ssid
    if [ -n "$ssid" ]; then
        echo "NetworkManager will request the passphrase securely if required."
        if nmcli --ask device wifi connect "$ssid" ifname "$wifi_device"; then
            run_diagnostics
            echo "Connected. Diagnostics were queued; see Alt+F4."
        fi
        echo
        echo "Press Enter to continue."
        IFS= read -r _
    fi
done
