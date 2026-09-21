from pathlib import Path
import shutil
import sys

from ultralytics import YOLO

# ============================================================
# WRAPSTATION - FINAL FRUIT OBJECT DETECTION TRAINING
# ============================================================
#
# Important:
# - Uses 100% of the TRAIN split.
# - Validation and test splits remain separate.
# - Dataset must first pass check_yolo_dataset.py.
# - Final weights are copied to 01-AI-Training/best.pt.
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset-yolo"
DATA_YAML = DATASET_DIR / "data.yaml"

# Local base model. If it does not exist, Ultralytics can download it.
MODEL_PATH = BASE_DIR / "yolo26n.pt"

EPOCHS = 10
IMAGE_SIZE = 640
BATCH_SIZE = 2
WORKERS = 0

# 1.0 = 100% of the TRAIN split.
# Do NOT use 0.25 for the final technical-test model.
DATA_FRACTION = 1.0

PROJECT_DIR = BASE_DIR / "runs"
RUN_NAME = "fruit_detection_final"


EXPECTED_CLASSES = [
    "Apple",
    "Banana",
    "Grapes",
    "Kiwi",
    "Mango",
    "Orange",
    "Pineapple",
    "Sugerapple",
    "Watermelon",
]


def validate_dataset_structure():
    print("=" * 64)
    print("DATASET PRE-FLIGHT CHECK")
    print("=" * 64)

    if not DATA_YAML.exists():
        raise FileNotFoundError(
            f"data.yaml tidak ditemukan:\n{DATA_YAML}"
        )

    split_info = {
        "train": DATASET_DIR / "images" / "train",
        "valid": DATASET_DIR / "images" / "valid",
        "test": DATASET_DIR / "images" / "test",
    }

    for split, image_dir in split_info.items():
        label_dir = DATASET_DIR / "labels" / split

        if not image_dir.exists():
            raise FileNotFoundError(
                f"Folder image {split} tidak ditemukan:\n{image_dir}"
            )

        if not label_dir.exists():
            raise FileNotFoundError(
                f"Folder label {split} tidak ditemukan:\n{label_dir}"
            )

        image_count = len([
            p for p in image_dir.iterdir()
            if p.is_file() and p.suffix.lower() in {
                ".jpg", ".jpeg", ".png", ".bmp", ".webp"
            }
        ])

        label_count = len([
            p for p in label_dir.iterdir()
            if p.is_file() and p.suffix.lower() == ".txt"
        ])

        print(
            f"{split:>5}: "
            f"{image_count:>5} images | "
            f"{label_count:>5} labels"
        )

        if image_count == 0:
            raise RuntimeError(
                f"Split {split} tidak memiliki image."
            )

    print()
    print("Expected classes:")
    for index, name in enumerate(EXPECTED_CLASSES):
        print(f"  {index}: {name}")

    print()
    print(
        "Catatan: jalankan check_yolo_dataset.py terlebih dahulu "
        "untuk memastikan semua label berformat YOLO detection."
    )


def load_model():
    if MODEL_PATH.exists():
        print(f"\nBase model: {MODEL_PATH}")
        return YOLO(str(MODEL_PATH))

    print(
        "\nBase model lokal tidak ditemukan."
        "\nUltralytics akan mencoba mengunduh yolo26n.pt."
    )
    return YOLO("yolo26n.pt")


def main():
    print("\n" + "=" * 64)
    print("WRAPSTATION - FINAL FRUIT OBJECT DETECTION TRAINING")
    print("=" * 64)

    validate_dataset_structure()

    print("\nTraining configuration:")
    print(f"  Dataset       : {DATA_YAML}")
    print(f"  Data fraction : {DATA_FRACTION * 100:.0f}% TRAIN split")
    print(f"  Epochs        : {EPOCHS}")
    print(f"  Image size    : {IMAGE_SIZE}")
    print(f"  Batch size    : {BATCH_SIZE}")
    print(f"  Workers       : {WORKERS}")
    print(f"  Device        : CPU/default")
    print()

    model = load_model()

    results = model.train(
        data=str(DATA_YAML),
        epochs=EPOCHS,
        imgsz=IMAGE_SIZE,
        batch=BATCH_SIZE,
        workers=WORKERS,
        device="cpu",
        project=str(PROJECT_DIR),
        name=RUN_NAME,
        exist_ok=True,
        fraction=DATA_FRACTION,
        pretrained=True,
        patience=5,
        save=True,
        plots=True,
        verbose=True,
    )

    run_weights = PROJECT_DIR / RUN_NAME / "weights"
    best_source = run_weights / "best.pt"

    if not best_source.exists():
        raise FileNotFoundError(
            "Training selesai tetapi best.pt tidak ditemukan:\n"
            f"{best_source}"
        )

    final_weights = BASE_DIR / "best.pt"
    shutil.copy2(best_source, final_weights)

    print("\n" + "=" * 64)
    print("TRAINING SELESAI")
    print("=" * 64)
    print(f"Best weights : {final_weights}")
    print(f"Size         : {final_weights.stat().st_size:,} bytes")
    print()
    print("Model final menggunakan 100% TRAIN split.")
    print("VALID dan TEST tidak dimasukkan ke TRAIN.")
    print()
    print("Lanjutkan dengan:")
    print("  python predict.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTraining dihentikan oleh user.")
        sys.exit(130)
    except Exception as exc:
        print("\nERROR:")
        print(exc)
        sys.exit(1)
