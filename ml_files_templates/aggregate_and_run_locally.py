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

#declear path to your mnist data folder
img_path = '/Users/michal/Documents/trainingSet/'

#get the path list using the path object
image_paths = list(paths.list_images(img_path))
#apply our function
image_list, label_list = load(image_paths, verbose=10000)

#binarize the labels
lb = LabelBinarizer()
label_list = lb.fit_transform(label_list)

#split data into training and test set
X_train, X_test, y_train, y_test = train_test_split(image_list,
                                                    label_list,
                                                    test_size=0.1,
                                                    random_state=42)

#initialize global model
smlp_global = SimpleMLP()
global_model = smlp_global.build(784, 10)
scaled_local_weight_list =list()
client_names = ['michal','karol','jan']
#create optimizer
lr = 0.01
loss='categorical_crossentropy'
metrics = ['accuracy']
optimizer = SGD(lr=lr,
                decay=lr / 1,
                momentum=0.9
               )

global_weights = global_model.get_weights()

    #loop through each client and create new local model
for client in client_names:
    smlp_local = SimpleMLP()
    local_model = smlp_local.build(784, 10)
    local_model.compile(loss=loss,
                      optimizer=optimizer,
                      metrics=metrics)

    #set local model weight to the weight of the global model
    # local_model.set_weights(global_weights)
    local_model.load_weights(f"session_1_user_{client}.h5")
    #scale the model weights and add to list
    # TO DO
    # zmienic 1 na local_count - liczbe danych uzytych przez klienta
    # zmienic 3 na global_count - liczbe danych uzytych przez wszystkich klientow
    scaling_factor = weight_scalling_factor(1, 3)
    scaled_weights = scale_model_weights(local_model.get_weights(), scaling_factor)
    scaled_local_weight_list.append(scaled_weights)
    # to not consume many resources on backend
    K.clear_session()


#to get the average over all the local model, we simply take the sum of the scaled weights
average_weights = sum_scaled_weights(scaled_local_weight_list)

#update global model
global_model.set_weights(average_weights)

test_batched = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(len(y_test))

#test global model and print out metrics after each communications round
for(X_test, Y_test) in test_batched:
    global_acc, global_loss = test_model(X_test, Y_test, global_model, 1)
