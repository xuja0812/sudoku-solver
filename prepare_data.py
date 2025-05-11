from tensorflow import keras
from sklearn.model_selection import train_test_split
import numpy as np
import glob
import cv2

def load_images():
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    non_zero_train_indices = np.where(y_train != 0)[0]
    non_zero_test_indices = np.where(y_test != 0)[0]
    x_train, y_train = x_train[non_zero_train_indices], y_train[non_zero_train_indices]
    x_test, y_test = x_test[non_zero_test_indices], y_test[non_zero_test_indices]
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, train_size = 0.75, random_state = 2023)

    # scale images
    x_train = x_train.astype("float32") / 255
    x_val = x_val.astype("float32") / 255
    x_test = x_test.astype("float32") / 255

    # normalize dimensions
    x_train = np.expand_dims(x_train, -1)
    x_val = np.expand_dims(x_val, -1)
    x_test = np.expand_dims(x_test, -1)

    # class vectors -> binary class matrices
    y_train = keras.utils.to_categorically(y_train, num_classes = 10)[:,1:]
    y_val = keras.utils.to_categorically(y_val, num_classes = 10)[:,1:]
    y_test = keras.utils.to_categorically(y_test, num_classes = 10)[:,1:]

    return x_train, x_val, x_test, y_train, y_val, y_test

def get_font_image_dict(excluded_names=None):    
    folder_names = glob.glob("data/digit_images/*")
    digit_image_filepaths = [glob.glob(folder + "/*.png") for folder in folder_names]
    
    if excluded_names:
        inclusion_list_indices = list(np.where([not any(elem in fpath for elem in excluded_names) for fpath in digit_image_filepaths[0]])[0])
        digit_image_filepaths = [[fpath_list[i] for i in inclusion_list_indices] for fpath_list in digit_image_filepaths]
    
    img_dict = {i: None for i in range(1, 10)}
    for k in img_dict:
        img_dict[k] = [cv2.imread(fpath) for fpath in digit_image_filepaths[k-1]]
    
    for k, v in img_dict.items():
        gray = [cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY) for arr in v]
        img_dict[k] = [cv2.resize(arr, (28, 28), interpolation=cv2.INTER_AREA) for arr in gray]
        img_dict[k] = np.expand_dims(img_dict[k], -1)
    
    return img_dict

def load_font_image_arrays(image_dict):
    x = np.array([v for v in image_dict.values()])
    x = np.reshape(x, newshape=(-1, 28, 28, 1))
    y = np.array([np.repeat(k, len(image_dict[k])) for k in image_dict])
    y = np.reshape(y, newshape=(-1, 1))
    y = keras.utils.to_categorical(y, num_classes=10)[:, 1:]
    
    x_train, x_test, y_train, y_test = train_test_split(x,
                                                        y,
                                                        test_size=0.15,
                                                        shuffle=True,
                                                        random_state=0)
    
    x_train, x_val, y_train, y_val = train_test_split(x_train,
                                                      y_train,
                                                      test_size=0.18,
                                                      shuffle=True,
                                                      random_state=33)
    
    x_train = np.array(list(map(cv2.bitwise_not, x_train)))
    x_val = np.array(list(map(cv2.bitwise_not, x_val)))
    x_test = np.array(list(map(cv2.bitwise_not, x_test)))
    
    x_train = x_train.astype("float32") / 255
    x_val = x_val.astype("float32") / 255
    x_test = x_test.astype("float32") / 255
    
    x_train = np.expand_dims(x_train, -1)
    x_val = np.expand_dims(x_val, -1)
    x_test = np.expand_dims(x_test, -1)

    return x_train, x_val, x_test, y_train, y_val, y_test

def get_data(data_choice, exclude=True):
    data_choice = data_choice.lower()
    if data_choice not in ['mnist', 'fonts', 'both']:
        raise ValueError("Invalid value for data_choice: {data_choice}. Valid options are: 'mnist', 'fonts', or 'both'")
    
    if data_choice == "mnist" or data_choice == "both":
        mnist_data = list(load_images())
    
    if data_choice == "fonts" or data_choice == "both":
        if exclude:
            to_exclude = glob.glob("data/font_exclude/*.png")
            to_exclude = [fpath.split("\\")[-1] for fpath in to_exclude]
            to_exclude = [fpath.split("-")[-1] for fpath in to_exclude]
        else:
            to_exclude=None
        img_dict = get_font_image_dict(excluded_names=to_exclude)
        font_data = list(load_font_image_arrays(img_dict))
    
    if data_choice == "mnist":
        x_train, x_val, x_test, y_train, y_val, y_test = mnist_data
    
    elif data_choice == "fonts":
        x_train, x_val, x_test, y_train, y_val, y_test = font_data
    
    elif data_choice == "both":
        x_train = np.concatenate((font_data[0], mnist_data[0]))
        x_val = np.concatenate((font_data[1], mnist_data[1]))
        x_test = np.concatenate((font_data[2], mnist_data[2]))
        y_train = np.concatenate((font_data[3], mnist_data[3]))
        y_val = np.concatenate((font_data[4], mnist_data[4]))
        y_test = np.concatenate((font_data[5], mnist_data[5]))

    return x_train, x_val, x_test, y_train, y_val, y_test