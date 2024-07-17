from pyzbar import pyzbar
import cv2
import atexit
import pymysql
from dotenv import set_key, find_dotenv, load_dotenv
import os
from wifi_connection import set_wifi_network
import subprocess
from led_control import control_ACT, control_PWR
from time import sleep


class MySqlHandler:
    def __init__(self):
        # DB 연결
        self.dotenv_file = find_dotenv()
        self.db = None

        try_cnt = 3
        while try_cnt:
            try:
                control_PWR("on")
                control_ACT("on")
                load_dotenv()
                self.db = pymysql.connect(
                    host=os.environ.get("DB_HOST"),
                    port=int(os.environ.get("DB_PORT")),
                    user=os.environ.get("DB_USERNAME"),
                    passwd=os.environ.get("DB_PASSWORD"),
                    db=os.environ.get("DB_DATABASE"),
                    charset="utf8",
                )
                print("db 연결됨!")
                control_PWR("heartbeat")
                break
            except Exception as ex:
                print(ex, "\ndb가 연결되지 않음")

        if not try_cnt:
            exit(2)

    # --------------------------------------------------------------------------
    def CREATE(self, insert_sql: str, val: tuple):
        # insert_sql = "INSERT INTO 테이블 (컬럼1, 컬럼2) VALUES(값1, '값2', 값3)"
        cursor = self.db.cursor()
        cursor.execute(insert_sql, val)
        self.db.commit()
        print(cursor.lastrowid)

    # --------------------------------------------------------------------------
    def READ(self, select_sql: str, val: tuple):
        # select_sql = "SELECT * FROM 테이블 WHERE 조건"
        cursor = self.db.cursor()
        cursor.execute(select_sql, val)
        result = cursor.fetchall()
        return result

    # --------------------------------------------------------------------------
    def UPDATE(self, update_sql: str, val: tuple):
        # update_sql = "UPDATE 테이블 SET 컬럼='값' WHERE 조건"
        with self.db.cursor() as cursor:
            cursor.execute(update_sql, val)
            self.db.commit()
            print(cursor.rowcount)

    # --------------------------------------------------------------------------
    def DELETE(self, delete_sql: str, val: tuple):
        # delete_sql = "DELETE FROM 테이블 WHERE 조건"
        with self.db.cursor() as cursor:
            cursor.execute(delete_sql, val)
            self.db.commit()
            print(cursor.rowcount)

    # --------------------------------------------------------------------------
    def close_connection(self):
        if self.db:
            self.db.close()
            print("DB 연결 종료!\n")


