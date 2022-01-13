import os
import io
from zipfile import *
def get_file_path(x):
    return {
        # models
        'CNN': '/common/models/SimpleMNISTCNN.py',
        'VGG': '/common/models/VGG_one_block.py',

        # loads
        'CIFAR10_from_keras':'/common/loads/load_CIFAR10_from_keras.py',
        'MNIST_FROM_keras': '/common/loads/load_MNIST_from_keras.py',
        'load_images': '/common/loads/load_images.py',
        'load_color_images': '/common/loads/load_color_images.py',
        'load_default': '/common/loads/load_images.py',
        'load_color_default': '/common/loads/load_color_images.py',

        # others
        'local_learning':'/common/local_learning.py',
        'local_learning_b_and_w': '/common/local_learning_black_and_white.py',

        'preparation':'/common/preparation.py',
        'initialize_weights':'/common/initialize_weights.py',

        # aggregate
        'aggregate_locally':'/common/aggregate_locally.py'

    }[x]   # message will be returned default if x is not found

def get_class_name(x):
    return {
        # models
        'CNN': 'SimpleCNN',
        'VGG': 'VGGOneBlock'
    }[x]    # message will be returned default if x is not found

def get_optimizer(x):
    return {
        # models
        'SGD': 'SGD(learning_rate=0.01,decay= 0.01,momentum=0.9)',
    }[x]

def zipFiles(files):
        outfile = io.StringIO()  # io.BytesIO() for python 3
        with ZipFile(outfile, 'w') as zf:
            for n, f in enumerate(files):
                zf.writestr("{}.h5".format(n), f.getvalue())
        return outfile.getvalue()