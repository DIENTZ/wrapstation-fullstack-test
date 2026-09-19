from pathlib import Path
import shutil

from ultralytics import YOLO


# ============================================================
# KONFIGURASI
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATASET_DIR = BASE_DIR / "dataset"
DATA_YAML = DATASET_DIR / "data.yaml"

RUNS_DIR = BASE_DIR / "runs"

OUTPUT_MODEL = BASE_DIR / "best.pt"

# Model YOLO pretrained
MODEL_NAME = "yolo26n.pt"

# Training
EPOCHS = 10
IMAGE_SIZE = 640
BATCH_SIZE = 8
WORKERS = 0


# ============================================================
# VALIDASI DATASET
# ============================================================

def check_dataset():
    print("=" * 60)
    print("MEMERIKSA DATASET")
    print("=" * 60)

    required_paths = [
        DATA_YAML,
        DATASET_DIR / "image" / "train",
        DATASET_DIR / "image" / "val",
        DATASET_DIR / "labels" / "train",
        DATASET_DIR / "labels" / "val",
    ]

    for path in required_paths:
        if not path.exists():
            raise FileNotFoundError(
                f"Dataset tidak ditemukan:\n{path}"
            )

        print(f"[OK] {path}")

    print()
    print("Dataset berhasil ditemukan.")
    print()


# ============================================================
# TRAINING
# ============================================================

def train_model():

    check_dataset()

    print("=" * 60)
    print("MEMULAI TRAINING YOLO")
    print("=" * 60)

    print(f"Dataset   : {DATA_YAML}")
    print(f"Model     : {MODEL_NAME}")
    print(f"Epochs    : {EPOCHS}")
    print(f"Image Size: {IMAGE_SIZE}")
    print(f"Batch     : {BATCH_SIZE}")
    print()

    # Load pretrained YOLO
    model = YOLO(MODEL_NAME)

    # Training
    model.train(
        data=str(DATA_YAML),
        epochs=EPOCHS,
        imgsz=IMAGE_SIZE,
        batch=BATCH_SIZE,
        workers=WORKERS,
        project=str(RUNS_DIR),
        name="fruit_detection",
        exist_ok=True,
        pretrained=True,
        patience=5,
        verbose=True
    )

    # Path best.pt hasil training
    best_model = Path(model.trainer.best)

    print()
    print("=" * 60)
    print("TRAINING SELESAI")
    print("=" * 60)

    print(f"Model terbaik:")
    print(best_model)

    if not best_model.exists():
        raise FileNotFoundError(
            "best.pt hasil training tidak ditemukan."
        )

    # Salin best.pt ke folder utama AI Training
    shutil.copy2(best_model, OUTPUT_MODEL)

    print()
    print("Model berhasil disalin ke:")
    print(OUTPUT_MODEL)

    print()
    print("=" * 60)
    print("SELESAI")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    train_model()