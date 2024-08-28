import io
import csv
import json
import time
import glob
from PIL import Image

def send_string_image_csv():
    global thread_num
    global global_object_list

    info = object_queue.get()
    time.sleep(5)

    # 소켓 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 이미지 파일 경로
    image_dir = "/.."

    # CSV 파일 경로
    csv_dir = "/.."

    # 전송할 문자열

    userID = info.get_userID()

    try:
        # 서버에 연결
        client_socket.connect((server_address_r, server_port_r))

        # 스레드 번호 전송
        print(thread_num)
        client_socket.sendall(str(thread_num).encode())

        # 문자열을 바이트 배열로 인코딩
        print(userID)
        userID_byte_array = userID.encode('utf-8')

        # 문자열의 길이를 먼저 전송
        client_socket.sendall(len(userID_byte_array).to_bytes(4, byteorder='big'))
        client_socket.sendall(userID_byte_array)
        print("문자열을 성공적으로 전송했습니다.")

        # 이미지 파일의 개수를 확인
        image_files = [f for f in os.listdir(image_dir) if
                       os.path.isfile(os.path.join(image_dir, f)) and f.lower().endswith(
                           ('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        num_images = len(image_files)
        print(f"이미지 파일의 개수: {num_images}")

        # 이미지 파일의 개수를 먼저 전송
        client_socket.sendall(num_images.to_bytes(4, byteorder='big'))

        for filename in image_files:
            image_path = os.path.join(image_dir, filename)

            # 이미지 이름을 바이트 배열로 인코딩하여 전송
            filename_byte_array = filename.encode('utf-8')
            client_socket.sendall(len(filename_byte_array).to_bytes(4, byteorder='big'))
            client_socket.sendall(filename_byte_array)

            # 이미지 불러오기
            image = Image.open(image_path)

            # 이미지를 JPEG로 변환하여 바이트 배열로 인코딩
            img_byte_array = io.BytesIO()
            image.save(img_byte_array, format='JPEG')
            img_byte_array = img_byte_array.getvalue()

            # 이미지 데이터 길이를 먼저 전송
            client_socket.sendall(len(img_byte_array).to_bytes(4, byteorder='big'))
            client_socket.sendall(img_byte_array)
            print(f"{filename} 이미지를 성공적으로 전송했습니다.")

        # CSV 파일들 전송
        for csv_file in os.listdir(csv_dir):
            csv_path = os.path.join(csv_dir, csv_file)
            if os.path.isfile(csv_path):
                data = []
                with open(csv_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        data.append(row)

                # CSV 데이터를 JSON으로 변환하여 전송
                csv_data = json.dumps(data)
                csv_data_bytes = csv_data.encode('utf-8')

                # CSV 데이터 길이를 먼저 전송
                client_socket.sendall(len(csv_data_bytes).to_bytes(4, byteorder='big'))
                client_socket.sendall(csv_data_bytes)

                print(f"CSV 파일 {csv_file}를 성공적으로 전송했습니다.")

        # CSV 디렉토리 내 파일 삭제
        [os.remove(f) for f in glob.glob("/..")]

        # IMG 디렉토리 내 파일 삭제
        [os.remove(f) for f in glob.glob("/..")]

    except Exception as e:
        print("전송 중 오류 발생:", e)

    finally:
        # 소켓 닫기
        client_socket.close()
