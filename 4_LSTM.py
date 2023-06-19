"""
Zeinab Sadat Sadrolhefazi
e_mail: zns.sadr@gmail.com
"""


from __future__ import print_function

from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding
from tensorflow.keras.layers import LSTM
from tensorflow.keras import  optimizers
from tensorflow.keras.datasets import imdb
import matplotlib.pyplot as plt

max_features = 20000
maxlen = 80  # cut texts after this number of words (among top max_features most common words)
batch_size = 50

print('Loading data...')
(x_train, y_train), (x_test, y_test) = imdb.load_data(path='imdb.npz',
                                                      num_words=max_features)
print(len(x_train), 'train sequences')
print(len(x_test), 'test sequences')

print('Pad sequences (samples x time)')
x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
print('x_train shape:', x_train.shape)
print('x_test shape:', x_test.shape)

print('Build model...')
model = Sequential()
model.add(Embedding(max_features, 128))
model.add(LSTM(64, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(1, activation='sigmoid'))

opt = optimizers.Adam(learning_rate = 0.01)
# try using different optimizers and different optimizer configs
model.compile(loss='binary_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

print('Train...')
train_history = model.fit(x_train, y_train,
                          batch_size=batch_size,
                          epochs=3,
                          validation_split=0.2)
score, acc = model.evaluate(x_test, y_test,
                            batch_size=batch_size)
print('Test score:', score)
print('Test accuracy:', acc)


def show_train_history(train_history,train,validation):
    plt.plot(train_history.history[train])
    plt.plot(train_history.history[validation])
    plt.title('Train History')
    plt.ylabel(train)
    plt.xlabel('Epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()


show_train_history(train_history,'accuracy','val_accuracy')
show_train_history(train_history,'loss','val_loss')