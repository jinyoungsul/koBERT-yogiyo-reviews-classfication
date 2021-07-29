import pandas as pd
from selenium import webdriver

import time

from tqdm import tqdm
from tqdm import trange

# 크롬 드라이버로 크롬 켜기
driver = webdriver.Chrome("./data/chromedriver.exe")

# 창 최소화모드에서는 카테고리가 보이지 않기에 창 최대화
driver.maximize_window()

# 접속할 웹 사이트 주소(요기요 홈페이지)
url = "https://www.yogiyo.co.kr/mobile/#/"
driver.get(url)


# 검색할 주소(나중에 구+동으로 나눠야 함)
location = "화성시 능동"

# 시간을 2초로 줌
interval = 2

# 주소 입력해서 페이지 넘어감
# 입력창 클릭 -> 입력창에 써져있는거 지우기 클릭 -> 로케이션 값 보내기 -> 검색버튼 클릭 -> 첫번째 검색결과 클릭
print(location +'으로 위치 설정 하는중...')
driver.find_element_by_css_selector('#search > div > form > input').click()
driver.find_element_by_css_selector('#button_search_address > button.btn-search-location-cancel.btn-search-location.btn.btn-default > span').click()
driver.find_element_by_css_selector('#search > div > form > input').send_keys(location)
driver.find_element_by_css_selector('#button_search_address > button.btn.btn-default.ico-pick').click()
time.sleep(interval)
driver.find_element_by_css_selector('#search > div > form > ul > li:nth-child(3) > a').click()
time.sleep(interval)
print(location+'으로 위치 설정 완료!')


#요기요 카테고리 페이지의 Element Number Dictionary 정의
#카테고리의 xpath 값이 카테고리 별로 다르기에 숫자를 다르게 넣어주려고 이렇게 정의한 것
food_dict = { '치킨':5, '피자&양식':6,
              '중국집':7, '한식':8, '일식&돈까스':9,
              '족발&보쌈':10, '야식':11,
              '분식':12, '카페&디저트':13 }


