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

def load(paths, verbose=-1):
    '''expects images for each class in seperate dir,
    e.g all digits in 0 class in the directory named 0 '''
    data = list()
    labels = list()
    # loop over the input images
    for (i, imgpath) in enumerate(paths):
        # load the image and extract the class labels
        im_gray = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE)
        image = np.array(im_gray).flatten()
        label = imgpath.split(os.path.sep)[-2]
        # scale the image to [0, 1] and add to list
        data.append(image/255)
        labels.append(label)
        # show an update every `verbose` images
        # print info after verbose number of images is going to be processed
        # e.g. if verbose = 100 print: [INFO] processed 100/42000
        #                              [INFO] processed 200/42000
        #                              [INFO] processed 300/42000
        if verbose > 0 and i > 0 and (i + 1) % verbose == 0:
            print("[INFO] processed {}/{}".format(i + 1, len(paths)))
    # return a tuple of the data and labels
    return data, labels

def test_model(X_test, Y_test,  model, comm_round):
    cce = tf.keras.losses.CategoricalCrossentropy(from_logits=True)
    #logits = model.predict(X_test, batch_size=100)
    logits = model.predict(X_test)
    loss = cce(Y_test, logits)
    acc = accuracy_score(tf.argmax(logits, axis=1), tf.argmax(Y_test, axis=1))
    print('comm_round: {} | global_acc: {:.3%} | global_loss: {}'.format(comm_round, acc, loss))
    return acc, loss

class SimpleMLP:
    @staticmethod
    def build(shape, classes):
        model = Sequential()
        model.add(Dense(200, input_shape=(shape,)))
        model.add(Activation("relu"))
        model.add(Dense(200))
        model.add(Activation("relu"))
        model.add(Dense(classes))
        model.add(Activation("softmax"))
        return model

def read_list_from_file(filename):
    file = open(filename, "r")
    file_lines = file.read()
    list_of_lines = file_lines.split("\n")
    return list_of_lines

def write_list_to_file(filename,list_to_write):
    with open(filename, "w") as file:
        for element in list_to_write:
            file.write(element)

img_path = '/Users/michal/Documents/trainingSet/'
client_name = 'user_karol'

#get the path list using the path object
# gets paths to every image
image_paths = list(paths.list_images(img_path))

image_list, label_list = load(image_paths, verbose=10000)






#binarize the labels
lb = LabelBinarizer()
label_list = lb.fit_transform(label_list)

#split data into training and test set
X_train, X_test, y_train, y_test = train_test_split(image_list,
                                                    label_list,
                                                    test_size=0.1,
                                                    random_state=42)

local_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train)).shuffle(len(y_train)).batch(320)
smlp_local = SimpleMLP()
local_model = smlp_local.build(784, 10)

learning_rate = 0.01
comms_round = 1
loss='categorical_crossentropy'
metrics = ['accuracy']
optimizer = SGD(learning_rate=learning_rate,
                decay=learning_rate / comms_round,
                momentum=0.9
               )

local_model.compile(loss=loss,
              optimizer=optimizer,
              metrics=metrics)

local_model.load_weights('session_1_global_weights.h5')
local_model.fit(local_dataset, epochs=1, verbose=0)
local_model.save_weights(f'session_1_{client_name}.h5')
test_batched = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(len(y_test))

for(X_test, Y_test) in test_batched:
        print(len(Y_test))
        local_model_acc, local_model_loss = test_model(X_test, Y_test, local_model, 1)

