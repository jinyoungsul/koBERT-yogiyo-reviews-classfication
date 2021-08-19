# -*- coding: utf-8 -*-

from vectorizers.bert_vectorizer import BERTVectorizer
from vectorizers import tokenizationK
from models.bert_nlu_model import BertNLUModel
from utils import flatten

import argparse
import os
import pickle
import tensorflow as tf

import pdb

# read command-line parameters
parser = argparse.ArgumentParser('Evaluating the Joint BERT / ALBERT NLU model')
parser.add_argument('--model', '-m', help = 'Path to BERT / ALBERT NLU model', type = str, required = True)
parser.add_argument('--type', '-tp', help = 'bert   or    albert', type = str, default = 'bert', required = False)


VALID_TYPES = ['bert', 'albert']

args = parser.parse_args()
load_folder_path = args.model
type_ = args.type

# this line is to disable gpu
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

config = tf.ConfigProto(intra_op_parallelism_threads=1,
                        inter_op_parallelism_threads=1,
                        allow_soft_placement=True,
                        device_count = {'CPU': 1})
sess = tf.compat.v1.Session(config=config)

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

vocab_file = "./bert-module/assets/vocab.korean.rawtext.list"
tokenizer = tokenizationK.FullTokenizer(vocab_file=vocab_file)

kobert_layer = model.model.layers[3]
# token_embedding = kobert_layer.weights[0]
token_embedding = kobert_layer.weights[0].eval(session=sess)
# pdb.set_trace()

out_m_path = os.path.join(load_folder_path, 'meta.tsv')
out_v_path = os.path.join(load_folder_path, 'vecs.tsv')

# make out_m(meta.tsv) first
print(f'creating {out_m_path} out of {vocab_file}')
os.system(f"sed 1,2d {vocab_file} | cut -f 1 > {out_m_path}")

out_v = open(out_v_path, 'w', encoding='utf-8')

print(f'creating {out_v_path}')
for token_emb in token_embedding:
    # pdb.set_trace()
    out_v.write('\t'.join([str(x) for x in token_emb]) + "\n")
