import tensorflow as tf

from preprocessing import (
    train_dataset,
    val_dataset,
    train_count,
    val_count
)


# ==============================
# CounterShield Custom CNN
# ==============================

model = tf.keras.Sequential([

    tf.keras.layers.Input(shape=(224, 224, 3)),

    tf.keras.layers.Conv2D(
        32,
        (3, 3),
        activation="relu"
    ),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(
        64,
        (3, 3),
        activation="relu"
    ),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(
        128,
        (3, 3),
        activation="relu"
    ),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.GlobalAveragePooling2D(),

    tf.keras.layers.Dense(
        64,
        activation="relu"
    ),

    tf.keras.layers.Dropout(0.5),

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
# Callbacks
# ==============================

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=8,
    restore_best_weights=True
)


# ==============================
# Train Model
# ==============================

print("\n=== Training CounterShield Custom CNN ===\n")

history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=40,
    callbacks=[early_stopping]
)


# ==============================
# Save Model
# ==============================

model.save("model/countershield_custom_cnn.keras")

import json

with open("model/custom_cnn_history.json", "w") as f:
    json.dump(history.history, f)


# ==============================
# Training Summary
# ==============================

print("\n=== Training Completed ===")

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