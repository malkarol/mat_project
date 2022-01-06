from aggregate_utils import *
import numpy as np
import random
import cv2
import os
from imutils import paths
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score


import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras import backend as K


class SimpleMLPAggregator():
    # for MNIST example dataset: 784     10
    def initialize_global_model(self,size, classes):
        '''Initializes global model'''
        #initialize global model
        self.smlp_global = SimpleMLP()
        self.global_model = self.smlp_global.build(size, classes)
        self.scaled_local_weight_list =list()

    # for MNIST example dataset: client_names = ['michal','karol','jan']
    def get_file_names(self,client_names):
        self.client_names = client_names

    # for MNIST example dataset: lr = 0.01
    #                            loss='categorical_crossentropy'
    #                            metrics = ['accuracy']
    def initialize_optimizer(self,lr, loss, metrics, nr_of_learning_rounds = 1):
        #create optimizer
        self.lr = lr
        self.loss = loss
        self.metrics = metrics
        self.optimizer = SGD(learning_rate=lr,
                        decay=lr / nr_of_learning_rounds,
                        momentum=0.9
                       )

    def aggregate(self):
            #loop through each client and create new local model
        for client in self.client_names:
            smlp_local = SimpleMLP()
            local_model = smlp_local.build(784, 10)
            local_model.compile(loss=self.loss,
                      optimizer=self.optimizer,
                      metrics=self.metrics)

            #set local model weight to the weight of the global model
            # local_model.set_weights(global_weights)
            local_model.load_weights(f"ml_files_templates/session_1_user_{client}.h5")
            #scale the model weights and add to list
            # TO DO
            # zmienic 1 na local_count - liczbe danych uzytych przez klienta
            # zmienic 3 na global_count - liczbe danych uzytych przez wszystkich klientow
            scaling_factor = weight_scalling_factor(1, 3)
            scaled_weights = scale_model_weights(local_model.get_weights(), scaling_factor)
            self.scaled_local_weight_list.append(scaled_weights)
            # to not consume many resources on backend
            K.clear_session()
        #to get the average over all the local model, we simply take the sum of the scaled weights
        average_weights = sum_scaled_weights(self.scaled_local_weight_list)
        return average_weights

#TO DO
# save to google cloud storage as a .h5 file
if __name__ == '__main__':
    size = 784
    classes = 10
    lr = 0.01
    client_names = ['michal','karol','jan']
    loss='categorical_crossentropy'
    metrics = ['accuracy']
    aggregator = SimpleMLPAggregator()
    aggregator.initialize_global_model(size,classes)
    aggregator.get_file_names(client_names)
    aggregator.initialize_optimizer(lr, loss, metrics)
    weights = aggregator.aggregate()
#TO DO
# save to google cloud storage as a .h5 file