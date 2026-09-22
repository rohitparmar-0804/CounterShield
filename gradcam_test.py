import sys
import tensorflow as tf
import numpy as np
import cv2

from PIL import Image


# ==============================
# Configuration
# ==============================

MODEL_PATH = "model/efficientnetb0/efficientnetb0_finetuned.keras"

if len(sys.argv) < 2:
    print("Usage: python gradcam_test.py <image_path>")
    sys.exit(1)

IMAGE_PATH = sys.argv[1]

IMG_SIZE = (224, 224)

CLASS_NAMES = ["Genuine", "Counterfeit"]


# ==============================
# Load model
# ==============================

model = tf.keras.models.load_model(MODEL_PATH)

# EfficientNetB0 base model
base_model = model.layers[1]

# Confirmed convolutional layer for Grad-CAM
gradcam_layer = base_model.get_layer("top_conv")


# ==============================
# Load and preprocess image
# ==============================

original_image = Image.open(IMAGE_PATH).convert("RGB")

original_array = np.array(original_image)

resized_image = original_image.resize(IMG_SIZE)

image_array = np.array(
    resized_image,
    dtype=np.float32
) / 255.0

image_array = np.expand_dims(image_array, axis=0)



# ==============================
# Grad-CAM model
# ==============================

grad_model = tf.keras.models.Model(
    inputs=base_model.input,
    outputs=[
        gradcam_layer.output,
        base_model.output
    ]
)

# ==============================
# Calculate Grad-CAM
# ==============================

with tf.GradientTape() as tape:

    # Get top_conv feature maps and EfficientNet output
    conv_outputs, base_output = grad_model(image_array * 255.0)

    # Pass EfficientNet output through the classification head
    x = model.layers[2](base_output)
    x = model.layers[3](x, training=False)
    predictions = model.layers[4](x)

    prediction = predictions[:, 0]

    predicted_class = (
        "Counterfeit"
        if prediction[0] >= 0.5
        else "Genuine"
    )


# Gradients of prediction with respect to top_conv feature maps
grads = tape.gradient(
    prediction,
    conv_outputs
)


# Global average pooling of gradients
pooled_grads = tf.reduce_mean(
    grads,
    axis=(1, 2)
)


# Remove batch dimension
conv_outputs = conv_outputs[0]
pooled_grads = pooled_grads[0]


# Weight feature maps
heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]

heatmap = tf.squeeze(heatmap)


# Keep only positive influence
heatmap = tf.maximum(heatmap, 0)

max_value = tf.reduce_max(heatmap)

if max_value > 0:
    heatmap /= max_value

heatmap = heatmap.numpy()

# ==============================
# Resize heatmap
# ==============================

heatmap = cv2.resize(
    heatmap,
    (original_array.shape[1], original_array.shape[0])
)


# ==============================
# Create visualization
# ==============================

heatmap_uint8 = np.uint8(
    255 * heatmap
)

heatmap_color = cv2.applyColorMap(
    heatmap_uint8,
    cv2.COLORMAP_JET
)

heatmap_color = cv2.cvtColor(
    heatmap_color,
    cv2.COLOR_BGR2RGB
)


# Blend original image and heatmap
overlay = cv2.addWeighted(
    original_array,
    0.6,
    heatmap_color,
    0.4,
    0
)


# ==============================
# Display results
# ==============================

confidence = (
    prediction[0].numpy()
    if prediction[0] >= 0.5
    else 1 - prediction[0].numpy()
)


print("\n=== CounterShield Grad-CAM ===")
print("Image:", IMAGE_PATH)
print("Predicted class:", predicted_class)
print("Confidence: {:.2f}%".format(
    confidence * 100
))
print("Grad-CAM layer:", gradcam_layer.name)


OUTPUT_PATH = "model/efficientnetb0/gradcam_result.png"

# Save Grad-CAM overlay directly without Matplotlib
cv2.imwrite(
    OUTPUT_PATH,
    cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR)
)

print("Grad-CAM saved to:", OUTPUT_PATH)

# Save structured result for the website
import json

result = {
    "prediction": predicted_class,
    "confidence": float(confidence),
    "gradcam_path": OUTPUT_PATH
}

with open("model/efficientnetb0/prediction_result.json", "w") as f:
    json.dump(result, f, indent=4)

print("Prediction result saved successfully.")