for category in food_dict:
    print(category+' 카테고리 페이지 로드중...')
    # food_dict.get(category) -> category라는 key에 대응되는 value를 리턴
    # .format() 이건 문자열 포매팅을 한 것이다.
    # food_dict.get() 이건 괄호 안에 들어가는 key에 대한 value를 리턴하는 것이다.
    # 그리고 문자열 안의 {} 안에 그 value(여기선 숫자)가 들어가게 되는 것이다.
    driver.find_element_by_xpath('//*[@id="category"]/ul/li[{}]/span'.format(food_dict.get(category))).click()
    time.sleep(interval)
    print(category+' 카테고리 페이지 로드 완료!')


    # 현재 문서 높이를 가져와서 저장
    prev_height = driver.execute_script("return document.body.scrollHeight")

    # 반복 수행
    while True:
        # 스크롤을 가장 아래로 내림
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    
    
        # 페이지 로딩 대기
        time.sleep(interval)


        # 현재 문서 높이를 가져와서 저장
        curr_height = driver.execute_script("return document.body.scrollHeight")
    
        # 전에 저장한 문서 높이와 현재 저장한 문서 높이가 같으면 while문 빠져나감
        if curr_height == prev_height:
            break

        prev_height = curr_height

    print("스크롤 완료")

    # 리스트 객체 만들고
    restaurant_list=[]

    # 우리동네플러스나 슈퍼레드위크추천이 아닌 요기요등록음식점 부분으로 설정하는 것
    restaurants = driver.find_elements_by_css_selector('#content > div > div:nth-child(4) > div > div.restaurant-list > div.col-sm-6.contract')
    
    #  restaurants에 저장된 elements에서 loop를 돌리며 (각각의 가게들을 순회하며)
    for restaurant in restaurants:
        restaurant_list.append(restaurant.find_element_by_css_selector('div > table > tbody > tr > td:nth-child(2) > div > div.restaurant-name.ng-binding').text)
        
    # 일단 실험해보는거니까 리스트에서 첫번째것만 빼서 전달
    for restaurant_name in restaurant_list:
        # 주소 설정창 말고 음식점 검색 버튼 클릭
        driver.find_element_by_xpath('//*[@id="category"]/ul/li[1]/a').click()

        # 음식점 검색 입력창에 가게 이름 전달
        driver.find_element_by_xpath('//*[@id="category"]/ul/li[15]/form/div/input').send_keys(restaurant_name)

        # 음식점 검색 버튼 클릭
        driver.find_element_by_xpath('//*[@id="category_search_button"]').click()

        time.sleep(interval)

        # 첫번째 나오는 음식점 클릭
        driver.find_element_by_css_selector('#content > div > div:nth-child(5) > div > div > div:nth-child(1) > div').click()
        
        time.sleep(interval)

        # 클린리뷰 클릭
        driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a').click()

        time.sleep(interval)

        # 클린리뷰 옆에 있는 리뷰 숫자가 써져있는데 그걸 보여주는 요소의 text를 가져와서 정수형으로 변환
        review_count = int(driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a/span').text)

        # 요기요 리뷰는 더보기를 눌렀을 때 10개를 로드하니까 몇번 더보기를 누를지 정해야하니까 10으로 나누어줌
        click_count = int((review_count/10))

        # 리뷰 페이지를 모두 펼치는 for문 시작
        print('모든 리뷰 불러오는 중...')
        for _ in trange(click_count):
            try:
                # 스크롤을 가장 아래로 내림
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                
                # 더보기 클릭
                driver.find_element_by_class_name('btn-more').click()
        
                # 2초 쉼
                time.sleep(2)
        
            except Exception as e:
                print(e)
                print('페이지 돌아가기중...')
                driver.execute_script("window.history.go(-1)")
                time.sleep(interval)
                print('페이지 돌아가기 완료!\n')
                continue
    
        # 스크롤을 가장 아래로 내림
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        print('모든 리뷰 불러오기 완료!')

        ### 리뷰 크롤링

        # 리뷰 가져와서 revies객체에 할당
        reviews = driver.find_elements_by_css_selector('#review > li.list-group-item.star-point.ng-scope')

        # 데이터프레임 객체 생성 및 열에 이름 부여
        print('리뷰 저장하는 중...')
        df = pd.DataFrame(columns=['Category','Location','Restaurant','UserID','Menu','Review','Date','Total','Taste','Quantity','Delivery'])
        
        for review in tqdm(reviews):
            try:
                df.loc[len(df)] = {
                    'Category':category,
                    'Location':location,
                    'Restaurant':driver.find_element_by_class_name('restaurant-name').text,
                    'UserID':review.find_element_by_css_selector('span.review-id.ng-binding').text,
                    'Menu':review.find_element_by_css_selector('div.order-items.default.ng-binding').text,
                    'Review':review.find_element_by_css_selector('p').text,
                    'Date':review.find_element_by_css_selector('div:nth-child(1) > span.review-time.ng-binding').text,
                    'Total':str(len(review.find_elements_by_css_selector('div > span.total > span.full.ng-scope'))),
                    'Taste':review.find_element_by_css_selector('div:nth-child(2) > div > span.category > span:nth-child(3)').text,
                    'Quantity':review.find_element_by_css_selector('div:nth-child(2) > div > span.category > span:nth-child(6)').text,
                    'Delivery':review.find_element_by_css_selector('div:nth-child(2) > div > span.category > span:nth-child(9)').text,
                    }
                
            except Exception as e:
                print('리뷰 페이지 에러')
                print(e)
                print('페이지 돌아가기중...')
                driver.execute_script("window.history.go(-1)")
                time.sleep(interval)
                print('페이지 돌아가기 완료!\n')
                continue
            
        df.to_csv('./data/yogiyo/' + df.Restaurant[0] + '.csv')
        print('리뷰 저장하는 완료!')
        
        print('페이지 돌아가기중...')
        driver.execute_script("window.history.go(-1)")
        time.sleep(interval)
        print('페이지 돌아가기 완료!\n')
