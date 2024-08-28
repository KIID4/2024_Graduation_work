import os
import subprocess
import shutil

# 모델 분석
def analyze_video(file_path, results_queue, client_address):
    try:
        # 파일 이름만 추출
        file_name = os.path.basename(file_path)
        base_name = file_name.split('_')[0]

        # AI 분석 명령어
        command = f"""
        source ../conda.sh &&
        conda activate ai2 &&
        cd ../AI_BasketBall_Video_Analysis &&
        python3 magic.py --detection_weight ../ckpt_best.pth --reid_weight mobilenetv3_best.pth --reid_model mobilenetv3 --person_thr 0.5 --cosine_thr 0.5 --video_file {file_name} &&
        conda deactivate
        """
        subprocess.run(["bash", "-c", command], check=True)

        # 결과 파일 이름 변경
        results_dir = "/.."
        for item in os.listdir(results_dir):
            item_path = os.path.join(results_dir, item)
            if item.endswith(".jpg") and "person_" in item:
                new_name = item.replace("person", base_name)
                new_path = os.path.join(results_dir, new_name)
                os.rename(item_path, new_path)
            elif item == "result_scoreboard.csv":
                new_name = f"{base_name}.csv"
                new_path = os.path.join(results_dir, new_name)
                os.rename(item_path, new_path)

        # csv,img위치변경 코드 추가
        # 현재 디렉토리 설정
        current_dir = "/.."

        # csv 폴더 경로 설정
        csv_dir = os.path.join(current_dir, 'csv')
        # img 폴더 경로 설정
        img_dir = os.path.join(current_dir, 'img')

        # 폴더가 없으면 생성
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)

        if not os.path.exists(img_dir):
            os.makedirs(img_dir)

        # 현재 디렉토리의 파일들을 확인
        for file_name in os.listdir(current_dir):
            file_path = os.path.join(current_dir, file_name)
            if os.path.isfile(file_path):
                # .csv 파일은 csv 폴더로 이동
                if file_name.endswith('.csv'):
                    shutil.move(file_path, csv_dir)
                # 이미지 파일은 img 폴더로 이동
                elif file_name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    shutil.move(file_path, img_dir)

        result_message = f"{file_path} 분석 완료"

        source_dir = "/.."
        destination_dir = "/.."

        # 영상 파일의 확장자 목록
        video_extensions = ('.mp4', '.avi', '.mov', '.mkv')

        try:
            # 소스 디렉토리의 파일들을 확인
            for file_name in os.listdir(source_dir):
                file_path = os.path.join(source_dir, file_name)
                if os.path.isfile(file_path) and file_name.endswith(video_extensions):
                    # 영상 파일을 대상 디렉토리로 이동
                    shutil.move(file_path, os.path.join(destination_dir, file_name))

            print(f"모든 영상이 {source_dir}에서 {destination_dir}(으)로 이동되었습니다.")
        except Exception as e:
            print(f"영상 파일 이동 중 오류 발생: {str(e)}")

    except subprocess.CalledProcessError as e:
        result_message = f"{file_path} 분석 중 오류 발생: {str(e)}"
    except Exception as e:
        result_message = f"{file_path} 처리 중 오류 발생: {str(e)}"

    send_string_image_csv()
    send_videos_to_db()
    results_queue.put((client_address, result_message))