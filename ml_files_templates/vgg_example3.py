# source : https://www.learndatasci.com/tutorials/hands-on-transfer-learning-keras/
#import required libraries - we do need the models, flatten, dense, input layers
import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Input, Lambda, Dense, Flatten, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from torch import tensor
import tensorflow as tf

# Path for train, validation and test datasets
train_path = '/Users/michal/Desktop/cifar10/dataset1/'
valid_path = '/Users/michal/Desktop/cifar10/dataset1/'
test_path = '/Users/michal/Desktop/cifar10/test/'

IMAGE_SIZE = [224, 224] #Default image size for VGG16

folders = glob('/Users/michal/Desktop/cifar10/dataset1/*') #Get number of classes


# ImageDataGenerator can help perform augumentation on existing images. This way, we get more diverse train set.
train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.2, zoom_range = 0.2, validation_split=0.1, horizontal_flip = True)
# validation_datagen = ImageDataGenerator(rescale = 1./255)
test_datagen = ImageDataGenerator(rescale = 1./255)

#Through flow_from_directory - we create an array of images that can be used for training.
training_set = train_datagen.flow_from_directory(train_path,
                                                 target_size = (224, 224),
                                                 batch_size = 64,
                                                 subset="training",
                                                 class_mode = 'categorical')

validation_set = train_datagen.flow_from_directory(valid_path,
                                                 target_size = (224, 224),
                                                 batch_size = 64,
                                                 subset="validation",
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory(test_path,
                                            target_size = (224, 224),
                                            batch_size = 32,
                                            class_mode = 'categorical')

# training_set  = tf.image.resize(training_set , (224, 224))
# validation_set = tf.image.resize(validation_set, (224, 224))
# test_set = tf.image.resize(test_set, (224, 224))

# Create a VGG16 model, and removing the last layer that is classifying 1000 images. This will be replaced with images classes we have.
vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False) #Training with Imagenet weights

# Use this line for VGG19 network. Create a VGG19 model, and removing the last layer that is classifying 1000 images. This will be replaced with images classes we have.
#vgg = VGG19(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

# This sets the base that the layers are not trainable. If we'd want to train the layers with custom data, these two lines can be ommitted.
for layer in vgg.layers:
  layer.trainable = False


x = Flatten()(vgg.output) #Output obtained on vgg16 is now flattened.
x = Dense(4096, activation='relu')(x)
x = Dense(1072, activation='relu')(x)
x = Dropout(0.2)(x)
prediction = Dense(len(folders), activation='softmax')(x) # We have 5 classes, and so, the prediction is being done on len(folders) - 5 classes

#Creating model object
model = Model(inputs=vgg.input, outputs=prediction)

model.summary()


#Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(training_set, validation_data=validation_set, epochs=5, batch_size=32)


# loss
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.legend()
plt.show()
plt.savefig('LossVal_loss')

# accuracies
plt.plot(history.history['accuracy'], label='train acc')
plt.plot(history.history['val_accuracy'], label='val acc')
plt.legend()
plt.show()
plt.savefig('AccVal_acc')