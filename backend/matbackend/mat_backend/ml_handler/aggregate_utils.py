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
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras import backend as K

# source: https://towardsdatascience.com/federated-learning-a-step-by-step-implementation-in-tensorflow-aac568283399
from io import BytesIO
from session_handler.models import SessionResult,Session, Participant
from storages.backends.gcloud import GoogleCloudStorage
import zipfile, shutil
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from django.core.files.base import ContentFile
import json
storage = GoogleCloudStorage()

def scale_model_weights(weight, scalar):
    '''function for scaling a models weights'''
    weight_final = []
    steps = len(weight)
    for i in range(steps):
        weight_final.append(scalar * weight[i])
    return weight_final

def sum_scaled_weights(scaled_weight_list):
    '''Return the sum of the listed scaled weights. The is equivalent to scaled avg of the weights'''
    avg_grad = list()
    #get the average grad accross all client gradients
    for grad_list_tuple in zip(*scaled_weight_list):
        layer_mean = tf.math.reduce_sum(grad_list_tuple, axis=0)
        avg_grad.append(layer_mean)

    return avg_grad

def weight_scalling_factor(local_count, global_count):
        return local_count/global_count
# source:
# https://keras.io/examples/vision/mnist_convnet/


def SimpleCNN(num_of_classes,input_shape):
    model = Sequential()
    model.add(Input(shape=input_shape+ [3]))
    model.add(Conv2D(32, kernel_size=(3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dropout(0.5))
    model.add(Dense(num_of_classes, activation="softmax"))
    return model

# source:
# https://machinelearningmastery.com/how-to-develop-a-cnn-from-scratch-for-cifar-10-photo-classification/
def VGGOneBlock(num_of_classes,input_shape):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same', input_shape=input_shape+ [3]))
    model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', padding='same'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu', kernel_initializer='he_uniform'))
    model.add(Dense(num_of_classes, activation='softmax'))
    return model


def unzip_dataset(self, testpath):
        storage_file = storage.open(testpath, 'rb')
        b = BytesIO(storage_file.read())
        with zipfile.ZipFile(b, 'r') as zip_ref:
            zip_ref.extractall(f'./user_files/session_Id_{self.parameters["session_id"]}/TESTSET/')
        return f'./user_files/session_Id_{self.parameters["session_id"]}/TESTSET/'

def load_dataset(self, testpath):
    test_path = unzip_dataset(self, testpath)
    #Default image size for VGG16
    # ImageDataGenerator can help perform augumentation on existing images. This way, we get more diverse train set.
    test_datagen = ImageDataGenerator(rescale = 1./255)
    #Through flow_from_directory - we create an array of images that can be used for training.
    test_set = test_datagen.flow_from_directory(test_path,
                                            target_size = tuple(self.input_shape),
                                            batch_size = int(self.parameters['batch_size']),
                                            class_mode = 'categorical')
    return test_set
def calculate_global_model_accuracy(self, global_model, testpath):
    loss, accuracy = global_model.evaluate(load_dataset(self, testpath))
    session = Session.objects.get(pk=self.parameters['session_id'])
    
    ses_result = SessionResult.objects.filter(session__session_id = self.parameters['session_id']).filter(federated_round = session.federated_round)[0]
    ses_result.finished = True
    ses_result.global_model_accuracy = accuracy
    ses_result.global_model_loss = loss
    ses_result.save()
    session.federated_round += 1
    session.save()
    newSessionResult = SessionResult.objects.create(session=session, federated_round = session.federated_round, finished=False)
    newSessionResult.save()
    dic = {'accuracies': [], 'losses': [], 'usernames': []}
    jsonn = json.dumps(dic)
    target_path = f'/sessions/session_Id_{session.session_id}/local_weights/federated_round_{session.federated_round}/round_stats.json'
    storage.save(target_path,ContentFile(bytes(jsonn, 'utf-8')))
    participants = Participant.objects.filter(session_id = session.session_id)
    for participant in participants:
        participant.is_model_uploaded = False
        participant.save()
    try:
        shutil.rmtree(f'./user_files/session_Id_{self.parameters["session_id"]}')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))