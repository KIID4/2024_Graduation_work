import socket
import threading
from multiprocessing import Process, Queue


# 분석 큐
analysis_queue = Queue(maxsize=2)
results_queue = Queue()

# 사용자 이름, 파일 제목 관련 저장 객체 리스트
object_queue = Queue()

thread_num = 0


def main():
    # 스레드 넘버
    global thread_num

    # TCP 소켓 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 바인딩 및 수신 대기
    server_socket.bind((SERVER_ADDRESS_R, SERVER_PORT_R))
    server_socket.listen(5)
    print('서버 연결중')

    def process_analysis_queue():
        while True:
            file_path, client_address = analysis_queue.get()
            analyze_video(file_path, results_queue, client_address)

    # 분석 작업을 처리할 프로세스 생성
    for _ in range(2):  # 동시에 2개의 분석 작업을 처리할 프로세스
        process = Process(target=process_analysis_queue)
        process.start()

    def send_results():
        while True:
            client_address, result = results_queue.get()
            print(f"{client_address}: {result}")
            # 실제로는 클라이언트에게 결과를 전송하는 코드로 대체
            # 여기서는 예시로 클라이언트 소켓을 재연결하여 결과 전송
            try:
                result_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result_socket.connect(client_address)
                result_socket.send(result.encode())
                result_socket.close()
            except Exception as e:
                print(f"결과 전송 중 오류 발생: {e}")

    # 결과를 처리할 스레드 생성
    result_thread = threading.Thread(target=send_results)
    result_thread.start()

    while True:
        # 연결 수락
        client_socket, client_address = server_socket.accept()
        print(f"{client_address} 연결이 되었습니다.")
        thread_num += 1

        # 각 클라이언트를 처리하기 위한 스레드 생성
        client_thread = threading.Thread(target=client_handler, args=(client_socket, client_address))
        client_thread.start()

    # 서버 소켓 닫기 (절대로 도달하지 않음)
    server_socket.close()