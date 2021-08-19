# -*- coding: utf-8 -*-

from readers.data_reader import Reader
from vectorizers.bert_vectorizer import BERTVectorizer
from vectorizers import tokenizationK as tk
from models.bert_nlu_model import BertNLUModel
from utils import flatten

import argparse
import os
import pickle
import tensorflow as tf
from sklearn import metrics


# read command-line parameters
parser = argparse.ArgumentParser('Evaluating the BERT / ALBERT NLU model')
parser.add_argument('--model', '-m', help = 'Path to BERT / ALBERT NLU model', type = str, required = True)
parser.add_argument('--data', '-d', help = 'Path to data', type = str, required = True)
parser.add_argument('--type', '-tp', help = 'bert   or    albert', type = str, default = 'bert', required = False)


VALID_TYPES = ['bert', 'albert']

args = parser.parse_args()
load_folder_path = args.model
data_folder_path = args.data
type_ = args.type

# this line is to disable gpu
os.environ['CUDA_VISIBLE_DEVICES']='-1'

config = tf.ConfigProto(intra_op_parallelism_threads=8, 
                        inter_op_parallelism_threads=0,
                        allow_soft_placement=True,
                        device_count = {'CPU': 8})
sess = tf.Session(config=config)

if type_ == 'bert':
    bert_model_hub_path = './bert-module'
    is_bert = True
elif type_ == 'albert':
    bert_model_hub_path = 'https://tfhub.dev/google/albert_base/1'
    is_bert = False
else:
    raise ValueError('type must be one of these values: %s' % str(VALID_TYPES))
    
bert_vectorizer = BERTVectorizer(is_bert, bert_model_hub_path)

# loading models
print('Loading models ...')
if not os.path.exists(load_folder_path):
    print('Folder `%s` not exist' % load_folder_path)

with open(os.path.join(load_folder_path, 'intents_label_encoder.pkl'), 'rb') as handle:
    intents_label_encoder = pickle.load(handle)
    intents_num = len(intents_label_encoder.classes_)
    
model = BertNLUModel.load(load_folder_path, sess)

tokenizer = tk.FullTokenizer('./bert-module/assets/vocab.korean.rawtext.list')

data_text_arr, data_intents = Reader.read(data_folder_path)
data_input_ids, data_input_mask, data_segment_ids = bert_vectorizer.transform(data_text_arr)

def get_results(input_ids, input_mask, segment_ids, intents, intents_label_encoder):
    first_inferred_intent, first_inferred_intent_score, _, _ = model.predict_intent([data_input_ids, data_input_mask, data_segment_ids], intents_label_encoder)
    acc = metrics.accuracy_score(intents, first_inferred_intent)

    intent_incorrect = ''
    for i, sent in enumerate(input_ids):

        if intents[i] != first_inferred_intent[i]:
            tokens = tokenizer.convert_ids_to_tokens(input_ids[i])
            intent_incorrect += ('sent {}\n'.format(tokens))
            intent_incorrect += ('pred: {}\n'.format(first_inferred_intent[i].strip()))
            intent_incorrect += ('score: {}\n'.format(first_inferred_intent_score[i]))
            intent_incorrect += ('ansr: {}\n'.format(intents[i].strip()))
            intent_incorrect += '\n'

    return acc, intent_incorrect

print('==== Evaluation ====')
acc, intent_incorrect = get_results(data_input_ids, data_input_mask, data_segment_ids,
                                                            data_intents, intents_label_encoder)

# 테스트 결과를 모델 디렉토리의 하위 디렉토리 'test_results'에 저장해 준다.
result_path = os.path.join(load_folder_path, 'test_results')

if not os.path.isdir(result_path):
    os.mkdir(result_path)

with open(os.path.join(result_path, 'intent_incorrect.txt'), 'w') as f:
    f.write(intent_incorrect)

with open(os.path.join(result_path, 'test_total.txt'), 'w') as f:
    f.write('Intent accuracy = {}\n'.format(acc))

tf.compat.v1.reset_default_graph()
