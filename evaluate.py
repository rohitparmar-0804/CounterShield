import tensorflow as tf
import numpy as np

from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

from preprocessing import test_dataset, test_count


# ==============================
# Load Trained Model
# ==============================

MODEL_PATH = "model/efficientnetb0/efficientnetb0.keras"

model = tf.keras.models.load_model(MODEL_PATH)


# ==============================
# Test Evaluation
# ==============================

print("\n=== CounterShield EfficientNetB0 Test Evaluation ===\n")

test_loss, test_accuracy = model.evaluate(
    test_dataset,
    verbose=1
)


# ==============================
# Collect Predictions
# ==============================

true_labels = []
predicted_labels = []

for images, labels in test_dataset:

    predictions = model.predict(
        images,
        verbose=0
    )

    predictions = (predictions >= 0.5).astype(int).flatten()

    true_labels.extend(
        labels.numpy().astype(int)
    )

    predicted_labels.extend(
        predictions
    )


true_labels = np.array(true_labels)
predicted_labels = np.array(predicted_labels)


# ==============================
# Classification Report
# ==============================

print("\n=== Classification Report ===\n")

print(
    classification_report(
        true_labels,
        predicted_labels,
        target_names=[
            "Genuine",
            "Counterfeit"
        ],
        digits=4
    )
)


# ==============================
# Confusion Matrix
# ==============================

cm = confusion_matrix(
    true_labels,
    predicted_labels
)

print("\n=== Confusion Matrix ===\n")

print(cm)


# ==============================
# Save Evaluation Results
# ==============================

report = classification_report(
    true_labels,
    predicted_labels,
    target_names=[
        "Genuine",
        "Counterfeit"
    ],
    output_dict=True
)


results = {
    "test_images": test_count,
    "test_loss": float(test_loss),
    "test_accuracy": float(test_accuracy),
    "genuine_precision": report["Genuine"]["precision"],
    "genuine_recall": report["Genuine"]["recall"],
    "genuine_f1": report["Genuine"]["f1-score"],
    "counterfeit_precision": report["Counterfeit"]["precision"],
    "counterfeit_recall": report["Counterfeit"]["recall"],
    "counterfeit_f1": report["Counterfeit"]["f1-score"],
    "macro_f1": report["macro avg"]["f1-score"],
    "weighted_f1": report["weighted avg"]["f1-score"],
    "confusion_matrix": cm.tolist()
}


import json

with open(
    "model/efficientnetb0/efficientnetb0_evaluation.json",
    "w"
) as f:
    json.dump(
        results,
        f,
        indent=4
    )


# ==============================
# Basic Test Results
# ==============================

print("\n=== Test Results ===")

print(f"Test images: {test_count}")
print(f"Test loss: {test_loss:.4f}")
print(f"Test accuracy: {test_accuracy:.4f}")
print(f"Test accuracy (%): {test_accuracy * 100:.2f}%")

print("\nEvaluation results saved successfully.")