# koBERT-yogiyo-reviews-classfication

## 1. 프로젝트 기획
 - 평점 추천 시스템(primary)
    - 새로운 개별 리뷰에 대한 점수 측정
    - 꼭 BERT 모델일 필요가 있을까?
      - 타 모델들과 성능 비교(textCNN, LSTM 등)
 - 과대평가 방지 시스템(optional)
    - 리뷰 이벤트를 통한 평점이 높아졌을 가능성 제기
    - 실제로 이벤트를 진행한 날짜에 다른 일자보다 평점이 높아졌는지에 대한 검증 필요
 - 실제 데모 시연까지 보이는 것을 목표로
    - 웹 or 터미널

## 2. ETRI koBERT(pre trained)
 - https://aiopen.etri.re.kr/service_dataset.php 에서 협약서 작성 및 tensorflow 버전 다운로드
