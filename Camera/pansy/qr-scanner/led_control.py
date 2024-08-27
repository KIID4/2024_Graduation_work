# PWR 및 ACT led 제어
# PWR(camera):           OFF           |        ON           |     HEARTBEAT      |       System Default(ON)       |     OFF(2s)
# ACT(network):          OFF           |     HEARTBEAT       |    HEARTBEAT(ON)   |    System Default(semi OFF)    |     OFF(2s)
#               카메라 인터페이스 열기  |  네트워크 연결 시도  |  QR코드 스캔(읽기)  |  네트워크 연결됨 & 기기 확인됨  |  기기 등록 완료
# 카메라 문제: 둘 다 OFF
# 인터넷 문제: (PWR:on, ACT:heartbeat)
# DB 문제: 둘 다 ON

import os

# import subprocess


def control_PWR(command: str):
    # command = "on" | "off" | "heartbeat" | "default"
    command = command.lower()
    if command == "on":
        os.popen("echo 1 > /sys/class/leds/PWR/brightness")

    elif command == "off":
        os.popen("echo 0 > /sys/class/leds/PWR/brightness")

    elif command == "heartbeat":
        os.popen("echo heartbeat > /sys/class/leds/PWR/trigger")

    elif command == "default":
        os.popen("echo input > /sys/class/leds/PWR/trigger")


def control_ACT(command: str):
    # command = "on" | "off" | "heartbeat" | "default"
    command = command.lower()
    if command == "on":
        os.popen("echo 1 > /sys/class/leds/ACT/brightness")

    elif command == "off":
        os.popen("echo 0 > /sys/class/leds/ACT/brightness")

    elif command == "heartbeat":
        os.popen("echo heartbeat > /sys/class/leds/ACT/trigger")

    elif command == "default":
        os.popen("echo mmc0 > /sys/class/leds/ACT/trigger")
