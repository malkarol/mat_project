# https://towardsdatascience.com/transfer-learning-with-vgg16-and-keras-50ea161580b4
import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
image_size = (28, 28)
batch_size = 32

data =  tf.keras.preprocessing.image_dataset_from_directory(
    "/Users/michal/Desktop/test folder/data/",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
    color_mode= "grayscale"
)
print(data)


labels = np.concatenate([y for x, y in data], axis=0)
images = np.concatenate([x for x, y in data], axis=0)
# data(labels)
(train_ds, train_labels), (test_ds, test_labels) = train_test_split(images,
                                                    labels,
                                                    test_size=0.1,
                                                    random_state=42)

# size = (150, 150)

# train_ds = tf.image.resize(train_ds, (150, 150))
# test_ds = tf.image.resize(test_ds, (150, 150))

# train_labels = to_categorical(train_labels, num_classes=5)
# test_labels = to_categorical(test_labels, num_classes=5)

# from tensorflow.keras.applications.vgg16 import VGG16
# from tensorflow.keras.applications.vgg16 import preprocess_input

# train_ds = preprocess_input(train_ds)
# test_ds = preprocess_input(test_ds)

# base_model = VGG16(weights="imagenet", include_top=False, input_shape=train_ds[0].shape)
# base_model.trainable = False


# from tensorflow.keras import layers, models


# flatten_layer = layers.Flatten()
# dense_layer_1 = layers.Dense(50, activation="relu")
# dense_layer_2 = layers.Dense(20, activation="relu")
# prediction_layer = layers.Dense(5, activation="softmax")


# model = models.Sequential(
#     [base_model, flatten_layer, dense_layer_1, dense_layer_2, prediction_layer]
# )

# from tensorflow.keras.callbacks import EarlyStopping

# model.compile(
#     optimizer="adam",
#     loss="categorical_crossentropy",
#     metrics=["accuracy"],
# )


# es = EarlyStopping(
#     monitor="val_accuracy", mode="max", patience=5, restore_best_weights=True
# )

# model.fit(
#     train_ds,
#     train_labels,
#     epochs=50,
#     validation_split=0.2,
#     batch_size=32,
#     callbacks=[es],
# )

# model.evaluate(test_ds, test_labels)