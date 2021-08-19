# -*- coding: utf-8 -*-

import tensorflow as tf
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.layers import Input, Dense, Multiply, TimeDistributed
from models.base_nlu_model import BaseNLUModel
from layers.korbert_layer import KorBertLayer
import numpy as np
import os
import json


class BertNLUModel(BaseNLUModel):

    def __init__(self, intents_num, bert_hub_path, sess, num_bert_fine_tune_layers=10,
                 is_bert=True, is_training=True):
        self.intents_num = intents_num
        self.bert_hub_path = bert_hub_path
        self.num_bert_fine_tune_layers = num_bert_fine_tune_layers
        self.is_bert = is_bert
        self.is_training = is_training
 
        self.model_params = {
                'intents_num': intents_num,
                'bert_hub_path': bert_hub_path,
                'num_bert_fine_tune_layers': num_bert_fine_tune_layers,
                'is_bert': is_bert
                }
        
        self.build_model()
        self.compile_model()
        
        self.initialize_vars(sess)
        
        
    def compile_model(self):
        
        optimizer = tf.keras.optimizers.Adam(lr=5e-5)#0.001)

        losses = {
        	'intent_classifier': 'sparse_categorical_crossentropy',
        }

        metrics = {'intent_classifier': 'acc'}

        self.model.compile(optimizer=optimizer, loss=losses, metrics=metrics)
        self.model.summary()
        

    def build_model(self):
        in_id = Input(shape=(None,), dtype=tf.int32, name='input_ids')
        in_mask = Input(shape=(None,), dtype=tf.int32, name='input_masks')
        in_segment = Input(shape=(None,), dtype=tf.int32, name='segment_ids')

        bert_inputs = [in_id, in_mask, in_segment] # tf.keras layers
        

        print('bert inputs :', bert_inputs)

        bert_pooled_output = KorBertLayer(
            n_tune_layers=self.num_bert_fine_tune_layers,
            pooling='mean', name='KorBertLayer')(bert_inputs)
    
        
        # fine-tuning layer
        intents_fc = Dense(self.intents_num, activation='softmax', name='intent_classifier')(bert_pooled_output)
        

        self.model =  Model(inputs=bert_inputs, outputs=intents_fc)

        
    def fit(self, X, Y, validation_data=None, epochs=5, batch_size=64, callbacks=None):
        """
        X: batch of [input_ids, input_mask, segment_ids, valid_positions]
        """

        X = (X[0], X[1], X[2])
        if validation_data is not None:
            X_val, Y_val = validation_data
            validation_data = ((X_val[0], X_val[1], X_val[2]), Y_val)

        history = self.model.fit(X, Y, validation_data=validation_data, 
                                 epochs=epochs, batch_size=batch_size, callbacks=callbacks)
        print(history.history)
        self.visualize_metric(history.history, 'loss')
        self.visualize_metric(history.history, 'acc')
        
        
    def initialize_vars(self, sess):
        sess.run(tf.compat.v1.local_variables_initializer())
        sess.run(tf.compat.v1.global_variables_initializer())
        K.set_session(sess)
        
        
    def predict_intent(self, x, intent_vectorizer, remove_start_end=True):

        # x = (x[0], x[1], x[2])
        y_intent = self.predict(x)

#        print('y_intent :', y_intent)

        first_intents_score = np.array([np.max(y_intent[i]) for i in range(y_intent.shape[0])])
        first_intents = np.array([intent_vectorizer.inverse_transform([np.argmax(y_intent[i])])[0] for i in range(y_intent.shape[0])])
        second_intents_score = np.array([np.sort(y_intent[i])[-2] for i in range(y_intent.shape[0])])
        second_intents = np.array([intent_vectorizer.inverse_transform([np.argsort(y_intent[i])[-2]])[0] for i in range(y_intent.shape[0])])
        
        return first_intents, first_intents_score, second_intents, second_intents_score

    def save(self, model_path):
        with open(os.path.join(model_path, 'params.json'), 'w') as json_file:
            json.dump(self.model_params, json_file)
        self.model.save(os.path.join(model_path, 'bert_nlu_model.h5'))
        
    def load(load_folder_path, sess): # load for inference or model evaluation
        with open(os.path.join(load_folder_path, 'params.json'), 'r') as json_file:
            model_params = json.load(json_file)
            
        intents_num = model_params['intents_num']
        bert_hub_path = model_params['bert_hub_path']
        num_bert_fine_tune_layers = model_params['num_bert_fine_tune_layers']
        is_bert = model_params['is_bert']
            
        new_model = BertNLUModel(intents_num, bert_hub_path, sess, num_bert_fine_tune_layers, is_bert, is_training=False)
        new_model.model.load_weights(os.path.join(load_folder_path,'bert_nlu_model.h5'))
        return new_model
