# -*- coding: utf-8 -*-

from vectorizers.bert_vectorizer import BERTVectorizer
from vectorizers import tokenizationK
from models.bert_nlu_model import BertNLUModel
from utils import flatten

import argparse
import os
import pickle
import numpy as np
import tensorflow as tf
import math


def sentiment_predict(input_sentence):
    # read command-line parameters
    load_folder_path = "yogiyo_model"
    type_ = "bert"

    # this line is to disable gpu
    #os.environ["CUDA_VISIBLE_DEVICES"]="-1"

    config = tf.ConfigProto(intra_op_parallelism_threads=1,
                            inter_op_parallelism_threads=1,
                            allow_soft_placement=True,)
    sess = tf.compat.v1.Session(config=config)

    bert_model_hub_path = './bert-module'
    is_bert = True

    bert_vectorizer = BERTVectorizer(is_bert, bert_model_hub_path)

    with open(os.path.join(load_folder_path, 'intents_label_encoder.pkl'), 'rb') as handle:
        intents_label_encoder = pickle.load(handle)
        intents_num = len(intents_label_encoder.classes_)

    model = BertNLUModel.load(load_folder_path, sess)

    vocab_file = "./bert-module/assets/vocab.korean.rawtext.list"
    tokenizer = tokenizationK.FullTokenizer(vocab_file=vocab_file)

    tokens = tokenizer.tokenize(input_sentence)
    tokens = [' '.join(tokens)]

    data_input_ids, data_input_mask, data_segment_ids = bert_vectorizer.transform(tokens)
    
    first_inferred_intent, first_inferred_intent_score, _, _ = model.predict_intent([data_input_ids, data_input_mask, data_segment_ids], intents_label_encoder)

    intent = str(first_inferred_intent[0])
    score = float(first_inferred_intent_score[0]) * 100

    tf.compat.v1.reset_default_graph()

    string = ''
    rating = int(float(intent))

    for i in range(1, 6):
        if i > rating:
            string +='☆'
        else:
            string += '★'

    answer_text = "{:.2f}% 확률로 [{} : {}점] 입니다.".format(score, string, intent)

    return answer_text, intent

def csv_predict(input_df):
    # read command-line parameters
    load_folder_path = "yogiyo_model"
    type_ = "bert"

    # this line is to disable gpu
    os.environ["CUDA_VISIBLE_DEVICES"]="-1"

    config = tf.ConfigProto(intra_op_parallelism_threads=1,
                            inter_op_parallelism_threads=1,
                            allow_soft_placement=True,)
    sess = tf.compat.v1.Session(config=config)

    bert_model_hub_path = './bert-module'
    is_bert = True

    bert_vectorizer = BERTVectorizer(is_bert, bert_model_hub_path)

    with open(os.path.join(load_folder_path, 'intents_label_encoder.pkl'), 'rb') as handle:
        intents_label_encoder = pickle.load(handle)
        intents_num = len(intents_label_encoder.classes_)

    model = BertNLUModel.load(load_folder_path, sess)

    vocab_file = "./bert-module/assets/vocab.korean.rawtext.list"
    tokenizer = tokenizationK.FullTokenizer(vocab_file=vocab_file)
    score_list = []
    for i,input_sentence in input_df[0].items():
        print(f'{i}번째 데이터:{input_sentence}')
        tokens = tokenizer.tokenize(input_sentence)
        tokens = [' '.join(tokens)]

        data_input_ids, data_input_mask, data_segment_ids = bert_vectorizer.transform(tokens)
    
        first_inferred_intent, first_inferred_intent_score, _, _ = model.predict_intent([data_input_ids, data_input_mask, data_segment_ids], intents_label_encoder)

        # intent = str(first_inferred_intent[0])
      
        intent = float(str(first_inferred_intent[0]))

        score_list.append(intent)
        score = float(first_inferred_intent_score[0]) * 100

    mean_score = np.mean(score_list)
    tf.compat.v1.reset_default_graph()

    # answer_text = "{:.2f}% 확률로 {}점입니다.".format(score, intent)
    print('평점의 평균:',mean_score)
    return round(mean_score, 1), math.floor(mean_score)

if __name__ == "__main__":
    print(sentiment_predict("최악입니다."))

