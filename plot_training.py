import json
import matplotlib.pyplot as plt


# ==============================
# Load Training History
# ==============================

with open("model/custom_cnn_history.json", "r") as f:
    history = json.load(f)


epochs = range(1, len(history["accuracy"]) + 1)


# ==============================
# Training vs Validation Accuracy
# ==============================

plt.figure(figsize=(8, 5))

plt.plot(
    epochs,
    history["accuracy"],
    label="Training Accuracy"
)

plt.plot(
    epochs,
    history["val_accuracy"],
    label="Validation Accuracy"
)

plt.title("Custom CNN Training and Validation Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)

plt.savefig(
    "model/custom_cnn_accuracy.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ==============================
# Training vs Validation Loss
# ==============================

plt.figure(figsize=(8, 5))

plt.plot(
    epochs,
    history["loss"],
    label="Training Loss"
)

plt.plot(
    epochs,
    history["val_loss"],
    label="Validation Loss"
)

plt.title("Custom CNN Training and Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.grid(True)

plt.savefig(
    "model/custom_cnn_loss.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


print("\nTraining graphs created successfully.")
print("Saved:")
print("1. model/custom_cnn_accuracy.png")
print("2. model/custom_cnn_loss.png")