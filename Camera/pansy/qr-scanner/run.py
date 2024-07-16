import os
from dotenv import load_dotenv
import subprocess
from led_control import control_ACT, control_PWR


def is_owner():
    subprocess.run(
        [
            "/usr/bin/sudo",
            "chmod",
            "666",
            "/home/<사용자명>/pansy/.env",
        ]
    )
    load_dotenv()
    print("현재 소유자는", os.environ.get("DEVICE_OWNER"))
    if os.environ.get("DEVICE_OWNER").strip() == "anonymous":
        return False
    return True


if __name__ == "__main__":
    # 기기의 인터넷 연결여부 및 기기 등록정보 확인
    from qr_scanner import QRcodeScanner

    qrs = QRcodeScanner()

    if not is_owner():
        print("소유자 없음.")
        qrs.qrcode_scan()
    else:
        # 기본 시스템 설정으로 바꿔주기
        control_PWR("default")
        control_ACT("default")
