import socket
from PIL import Image
import io
import threading
import json
import os

def info_server(client_socket, client_address):
    image_folder = "../"

    try:
        print(f"클라이언트가 연결되었습니다: {client_address}")

        # 스레드 번호 수신
        thread_num_len_data = client_socket.recv(4)
        thread_num_len = int.from_bytes(thread_num_len_data, byteorder='big')
        thread_num = receive_data(client_socket, thread_num_len).decode('utf-8')
        print(f"스레드 번호: {thread_num}")

        # ID 수신
        userID_len_data = client_socket.recv(4)
        userID_len = int.from_bytes(userID_len_data, byteorder='big')
        userID_data = receive_data(client_socket, userID_len).decode('utf-8')
        print(f"수신한 ID: {userID_data}")

        # 문자열 수신
        fileName_len_data = client_socket.recv(4)
        fileName_len = int.from_bytes(fileName_len_data, byteorder='big')
        fileName_data = receive_data(client_socket, fileName_len).decode('utf-8')
        print(f"수신한 fileName: {fileName_data}")

        # 이미지 파일의 개수 수신
        num_images_bytes = client_socket.recv(4)
        num_images = int.from_bytes(num_images_bytes, byteorder='big')
        print(f"수신할 이미지 파일의 개수: {num_images}")

        image_paths = []

        # 이미지 파일 개수만큼 이미지 수신
        for i in range(num_images):
            # 이미지 파일 이름 수신
            filename_len_data = client_socket.recv(4)
            filename_len = int.from_bytes(filename_len_data, byteorder='big')
            filename = receive_data(client_socket, filename_len).decode('utf-8')
            print(f"수신한 이미지 파일 이름: {filename}")

            # 이미지 수신
            image_size_bytes = client_socket.recv(4)
            image_size = int.from_bytes(image_size_bytes, byteorder='big')
            received_image_data = receive_data(client_socket, image_size)
            image = Image.open(io.BytesIO(received_image_data))
            image_path = os.path.join(image_folder, filename)
            image.save(image_path, "JPEG")
            image_paths.append(image_path)
            print(f"이미지를 성공적으로 수신하고 {image_path}에 저장했습니다.")

        # JSON 데이터 수신
        json_size_bytes = client_socket.recv(4)
        json_size = int.from_bytes(json_size_bytes, byteorder='big')
        json_data = receive_data(client_socket, json_size).decode('utf-8')
        received_data = json.loads(json_data)
        print(f"수신한 JSON 데이터: {received_data}")

        # 데이터베이스에 저장 (이 함수는 따로 정의해야 합니다)
        save_data_to_database(userID_data, fileName_data, image_paths, received_data, thread_num)

    except Exception as e:
        print("수신 중 오류 발생:", e)

    finally:
        client_socket.close()



def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("서버가 시작되었습니다. 연결을 기다리는 중입니다.")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=info_server, args=(client_socket, client_address))
            client_thread.start()

    except Exception as e:
        print("서버 실행 중 오류 발생:", e)

    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server(host, port)
