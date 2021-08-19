# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import sys
from vectorizers import tokenizationK as tk

class BERTVectorizer:
    
    def __init__(self, is_bert,
                 bert_model_hub_path="./bert-module"):

        print('initializing!')
        self.is_bert = is_bert
        print('is_bert :', self.is_bert)
        self.bert_model_hub_path = bert_model_hub_path
        print('bert_model_hub_path :', self.bert_model_hub_path)
        self.tokenizer = tk.FullTokenizer('./bert-module/assets/vocab.korean.rawtext.list')
        print('initialized!')

    
    def transform(self, text_arr):
        print('transform started')

        input_ids = []
        input_mask = []
        segment_ids = []

        # print('text arr :', text_arr)
        for text in text_arr: 

            ids, mask, seg_ids= self.__vectorize(text.strip())

            # print('text :', text)
            # print('ids :', ids)
            # print('mask :', mask)
            # print('seg_ids :', seg_ids)
            # print('valid pos :', valid_pos)

            input_ids.append(ids)
            input_mask.append(mask)
            segment_ids.append(seg_ids)

        input_ids = tf.keras.preprocessing.sequence.pad_sequences(input_ids, padding='post')
        input_mask = tf.keras.preprocessing.sequence.pad_sequences(input_mask, padding='post')
        segment_ids = tf.keras.preprocessing.sequence.pad_sequences(segment_ids, padding='post')
        return input_ids, input_mask, segment_ids
    
    
    def __vectorize(self, text: str):

        # str -> tokens list
        tokens = text.split() # whitespace tokenizer


        # insert "[CLS]"
        tokens.insert(0, '[CLS]')
        # insert "[SEP]"
        tokens.append('[SEP]')
        
        segment_ids = [0] * len(tokens)
        input_ids = self.tokenizer.convert_tokens_to_ids(tokens)

        input_mask = [1] * len(input_ids)
        
        return input_ids, input_mask, segment_ids
        
