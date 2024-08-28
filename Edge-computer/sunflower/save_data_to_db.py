
import mysql.connector

def save_data_to_db(video_num, video_path):
    connection = mysql.connector.connect(**db_config)

    cursor = connection.cursor()

    # save_video_query

    cursor.execute(save_video_query, (video_path, video_num))

    connection.commit()
    cursor.close()
    connection.close()