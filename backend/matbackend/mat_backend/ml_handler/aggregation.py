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
import tensorflow as tf
from sklearn.metrics import accuracy_score
import io
import json
import tensorflow as tf
from session_handler.models import SessionResult,Session, Participant
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras import backend as K
import session_handler.file_finder as ff
from tensorflow.keras.models import Model
import ssl
from io import BytesIO
import zipfile, shutil
from django.core.files.base import ContentFile
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.vgg16 import *
from tensorflow.keras.applications.vgg19 import *
from tensorflow.keras.applications.resnet50 import *
from tensorflow.keras.applications.resnet_v2 import *
from tensorflow.keras.applications.mobilenet_v2 import *
from tensorflow.keras.applications.mobilenet import *
from tensorflow.keras.applications.inception_v3 import *
from tensorflow.keras.applications.inception_resnet_v2 import *
from tensorflow.keras.applications.xception import *
from tensorflow.keras.applications.densenet import *
from tensorflow.keras.applications.efficientnet import *
ssl._create_default_https_context = ssl._create_unverified_context


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
        session = Session.objects.get(pk=self.session)
        file_path = f'/sessions/session_Id_{self.session}/local_weights/federated_round_{session.federated_round}/{client}_{count}.h5'
        storage_file = storage.open(file_path , 'rb')
        return  storage_file.read()



    def aggregate(self, parameters):
            # iterator for local_counts
            i = 0
            scaled_local_weight_list =list()
            client_counts = [int(x) for x in self.parameters['clients_counts']]
            optimizer = eval(parameters["optimizer"])
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
                          optimizer=optimizer,
                          metrics=["accuracy"])
            global_model.set_weights(average_weights)

            test_path = f'/sessions/session_Id_{self.parameters["session_id"]}/TEST_SET.zip'

            calculate_global_model_accuracy(self, global_model, test_path)

            global_model.save_weights("tmp_aver_weight.h5")
            return "tmp_aver_weight.h5"

class PretrainedAggregator(Aggregator):
    def __init__(self,input_shape, num_classes, parameters, session_id):
        Aggregator.__init__(self,input_shape, num_classes, parameters, session_id)

    def aggregate(self, parameters):
        # iterator for local_counts
            i = 0
            scaled_local_weight_list =list()
            client_counts = [int(x) for x in self.parameters['clients_counts']]

            sum_local_counts = sum(client_counts)
            # loop through each client and create new local model

            for client in self.parameters['client_names']:

                base_model = eval( self.parameters['model_name'])(input_shape=self.input_shape + [3], weights='imagenet', include_top=False) #Training with Imagenet weights

                # This sets the base that the layers are not trainable. If we'd want to train the layers with custom data, these two lines can be ommitted.
                for layer in base_model.layers:
                    layer.trainable = False
                x = Flatten()(base_model.output) #Output obtained on vgg16 is now flattened.
                prediction = Dense(self.num_classes, activation='softmax')(x) # We have 5 classes, and so, the prediction is being done on len(folders) - 5 classes
                #Creating model object
                model = Model(inputs=base_model.input, outputs=prediction)
                local_model = model
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
                scaling_factor = weight_scalling_factor(client_counts[i], sum_local_counts)
                scaled_weights = scale_model_weights(local_model.get_weights(), scaling_factor)
                scaled_local_weight_list.append(scaled_weights)
                i = i + 1
                print(i)
                # to not consume many resources on backend
                K.clear_session()
            # to get the average over all the local model, we simply take the sum of the scaled weights
            print("before sum")
            average_weights = sum_scaled_weights(scaled_local_weight_list)
            base_model = eval( self.parameters['model_name'])(input_shape=self.input_shape + [3], weights='imagenet', include_top=False) #Training with Imagenet weights

                # This sets the base that the layers are not trainable. If we'd want to train the layers with custom data, these two lines can be ommitted.
            for layer in base_model.layers:
                layer.trainable = False
            x = Flatten()(base_model.output) #Output obtained on vgg16 is now flattened.
            prediction = Dense(self.num_classes, activation='softmax')(x) # We have 5 classes, and so, the prediction is being done on len(folders) - 5 classes
            #Creating model object
            global_model = Model(inputs=base_model.input, outputs=prediction)
            local_model =  global_model
            local_model.compile(loss=parameters["loss_function"],
                      optimizer=eval(parameters["optimizer"]),
                      metrics=["accuracy"])
            global_model.set_weights(average_weights)

            test_path = f'/sessions/session_Id_{self.parameters["session_id"]}/TEST_SET.zip'

            calculate_global_model_accuracy(self, global_model, test_path)

            global_model.save_weights("tmp_aver_weight.h5")


            print("done")
            return "tmp_aver_weight.h5"




    