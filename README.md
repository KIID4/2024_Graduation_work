# 1.  **프로젝트 개요**
> 현대 스포츠, 특히 농구와 같은 팀 스포츠에서는 경기 데이터를 체계적으로 분석하는 것이 매우 중요합니다.<br>
> 과거에는 선수들의 경기 영상과 성과 데이터를 분석하는 데 많은 시간과 인력이 필요했지만, <br>
> 최근의 기술 발전으로 인해 이러한 분석이 더욱 정밀하고 신속하게 이루어질 수 있게 되었습니다.<br>
> 특히,  AI와 엣지 컴퓨팅의 기술을 이용하여 데이터 분석을 통해 경기 중에도 <br>
> 선수들의 퍼포먼스를 평가하고 전략을 수정할 수 있는 기회를 제공할 수 있습니다.<br>

> 그래서, 저희는 농구 경기를 라즈베리파이를 이용하여 현장에서 촬영 후 분석 과정을 통해<br>
> 슛 성공률을 분석하고 이를 웹 대시보드를 통해 사용자에게 제공하는 플랫폼을 제작하고자 합니다

<br>

# 2. 기술 스택
<img src="https://github.com/user-attachments/assets/11182daa-5c7c-4098-8371-eacc71365567" width="600"/>

<br>

# 3. 시스템 구성
<img src="https://github.com/user-attachments/assets/0f656fc4-a1cc-4920-8087-55510b6b604a" width="600"/>
<!-- 여기에 시나리오 작성 -->

<br>

# 4. 실제 테스트
## 1) QR코드를 이용하여 라즈베리파이 기기를 등록
<table border="0">
  <tr>
    <td rowspan="2"> <img src="https://github.com/user-attachments/assets/8ecd3978-ddf5-470c-856e-b5c39e7a7387" height="220"/> </td>
    <td rowspan="2"> <img src="https://github.com/user-attachments/assets/198bfe67-39b2-444a-9eb4-de95a0c0b7ce" height="220"/> </td>
    <td> <img src="https://github.com/user-attachments/assets/2ae369c0-80be-4b18-8b82-806a6b92e9c9" height="120"/> </td>
  </tr>
  <tr>    
    <td> <img src="https://github.com/user-attachments/assets/bc8be5c6-2c96-467a-b17d-1925a4cfbb36" height="100"/> </td>
  </tr>
</table>

<br>

## 2) 카메라용 라즈베리파이를 들고 실제 농구경기 영상을 촬영 후 로컬에 저장
<img src="https://github.com/user-attachments/assets/242b1be3-4674-4cf5-8698-121e2e4d74e0" width="400"/><br>
<img src="https://github.com/user-attachments/assets/f498b3e2-f28a-4038-96d3-3e68934a770d" width="300"/>

<br>

## 3) 해당 영상을 학내망 컴퓨터로 전송하여 엣지 컴퓨터로 전송
<img src="https://github.com/user-attachments/assets/e084741a-25c8-4a5a-be37-ff0436596010" width="400"/>

<br>

## 4) 엣지컴퓨터에서 분석 과정이 끝난 후 결과를 각각 DB로 전송
<img src="https://github.com/user-attachments/assets/181a68da-11b1-4e87-b5f8-3f5318ccb945" width="600"/>

<br>

## 5) 전송이 끝나면 웹 대시보드에서 확인
<img src="https://github.com/user-attachments/assets/5744762d-a5e4-4a02-a2e3-1f59b65851f4" width="700"/><br>
<img src="https://github.com/user-attachments/assets/087e847f-18cc-4af6-9b2f-9a62b955b1d0" width="350"/>
<img src="https://github.com/user-attachments/assets/3baaa7c2-f697-4ed1-be30-b2c4a820159b" width="350"/>


# 5. **팀원**

| **No.** | **성명** | **담당** | **수행역할** |
| --- | --- | --- | --- |
| 1 | 안동균 | DB, 엣지컴퓨터 | 각 기기 사이의 데이터 전송 모듈 개발 및 DB 프로그래밍 |
| 2 | 조용민 | AI | AI 모델 개발(학습, 분석 진행), AI 결과 송수신 보조 |
| 3 | 강승우 | AI | AI 기술적 환경 설정, 데이터 라벨링 작업 |
| 4 | 이정민 | IoT, 웹 | 카메라 RPI 촬영 관련 모듈 개발 전담, RPI HW 관리, <br>웹서버·WAS·API서버 전담, DB 설계, 웹 디자인·설계 및 개발 전담 |
| 5 | 김도형 | IoT, 웹 | IoT 및 웹 개발 지원, 자료 및 리소스 제공 |

<br>

# 6. 참고 문헌

**논문**

[1] Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks (Shaoqing Ren, Kaiming He, Ross Girshick, and Jian Sun)
[2] 객체탐지모델 YOLO의 버전별 특성 비교 연구 (서울신학대학교 김준용 교수)
[3] Simple Online and Realtime Tracking (Alex Bewley, Zongyuan Ge, Lionel Ott, Fabio Ramos, Ben Upcroft)
[4] Searching for MobileNetV3(Andrew Howard, Mark Sandler, Grace Chu, Liang-Chieh Chen, Bo Chen, Mingxing Tan, Weijun Wang, Yukun Zhu, Ruoming Pang, Vijay Vasudevan, Quoc V. Le, Hartwig Adam)

**도서**

[1] 데이터 통신과 네트워킹 TCP/IP 프로토콜 기반 (이재광, 김중규, 이경현, 홍충선)
[2] 데이터 과학을 위한 파이썬 머신러닝 (최성철)
[3] 파이썬으로 만드는 인공지능 (오일석, 이진선)
[4] 점프 투 플라스크 (박응용)
