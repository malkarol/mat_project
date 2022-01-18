import os
import io
from zipfile import *
import inspect
import tensorflow
def get_file_path(x):
    return {
        # models
        'CNN': '/common/models/SimpleMNISTCNN.py',
        'VGG': '/common/models/VGG_one_block.py',
        'Xception': 'pretrained',
        'VGG19': 'pretrained',
        'VGG16': 'pretrained',
        'ResNet50V2': 'pretrained',
        'ResNet50': 'pretrained',
        'MobileNetV2': 'pretrained',
        'MobileNet': 'pretrained',
        'InceptionV3': 'pretrained',
        'InceptionResNetV2': 'pretrained',
        'EfficientNetB0': 'pretrained',
        'EfficientNetB1': 'pretrained',
        'EfficientNetB2': 'pretrained',
        'EfficientNetB3': 'pretrained',
        'DenseNet121': 'pretrained',
        'DenseNet169': 'pretrained',
        'DenseNet201': 'pretrained',

        # loads
        'CIFAR10_from_keras':'/common/loads/load_CIFAR10_from_keras.py',
        'MNIST_FROM_keras': '/common/loads/load_MNIST_from_keras.py',
        'load_data': '/common/load_data.py',



        # others
        'local_learning':'/common/local_learning.py',
        'local_learning_b_and_w': '/common/local_learning_black_and_white.py',
        'learning': '/common/learning.py',
        'preparation':'/common/preparation.py',
        'initialize_weights':'/common/initialize_weights.py',

        # aggregate
        'aggregate_locally':'/common/aggregate_locally.py'

    }.get(x,'pretrained')   # message will be returned default if x is not found

# simple models
def get_class_name(x):
    return {
        # models
        'CNN': 'SimpleCNN',
        'VGG': 'VGGOneBlock',


    }[x]    # message will be returned default if x is not found

def get_optimizer(x):
    return {
        # optimizers
        'SGD': 'SGD(learning_rate=0.01,decay= 0.01,momentum=0.9)',
    }[x]

def get_pretrained_model_line(x):
    return {

    }[x]

def get_pretrained_import_line(func):
    modules = [m[0] for m in inspect.getmembers(tensorflow.keras.applications , inspect.ismodule)]
    module_func_tuples = []
    for module in modules:
        if(module not in ['_sys','keras']):
           functions = [(m[0],"tensorflow.keras.applications."+module) for m in inspect.getmembers(eval("tensorflow.keras.applications."+module), inspect.isfunction)]
           module_func_tuples.append(functions[0])
    myresult = ()
    for elem in module_func_tuples:
        if func == elem[0]:
            myresult = elem
    return 'from '+myresult[1]+' import '+myresult[0]



def zipFiles(files):
        outfile = io.StringIO()  # io.BytesIO() for python 3
        with ZipFile(outfile, 'w') as zf:
            for n, f in enumerate(files):
                zf.writestr("{}.h5".format(n), f.getvalue())
        return outfile.getvalue()