from ml_handler.aggregate_utils import *
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
import session_handler.file_finder as ff
class Aggregator():
    def __init__(self, class_name, input_shape, num_classes):
        self.class_name = ff.get_class_name(class_name)
        self.input_shape = input_shape
        self.num_classes = num_classes

    def initialize_global_weights(self, parameters):
        '''Initializes global weight'''
        #initialize global model
        global_model = eval(self.class_name+f"({self.num_classes},{self.input_shape})")
        print(global_model)
        global_model.compile(loss=parameters["loss_function"],
                      optimizer=parameters["optimizer"],
                      metrics=["accuracy"])

        weights = global_model.get_weights()
        # print(weights)
        list_of_arrays=bytes()
        for array in weights:
             list_of_arrays = list_of_arrays + array.tobytes()
        return  list_of_arrays

        # for MNIST example dataset: client_names = ['michal','karol','jan']
        #                            client_counts = [4200,4200,4200]
    def get_file_names_and_counts(self,client_names, clients_counts):
        self.client_names = client_names
        self.local_counts = clients_counts
        self.sum_local_counts = sum(clients_counts)


    def aggregate(self, parameters, client_names, global_weights):
            # iterator for local_counts
            i = 0
            scaled_local_weight_list =list()
            # loop through each client and create new local model
            for client in client_names:
                local_model = eval(self.class_name+f"({self.input_shape}, {self.num_classes})")
                local_model.compile(loss=parameters["loss"],
                          optimizer=parameters["optimizer"],
                          metrics=parameters["metrics"])

                # set local model weight to the weight of the global model
                # local_model.set_weights(global_weights)
                local_model.set_weights(client)
                # scale the model weights and add to list
                # TO DO
                # zmienic 1 na local_count - liczbe danych uzytych przez klienta
                # zmienic 3 na global_count - liczbe danych uzytych przez wszystkich klientow
                scaling_factor = weight_scalling_factor(self.local_counts[i], self.sum_local_counts)
                scaled_weights = scale_model_weights(local_model.get_weights(), scaling_factor)
                scaled_local_weight_list.append(scaled_weights)
                i = i + 1
                # to not consume many resources on backend
                K.clear_session()
            # to get the average over all the local model, we simply take the sum of the scaled weights
            average_weights = sum_scaled_weights(scaled_local_weight_list)
            return average_weights
