# -*- coding: utf-8 -*-

import os


class Reader:
    
    def __init__(self):
        pass
    
    def read(dataset_folder_path):
        labels = None
        text_arr = None

        with open(os.path.join(dataset_folder_path, 'label'), encoding='utf-8') as f:
            labels = f.read().splitlines()
        
        with open(os.path.join(dataset_folder_path, 'seq.in'), encoding='utf-8') as f:
            text_arr = f.read().splitlines()
        
            
        assert len(text_arr) == len(labels)
        return text_arr, labels
        
if __name__ == '__main__':
    text_arr, labels = Reader.read('data/atis/train')
