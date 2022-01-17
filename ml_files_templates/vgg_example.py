# https://towardsdatascience.com/transfer-learning-with-vgg16-and-keras-50ea161580b4
import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from imutils import paths
import cv2
import os

image_size = (28, 28)
batch_size = 32

def load_color_images(path,verbose=10000):
    path_lists = list(paths.list_images(path))
    data = list()
    labels = list()
    for (i, imgpath) in enumerate(path_lists):
        img = cv2.imread(imgpath)
        label = imgpath.split(os.path.sep)[-2]
        data.append(img)
        labels.append(label)
        if verbose > 0 and i > 0 and (i + 1) % verbose == 0:
            print(f"[LOG] Processed {i + 1}/{len(path_lists)}")
    return np.array(data),np.array(labels)

def load_dataset():
    # load dataset
    images_path = "/Users/michal/Downloads/CIFAR-10-images-master/train/"
    image_list, label_list = load_color_images(images_path)
    lb = LabelBinarizer()
    label_list = lb.fit_transform(label_list)
    trainX, testX, trainY, testY = train_test_split(image_list,
                                                    label_list,
                                                    test_size=0.1,
                                                    random_state=42)


    return trainX, testX, trainY, testY


# data(labels)
train_ds, test_ds, train_labels, test_labels = load_dataset()

# size = (150, 150)

# train_ds = tf.image.resize(train_ds, (150, 150))
# test_ds = tf.image.resize(test_ds, (150, 150))

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input

train_ds = preprocess_input(train_ds)
test_ds = preprocess_input(test_ds)

print(train_ds[0].shape)

base_model = VGG16(weights="imagenet", include_top=False, input_shape=train_ds[0].shape)
base_model.trainable = False
base_model.summary()

from tensorflow.keras import layers, models


flatten_layer = layers.Flatten()
dense_layer_1 = layers.Dense(50, activation="relu")
dense_layer_2 = layers.Dense(20, activation="relu")
prediction_layer = layers.Dense(10, activation="softmax")


model = models.Sequential(
    [base_model, flatten_layer, dense_layer_1, dense_layer_2, prediction_layer]
)

model.summary()
from tensorflow.keras.callbacks import EarlyStopping

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)


# es = EarlyStopping(
#     monitor="val_accuracy", mode="max", patience=5, restore_best_weights=True
# )

model.fit(
    train_ds,
    train_labels,
    epochs=50,
    validation_split=0.2,
    batch_size=32,
    # callbacks=[es],
)

model.evaluate(test_ds, test_labels)