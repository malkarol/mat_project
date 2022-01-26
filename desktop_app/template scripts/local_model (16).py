#import pandas as pd
from glob import glob
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# data_path =''
# testpath = ''
# absolute_path=''
# number_of_classes = len(glob(data_path+'*'))
from tensorflow.keras.applications.vgg16 import VGG16

def define_model(input_shape,number_of_classes):
    base_model = VGG16(input_shape=input_shape + [3], weights='imagenet', include_top=False) #Training with Imagenet weights

    # This sets the base that the layers are not trainable. If we'd want to train the layers with custom data, these two lines can be ommitted.
    for layer in base_model.layers:
        layer.trainable = False
    x = Flatten()(base_model.output) #Output obtained on vgg16 is now flattened.
    prediction = Dense(number_of_classes, activation='softmax')(x) # We have 5 classes, and so, the prediction is being done on len(folders) - 5 classes
    #Creating model object
    model = Model(inputs=base_model.input, outputs=prediction)
    return model


number_of_epochs = 5
loss_function = "categorical_crossentropy"
learning_rate = 0.0001
momentum = 0.9
batch_size = 32
validation_split = 0.2
width_size = 64
height_size = 64
number_of_classes = 3
username = "mlem"
model_name = "VGG16"
load_data = "load_data"
federated_round = 2
input_shape = [64, 64]
session_id = 110
optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
def load_dataset(datapath,testpath):
    train_path = datapath
    valid_path = datapath
    test_path = testpath
    #Default image size for VGG16

    # ImageDataGenerator can help perform augumentation on existing images. This way, we get more diverse train set.
    train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.2, zoom_range = 0.2, validation_split=validation_split, horizontal_flip = True)
    test_datagen = ImageDataGenerator(rescale = 1./255)
    #Through flow_from_directory - we create an array of images that can be used for training.
    training_set = train_datagen.flow_from_directory(train_path,
                                                     target_size = tuple(input_shape),
                                                     batch_size = batch_size,
                                                     subset="training",
                                                     class_mode = 'categorical')

    validation_set = train_datagen.flow_from_directory(valid_path,
                                                     target_size = tuple(input_shape),
                                                     batch_size = batch_size,
                                                     subset="validation",
                                                     class_mode = 'categorical')

    test_set = test_datagen.flow_from_directory(test_path,
                                            target_size = tuple(input_shape),
                                            batch_size = batch_size,
                                            class_mode = 'categorical')

    return training_set, validation_set, test_set

def local_learning(token,datapath,testpath, absolute_path, global_weights_path):
    # load dataset
    print("Loading dataset...")
    training_set, validation_set, test_set = load_dataset(datapath, testpath)
    print("Dataset loaded successfully...")
    # define model
    model = define_model(input_shape, number_of_classes)
    # fit model
    model.compile(loss=loss_function, optimizer=optimizer, metrics=["accuracy"])

    if federated_round > 1:
        model.load_weights(global_weights_path)

    print("Datasets size (training/validation):")
    print(training_set.samples + validation_set.samples)
    # fit model
    model.fit(training_set, epochs=number_of_epochs, batch_size=batch_size, validation_data=validation_set)

    data_count =  training_set.samples + validation_set.samples
    weights_path = absolute_path +'/'+f'{username}_{data_count}.h5'
    print(weights_path)
    model.save_weights(weights_path)

    print("Calculating loss and accuracy")
    loss, accuracy = model.evaluate(test_set)
    print("Saving results...")
    with open(weights_path, 'rb') as f:
        r = requests.post('http://127.0.0.1:8000/api/v1/upload-local-model/',
        files={'model_weights': f}, data={'session_id': session_id, 'local_data_count': data_count,
         'accuracy': accuracy, 'loss': loss},headers={'Authorization': f'Token {token}'})
    print("Sent")



