def client_handler(client_socket, client_address):
    global thread_num
    global global_object_list

    try:
        # 파일 이름 수신
        filename_data = client_socket.recv(1024)
        print("ddd")
        filename = filename_data.decode('utf-8')
        print(f"수신한 파일 이름: {filename}")

        # 파일 이름에서 필요한 부분 추출
        user_id = filename.split('_')[0]
        fileName = filename.split('_')[1]

        info = userInfo(user_id, fileName)
        object_queue.put(info)

        print("객체 리스트 저장 성공!")

        file_path = f'"/.."'

        # 파일 저장
        with open(file_path, 'wb') as f:
            while True:
                data = client_socket.recv(1500)
                if not data:
                    break
                f.write(data)
        print(f"{client_address}에서 받은 영상 저장이 완료되었습니다.")

        # 큐에 분석 작업 추가
        analysis_queue.put((file_path, client_address,))
    except Exception as e:
        print(f"클라이언트 처리 중 오류 발생: {e}")
    finally:
        # 클라이언트 소켓 닫기
        client_socket.close()