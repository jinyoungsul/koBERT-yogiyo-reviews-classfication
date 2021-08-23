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
 - 카테고리별 식당 리뷰 무작위 수집
 
