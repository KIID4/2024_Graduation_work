import base64
from io import BytesIO
import matplotlib as plt


def get_all_basketball_play_shooting_mean_graph():
    # 추출된 데이터를 토대로 matplotlib을 통해서 그래프화
    df_graph = df_weather[df_weather["date"] > "2022-12-31"]
    plt.figure(figsize=(10, 5))
    plt.title(f"{point} 관측소 정보", fontsize=15)
    plt.plot(
        df_graph["date"], df_graph["temperature"], "-", color="orange", label=str(point)
    )
    plt.grid()
    plt.legend(fontsize=13)
    plt.xticks(rotation=45)

    # 그래진 그래프를 텍스트 형태로 저장하여 decode
    img = BytesIO()
    plt.savefig(img, format="png", dpi=200)
    img.seek(0)
    img_str = base64.b64encode(img.read()).decode("utf-8")
    return img_str
