from tensorflow import keras
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, Dropout, SpatialDropout2D, AveragePooling2D
import numpy as np
import pickle
x_val=pickle.load(open('x_val.bin','rb'))
y_val=pickle.load(open('y_val.bin','rb'))

# Rishi Model

layerz = [Conv2D(72, kernel_size=(3,3), input_shape=(256,256,3)),  
		Conv2D(72, kernel_size=(3,3),activation='relu'),  
		MaxPooling2D(pool_size=(2,2)), 
		Conv2D(72, kernel_size=(3,3)),
		Conv2D(72, kernel_size=(3,3),activation='relu'),
		MaxPooling2D(pool_size=(2,2)),
		Conv2D(72, kernel_size=(3,3)), 
		Conv2D(72, kernel_size=(3,3),activation='relu'),
		MaxPooling2D(pool_size=(2,2)),
		Flatten(), 
		Dense(250, activation='relu'),
		Dense(6,activation='softmax')]

# AM's model
# layerz = [Conv2D(128,(3,3),input_shape=(256,256,3), activation='relu'),
# 		MaxPooling2D(pool_size=2),
# 		Conv2D(32,(3,3),activation='relu'),
# 		MaxPooling2D(pool_size=2),
# 		Flatten(),
# 		Dense(512,activation='relu'),
# 		Dropout(0.2),
# 		Dense(6,activation='softmax')]

batch=18
model=keras.Sequential(layerz)
model.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.Adam(learning_rate=0.0000025*batch), metrics=['accuracy'])

print('\n \nTraining: \n \n')
	
checkpoint = keras.callbacks.ModelCheckpoint('ckpt.hdf5', monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=15)

#model.load_weights('ckpt.hdf5')

from keras.preprocessing.image import ImageDataGenerator
# Generator Object with transformation settings
train_datagen = ImageDataGenerator(
   	shear_range=0.1,	height_shift_range=0.2,
        zoom_range=0.2,     horizontal_flip=True,
        vertical_flip=True, width_shift_range=0.2)
# Vectorize Images in Training Directory

train_generator = train_datagen.flow_from_directory(
        'train',           target_size=(256, 256),
        batch_size=batch,      class_mode='categorical')

#Similarly generate validation set too called validation_generator

# Train Model
model.fit(
        train_generator, steps_per_epoch=1995//batch,
        epochs=10, validation_data=(x_val,y_val), callbacks=[checkpoint])

model.save("AWS")

print('\n\nSaving Model Successful')