from pyzbar import pyzbar
import cv2
import atexit
import pymysql
from dotenv import set_key, find_dotenv, load_dotenv
import os
from wifi_connection import set_wifi_network, is_connected_internet
import subprocess
from led_control import control_ACT, control_PWR
from time import sleep


class MySqlHandler:
    def __init__(self):
        self.dotenv_file = find_dotenv()
        self.db = None
        load_dotenv()

        if QRcodeScanner.exit_code != 3:
            # 인터넷 연결 확인
            control_PWR("on")
            control_ACT("heartbeat")
            if not is_connected_internet():
                print("\n\n인터넷 연결 실패")
                QRcodeScanner.exit_code = 2
                exit(2)

        # DB 연결 확인 (PWR:on, ACT:on)
        control_PWR("on")
        control_ACT("on")
        flag = False
        for try_cnt in range(1, 4):
            try:
                self.db = pymysql.connect(
                    host=os.environ.get("user_DB_HOST"),
                    port=int(os.environ.get("user_DB_PORT")),
                    user=os.environ.get("user_DB_USERNAME"),
                    passwd=os.environ.get("user_DB_PASSWORD"),
                    db=os.environ.get("user_DB_DATABASE"),
                    charset="utf8",
                )
                print("\n\ndb 연결됨!")
                flag = True
                control_PWR("heartbeat")
                break
            except Exception as ex:
                print(ex, f"\n\ndb가 연결되지 않음({try_cnt})")

        if not flag:
            QRcodeScanner.exit_code = 3
            exit(3)

    # --------------------------------------------------------------------------
    def CREATE(self, insert_sql: str, val: tuple):
        # insert_sql = "INSERT INTO 테이블 (컬럼1, 컬럼2) VALUES(값1, '값2', 값3)"
        cursor = self.db.cursor()
        cursor.execute(insert_sql, val)
        print(cursor.lastrowid)

    # --------------------------------------------------------------------------
    def READ(self, select_sql: str, val: tuple):
        # select_sql = "SELECT * FROM 테이블 WHERE 조건"
        cursor = self.db.cursor()
        cursor.execute(select_sql, val)
        result = cursor.fetchone()
        return result

    # --------------------------------------------------------------------------
    def UPDATE(self, update_sql: str, val: tuple):
        # update_sql = "UPDATE 테이블 SET 컬럼='값' WHERE 조건"
        with self.db.cursor() as cursor:
            cursor.execute(update_sql, val)
            print(cursor.rowcount)

    # --------------------------------------------------------------------------
    def DELETE(self, delete_sql: str, val: tuple):
        # delete_sql = "DELETE FROM 테이블 WHERE 조건"
        with self.db.cursor() as cursor:
            cursor.execute(delete_sql, val)
            print(cursor.rowcount)

    # --------------------------------------------------------------------------
    def COMMIT(self):
        self.db.commit()

    # --------------------------------------------------------------------------
    def ROLLBACK(self):
        self.db.rollback()

    # --------------------------------------------------------------------------
    def close_connection(self):
        if self.db:
            self.db.close()


