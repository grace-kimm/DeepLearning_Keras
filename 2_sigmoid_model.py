# -*- coding: utf-8 -*-
"""2020451132_hw2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qttuE4TVmh0QLEytHiEfvHZkZnVmnGIq
"""

import numpy as np

from google.colab import files
uploaded = files.upload()

data = np.genfromtxt('BrainBody.txt', encoding='ascii')

data = np.delete(data, np.s_[0:1], axis=1)

dataX, dataY = np.split(data, 2, axis=1)

print(type(data))

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 2.x

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation, Dense 
from tensorflow.keras import optimizers

from sklearn.model_selection import train_test_split

data[:5, :]

data.shape

x_train_all, x_test, y_train_all, y_test = train_test_split(dataX, dataY, test_size=0.2, random_state=42)

x_train, x_val, y_train, y_val = train_test_split(x_train_all, y_train_all, test_size=0.2, random_state=42)
print(len(x_train), len(x_val))

print(x_train_all.shape, x_test.shape, y_train_all.shape, y_test.shape)

# Creating Model

model = Sequential()

model.add(Dense(10, input_shape=(1,), activation='sigmoid'))
model.add(Dense(10, activation='sigmoid'))
model.add(Dense(10, activation='sigmoid'))
model.add(Dense(1))

# Optimizer

sgd = optimizers.SGD(lr = 0.01)

# Model Summary

model.summary()

# Model Compile

model.compile(optimizer=sgd, loss='mean_squared_error', metrics = ['mse'])

# Model Learning

model.fit(x_train, y_train, batch_size=20, epochs=100, verbose=1)
model.evaluate(x_val, y_val)

#Model Evaluation

results = model.evaluate(x_test, y_test)

print('loss : ', results[0])
print('mse : ', results[1])