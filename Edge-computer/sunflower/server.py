import socket
import threading


def server_info(client_socket, client_address):
    print(f'연결 성공: {client_address}')
    try:
        video_num = client_socket.recv(1024).decode('utf-8')  # 비디오 번호 디코딩
        print(f'비디오 번호: {video_num}')

        video_path = f'"../"'

        # 파일 저장
        with open(video_path, 'wb') as f:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                f.write(data)

        print(f"{client_address}에서 받은 영상 저장이 완료되었습니다.")

        save_data_to_db(video_num, video_path)
        print('데이터베이스 저장 성공.')

    except Exception as e:
        print(f'클라이언트 요청 오류: {e}')
    finally:
        client_socket.close()


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
    server_socket.listen(5)
    print('연결 대기 중...')

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=server_info, args=(client_socket, client_address))
        client_handler.start()
