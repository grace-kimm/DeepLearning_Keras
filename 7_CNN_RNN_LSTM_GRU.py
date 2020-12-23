# -*- coding: utf-8 -*-
"""2020451132_hw7

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LFuRoyqPkThjxRrs56HHreNMAx5505ZJ

총 6개 방법으로 테스트를 했다.
1. CNN
2. Simple RNN
3. Simple RNN + Word Embedding
4. RNN
5. LSTM
6. Bidirectional LSTM
7. GRU

1, 5, 6, 7 모두 약 87%로 성능이 비슷했으나 이 중에서는 **1. CNN**의 성과가 가장 높았다. </br>
1, 2, 3은 epoch=10으로 했으며, wall time이 각각 1min, 11min, 12min으로 RNN은 시간이 오래 걸렸다.</br>
4, 5, 6, 7은 그래서 **epoch를 3으로 낮추고** 시도했다. **5, 6은 epoch 대비 정확도가 높게** 나왔으며, epoch를 올리면 1. CNN 보다 높은 성과가 나올 것으로 생각된다.
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 2.x

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Conv1D, MaxPooling2D, Embedding, Flatten
from tensorflow.keras.layers import Reshape, Conv2D, GlobalMaxPooling2D
from tensorflow.keras import optimizers

num_features = 3000
sequence_length = 300
embedding_dimension = 100
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words = num_features)
X_train = pad_sequences(X_train, maxlen = sequence_length, padding='post')
X_test = pad_sequences(X_test, maxlen = sequence_length, padding='post')

print(X_train.shape, y_train.shape, X_test.shape, y_train.shape)

from tensorflow.keras.models import Model
from tensorflow.keras.layers import concatenate, Input

"""**1. CNN**"""

filter_sizes = [3, 4, 5]

def convolution():
    inn = Input(shape = (sequence_length, embedding_dimension, 1))
    convolutions = []
    # we conduct three convolutions & poolings then concatenate them.
    for fs in filter_sizes:
        conv = Conv2D(filters = 100, kernel_size = (fs, embedding_dimension), strides = 1, padding = "valid")(inn)
        nonlinearity = Activation('relu')(conv)
        maxpool = MaxPooling2D(pool_size = (sequence_length - fs + 1, 1), padding = "valid")(nonlinearity)
        convolutions.append(maxpool)
        
    outt = concatenate(convolutions)
    model = Model(inputs = inn, outputs = outt)
        
    return model

def imdb_cnn_3():
    
    model = Sequential()
    model.add(Embedding(input_dim = 3000, output_dim = embedding_dimension, input_length = sequence_length))
    model.add(Reshape((sequence_length, embedding_dimension, 1), input_shape = (sequence_length, embedding_dimension)))
    
    # call convolution method defined above
    model.add(convolution())
    
    model.add(Flatten())
    model.add(Dense(10))
    model.add(Activation('relu'))
    model.add(Dropout(0.3))
    model.add(Dense(10))
    model.add(Activation('relu'))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    adam = optimizers.Adam(lr = 0.001)

    model.compile(loss='binary_crossentropy', optimizer=adam , metrics=['accuracy'])
    
    return model

model = imdb_cnn_3()
model.summary()

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history = model.fit(X_train, y_train, batch_size = 50, epochs = 10, validation_split = 0.2, verbose = 1)

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.legend(['training', 'validation'], loc = 'upper left')
plt.show()

results = model.evaluate(X_test, y_test)
print('Test accuracy: ', results[1])

"""**2. SimpleRNN**"""

from keras.models import Sequential
from keras.layers import Dense, SimpleRNN, Activation
from keras import optimizers
from keras.wrappers.scikit_learn import KerasClassifier

from sklearn.metrics import accuracy_score
from keras.datasets import reuters
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical

X_train = np.array(X_train).reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = np.array(X_test).reshape((X_test.shape[0], X_test.shape[1], 1))

print(X_train.shape)
print(X_test.shape)

y_data = np.concatenate((y_train, y_test))
y_data = to_categorical(y_data)

y_data = np.array(y_train).reshape((y_data.shape[0], y_data.shape[1]))

y_train = y_data[:25000]
y_test = y_data[25000:]

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

def vanilla_rnn():
    model = Sequential()

    model.add(SimpleRNN(50, input_shape = (300,1), return_sequences = False))
    model.add(Dense(2))
    model.add(Activation('softmax'))
    
    adam = optimizers.Adam(lr = 0.001)
    model.compile(loss = 'categorical_crossentropy', optimizer = adam, metrics = ['accuracy'])
    
    return model

model = vanilla_rnn()
model.summary()

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history = model.fit(X_train, y_train, batch_size = 50, epochs = 10, validation_split = 0.2, verbose = 1)

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.legend(['training', 'validation'], loc = 'upper left')
plt.show()

results = model.evaluate(X_test, y_test)
print('Test accuracy: ', results[1])

"""**3. SimpleRNN + Word Embedding**"""

from keras import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout

X_train = np.array(X_train).reshape((X_train.shape[0], X_train.shape[1]))
X_test = np.array(X_test).reshape((X_test.shape[0], X_test.shape[1]))

print(X_train.shape)
print(X_test.shape)

def vanilla_emb_rnn():
    model = Sequential()
    model.add(Embedding(3000, 32))

    model.add(SimpleRNN(50, return_sequences = False))
    model.add(Dense(2))
    model.add(Activation('softmax'))
    
    adam = optimizers.Adam(lr = 0.001)
    model.compile(loss = 'categorical_crossentropy', optimizer = adam, metrics = ['accuracy'])
    
    return model

model = vanilla_emb_rnn()
model.summary()

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history = model.fit(X_train, y_train, batch_size = 50, epochs = 10, validation_split = 0.2, verbose = 1)

results = model.evaluate(X_test, y_test)
print('Test accuracy: ', results[1])

y_test_ = np.argmax(y_test, axis = 1)

print(accuracy_score(y_pred, y_test_))

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.legend(['training', 'validation'], loc = 'upper left')
plt.show()

"""**4. RNN**"""

model=Sequential()
model.add(Embedding(3000, 32))
model.add(SimpleRNN(50, return_sequences = True))
model.add(SimpleRNN(50, return_sequences = False))
model.add(Dense(1, activation='sigmoid'))
print(model.summary())

model.compile(loss='binary_crossentropy', 
             optimizer='adam', 
             metrics=['accuracy'])

batch_size = 64
num_epochs = 3

X_valid, y_valid = X_train[:batch_size], y_train[:batch_size]
X_train2, y_train2 = X_train[batch_size:], y_train[batch_size:]
model.fit(X_train2, y_train2, validation_data=(X_valid, y_valid), batch_size=batch_size, epochs=num_epochs)

scores = model.evaluate(X_test, y_test, verbose=0)
print('Test accuracy:', scores[1])

"""**5. LSTM + Word Embedding**"""

vocabulary_size = 3000

(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words = vocabulary_size)
print('Loaded dataset with {} training samples, {} test samples'.format(len(X_train), len(X_test)))

print('---review---')
print(X_train[6])
print('---label---')
print(y_train[6])

word2id = imdb.get_word_index()
id2word = {i: word for word, i in word2id.items()}
print('---review with words---')
print([id2word.get(i, ' ') for i in X_train[6]])
print('---label---')
print(y_train[6])

print('Maximum review length: {}'.format(
len(max((X_train + X_test), key=len))))

print('Minimum review length: {}'.format(
len(min((X_test + X_test), key=len))))

from keras.preprocessing import sequence

max_words = 300
X_train = sequence.pad_sequences(X_train, maxlen=max_words)
X_test = sequence.pad_sequences(X_test, maxlen=max_words)

from keras import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout

embedding_size=32

model=Sequential()
model.add(Embedding(vocabulary_size, embedding_size, input_length=max_words))
model.add(LSTM(100))
model.add(Dense(1, activation='sigmoid'))
print(model.summary())

model.compile(loss='binary_crossentropy', 
             optimizer='adam', 
             metrics=['accuracy'])

batch_size = 64
num_epochs = 3
X_valid, y_valid = X_train[:batch_size], y_train[:batch_size]
X_train2, y_train2 = X_train[batch_size:], y_train[batch_size:]
model.fit(X_train2, y_train2, validation_data=(X_valid, y_valid), batch_size=batch_size, epochs=num_epochs)

scores = model.evaluate(X_test, y_test, verbose=0)
print('Test accuracy:', scores[1])

"""**6. Bidirectional LSTM**"""

from keras import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional

embedding_size=32

model=Sequential()
model.add(Embedding(vocabulary_size, embedding_size, input_length=max_words))
model.add(Bidirectional(LSTM(100)))
model.add(Dense(1, activation='sigmoid'))
print(model.summary())

model.compile(loss='binary_crossentropy', 
             optimizer='adam', 
             metrics=['accuracy'])

batch_size = 64
num_epochs = 3
X_valid, y_valid = X_train[:batch_size], y_train[:batch_size]
X_train2, y_train2 = X_train[batch_size:], y_train[batch_size:]
model.fit(X_train2, y_train2, validation_data=(X_valid, y_valid), batch_size=batch_size, epochs=num_epochs)

scores = model.evaluate(X_test, y_test, verbose=0)
print('Test accuracy:', scores[1])

"""**7. GRU**"""

from keras import Sequential
from keras.layers import Embedding, GRU, Dense, Dropout
vocabulary_size = 3000
embedding_size=32

model=Sequential()
model.add(Embedding(vocabulary_size, embedding_size, input_length=max_words))
model.add(GRU(100))
model.add(Dense(1, activation='sigmoid'))
print(model.summary())

model.compile(loss='binary_crossentropy', 
             optimizer='adam', 
             metrics=['accuracy'])

batch_size = 64
num_epochs = 3
X_valid, y_valid = X_train[:batch_size], y_train[:batch_size]
X_train2, y_train2 = X_train[batch_size:], y_train[batch_size:]
model.fit(X_train2, y_train2, validation_data=(X_valid, y_valid), batch_size=batch_size, epochs=num_epochs)

scores = model.evaluate(X_test, y_test, verbose=0)
print('Test accuracy:', scores[1])