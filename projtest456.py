# -*- coding: utf-8 -*-
"""projTEST456.ipynb

Automatically generated by Colab.

Original file is located in Google Colab
  
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Constants
IMAGE_SIZE = (150, 150)
BATCH_SIZE =  16
EPOCHS = 5
CLASS_COUNT = 8
DATASET_PATH = r'C:\Users\jonat\Dropbox\data\natural_images'

import requests
import zipfile
import io

# Dropbox shared link with `dl=1` for direct download
url = "https://www.dropbox.com/scl/fo/b6poy452p3rr7jty89chi/AK0qxajwc0tylE1Cv_dpiFI?rlkey=heqizpbovo0y2cgar6cnn5l5h&st=ud2z2mub&dl=1"

# Download the file from Dropbox
response = requests.get(url)
with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    z.extractall("/content/natural_images")

# Path to extracted dataset
DATASET_PATH = "/content/natural_images"

# Verify the dataset
import os
print("Path exists:", os.path.exists(DATASET_PATH))
print("Folders inside:", os.listdir(DATASET_PATH))

# Data Augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    fill_mode='reflect',
    validation_split=0.2
)

train_data = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

validation_data = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# Building the model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.3),
    Dense(CLASS_COUNT, activation='softmax')
])

# Compile the Model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Training
history = model.fit(
    train_data,
    epochs=EPOCHS,
    validation_data=validation_data
)

# Save the Model
model.save('final_project_cnn.h5')
# Load the trained model
loaded_model = tf.keras.models.load_model('final_project_cnn.h5')

validation_loss, validation_accuracy = loaded_model.evaluate(validation_data)
print("Validation Loss:", validation_loss)
print("Validation Accuracy:", validation_accuracy)
# Select the first three images from the validation set
X_new, y_new =  validation_data[0]  # Load the first batch of images and labels
X_new, y_new = X_new[:3], y_new[:3]
# Make predictions on the first three images
y_proba = loaded_model.predict(X_new)  # Predicted probabilities
y_pred = np.argmax(y_proba, axis=1)  # Pclass indices

# Map class indices to class names
class_names = list( validation_data.class_indices.keys())  # Get class names from generator
y_pred_names = np.array(class_names)[y_pred]  # Predicted class names
y_true_names = np.array(class_names)[np.argmax(y_new, axis=1)]  # correct class names

# predictions and true labels
print("Predicted Class Names:", y_pred_names)
print("True Class Names:", y_true_names)

# Plot the first three images with their predicted and correct labels
import matplotlib.pyplot as plt

plt.figure(figsize=(7.2, 2.4))
for index, image in enumerate(X_new):
    plt.subplot(1, 3, index + 1)
    plt.imshow(image, cmap="binary", interpolation="nearest")
    plt.axis("off")
    plt.title(f"Pred: {y_pred_names[index]}\nTrue: {y_true_names[index]}", fontsize=10)
plt.subplots_adjust(wspace=0.5, hspace=0.5)
plt.show()

#Jonathan Martinez CECS456 sec03