class QRcodeScanner:
    def __init__(self):
        QRcodeScanner.exit_code = 0
        self.cam = self.myDB = None

        # 카메라 설정
        self.allow_led_control()

        # 카메라 상태 확인 (PWR:off, ACT:off)
        control_PWR("off")
        control_ACT("off")
        flag = False
        for try_cnt in range(1, 4):
            try:
                self.cam = cv2.VideoCapture(0)
                print("\n\n카메라 연결됨!")
                flag = True
                break
            except Exception as ex:
                print(ex, f"\n\n카메라 연결 실패({try_cnt})")

        if not flag:
            QRcodeScanner.exit_code = 1
            exit(1)

        # DB Handler 객체 생성 (+인터넷 연결 및 DB 연결 확인)
        self.myDB = MySqlHandler()

        # 프로그램 종료 시 호출
        atexit.register(self.close)

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
    def is_registered_device(self):
        return self.myDB.READ(
            select_sql="SELECT 1 FROM devices WHERE device_id=%s AND user_id=%s AND device_alias=%s AND device_serial=%s",
            val=(
                os.environ.get("DEVICE_ID"),
                os.environ.get("DEVICE_OWNER"),
                os.environ.get("DEVICE_ALIAS"),
                self.get_rasp_serial(),
            ),
        )

    # --------------------------------------------------------------------------
    def register_device(self, user_id, device_alias):
        print("\n\n기기 등록 진행 중..")
        self.myDB.CREATE(
            insert_sql="INSERT INTO devices VALUES (%s, %s, %s, %s)",
            val=(None, self.get_rasp_serial(), device_alias, user_id),
        )
        new_device_id = self.myDB.READ(
            select_sql="SELECT d.device_id FROM devices d ORDER BY d.device_id DESC LIMIT 1",
            val=(),
        )[0]
        self.save_owner(
            device_id=str(new_device_id),
            user_id=user_id,
            device_alias=device_alias,
        )
        self.myDB.COMMIT()
        print("\n\n기기 등록 성공!")

    # --------------------------------------------------------------------------
    def save_owner(self, device_id, user_id, device_alias):
        set_key(self.myDB.dotenv_file, "DEVICE_ID", device_id)
        set_key(self.myDB.dotenv_file, "DEVICE_OWNER", user_id)
        set_key(self.myDB.dotenv_file, "DEVICE_ALIAS", device_alias)

    # --------------------------------------------------------------------------
    def qrcode_scan(self):
        # QR코드 스캔 시도
        print("\n\n[QR코드 스캔 수행]")
        control_PWR("heartbeat")
        control_ACT("heartbeat")

        # TIMES = 0
        barcodes = []
        while True:
            ret, image = self.cam.read()
            # cv2.imwrite(filename="./photo.jpg", img=image)

            # 이미지에서 바코드 찾기
            try:
                barcodes = pyzbar.decode(image)
                # print("\nbarcodes=", barcodes)
                control_ACT("ON")
            except Exception as ex:
                barcodes = []
                # TIMES += 1
                # print(f"{ex} 바코드가 아님 {TIMES}", end="\r")

            for barcode in barcodes:
                # print("\nbarcode=", barcode)
                # 이미지에서 바코드의 경계 상자부분을 그리고, 바코드의 경계 상자부분(?)을 추출한다.
                (x, y, w, h) = barcode.rect
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # 바코드 데이터는 바이트 객체이므로, 어떤 출력 이미지에 그리려면 가장 먼저 문자열로 변환해야 한다.
                barcodeData = barcode.data.decode("utf-8")
                # barcodeType = barcode.type
                # 이미지에서 바코드 데이터와 테입(유형)을 그린다
                # text = "{} ({})".format(barcodeData, barcodeType)
                # cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                try:
                    # 터미널을 통해 바코드 유형과 데이터를 출력
                    barcodeData = barcodeData.split(";")
                    # print("\n\nbarcode data=", barcodeData)

                    network_ssid = barcodeData[0]
                    network_security = barcodeData[1]
                    network_password = barcodeData[2]
                    print("\n\nnetwork_ssid:", network_ssid)
                    print("\n\nnetwork_security:", network_security)
                    print("\n\nnetwork_password:", network_password)

                    # 네트워크 연결
                    print("\n\n네트워크 연결?")
                    if network_ssid and network_security and network_password:
                        set_wifi_network(
                            network_ssid, network_security, network_password
                        )
                        # 네트워크 연결 문제 해결됨 (exit_code 2 => 3)
                        QRcodeScanner.exit_code = 3
                        self.myDB = MySqlHandler()

                    user_id = barcodeData[3]
                    device_alias = barcodeData[4]
                    print("\n\nuser_id:", user_id)
                    print("\n\ndevice_alias:", device_alias)

                    # 기기 등록
                    print("\n\n기기 등록?")
                    if user_id and device_alias:
                        self.register_device(user_id=user_id, device_alias=device_alias)
                    else:
                        control_PWR("HEARTBEAT")
                        control_ACT("HEARTBEAT")
                        break

                    # 정상 종료
                    control_PWR("OFF")
                    control_ACT("OFF")
                    sleep(2)

                    control_PWR("default")
                    control_ACT("default")
                    print("정상종료됨")

                    exit(0)  # 기기 확인(등록) 절차 완료 시, 종료

                except Exception as ex:
                    print("\n\n에러 코드: ", ex)
                    control_PWR("HEARTBEAT")
                    control_ACT("HEARTBEAT")

    # --------------------------------------------------------------------------
    def close(self):
        print("\n종료 수행!!!")
        if self.cam:
            self.cam.release()
            print("\n\nusb cam 종료!\n")

        if self.myDB:
            self.myDB.close_connection()
            print("\n\nDB 연결 종료!\n")
