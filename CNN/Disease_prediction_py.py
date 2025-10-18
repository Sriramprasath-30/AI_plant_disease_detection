# predict_disease.py
"""
Rose Plant Disease Prediction
Loads model.h5 and predicts disease of a given leaf image.
"""

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# -----------------------------
# 1. Load trained model
# -----------------------------
model = load_model('model.h5')
print("Loaded model.h5 successfully")

# -----------------------------
# 2. Define class labels
# -----------------------------
class_labels = ['healthy', 'rose_rust', 'rose_sawfly_slug']  # Update based on your dataset

# -----------------------------
# 3. Prediction function
# -----------------------------
def predict_leaf_disease(img_path):
    # Load and preprocess image
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Predict
    preds = model.predict(img_array)
    class_idx = np.argmax(preds, axis=1)[0]
    confidence = preds[0][class_idx]

    predicted_label = class_labels[class_idx]
    return predicted_label, confidence

# -----------------------------
# 4. Test Example
# -----------------------------
if __name__ == "__main__":
    test_image = 'sample_leaf.jpg'  # Replace with your test leaf image
    label, conf = predict_leaf_disease(test_image)
    print(f"Predicted Disease: {label} (Confidence: {conf*100:.2f}%)")
