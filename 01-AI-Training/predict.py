from pathlib import Path

import cv2
from ultralytics import YOLO


BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "best.pt"

IMAGE_DIR = (
    BASE_DIR
    / "dataset-yolo"
    / "images"
    / "test"
)

WINDOW_NAME = (
    "Wrapstation - Fruit Object Detection"
)

CONFIDENCE = 0.25

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
}


def get_images():

    if not IMAGE_DIR.exists():

        return []

    images = []

    for file in IMAGE_DIR.iterdir():

        if (
            file.is_file()
            and file.suffix.lower()
            in IMAGE_EXTENSIONS
        ):

            images.append(file)

    return sorted(images)


def print_detections(result):

    if (
        result.boxes is None
        or len(result.boxes) == 0
    ):

        print(
            "Tidak ada objek "
            "yang terdeteksi."
        )

        return

    print(
        "Objek yang terdeteksi:"
    )

    for box in result.boxes:

        class_id = int(
            box.cls[0]
        )

        confidence = float(
            box.conf[0]
        )

        class_name = (
            result.names[class_id]
        )

        print(
            f"  - {class_name}: "
            f"{confidence * 100:.2f}%"
        )


def main():

    print("=" * 70)
    print(
        "WRAPSTATION - "
        "FRUIT OBJECT DETECTION"
    )
    print("=" * 70)

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"Model tidak ditemukan:\n"
            f"{MODEL_PATH}\n\n"
            "Jalankan train.py "
            "terlebih dahulu."
        )

    images = get_images()

    if not images:

        raise FileNotFoundError(
            f"Tidak ada gambar pada:\n"
            f"{IMAGE_DIR}"
        )

    print()
    print(
        f"Model : {MODEL_PATH}"
    )

    print(
        f"Folder image : {IMAGE_DIR}"
    )

    print(
        f"Jumlah gambar : "
        f"{len(images)}"
    )

    print()

    model = YOLO(
        str(MODEL_PATH)
    )

    for index, image_path in enumerate(
        images,
        start=1
    ):

        print("-" * 70)

        print(
            f"[{index}/{len(images)}] "
            f"{image_path.name}"
        )

        results = model.predict(

            source=str(
                image_path
            ),

            conf=CONFIDENCE,

            verbose=False
        )

        result = results[0]

        annotated_image = (
            result.plot()
        )

        print_detections(
            result
        )

        cv2.imshow(
            WINDOW_NAME,
            annotated_image
        )

        print()
        print(
            "ENTER / SPACE : "
            "gambar berikutnya"
        )

        print(
            "Q / ESC       : "
            "keluar"
        )

        key = (
            cv2.waitKey(0)
            & 0xFF
        )

        if (
            key == 27
            or key == ord("q")
            or key == ord("Q")
        ):

            break

    cv2.destroyAllWindows()

    print()
    print("=" * 70)
    print("INFERENCE SELESAI")
    print("=" * 70)


if __name__ == "__main__":

    main()