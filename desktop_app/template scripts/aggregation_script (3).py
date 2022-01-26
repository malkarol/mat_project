
from glob import glob
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import tensorflow.keras.backend as K
import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


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

federated_round =2
number_of_epochs = 20
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
client_names = ['John_Fisher', 'Rachel_Mcbride', 'mlem']
clients_counts = [3000, 3000, 3000]
aggregate_locally = "aggregate_locally"
input_shape = [64, 64]
session_id = 110
optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
def load_dataset(testpath):

    test_path = testpath
    #Default image size for VGG16

    # ImageDataGenerator can help perform augumentation on existing images. This way, we get more diverse train set.
    test_datagen = ImageDataGenerator(rescale = 1./255)
    #Through flow_from_directory - we create an array of images that can be used for training.


    test_set = test_datagen.flow_from_directory(test_path,
                                            target_size = tuple(input_shape),
                                            batch_size = batch_size,
                                            class_mode = 'categorical')

    return test_set


sum_local_counts = sum(clients_counts)
# source:
# https://towardsdatascience.com/federated-learning-a-step-by-step-implementation-in-tensorflow-aac568283399


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

def aggregate(token,testpath,absolute_path,local_weights_path):
    # iterator for local_counts
    i = 0
    scaled_local_weight_list =list()
    # loop through each client and create new local model
    print("Performing aggregation...")
    for client in client_names:
        model = define_model(input_shape,number_of_classes)
        # fit model
        model.compile(loss=loss_function, optimizer=optimizer, metrics=["accuracy"])
        model.load_weights(local_weights_path+'/' + f'{client}_{clients_counts[i]}.h5')
        # scale the model weights and add to list
        # TO DO
        # zmienic 1 na local_count - liczbe danych uzytych przez klienta
        # zmienic 3 na global_count - liczbe danych uzytych przez wszystkich klientow
        scaling_factor = weight_scalling_factor(clients_counts[i], sum_local_counts)
        scaled_weights = scale_model_weights(model.get_weights(), scaling_factor)
        scaled_local_weight_list.append(scaled_weights)
        i = i + 1
        # to not consume many resources on backend
        K.clear_session()
    # to get the average over all the local model, we simply take the sum of the scaled weights
    print("Calculating common weights...")
    average_weights = sum_scaled_weights(scaled_local_weight_list)
    global_model = define_model(input_shape,number_of_classes)
    global_model.compile(loss=loss_function, optimizer=optimizer, metrics=["accuracy"])
    global_model.set_weights(average_weights)
    print("Calculating aggregated model accuracy and loss...")
    loss, accuracy = global_model.evaluate(load_dataset(testpath))
    print(loss, accuracy)
    global_model.save_weights(absolute_path+'/'+"global_weights.h5")
    print("Sending aggregated weights to the server...")
    with open(absolute_path+'/'+"global_weights.h5", 'rb') as f:
        r = requests.post('http://127.0.0.1:8000/api/v1/upload-global-weights/',
        files={'model_weights': f}, data={'session_id': session_id, 'loss': loss,
        'accuracy': accuracy},headers={'Authorization': f'Token {token}'})
    print("Sent")
