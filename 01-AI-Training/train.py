from pathlib import Path
import shutil

from ultralytics import YOLO


BASE_DIR = Path(__file__).resolve().parent

DATASET_YAML = (
    BASE_DIR
    / "dataset-yolo"
    / "data.yaml"
)

RUNS_DIR = BASE_DIR / "runs"

OUTPUT_MODEL = BASE_DIR / "best.pt"

MODEL_NAME = "yolo26n.pt"

# CPU friendly
EPOCHS = 5
IMAGE_SIZE = 320
BATCH_SIZE = 2
WORKERS = 0

PROJECT_NAME = "fruit_detection"

# Untuk test awal.
# Setelah berhasil, bisa dinaikkan menjadi 1.0
DATA_FRACTION = 0.25


def main():

    print("=" * 70)
    print("WRAPSTATION - FRUIT OBJECT DETECTION")
    print("=" * 70)
    print()

    print(f"Dataset  : {DATASET_YAML}")
    print(f"Model    : {MODEL_NAME}")
    print(f"Epochs   : {EPOCHS}")
    print(f"Image    : {IMAGE_SIZE}")
    print(f"Batch    : {BATCH_SIZE}")
    print(f"Workers  : {WORKERS}")
    print(f"Fraction : {DATA_FRACTION}")
    print()

    if not DATASET_YAML.exists():

        raise FileNotFoundError(
            f"data.yaml tidak ditemukan:\n"
            f"{DATASET_YAML}"
        )

    print(
        "[OK] data.yaml ditemukan."
    )

    print()
    print("=" * 70)
    print("MEMUAT MODEL YOLO")
    print("=" * 70)

    model = YOLO(MODEL_NAME)

    print(
        "[OK] Model berhasil dimuat."
    )

    print()
    print("=" * 70)
    print("MEMULAI TRAINING")
    print("=" * 70)

    model.train(

        data=str(DATASET_YAML),

        epochs=EPOCHS,

        imgsz=IMAGE_SIZE,

        batch=BATCH_SIZE,

        workers=WORKERS,

        fraction=DATA_FRACTION,

        device="cpu",

        project=str(RUNS_DIR),

        name=PROJECT_NAME,

        exist_ok=True,

        pretrained=True,

        patience=3,

        cache=False,

        verbose=True,
    )

    print()
    print("=" * 70)
    print("TRAINING SELESAI")
    print("=" * 70)

    best_model = Path(
        model.trainer.best
    )

    print(
        f"\nBest model:\n{best_model}"
    )

    if not best_model.exists():

        raise FileNotFoundError(
            "best.pt hasil training tidak ditemukan."
        )

    shutil.copy2(
        best_model,
        OUTPUT_MODEL
    )

    print(
        f"\nModel final disimpan di:\n"
        f"{OUTPUT_MODEL}"
    )

    print()
    print("=" * 70)
    print("MODEL SIAP DIGUNAKAN")
    print("=" * 70)


if __name__ == "__main__":
    main()