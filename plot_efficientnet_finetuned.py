import json
import matplotlib.pyplot as plt

HISTORY_PATH = "model/efficientnetb0/efficientnetb0_finetuned_history.json"

with open(HISTORY_PATH, "r") as f:
    history = json.load(f)

epochs = range(1, len(history["accuracy"]) + 1)

# Accuracy graph
plt.figure(figsize=(10, 7))
plt.plot(epochs, history["accuracy"], label="Training Accuracy")
plt.plot(epochs, history["val_accuracy"], label="Validation Accuracy")
plt.title("Fine-Tuned EfficientNetB0 Training and Validation Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "model/efficientnetb0/efficientnetb0_finetuned_accuracy.png",
    dpi=300
)
plt.close()

# Loss graph
plt.figure(figsize=(10, 7))
plt.plot(epochs, history["loss"], label="Training Loss")
plt.plot(epochs, history["val_loss"], label="Validation Loss")
plt.title("Fine-Tuned EfficientNetB0 Training and Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "model/efficientnetb0/efficientnetb0_finetuned_loss.png",
    dpi=300
)
plt.close()

print("Fine-tuned EfficientNetB0 graphs created successfully.")
print("Accuracy graph: model/efficientnetb0/efficientnetb0_finetuned_accuracy.png")
print("Loss graph: model/efficientnetb0/efficientnetb0_finetuned_loss.png")