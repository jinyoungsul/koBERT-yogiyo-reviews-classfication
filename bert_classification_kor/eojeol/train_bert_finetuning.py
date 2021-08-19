# -*- coding: utf-8 -*-

from readers.data_reader import Reader
from vectorizers.bert_vectorizer import BERTVectorizer
from models.bert_nlu_model import BertNLUModel

import argparse
from sklearn.preprocessing import LabelEncoder
import numpy as np
import os
import pickle
import tensorflow as tf
from tensorflow import keras


# read command-line parameters
parser = argparse.ArgumentParser('Training the BERT NLU model')
parser.add_argument('--train', '-t', help = 'Path to training data', type = str, required = True)
parser.add_argument('--val', '-v', help = 'Path to validation data', type = str, default = "", required = False)
parser.add_argument('--save', '-s', help = 'Folder path to save the trained model', type = str, required = True)
parser.add_argument('--epochs', '-e', help = 'Number of epochs', type = int, default = 5, required = False)
parser.add_argument('--batch', '-bs', help = 'Batch size', type = int, default = 64, required = False)
parser.add_argument('--type', '-tp', help = 'bert   or    albert', type = str, default = 'bert', required = False)
parser.add_argument('--model', '-mo', help = 'load model', type = str, default = "", required = False)


VALID_TYPES = ['bert', 'albert']

args = parser.parse_args()
train_data_folder_path = args.train
val_data_folder_path = args.val
save_folder_path = args.save
epochs = args.epochs
batch_size = args.batch
type_ = args.type
model_path = args.model

# # this line is to disable gpu
# os.environ["CUDA_VISIBLE_DEVICES"]="-1"

tf.compat.v1.random.set_random_seed(7)

config = tf.ConfigProto(intra_op_parallelism_threads=8, 
                        inter_op_parallelism_threads=0,
                        allow_soft_placement=True,
                        device_count = {'CPU': 8})
sess = tf.compat.v1.Session(config=config)

if type_ == 'bert':
    bert_model_hub_path = "./bert-module" # to use KorBert by Etri
    is_bert = True
elif type_ == 'albert':
    bert_model_hub_path = 'https://tfhub.dev/google/albert_base/1'
    is_bert = False
else:
    raise ValueError('type must be one of these values: %s' % str(VALID_TYPES))

#이 부분을 고쳐서 Database를 이용해서 데이터를 읽어올 수 있음
print('read data ...')
train_text_arr, train_intents = Reader.read(train_data_folder_path)

print('train_text_arr[0:2] :', train_text_arr[0:2])
print('train_intents[0:2] :', train_intents[0:2])

print('vectorize data ...')
bert_vectorizer = BERTVectorizer(is_bert, bert_model_hub_path) 
# now bert model hub path exists --> already tokenized dataset
# bert vectorizer MUST NOT tokenize input !!!

print('bert vectorizer started ...') #valid pos removed
train_input_ids, train_input_mask, train_segment_ids = bert_vectorizer.transform(train_text_arr)


print('encode labels ...')
intents_label_encoder = LabelEncoder()
train_intents = intents_label_encoder.fit_transform(train_intents).astype(np.int32)
intents_num = len(intents_label_encoder.classes_)
print('intents num :', intents_num)

if model_path == "":
    model = BertNLUModel(intents_num, bert_model_hub_path, sess, num_bert_fine_tune_layers=10, is_bert=is_bert)
else:
    model = BertNLUModel.load(load_folder_path, sess)

print('train input shape :', train_input_ids.shape, train_input_ids[0:2])
print('train_input_mask :', train_input_mask.shape, train_input_mask[0:2])
print('train_segment_ids :', train_segment_ids.shape, train_segment_ids[0:2])
print('train_intents :', train_intents.shape, train_intents[0:2])

if not os.path.exists(save_folder_path):
    os.makedirs(save_folder_path)
    print('Folder `%s` created' % save_folder_path)

checkpoint_cb = keras.callbacks.ModelCheckpoint(save_folder_path+"/my_yogiyo_model.h5", save_best_only=True)
early_stopping_cb = keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True)

if val_data_folder_path:
    print('preparing validation data')
    val_text_arr, val_intents = Reader.read(val_data_folder_path)
    val_input_ids, val_input_mask, val_segment_ids = bert_vectorizer.transform(val_text_arr)
    val_intents = intents_label_encoder.transform(val_intents).astype(np.int32)
    
    print('training model ...')
    model.fit([train_input_ids, train_input_mask, train_segment_ids], train_intents,
        validation_data=([val_input_ids, val_input_mask, val_segment_ids], val_intents),
        epochs=epochs, batch_size=batch_size, callbacks=[checkpoint_cb, early_stopping_cb])    
else:
    print('training model ...')
    model.fit([train_input_ids, train_input_mask, train_segment_ids], train_intents,
        validation_data=None, 
        epochs=epochs, batch_size=batch_size, callbacks=[checkpoint_cb, early_stopping_cb])    

### saving
print('Saving ..')
model.save(save_folder_path)
with open(os.path.join(save_folder_path, 'intents_label_encoder.pkl'), 'wb') as handle:
    pickle.dump(intents_label_encoder, handle, protocol=pickle.HIGHEST_PROTOCOL)


tf.compat.v1.reset_default_graph()