class QRcodeScanner:
    def __init__(self):
        # 카메라 설정
        # PWR off, ACT off: 카메라 인터페이스 열기
        try_cnt = 3
        while try_cnt:
            try:
                self.allow_led_control()
                control_PWR("off")
                control_ACT("off")
                self.cam = cv2.VideoCapture(0)
                self.TIMES = 1
                print("카메라 연결됨!")
                break
            except Exception as ex:
                print(ex, "\n카메라 연결 실패(오류)")

        if not try_cnt:
            exit(1)

        # DB Handler 객체 생성
        self.myDB = MySqlHandler()

        # 프로그램 종료 시 호출
        atexit.register(self.close_camera)

    def allow_led_control(self):
        # PWR, ACK led 제어 파일에 대해 write 권한 전체 부여
        subprocess.run(
            [
                "/usr/bin/sudo",
                "chmod",
                "a+w",
                "/sys/class/leds/PWR/brightness",
            ]
        )
        subprocess.run(
            [
                "/usr/bin/sudo",
                "chmod",
                "a+w",
                "/sys/class/leds/PWR/trigger",
            ]
        )
        subprocess.run(
            [
                "/usr/bin/sudo",
                "chmod",
                "a+w",
                "/sys/class/leds/ACT/brightness",
            ]
        )
        subprocess.run(
            [
                "/usr/bin/sudo",
                "chmod",
                "a+w",
                "/sys/class/leds/ACT/trigger",
            ]
        )

    # --------------------------------------------------------------------------
    def idle(self, time):
        sleep(time)
        self.TIMES += time
        # print(f">> TIMES: {self.TIMES}", end="\r")

    # --------------------------------------------------------------------------
    def get_rasp_serial(self):
        command = [
            "/usr/bin/sudo",
            "cat",
            "/sys/firmware/devicetree/base/serial-number",
        ]
        rasp_serial = subprocess.check_output(command, encoding="utf-8")
        print("rasp_serial=", rasp_serial)
        return rasp_serial.strip()

    # --------------------------------------------------------------------------
    def save_owner(self, user_id, secret, device_alias):
        set_key(self.myDB.dotenv_file, "DEVICE_OWNER", user_id)
        set_key(self.myDB.dotenv_file, "SECRET", secret)
        set_key(self.myDB.dotenv_file, "DEVICE_ALIAS", device_alias)

    # --------------------------------------------------------------------------
    def qrcode_scan(self):
        barcodes = []
        while True:
            ret, image = self.cam.read()

            # 이미지에서 바코드 찾기
            try:
                barcodes = pyzbar.decode(image)
            except Exception as ex:
                barcodes = []
                # print(ex, f"바코드가 아님 {self.TIMES}", end="\r")

            for barcode in barcodes:
                # print("\n\n\nbarcode=", barcode)
                # QR코드 스캔 시도
                control_PWR("heartbeat")
                control_ACT("heartbeat")

                # 이미지에서 바코드의 경계 상자부분을 그리고, 바코드의 경계 상자부분(?)을 추출한다.
                (x, y, w, h) = barcode.rect
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # 바코드 데이터는 바이트 객체이므로, 어떤 출력 이미지에 그리려면 가장 먼저 문자열로 변환해야 한다.
                barcodeData = barcode.data.decode("utf-8")
                print("\n\n\nbarcode data=", barcodeData)
                # barcodeType = barcode.type

                # 이미지에서 바코드 데이터와 테입(유형)을 그린다
                # text = "{} ({})".format(barcodeData, barcodeType)
                # cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                try:
                    # print the barcode type and data to the terminal
                    # 터미널을 통해 바코드 유형과 데이터를 출력
                    barcodeData = barcodeData.split(";")
                    network_ssid = barcodeData[0]
                    network_security = barcodeData[1]
                    network_password = barcodeData[2]
                    user_id = barcodeData[3]
                    secret = barcodeData[4]  # user_pw
                    device_alias = barcodeData[5]

                    print("network_ssid:", network_ssid)
                    print("network_security:", network_security)
                    print("network_password:", network_password)

                    # 네트워크 연결
                    # 인터넷 연결 상태 확인

                    set_wifi_network(network_ssid, network_security, network_password)
                    print("네트워크 연결 작업 종료!")

                    print("user_id:", user_id)
                    print("device_alias:", device_alias)

                    # 기기 등록
                    device_serial = self.get_rasp_serial()
                    is_registered_device = len(
                        self.myDB.READ(
                            select_sql="SELECT * FROM devices WHERE device_serial=%s",
                            val=(device_serial),
                        )
                    )
                    if not is_registered_device:
                        self.myDB.CREATE(
                            insert_sql="INSERT INTO devices VALUES (%s, %s, %s, %s)",
                            val=(None, device_serial, device_alias, user_id),
                        )
                        self.save_owner(user_id, secret, device_alias)
                        print("기기 등록 성공!")

                    else:
                        print("이미 등록된 기기입니다.")

                    # 정상 종료
                    control_PWR("OFF")
                    control_ACT("OFF")
                    sleep(2)

                    control_PWR("default")
                    control_ACT("default")
                    print("정상종료됨")
                    exit(0)  # 기기 확인(등록) 절차 완료 시, 종료

                except Exception as ex:
                    print(ex)

            self.idle(1)
            control_PWR("on")

    # --------------------------------------------------------------------------
    def close_camera(self):
        if self.cam:
            self.cam.release()
            print("usb cam 종료!\n")

        if self.myDB:
            self.myDB.close_connection()  # DB 연결 종료
