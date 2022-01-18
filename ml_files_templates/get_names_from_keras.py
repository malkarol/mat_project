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
# pkgpath = os.path.dirname(tensorflow.keras.applications.__file__)
# modules = [name for _, name, _ in pkgutil.iter_modules([pkgpath])]
# print(modules)



# # print functions for vgg16 module
# functions = [m[0] for m in inspect.getmembers(tensorflow.keras.applications.vgg16, inspect.isfunction)]
# print(functions)

# the same for resnet50


# modules = [m[0] for m in inspect.getmembers(tensorflow.keras.applications , inspect.ismodule)]
# module_func_tuples = []
# for module in modules:
#     if(module not in ['_sys','keras']):
#        functions = [(m[0],"tensorflow.keras.applications."+module) for m in inspect.getmembers(eval("tensorflow.keras.applications."+module), inspect.isfunction)]
#        module_func_tuples.append(functions[0])
# myresult = ()
# for elem in module_func_tuples:
#     if 'VGG16' == elem[0]:
#         myresult = elem
# print(myresult[1]+'.'+myresult[0]+' import '+myresult[0])
# # get everything from tf.keras.applications
# print(dir(tensorflow.keras.applications))

# # get parameters/attributes for VGG16
# attributes = inspect.signature(VGG16)
# print(attributes)

print(len(10))