import json

results = {
    "model": "EfficientNetB0 Fine-Tuned",
    "test_images": 48,
    "test_accuracy": 0.9583,
    "test_accuracy_percent": 95.83,
    "test_loss": 0.3435,
    "genuine": {
        "precision": 1.0000,
        "recall": 0.9167,
        "f1_score": 0.9565,
        "support": 24
    },
    "counterfeit": {
        "precision": 0.9231,
        "recall": 1.0000,
        "f1_score": 0.9600,
        "support": 24
    },
    "macro_f1": 0.9583,
    "weighted_f1": 0.9583,
    "confusion_matrix": [
        [22, 2],
        [0, 24]
    ]
}

OUTPUT_PATH = "model/efficientnetb0/efficientnetb0_finetuned_evaluation.json"

with open(OUTPUT_PATH, "w") as f:
    json.dump(results, f, indent=4)

print("Fine-tuned evaluation results saved successfully.")
print("Saved to:", OUTPUT_PATH)