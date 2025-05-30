import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import os

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    brightness_range=(0.8, 1.2),
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)

train_dir = "/kaggle/input/fer2013/train"

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(128, 128),
    batch_size=32,
    class_mode='categorical',
    color_mode='grayscale', 
    shuffle=True
)

print("Clases detectadas:", train_generator.class_indices)
NUM_CLASSES = len(train_generator.class_indices)


model = Sequential([
    Input(shape=(128, 128, 1)),  
    Conv2D(32, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.25),

    Conv2D(64, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.25),

    Conv2D(128, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.3),

    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(NUM_CLASSES, activation='softmax')
])

model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

early_stop = EarlyStopping(monitor='accuracy', patience=5, restore_best_weights=True)

model.fit(
    train_generator,
    epochs=20,
    callbacks=[early_stop]
)

os.makedirs('model', exist_ok=True)
model.save('model/modelo_emociones.h5')
