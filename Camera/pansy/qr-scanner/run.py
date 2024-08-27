import os
from time import sleep
from dotenv import load_dotenv
from led_control import control_ACT, control_PWR


if __name__ == "__main__":
    sleep(1)
    # 기기의 인터넷 연결여부 및 기기 등록정보 확인
    from qr_scanner import QRcodeScanner

    qrs = QRcodeScanner()
    # exit_code =>
    # 0:"문제 없음" => 소유자 기기 확인
    #               => non-pass 시, QR코드 스캔(기기 등록)
    # 1:"카메라 문제" => 종료(PWR:off, ACT:off)
    # 2:"인터넷 문제" => QR코드 스캔(PWR:on, ACT:heartbeat)
    # 3:"DB 문제" => 종료(PWR:on, ACT:on)

    if QRcodeScanner.exit_code == 0:
        if qrs.is_registered_device():
            load_dotenv()
            print("현재 소유자는 '" + os.environ.get("DEVICE_OWNER") + "'")
            # 기본 시스템 설정으로 바꿔주기
            control_PWR("default")
            control_ACT("default")
        else:
            print("\n소유자가 없거나 잘못 등록된 기기입니다.")
            qrs.qrcode_scan()
    elif QRcodeScanner.exit_code == 2:
        qrs.qrcode_scan()

    print("\n\n종료!!!!!")
