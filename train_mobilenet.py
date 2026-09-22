import tensorflow as tf
import json

from preprocessing import (
    train_dataset,
    val_dataset,
    train_count,
    val_count
)


# ==============================
# CounterShield MobileNetV2
# ==============================

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

# Freeze pretrained layers
base_model.trainable = False


model = tf.keras.Sequential([

    tf.keras.layers.Input(shape=(224, 224, 3)),

    # Convert 0-1 pixels to -1 to 1
    tf.keras.layers.Rescaling(
        scale=2.0,
        offset=-1.0
    ),

    base_model,

    tf.keras.layers.GlobalAveragePooling2D(),

    tf.keras.layers.Dropout(0.3),

    tf.keras.layers.Dense(
        1,
        activation="sigmoid"
    )
])


# ==============================
# Compile Model
# ==============================

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.0001
    ),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)


# ==============================
# Early Stopping
# ==============================

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=8,
    restore_best_weights=True
)


# ==============================
# Train MobileNetV2
# ==============================

print("\n=== Training CounterShield MobileNetV2 ===\n")

history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=40,
    callbacks=[early_stopping]
)


# ==============================
# Save Model
# ==============================

model.save(
    "model/countershield_mobilenetv2.keras"
)


# ==============================
# Save Training History
# ==============================

with open(
    "model/mobilenetv2_history.json",
    "w"
) as f:

    json.dump(
        history.history,
        f,
        indent=4
    )


# ==============================
# Training Summary
# ==============================

print("\n=== MobileNetV2 Training Completed ===")

print(f"Training images: {train_count}")
print(f"Validation images: {val_count}")

print(
    f"Best validation accuracy: "
    f"{max(history.history['val_accuracy']):.4f}"
)

print(
    f"Best validation loss: "
    f"{min(history.history['val_loss']):.4f}"
)

print("\nModel saved successfully.")
print("Training history saved successfully.")