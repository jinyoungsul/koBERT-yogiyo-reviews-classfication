# -*- coding: utf-8 -*-

from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np


class BaseNLUModel:
    
    def __init__(self):
        self.model = None
    
    def visualize_metric(self, history_dic, metric_name):
        plt.plot(history_dic[metric_name])
        legend = ['train']
        if 'val_' + metric_name in history_dic:
            plt.plot(history_dic['val_' + metric_name])
            legend.append('test')
        plt.title('model ' + metric_name)
        plt.ylabel(metric_name)
        plt.xlabel('epoch')
        plt.legend(legend, loc='upper left')
        plt.savefig('train_log.png')
        
    def predict(self, x):
        return self.model.predict(x)
    
    def save(self, model_path):
        self.model.save(model_path)
        
    def load(model_path, custom_objects=None):
        new_model = BaseNLUModel()
        new_model.model = load_model(model_path, custom_objects=custom_objects)
        return new_model
    
    def predict_intent(self, x, intents_label_encoder):
        if len(x.shape) == 1:
            x = x[np.newaxis, ...]
        y = self.predict(x)
        intents = np.array([intents_label_encoder.inverse_transform([np.argmax(y[i])])[0] for i in range(y.shape[0])])
        return intents, slots
