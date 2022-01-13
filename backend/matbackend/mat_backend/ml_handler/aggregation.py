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
import io
import json
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
from storages.backends.gcloud import GoogleCloudStorage
storage = GoogleCloudStorage()

def SimpleCNN(num_of_classes,input_shape):
    model = Sequential()
    model.add(Input(shape=input_shape))
    model.add(Conv2D(32, kernel_size=(3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dropout(0.5))
    model.add(Dense(num_of_classes, activation="softmax"))
    return model
class Aggregator():
    def __init__(self,input_shape, num_classes, parameters, session_id):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.parameters = parameters
        self.session = session_id

    def initialize_global_weights(self, parameters):
        '''Initializes global weight'''
        #initialize global model
        global_model = eval(self.parameters['model_name']+f"({self.num_classes},{self.input_shape})")
        print(self.parameters['model_name'])
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
    def getClientsWeightsFromJson(self,client,count):
        file_path = f'/sessions/session_Id_{self.session}/local_weights/{client}_{count}.h5'
        storage_file = storage.open(file_path , 'rb')
        return  storage_file.read()



    def aggregate(self, parameters):
            # iterator for local_counts
            i = 0
            scaled_local_weight_list =list()
            client_counts = [int(x) for x in self.parameters['clients_counts']]

            sum_local_counts = sum(client_counts)
            # loop through each client and create new local model
            for client in self.parameters['client_names']:
                local_model = eval( self.parameters['model_name']+f"({self.num_classes},{self.input_shape})")
                local_model.compile(loss=parameters["loss_function"],
                          optimizer=eval(parameters["optimizer"]),
                          metrics=["accuracy"])

                # set local model weight to the weight of the global model
                # local_model.set_weights(global_weights)
                content = self.getClientsWeightsFromJson(client,client_counts[i])
                with open("tmp_weight.h5", 'wb') as f:
                    f.write(content)

                local_model.load_weights('tmp_weight.h5')
                os.remove("tmp_weight.h5")
                # scale the model weights and add to list
                # TO DO
                # zmienic 1 na local_count - liczbe danych uzytych przez klienta
                # zmienic 3 na global_count - liczbe danych uzytych przez wszystkich klientow
                scaling_factor = weight_scalling_factor(client_counts[i], sum_local_counts)
                scaled_weights = scale_model_weights(local_model.get_weights(), scaling_factor)
                scaled_local_weight_list.append(scaled_weights)
                i = i + 1
                # to not consume many resources on backend
                K.clear_session()
            # to get the average over all the local model, we simply take the sum of the scaled weights
            average_weights = sum_scaled_weights(scaled_local_weight_list)
            global_model = eval( self.parameters['model_name']+f"({self.num_classes},{self.input_shape})")
            global_model.compile(loss=parameters["loss_function"],
                          optimizer=eval(parameters["optimizer"]),
                          metrics=["accuracy"])
            global_model.set_weights(average_weights)
            global_model.save_weights("tmp_aver_weight.h5")
            return "tmp_aver_weight.h5"
