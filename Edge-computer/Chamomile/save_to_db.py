import mysql.connector

def save_data_to_database(user_id, fileName_data, image_paths, csv_data, thread_num):
    db_connection = mysql.connector.connect(**db_config)

    try:
        cursor = db_connection.cursor()

        print(f'thread_num : {thread_num}')

        for image_path, row in zip(image_paths, csv_data):
            re_id = os.path.basename(image_path).split('.')[0]  # 이미지 파일 이름에서 ID 추출
            # game_info_query
            cursor.execute(game_info_query,
                           (int(thread_num), fileName_data, user_id, image_path, re_id, row['Shoot Try'], row['Goal']))

        db_connection.commit()

        # user_info_query
        cursor.execute(user_info_query, (user_id, int(thread_num)))

        db_connection.commit()
        print("데이터를 데이터베이스에 저장했습니다.")

    except Exception as e:
        db_connection.rollback()
        print("데이터베이스에 데이터를 저장하는 중 오류 발생:", e)

    finally:
        cursor.close()
        db_connection.close()