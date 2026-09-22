import json
import matplotlib.pyplot as plt


# ==============================
# Load MobileNetV2 History
# ==============================

with open(
    "model/mobilenetv2/mobilenetv2_history.json",
    "r"
) as f:

    history = json.load(f)


epochs = range(
    1,
    len(history["accuracy"]) + 1
)


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

plt.title(
    "MobileNetV2 Training and Validation Accuracy"
)

plt.xlabel("Epoch")
plt.ylabel("Accuracy")

plt.legend()
plt.grid(True)

plt.savefig(
    "model/mobilenetv2/mobilenetv2_accuracy.png",
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

plt.title(
    "MobileNetV2 Training and Validation Loss"
)

plt.xlabel("Epoch")
plt.ylabel("Loss")

plt.legend()
plt.grid(True)

plt.savefig(
    "model/mobilenetv2/mobilenetv2_loss.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


print("\nMobileNetV2 training graphs created successfully.")

print(
    "1. model/mobilenetv2/mobilenetv2_accuracy.png"
)

print(
    "2. model/mobilenetv2/mobilenetv2_loss.png"
)