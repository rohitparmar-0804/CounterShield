import sys
import numpy as np
import tensorflow as tf
from PIL import Image

MODEL_PATH = "model/efficientnetb0/efficientnetb0.keras"
IMG_SIZE = (224, 224)

CLASS_NAMES = ["Genuine", "Counterfeit"]


# Load trained model
model = tf.keras.models.load_model(MODEL_PATH)


# Check image path
if len(sys.argv) < 2:
    print("Usage: python predict.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]


# Load and preprocess image
image = Image.open(image_path).convert("RGB")
image = image.resize(IMG_SIZE)

image_array = np.array(image, dtype=np.float32) / 255.0
image_array = np.expand_dims(image_array, axis=0)


# Make prediction
prediction = model.predict(image_array, verbose=0)[0][0]

if prediction >= 0.5:
    predicted_class = "Counterfeit"
else:
    predicted_class = "Genuine"


confidence = prediction if prediction >= 0.5 else 1 - prediction


print("\n=== CounterShield Prediction ===")
print("Image:", image_path)
print("Prediction:", predicted_class)
print("Confidence: {:.2f}%".format(confidence * 100))
print("Raw probability: {:.4f}".format(prediction))