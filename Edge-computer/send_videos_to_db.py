

# 분석된 후 영상 저장 메소드
def send_videos_to_db():
    global thread_num

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address_r1, server_port_r1))

    videos_path = "/.."  # 비디오 저장 경로
    print('서버에 연결됨!')

    print(thread_num)
    client_socket.sendall(str(thread_num).encode())

    # 디렉토리 내 모든 파일 리스트
    videos = os.listdir(videos_path)

    for video in videos:
        video_full_path = os.path.join(videos_path, video)

        # 파일이 비디오 파일인지 확인
        if os.path.isfile(video_full_path) and video_full_path.endswith('.mp4'):
            file_size = os.path.getsize(video_full_path)
            print(f'{video} 파일 전송 시작 (크기: {file_size} bytes).')

            # 파일 전송
            with open(video_full_path, 'rb') as f:
                while True:
                    data = f.read(1500)
                    if not data:
                        break
                    client_socket.sendall(data)
            print(f'{video} 파일 전송 완료!')

    # 파일 삭제
    os.remove(video_full_path)
    print(f'{video} 파일 삭제 완료!')
    client_socket.close()
    print('모든 파일 전송 완료, 소켓 연결 종료.')