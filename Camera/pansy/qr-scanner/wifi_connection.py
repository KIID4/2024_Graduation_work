import re
import subprocess
from led_control import control_ACT, control_PWR


def is_registered_network(ssid):
    output = subprocess.check_output(
        ["/usr/bin/sudo", "nmcli", "connection", "show"],
        encoding="utf-8",
    )
    pattern = r"\s+"
    lines = re.split(pattern, output)
    return ssid in set(lines)


def is_connected_internet():
    try:
        # PWR on, ACT heartbeat: 네트워크 연결 시도
        control_PWR("on")
        control_ACT("heartbeat")
        subprocess.check_output(["/usr/bin/sudo", "ping", "-c", "1", "8.8.8.8"])
        print("인터넷 연결됨 (O)")
        return True

    except subprocess.CalledProcessError:
        print("인터넷 연결되지 않음 (X)")
        return False


def add_wifi_network(network_ssid, network_security, network_pw):
    config_lines = [
        "\n",
        "network={",
        f'\tssid="{network_ssid}"',
        f"\tkey_mgmt={network_security}",
        f'\tpsk="{network_pw}"',
        "}",
    ]
    config = "\n".join(config_lines)

    # wpa_supplicant.conf 파일에 대해 write 및 read 권한 전체 부여
    # os.popen("chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")
    subprocess.run(
        [
            "/usr/bin/sudo",
            "chmod",
            "a+w",
            "/etc/wpa_supplicant/wpa_supplicant.conf",
        ]
    )
    subprocess.run(
        [
            "/usr/bin/sudo",
            "chmod",
            "a+r",
            "/etc/wpa_supplicant/wpa_supplicant.conf",
        ]
    )

    # wpa_supplicant.conf 파일에 이미 등록되어 있는지 확인
    print("\n네트워크 정보 확인..")
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "r") as wifi_info:
        if network_ssid in wifi_info.read().split('"'):
            print("\n\t네트워크 정보에 이미 등록되어 있음!")
            return

    # 네트워크 정보를 담는 파일에 네트워크 추가
    print("\n새로운 네트워크 정보 등록")
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a") as wifi_info:
        wifi_info.write(config)
        print("\n\t새로운 Wifi 네트워크 등록 완료!")


def set_wifi_network(network_ssid, network_security, network_pw):
    # 저장되어 있는 네트워크가 아니라면,
    # 인터넷 연결여부 상관없이 우선 네트워크 등록
    if not is_registered_network(network_ssid):
        add_wifi_network(network_ssid, network_security, network_pw)

        if not is_connected_internet():
            # 네트워크 재설정 수행
            subprocess.check_output(
                ["/usr/bin/sudo", "wpa_cli", "-i", "wlan0", "reconfigure"]
            )
            print("\n네트워크 재설정 수행.")
            # os.popen("wpa_cli -i wlan0 reconfigure")
            # 재부팅 수행
            # subprocess.check_output(["/usr/bin/sudo", "reboot"])
