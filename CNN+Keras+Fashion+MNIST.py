
# coding: utf-8

# In[24]:

import numpy as np
import pandas as pd
from keras.utils import to_categorical

data_train = pd.read_csv("/Users/rahmi/Downloads/fashion-mnist_train.csv")
data_train.head(5)


# In[25]:

data_test = pd.read_csv("/Users/rahmi/Downloads/fashion-mnist_test.csv")


# In[26]:

img_rows,img_cols = 28,28
input_shape = (img_rows,img_cols,1)


# In[48]:

img_rows


# In[27]:

X = np.array(data_train.iloc[:,1:])
y = to_categorical(np.array(data_train.iloc[:,0]))


# In[28]:

#Test data
X_test = np.array(data_test.iloc[:, 1:])
y_test = to_categorical(np.array(data_test.iloc[:, 0]))


# In[29]:

from sklearn.model_selection import train_test_split

X_train,X_val,y_train,y_val = train_test_split(X,y,test_size = 0.2,random_state = 13)


# In[30]:

X_train = X_train.reshape(X_train.shape[0],img_rows,img_cols,1)
X_val = X_val.reshape(X_val.shape[0],img_rows,img_cols,1)
X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)


# In[31]:

X_train.shape


# In[32]:

X_train = X_train.astype('float32')
X_val = X_val.astype('float32')
X_test = X_test.astype('float32')


# In[33]:

X_train /= 255
X_val /= 255
X_test /= 255


# In[34]:

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization


# In[35]:

batch_size = 256
num_classes = 10
epochs = 2


# In[36]:

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 kernel_initializer='he_normal',
                 input_shape=input_shape))
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(Dropout(0.4))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])


# In[37]:

history = model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(X_val, y_val))
score = model.evaluate(X_test, y_test, verbose=0)


# In[38]:

print('Test loss:', score[0])
print('Test accuracy:', score[1])


# In[44]:

#get the predictions for the test data
predicted_classes = model.predict_classes(X_test)

#get the indices to be plotted
y_true = data_test.iloc[:, 0]


# In[45]:

#get the indices to be plotted
#y_true = data_test.iloc[:, 0]
correct = np.nonzero(predicted_classes==y_test)[0]
incorrect = np.nonzero(predicted_classes!=y_test)[0]


# In[46]:

from sklearn.metrics import classification_report
target_names = ["Class {}".format(i) for i in range(num_classes)]
print(classification_report(y_true, predicted_classes, target_names=target_names))

