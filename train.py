# from tensorflow import keras
# from tensorflow.keras import layers
# import os
# from datetime import datetime
# import argparse
# import prepare_data as prep_data

# def build_model():
#     model = keras.Sequential([
#         keras.Input(shape=(28, 28, 1)),
#         layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
#         layers.MaxPooling2D(pool_size=(2, 2)),
#         layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
#         layers.MaxPooling2D(pool_size=(2, 2)),
#         layers.Flatten(),
#         layers.Dropout(0.5),
#         layers.Dense(9, activation="softmax")]
#     )
#     model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    
#     return model

# def main(args):
#     data_choice = args['data']
#     batch_size = args['batch_size']
#     epochs = args['epochs']
#     model_save_fpath = args['model_save_fpath']
#     exclude_fonts = args['exclude_fonts']

#     x_train, x_val, x_test, y_train, y_val, y_test = prep_data.get_data(data_choice=data_choice,
#                                                                         exclude=exclude_fonts)
        
#     model = build_model()
#     print("Starting training...")
#     model.fit(x_train, y_train,
#               validation_data=(x_val, y_val),
#               batch_size=batch_size,
#               epochs=epochs)
#     print("Training complete")
    
#     if os.path.exists(model_save_fpath):
#         now = datetime.now()
#         suffix = now.strftime("%d_%m_%Y_%H_%M_%S")
#         model_save_fpath = f"models/model_{suffix}.keras"

#     model.save(model_save_fpath)

#     print(f"Model saved at: {model_save_fpath}")

# if __name__ == '__main__':
#     ap = argparse.ArgumentParser()
#     ap.add_argument("--data", default="both", type=str, help="Choose data to use ('mnist', 'fonts', 'both')")
#     ap.add_argument("--exclude_fonts", default=True, type=bool, help="Whether or not to exclude fonts like those in 'data/font_exclude/'")
#     ap.add_argument("--model_save_fpath", default="models/model.keras", type=str)
#     ap.add_argument("--batch_size", default="128", type=int)
#     ap.add_argument("--epochs", default="10", type=int)
    
#     args = vars(ap.parse_args())

#     main(args)

# train.py
import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist
from prepare_data import load_images  # Optional

# Create model directory if it doesn't exist
os.makedirs("models", exist_ok=True)

# Load MNIST data
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = np.expand_dims(x_train, axis=-1) / 255.0
x_test = np.expand_dims(x_test, axis=-1) / 255.0
print("Unique labels in y_train:", np.unique(y_train))

# Cast labels to int before subtracting 1 to avoid uint8 wraparound
y_train = y_train.astype(int) - 1
y_test = y_test.astype(int) - 1

y_train = to_categorical(y_train, 9)  # 9 classes: digits 1–9
y_test = to_categorical(y_test, 9)

# Optional: include synthetic font images
# x_font, y_font = load_font_images()
# x_train = np.concatenate([x_train, x_font], axis=0)
# y_train = np.concatenate([y_train, y_font], axis=0)

# Define model
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

# Train model
model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=5)

# Save model
model.save("models/model.keras")
print("✅ Model saved to models/model.keras")
