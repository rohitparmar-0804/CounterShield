import tensorflow as tf

from preprocessing import (
    train_dataset,
    val_dataset
)

MODEL_PATH = "model/efficientnetb0/efficientnetb0.keras"

SAVE_PATH = "model/efficientnetb0/efficientnetb0_finetuned.keras"
HISTORY_PATH = "model/efficientnetb0/efficientnetb0_finetuned_history.json"


# Load the already-trained frozen EfficientNetB0 model
model = tf.keras.models.load_model(MODEL_PATH)

# The EfficientNetB0 base model is the second layer
base_model = model.layers[1]

print("\n=== Before Fine-Tuning ===")
print("Base model:", base_model.name)
print("Total layers:", len(base_model.layers))


# Unfreeze the base model
base_model.trainable = True

# Keep BatchNormalization layers frozen
for layer in base_model.layers:
    if isinstance(layer, tf.keras.layers.BatchNormalization):
        layer.trainable = False


# Recompile with a very small learning rate
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)


print("\n=== Fine-Tuning Configuration ===")
print("Learning rate: 0.00001")
print("BatchNormalization layers: frozen")
print("Fine-tuning model is ready.")


# Early stopping
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)


# Fine-tune
history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=15,
    callbacks=[early_stopping]
)


# Save fine-tuned model
model.save(SAVE_PATH)


# Save training history
import json

with open(HISTORY_PATH, "w") as f:
    json.dump(history.history, f, indent=4)


best_val_accuracy = max(history.history["val_accuracy"])
best_val_loss = min(history.history["val_loss"])


print("\n=== Fine-Tuning Complete ===")
print("Best validation accuracy: {:.2f}%".format(
    best_val_accuracy * 100
))
print("Best validation loss: {:.4f}".format(
    best_val_loss
))
print("Saved model:", SAVE_PATH)
print("Saved history:", HISTORY_PATH)