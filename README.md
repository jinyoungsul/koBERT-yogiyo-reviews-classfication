# koBERT-yogiyo-reviews-classfication

## 1. 프로젝트 기획
 - 맛집 리뷰 평점 개선 솔루션
 - 현 별점 시스템의 문제점 의식
    - 리뷰 내용-별점 불일치가 많아 별점만으로는 식당에 대한 긍정/부정 판단이 어려움
    - 쿠폰 및 리뷰 이벤트로 인한 이벤트성 리뷰와 의미 없는 댓글로 매장에 대한 정확한 평가가 어려움
 - 리뷰 데이터에 대한 평점을 KorBERT 모델을 이용하여 계산하는 시스템
 
## 2. ETRI koBERT(pre trained)
 - https://aiopen.etri.re.kr/service_dataset.php 에서 협약서 작성 및 tensorflow 버전 다운로드
 - DNN, LSTM, CNN 모델들과 성능 비교시 정확도가 더 우수해서 해당 모델 채택
 
 ![](https://i.imgur.com/gYlPKr7.png)
## 3. 데이터 수집 및 전처리
 - 카테고리별 식당 리뷰 무작위 수집 (Selenium을 사용하여 리뷰 크롤링 진행)
 
![KakaoTalk_20210823_170740087](https://user-images.githubusercontent.com/8359931/130415887-f93f4949-19bf-43df-b39b-e86277d07ebe.gif)
 
 - 수집된 데이터에 대해 한글, 공백 제외한 모든 숫자/특수문자/모음과 자음만 있는 글자 제거
 - 맞춤법 교정
 - 리뷰 최소 길이 : 12음절
 - 성능 개선을 위해 문장당 긍부정 비율에 기반한 기준 수립후 재라벨링
 - 수집된 리뷰 코멘트를 30797 vocabs로 토큰화
 - KorBERT 모델을 파인튜닝 할 수 있게 label과 input sequence로 나누어 줌 data.txt -> label, seq.in
   seq.in은 KorBERT가 pre-train된 대로 tokenization 과정을 거쳐 생성됨
   
 ![label](https://user-images.githubusercontent.com/8359931/130418608-57c32632-98ba-4119-a9de-e7ad8379d231.PNG)
 ![sequence](https://user-images.githubusercontent.com/8359931/130418620-d5982006-9965-403f-b732-7b9a51d65604.PNG)
  
 ## 4. 파인튜닝 및 서비스
  - 생성된 label, seq.in을 통해 파인튜닝 진행
  - Flask를 이용해 웹 서버를 구동하고, 개별 리뷰에 대한 평점과
    csv파일 업로드를 한 후 개선된 평점 확인 가능
  
  


