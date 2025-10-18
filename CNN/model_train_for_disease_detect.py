# train_model.py
"""
Rose Plant Disease Detection - CNN Training Script
Trains a CNN on rose leaf images to classify diseases.
Generates model.h5 for predictions.
"""

import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.optimizers import Adam

# -----------------------------
# 1. Dataset paths
# -----------------------------
train_dir = 'dataset/train'  # Training images
val_dir = 'dataset/val'      # Validation images

# -----------------------------
# 2. Image Data Generators
# -----------------------------
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    shear_range=0.2,
    zoom_range=0.2
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# Get class labels
class_labels = list(train_generator.class_indices.keys())
num_classes = len(class_labels)
print("Detected classes:", class_labels)

# -----------------------------
# 3. Define CNN Model
# -----------------------------
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze base layers
for layer in base_model.layers:
    layer.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# Compile model
model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# -----------------------------
# 4. Train Model
# -----------------------------
epochs = 10  # Increase if needed
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=epochs
)

# -----------------------------
# 5. Save Model
# -----------------------------
model.save('model.h5')
print("Training complete. Model saved as 'model.h5'")
