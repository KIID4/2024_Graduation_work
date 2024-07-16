import io
import os
import queue
import threading
import numpy as np
import cv2
from PIL import Image
from dotenv import load_dotenv


# 싱글톤 패턴
class SingletonInstane:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance


class Camera(SingletonInstane):
    def __init__(self):
        import atexit

        self.cam = cv2.VideoCapture(0)
        self.basic_settings()

        # 프로그램 종료 시 호출
        atexit.register(self.close_camera)

        # 비디오 프레임 Queue 생성
        self.queue = queue.Queue()

        # 녹화기능 사용을 위한 세팅 초기화 (* -> 녹화 시작 -> 녹화 중 -> 녹화 중지 -> 영상 전송 -> *)
        self.revert_settings()

    # --------------------------------------------------------------------------
    def basic_settings(self):
        load_dotenv()
        self.user_name = os.environ.get("DEVICE_OWNER")  # 사용자명 초기화
        self.video_dir = os.environ.get("VIDEO_DIR")  # 비디오 파일의 디렉터리 경로 초기화
        self.file_name_extension = ".mp4"  # 비디오 파일의 확장자 초기화

        # 해상도 설정
        self.resolutions = (1280, 800)

        # frame속도 설정
        self.frame_rate = 30.0

        # 카메라 환경 세팅
        self.fourcc = cv2.VideoWriter_fourcc(*"avc1")  # h264
        # self.fourcc = cv2.VideoWriter_fourcc(*"hev1")
        self.cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        self.cam.set(cv2.CAP_PROP_FPS, self.frame_rate)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolutions[0])
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolutions[1])

        # 서버 주소 및 포트 설정
        self.SERVER_ADDRESS = os.environ.get("EDGE_SERVER_HOST")
        self.SERVER_PORT = os.environ.get("EDGE_SERVER_PORT")

    # --------------------------------------------------------------------------
    def revert_settings(self):
        self.is_recording = None  # 녹화 제어 변수 초기화
        self.DONE_FRAME = 0  # 녹화 중 write한 프레임 수 초기화
        self.start_rec_time = None  # 녹화 시작 시간 초기화
        self.stop_rec_time = None  # 녹화 중지 시간 초기화
        self.duration = 0  # 지속 시간 초기화
        self.file_name = (
            self.user_name + "_none_none" + self.file_name_extension
        )  # 비디오 파일명 초기화
        self.writing_status = None  # 녹화 프레임 쓰기 상태 변수 초기화
        self.record_thread = threading.Thread(target=self.write_to_video_writer)

    # --------------------------------------------------------------------------
    def gen_frame(self):
        print("\n\ngen_frame 수행!\n\n")

        while True:  # 중요한 부분 (프레임으로 스트리밍 및 영상 녹화 제어)
            ref, frame = self.cam.read()  # 현재 영상을 받아옴
            if not ref:  # 촬영된 영상의 상태가 false 이면, 종료
                # return Image.open("../static/assets/no-pictures.png")
                break

            if self.is_recording:
                self.queue.put(frame)

            # 프레임을 업데이트하며 스트리밍
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield b"--FRAME\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"

    # --------------------------------------------------------------------------
    def start_video_writer(self):
        # 임시 비디오 파일명
        temp_file_name = (
            self.user_name
            + "_"
            + self.start_rec_time.strftime("%Y%m%d_%H%M%S")
            + "_none"
            + self.file_name_extension
        )

        self.video_writer = cv2.VideoWriter(
            filename=self.video_dir + temp_file_name,
            fourcc=self.fourcc,
            fps=self.frame_rate,
            frameSize=self.resolutions,
        )

        # 임시 비디오 파일명 적용
        self.file_name = temp_file_name

    # --------------------------------------------------------------------------
    def write_to_video_writer(self):
        while True:
            try:
                # Queue에서 프레임 가져오기
                frame = self.queue.get()

                # video_writer에 프레임 쓰기
                self.video_writer.write(frame)
                self.DONE_FRAME += 1
                print(
                    f"쓰는 중: (write: {self.DONE_FRAME}) <- (queue: {self.queue.qsize()})",
                    end="\r",
                )

            except queue.Empty as e:
                print("\n\n\n큐가 비었음!\n\n\n", e)

            finally:
                self.queue.task_done()

    # --------------------------------------------------------------------------
    def get_writing_status(self):
        if self.is_recording == False:
            if not self.queue.empty():
                all_frame_size = self.DONE_FRAME + self.queue.qsize()
                self.writing_status = f"쓰는 중: {(self.DONE_FRAME / all_frame_size ) * 100:.1f} % (남은 frame: {self.queue.qsize()})"
            return self.writing_status
        return None

    # --------------------------------------------------------------------------
    def stop_video_writer(self):
        sec = (self.stop_rec_time - self.start_rec_time).seconds
        min = sec // 60
        sec %= 60
        hour = min // 60
        min %= 60
        self.duration = "%02d%02d%02d" % (hour, min, sec)

        # Queue에 있는 프레임을 모두 쓸 때까지 기다리기
        self.queue.join()
        # self.record_thread.join()
        print("\n\nframe write 작업 all done!\n\n")
        self.writing_status = self.file_name_extension + " 쓰는 중.."

        # 비디오 작성기 종료
        self.video_writer.release()
        print(f"\n\n{self.file_name_extension} 쓰기 끝!\n\n")
        self.writing_status = self.file_name_extension + " 쓰기 끝!"

        # 파일명 바꾸기
        new_file_name = (
            self.user_name
            + "_"
            + self.start_rec_time.strftime("%Y%m%d_%H%M%S")
            + "_"
            + self.duration
            + self.file_name_extension
        )
        os.rename(self.video_dir + self.file_name, self.video_dir + new_file_name)
        self.file_name = new_file_name
        print(f"\n\n영상 파일명 변환 완료!\n\n")

        # 영상 전송하기
        # self.send_video()

        # 녹화기능 사용을 위한 세팅 초기화
        self.revert_settings()

    # --------------------------------------------------------------------------
    def send_video(self):

        # socket 통신 방식
        import socket

        # 전송할 파일 경로
        FILE_PATH = self.video_dir + self.file_name

        # TCP 소켓 생성
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 서버에 연결
        client_socket.connect((self.SERVER_ADDRESS, self.SERVER_PORT))
        print("서버 연결됨!")

        # 사용자 ID명 전송
        client_socket.sendall(self.user_name.encode("utf-8"))

        # 영상 파일명 전송
        client_socket.sendall(self.file_name.encode("utf-8"))

        # 파일 크기 전송
        file_size = os.path.getsize(FILE_PATH)
        client_socket.sendall(str(file_size).encode())

        # 파일 내용 전송
        with open(FILE_PATH, "rb") as f:
            try:
                while True:
                    data = f.read(1500)  # 1500 bytes 간격
                    if not data:
                        break
                    client_socket.sendall(data)
                print("파일 전송 완료!")
            except Exception as e:
                print(e)

        # 연결 종료
        client_socket.close()

        print("\n\n서버로 영상 업로드 완료!\n\n")

    # --------------------------------------------------------------------------
    def close_camera(self):
        self.cam.release()
        print("usb cam 종료!\n")
