import os, re
import pandas as pd
import numpy as np
from selenium import webdriver
import time



class WebUtil :
    
    def __init__(self) :
        self.driver = webdriver.Chrome("C:/Users/samsung/Downloads/chromedriver.exe")
        self.driver.maximize_window()
        self.url = "https://www.yogiyo.co.kr/mobile/#/"
        self.driver.get(self.url)
        
        self.category_dict = {'치킨':5, '피자&양식':6,
                              '중국집':7, '한식':8, '일식&돈까스':9,
                              '족발&보쌈':10, '야식':11,
                              '분식':12, '카페&디저트':13 }
                  
    def set_location(self, location) :
        print(location +'으로 위치 설정 하는중...')
        self.driver.find_element_by_css_selector('#search > div > form > input').click()
        self.driver.find_element_by_css_selector('#button_search_address > button.btn-search-location-cancel.btn-search-location.btn.btn-default > span').click()
        self.driver.find_element_by_css_selector('#search > div > form > input').send_keys(location)
        self.driver.find_element_by_css_selector('#button_search_address > button.btn.btn-default.ico-pick').click()
        time.sleep(2)
        self.driver.find_element_by_css_selector('#search > div > form > ul > li:nth-child(3) > a').click()
        time.sleep(2)
        print(location+'으로 위치 설정 완료!')

        
    def go_to_category(self, category) :
        print(category+' 카테고리 페이지 로드중...')
        self.driver.find_element_by_xpath('//*[@id="category"]/ul/li[{}]/span'.format(self.category_dict.get(category))).click()
        time.sleep(2)
        print(category+' 카테고리 페이지 로드 완료!')

        
    def scroll_bottom(self) :
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        
    def scroll_to_bottom(self) : 
        print("카테고리 가게 펼치는 중...")
        prev_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True :
            self.scroll_bottom()
            time.sleep(2)
            curr_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if curr_height == prev_height:
                break
        
            prev_height = curr_height
    
        print("카테고리 가게 펼치기 완료!")
        

    def get_restaurant_list(self) :
        print("가게 리스트 만들기 시작...")
        self.restaurant_list = []
        self.restaurants = self.driver.find_elements_by_css_selector('#content > div > div:nth-child(4) > div > div.restaurant-list > div.col-sm-6.contract')
        for restaurant in self.restaurants:
            self.review_cnt = restaurant.find_element_by_css_selector('div > table > tbody > tr > td:nth-child(2) > div > div.stars > span:nth-child(2)').text
            try :
                if int(self.review_cnt.replace('리뷰 ', '')) >= 10 :
                    self.restaurant_list.append(restaurant.find_element_by_css_selector('div > table > tbody > tr > td:nth-child(2) > div > div.restaurant-name.ng-binding').text)
            except ValueError as e :
                pass        
        self.restaurant_list = list(set(self.restaurant_list)) 
        print("가게 리스트 만들기 성공!")
        return self.restaurant_list
    

    def search_restaurant(self, restaurant_name):
        print("가게 검색중...")
        self.driver.find_element_by_xpath('//*[@id="category"]/ul/li[1]/a').click()
        self.driver.find_element_by_xpath('//*[@id="category"]/ul/li[15]/form/div/input').send_keys(restaurant_name)
        self.driver.find_element_by_xpath('//*[@id="category_search_button"]').click()
        time.sleep(5)
        print("가게 검색 성공!")

        
    def go_to_restaurant(self):
        print("검색한 가게 가는 중...")
        self.driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div/div/div/div/table/tbody/tr/td[2]/div/div[1]').click()
        time.sleep(5)
        print("검색한 가게 갔음!")

        
    def go_to_cleanreview(self):
        print("클린리뷰 가는 중")
        self.driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a').click()
        time.sleep(2)
        print("클린리뷰 갔음!")

        
    def click_more_review(self):
        self.driver.find_element_by_class_name('btn-more').click()
        time.sleep(2)

        
    def stretch_review_page(self):
        review_count = int(self.driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a/span').text)
        # click_count = int((review_count/10))
        click_count = min(int(review_count/10), 10)
        print('모든 리뷰 불러오기 시작...')
        for _ in range(click_count):
            self.scroll_bottom()
            self.click_more_review()
        
        self.scroll_bottom()
        print('모든 리뷰 불러오기 완료!')

        
    def get_all_review_elements(self):
        print('리뷰 모든 요소 가져오는 중...')
        self.reviews = self.driver.find_elements_by_css_selector('#review > li.list-group-item.star-point.ng-scope')
        print('리뷰 모든 요소 가져옴!')
        return self.reviews    


    def go_back_page(self):
        print('페이지 돌아가기중...')
        self.driver.execute_script("window.history.go(-1)")
        time.sleep(5)
        print('페이지 돌아가기 완료!'+'\n')    
    
            
            
    def Crawl_Main(self, gu: str, file_path: str, encoding: str) :
        Gu = Location()
        dong_list = Gu.Location_setting(gu)
        for dong in dong_list :
            location = gu + " " + dong
            self.set_location(location)
            
            for key in self.category_dict :
                self.go_to_category(key)
                self.scroll_to_bottom()
                self.get_restaurant_list()
                
                for restaurant_name in self.restaurant_list :
                    self.search_restaurant(restaurant_name)
                    self.go_to_restaurant()
                    self.go_to_cleanreview()
                    self.stretch_review_page()
                    self.get_all_review_elements()
                    
                    store = Store()
                    self.review_dic = store.get_all_review(self.reviews)
                    
                    restaurant_file_path = file_path + restaurant_name + ".txt"
                    
                    writing = WriteFile()
                    writing.write_dict(restaurant_file_path, encoding, self.review_dic)
                    
                    self.go_back_page()
                    
                    
        
            
        


class Store :
    def __init__(self) :
        # 키는 review 내용, 벨류는 평점
        self.review_dic = dict()
    
        
    def get_all_review(self, reviews) :
        print("리뷰 dict 만드는 중...")
        for review in reviews :
            self.review_dic[review.find_element_by_css_selector('p').text] = review.find_element_by_css_selector('div:nth-child(2) > div > span.category > span:nth-child(3)').text
            # self.review_dic = {review.find_element_by_css_selector('p').text : review.find_element_by_css_selector('div:nth-child(2) > div > span.category > span:nth-child(3)').text}
        print("리뷰 dict 완성!")
        return self.review_dic



class Location :
    def __init__(self) :
        pass
    
        
    def Location_setting(self, gu) :
        
        if gu == '송파구' :
            dong_list = ['가락동','거여동','마천동','문정동','방이동','삼전동','석촌동','송파동','오금동','오륜동','잠실동','장지동','풍납동']
            return dong_list
        
        elif gu == '강남구' :
            dong_list = ['역삼동','개포동','청담동','삼성동','대치동','신사동','논현동','압구정동','세곡동','자곡동','율현동','일원동','수서동','도곡동']
            return dong_list
        
        elif gu == '서초구' :
            dong_list = ['방배동','양재동','우면동','원지동','잠원동','반포동','서초동','내곡동','염곡동','신원동']
            return dong_list
        
       
        
       
class WriteFile :
    def __init__(self) :
        pass
    
    
    def open_file(self, file_path, encoding, mode) :
        if len(encoding) == 0 :
            return open(file_path, mode)
        else:
            return open(file_path, mode, encoding = encoding)
    
        
    def write_dict(self, file_path: str, encoding: str, review_dic: dict):
        file = self.open_file(file_path, encoding, "w")
        
        for key in review_dic.keys() :
            file.write(f"{key}\t{review_dic[key]}\n")
            
        file.close

            



    
            
    
if __name__ == "__main__" :
    gu = '강남구'
    file_path = "C:/sklee/Academy/미디어젠 프로젝트/Crawl_test/"
    encoding = "UTF-8"
    
    Crawl = WebUtil()
    Crawl.Crawl_Main(gu, file_path, encoding)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    