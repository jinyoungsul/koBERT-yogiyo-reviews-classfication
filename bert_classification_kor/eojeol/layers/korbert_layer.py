# -*- coding: utf-8 -*-

import tensorflow as tf
import os
from tensorflow.keras import backend as K
import tensorflow_hub as hub
import json

class KorBertLayer(tf.keras.layers.Layer):
    def __init__(self, bert_path="./bert-module", n_tune_layers=10, 
                 pooling="cls", tune_embeddings=True, trainable=True, **kwargs):

        self.trainable = trainable
        self.n_tune_layers = n_tune_layers
        self.tune_embeddings = tune_embeddings
        self.pooling = pooling
        self.bert_path = bert_path
        self.output_size = 768

        self.var_per_encoder = 16
        if self.pooling not in ["cls", "mean", None]:
            raise NameError(
                f"Undefined pooling type (must be either 'cls', 'mean', or None, but is {self.pooling}"
            )

        super(KorBertLayer, self).__init__(**kwargs)
        print('init ok')

    def build(self, input_shape):

        self.bert = hub.Module(self.build_abspath(self.bert_path), 
                               trainable=self.trainable, name=f"{self.name}_module")

        # Remove unused layers
        trainable_vars = self.bert.variables
        if self.pooling == 'cls':
            trainable_vars = [var for var in trainable_vars if not "/cls/" in var.name]
            trainable_layers = ["pooler/dense"]

        elif self.pooling == 'mean':
            trainable_vars = [var for var in trainable_vars
                if not "/cls/" in var.name and not "/pooler/" in var.name
            ]
            trainable_layers = []
        else:
            raise NameError(
                f"Undefined pooling type (must be either first or mean, but is {self.pooling}"
            )

        # append word_embedding to trainable_layers
        trainable_layers.append('bert/embeddings/word_embeddings:0')

        # Select how many layers to fine tune
        for i in range(self.n_tune_layers):
            trainable_layers.append(f"encoder/layer_{str(11 - i)}")

        # Update trainable vars to contain only the specified layers
        trainable_vars = [
            var
            for var in trainable_vars
            if any([l in var.name for l in trainable_layers])
        ]

        # Add to trainable weights
        for var in trainable_vars:
            self._trainable_weights.append(var)

        for var in self.bert.variables:
            if var not in self._trainable_weights:
                self._non_trainable_weights.append(var)

        super(KorBertLayer, self).build(input_shape)



    def build_abspath(self, path):
        if path.startswith("https://") or path.startswith("gs://"):
          return path
        else:
          return os.path.abspath(path)

    def call(self, inputs):
        inputs = [K.cast(x, dtype="int32") for x in inputs]
        input_ids, input_mask, segment_ids= inputs
        bert_inputs = dict(
            input_ids=input_ids, input_mask=input_mask, segment_ids=segment_ids
        )
        result = self.bert(inputs=bert_inputs, signature='tokens', as_dict=True)

        print('call ok')
        return result['pooled_output']
    
    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[1], self.output_size)


    def get_config(self):
        config = super().get_config().copy()
        config.update({
            'n_tune_layers': self.n_tune_layers,
            'trainable': self.trainable,
            'output_size': self.output_size,
            'pooling': self.pooling,
            'bert_path': self.bert_path,
        })
        return config
