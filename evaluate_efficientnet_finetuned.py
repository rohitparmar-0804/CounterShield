import tensorflow as tf
import numpy as np

from sklearn.metrics import classification_report, confusion_matrix

from preprocessing import test_dataset


MODEL_PATH = "model/efficientnetb0/efficientnetb0_finetuned.keras"


# Load fine-tuned model
model = tf.keras.models.load_model(MODEL_PATH)


print("\n=== CounterShield EfficientNetB0 Fine-Tuned Test Evaluation ===")

# Evaluate test set
test_loss, test_accuracy = model.evaluate(test_dataset, verbose=0)

print("Test Loss: {:.4f}".format(test_loss))
print("Test Accuracy: {:.2f}%".format(test_accuracy * 100))


# Collect true labels and predictions
y_true = []
y_pred = []

for images, labels in test_dataset:
    predictions = model.predict(images, verbose=0)

    predicted_labels = (predictions >= 0.5).astype(int).flatten()

    y_true.extend(labels.numpy())
    y_pred.extend(predicted_labels)


# Classification report
print("\n=== Classification Report ===")

report = classification_report(
    y_true,
    y_pred,
    target_names=["Genuine", "Counterfeit"],
    digits=4
)

print(report)


# Confusion matrix
print("=== Confusion Matrix ===")

cm = confusion_matrix(y_true, y_pred)

print(cm)