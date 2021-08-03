import os
import csv

folder_path = "C:/sklee/Academy/미디어젠 프로젝트/Crawl_test/counttest/" # 여기에 csv 파일들이 있는 폴더의 경로를 설정해주시면 됩니다.
encoding = "utf-8"

one_count = int()
two_count = int()
three_count = int()
four_count = int()
five_count = int()

def make_file_path(folder_path: str, encoding) :
    file_names = os.listdir(folder_path)
    
    for file_name in file_names :
        file_path = folder_path + file_name
        
        count_rating(file_path, encoding, file_name)

def count_rating(file_path: str, encoding, file_name) :
    file = open(file_path, 'r', encoding = encoding)
    csvfile = csv.reader(file)
    
    global one_count 
    global two_count
    global three_count
    global four_count
    global five_count
    
    for line in csvfile :
        if line[7] == '1':
            one_count += line[7].count('1')
        elif line[7] == '2':
            two_count += line[7].count('2')
        elif line[7] == '3':
            three_count += line[7].count('3')    
        elif line[7] == '4':
            four_count += line[7].count('4')    
        elif line[7] == '5':
            five_count += line[7].count('5')
        elif line[7] == None :
            print(f"{file_name}파일의 {line[0]}번째 라인에서 None값이 발견되었습니다.")


make_file_path(folder_path, encoding)            
print(one_count)
print(two_count)
print(three_count)
print(four_count)
print(five_count)

