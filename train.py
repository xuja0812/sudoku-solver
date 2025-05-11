import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist
from prepare_data import load_images 

# create model directory 
os.makedirs("models", exist_ok=True)

# data
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = np.expand_dims(x_train, axis=-1) / 255.0
x_test = np.expand_dims(x_test, axis=-1) / 255.0
print("Unique labels in y_train:", np.unique(y_train))

# cast labels to int before subtracting 1 to avoid uint8 wraparound
y_train = y_train.astype(int) - 1
y_test = y_test.astype(int) - 1

y_train = to_categorical(y_train, 9)  # 9 classes: digits 1–9
y_test = to_categorical(y_test, 9)

# model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(9, activation='softmax')  # 9 classes: digits 1–9
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# train
model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=5)

# save
model.save("models/model.keras")
print("Model saved to models/model.keras")
