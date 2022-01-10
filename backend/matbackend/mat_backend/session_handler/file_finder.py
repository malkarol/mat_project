import os

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

        # others
        'local learning':'/common/local_learning.py',
        'local_learning_b_and_w': '/common/local_learning_black_and_white.py',
        'preparation':'/common/preparation.py',

    }[x].get(x, 'File not found')    # message will be returned default if x is not found

def get_class_name(x):
    return {
        # models
        'CNN': 'SimpleCNN',
        'VGG': 'VGGOneBlock'
    }[x].get(x, 'Class not found')    # message will be returned default if x is not found