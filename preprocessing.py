import os
import tensorflow as tf

# ==============================
# CounterShield Configuration
# ==============================

DATASET_DIR = "CounterShield_Final_v3"

IMG_SIZE = (224, 224)
BATCH_SIZE = 16

CLASS_NAMES = ["Genuine", "Counterfeit"]


# ==============================
# Find Images
# ==============================

def collect_images(split):

    image_paths = []
    labels = []

    split_path = os.path.join(DATASET_DIR, split)

    for product in sorted(os.listdir(split_path)):

        product_path = os.path.join(split_path, product)

        if not os.path.isdir(product_path):
            continue

        for class_name in CLASS_NAMES:

            class_path = os.path.join(product_path, class_name)

            if not os.path.isdir(class_path):
                continue

            label = CLASS_NAMES.index(class_name)

            for filename in sorted(os.listdir(class_path)):

                if filename.lower().endswith(
                    (".jpg", ".jpeg", ".png", ".webp")
                ):

                    image_paths.append(
                        os.path.join(class_path, filename)
                    )

                    labels.append(label)

    return image_paths, labels


# ==============================
# Image Preprocessing
# ==============================

def load_and_preprocess(image_path, label):

    image = tf.io.read_file(image_path)

    image = tf.io.decode_image(
        image,
        channels=3,
        expand_animations=False
    )

    image = tf.image.resize(image, IMG_SIZE)

    image = tf.cast(image, tf.float32) / 255.0

    return image, label


# ==============================
# Create TensorFlow Dataset
# ==============================

def create_dataset(split):

    image_paths, labels = collect_images(split)

    dataset = tf.data.Dataset.from_tensor_slices(
        (image_paths, labels)
    )

    dataset = dataset.map(
        load_and_preprocess,
        num_parallel_calls=tf.data.AUTOTUNE
    )

    dataset = dataset.batch(BATCH_SIZE)

    dataset = dataset.prefetch(tf.data.AUTOTUNE)

    return dataset, len(image_paths)


# ==============================
# Training Augmentation
# ==============================

data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomRotation(0.05),
    tf.keras.layers.RandomZoom(0.10),
    tf.keras.layers.RandomTranslation(
        height_factor=0.05,
        width_factor=0.05
    )
])


# ==============================
# Create Datasets
# ==============================

train_dataset, train_count = create_dataset("train")

val_dataset, val_count = create_dataset("val")

test_dataset, test_count = create_dataset("test")


# ==============================
# Apply Augmentation to Training
# ==============================

train_dataset = train_dataset.map(
    lambda images, labels: (
        data_augmentation(images, training=True),
        labels
    ),
    num_parallel_calls=tf.data.AUTOTUNE
)


# ==============================
# Dataset Information
# ==============================

print("\n=== CounterShield Preprocessing Pipeline ===")

print(f"Training images:   {train_count}")
print(f"Validation images: {val_count}")
print(f"Test images:       {test_count}")

print(f"Image size:        {IMG_SIZE}")
print(f"Batch size:        {BATCH_SIZE}")

print("\nPreprocessing:")
print("1. RGB image loading")
print("2. Resize to 224 x 224")
print("3. Pixel normalization to 0-1")
print("4. Training-only augmentation")
print("5. TensorFlow batching and prefetching")

print("\nPreprocessing pipeline created successfully.")