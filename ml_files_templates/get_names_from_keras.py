import sys
import inspect
import os
import pkgutil

import tensorflow.keras.applications
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.applications.resnet50 import ResNet50



# all info from tf.keras doc
# https://www.tensorflow.org/api_docs/python/tf/keras/applications

# get modules like tensorflow.keras.applications.vgg16
pkgpath = os.path.dirname(tensorflow.keras.applications.__file__)
modules = [name for _, name, _ in pkgutil.iter_modules([pkgpath])]
print(modules)



# print functions for vgg16 module
functions = [m[0] for m in inspect.getmembers(tensorflow.keras.applications.vgg16, inspect.isfunction)]
print(functions)

# the same for resnet50
functions = [m[0] for m in inspect.getmembers(tensorflow.keras.applications.resnet50 , inspect.isfunction)]
print(functions)

# get everything from tf.keras.applications
print(dir(tensorflow.keras.applications))

# get parameters/attributes for VGG16
attributes = inspect.signature(VGG16)
print(attributes)