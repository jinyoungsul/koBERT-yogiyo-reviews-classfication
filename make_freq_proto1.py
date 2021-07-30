import os
import re
import pandas as pd


class FreqUtil :
    
    def __init__(self) :
        self.sentence_freq = dict()
        self.eojeol_freq = dict()
        self.emjeol_freq = dict()
        
    def make_files_path(self, in_path, encoding) :
        file_names = os.listdir(in_path)
        
        for file_name in file_names :
            in_file_path = in_path + file_name
            self.make_freq_dict(in_file_path, encoding)

        
    def make_freq_dict(self, in_file_path, encoding) :
        
        re_reviews = ReUtil.make_re_review(frequtil, in_file_path, encoding)    #
        
        for re_review in re_reviews :
            
            sentence = re_review
            self.add_freq_dic(self.sentence_freq, sentence, 1)
            
            eojeols = re_review.split()
                        
            for eojeol in eojeols :
                self.add_freq_dic(self.eojeol_freq, eojeol, 1)
                
                for emjeols in eojeol :
                    for emjeol in list(emjeols) :
                        self.add_freq_dic(self.emjeol_freq, emjeol, 1)

                
    def add_freq_dic(self, freq_dict, key, value) :
        if key in freq_dict :
            freq_count = freq_dict[key]
            freq_dict[key] = freq_count + value
        else :
            freq_dict[key] = value
            
            
    def write_freq_file(self, out_path, encoding) :
        sentence_freq_file_path = out_path + "sentence_freq.dic"
        eojeol_freq_file_path = out_path + "eojeol_freq.dic"
        emjeol_freq_file_path = out_path + "emjeol_freq.dic"
        
        self.write_freq_dic_unit(sentence_freq_file_path, encoding, self.sentence_freq)
        self.write_freq_dic_unit(eojeol_freq_file_path, encoding, self.eojeol_freq)
        self.write_freq_dic_unit(emjeol_freq_file_path, encoding, self.emjeol_freq)
        
        
    def write_freq_dic_unit(self, out_file_path, encoding, freq_dic) :
        
        file = open_file(out_file_path, encoding, 'w')  #
        
        for key in freq_dic.keys() :
            file.write(f"{key}\t{freq_dic[key]}\n")
            
        file.close
        
        
# 나중에 가독성을 위해 다른 py로 빠질 수 있음
def open_file(file_path, encoding, mode) :
    if len(encoding) == 0 :
        return open(file_path, mode)
    else :
        return open(file_path, mode, encoding = encoding)
    

# 목적에 따라 나중에 바뀔 수 있음
# 나중에 가독성을 위해 다른 py로 빠질 수 있음
class ReUtil :
    def __init__(self) :
        pass
    
    def make_re_review(self, in_file_path, encoding) :
        re_reviews = list()
        
        dataframe = pd.read_csv(in_file_path, encoding = encoding)
        reviews = dataframe['Review']
        reviews_array = reviews.values
        for review in reviews_array :
            re_review = re.sub('[^a-zA-Z0-9ㄱ-ㅎㅏ-ㅣ가-힣 ]', '', review)
            re_reviews.append(re_review)
        
        return re_reviews




if __name__ == "__main__" :
    
    in_path = "C:/sklee/Academy/미디어젠 프로젝트/Crawl_test/in_path/"
    out_path = "C:/sklee/Academy/미디어젠 프로젝트/Crawl_test/out_path/"
    encoding = "UTF-8"
    
    frequtil = FreqUtil()
    frequtil.make_files_path(in_path, encoding)
    frequtil.write_freq_file(out_path, encoding)
    
    
##############################################################################

"""
Yogiyo_Crawler_df_to_csv_final.py로 크롤링해서 저장된 csv 파일에서
Review열의 리뷰내용만을 뽑아 정규식을 거쳐 문장, 어절, 음절 별로 빈도수를 세어 dict로 만든 것입니다.
value는 평점이 아니라 빈도 수 입니다.

in_path에는 크롤링한 데이터가 있는 폴더경로를 넣어주고
out_path에는 빈도 파일이 생성될 폴더경로를 넣어주면 됩니다.

기본적인 정제만 거쳤기에 아직 더 정제해야할 것들이 많습니다.
추후 보완할 예정입니다.

output 파일은 구글드라이브에 올려놨습니다.
"""























    
    