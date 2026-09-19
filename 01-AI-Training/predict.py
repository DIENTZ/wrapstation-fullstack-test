from pathlib import Path

import cv2
from ultralytics import YOLO


# ============================================================
# KONFIGURASI PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

# Model hasil training
MODEL_PATH = BASE_DIR / "best.pt"

# Direktori gambar test
IMAGE_DIR = BASE_DIR / "dataset" / "image" / "test"

# Alternatif jika folder test kosong
VAL_IMAGE_DIR = BASE_DIR / "dataset" / "image" / "val"


# ============================================================
# KONFIGURASI DETEKSI
# ============================================================

CONFIDENCE = 0.25

WINDOW_NAME = "Wrapstation - Fruit Detection"


# ============================================================
# MENCARI GAMBAR
# ============================================================

def get_images():

    image_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".webp"
    }

    images = []

    # Prioritas folder test
    if IMAGE_DIR.exists():

        for file in IMAGE_DIR.iterdir():

            if file.is_file() and file.suffix.lower() in image_extensions:
                images.append(file)

    # Jika test kosong, gunakan validation
    if not images and VAL_IMAGE_DIR.exists():

        for file in VAL_IMAGE_DIR.iterdir():

            if file.is_file() and file.suffix.lower() in image_extensions:
                images.append(file)

    return sorted(images)


# ============================================================
# PREDICTION
# ============================================================

def run_detection():

    print("=" * 60)
    print("WRAPSTATION - FRUIT OBJECT DETECTION")
    print("=" * 60)

    # Cek model
    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"Model tidak ditemukan:\n{MODEL_PATH}\n\n"
            "Jalankan train.py terlebih dahulu."
        )

    # Cari gambar
    images = get_images()

    if not images:

        raise FileNotFoundError(
            "Tidak ditemukan gambar pada folder test atau val."
        )

    print(f"Model : {MODEL_PATH}")
    print(f"Jumlah gambar: {len(images)}")
    print()

    # Load model
    model = YOLO(str(MODEL_PATH))

    # Proses gambar satu per satu
    for image_path in images:

        print("-" * 60)
        print(f"Memproses: {image_path.name}")

        # Jalankan YOLO
        results = model.predict(
            source=str(image_path),
            conf=CONFIDENCE,
            verbose=False
        )

        # Ambil hasil pertama
        result = results[0]

        # Buat gambar dengan bounding box + label
        annotated_image = result.plot()

        # Tampilkan hasil deteksi
        cv2.imshow(
            WINDOW_NAME,
            annotated_image
        )

        # Informasi hasil deteksi
        if result.boxes is not None and len(result.boxes) > 0:

            print("Objek terdeteksi:")

            for box in result.boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                class_name = result.names[class_id]

                print(
                    f"  - {class_name}: "
                    f"{confidence * 100:.2f}%"
                )

        else:

            print("Tidak ada objek buah yang terdeteksi.")

        print()
        print("Tekan tombol:")
        print("  ENTER / SPACE = gambar berikutnya")
        print("  Q / ESC       = keluar")

        key = cv2.waitKey(0) & 0xFF

        # ESC atau Q
        if key == 27 or key == ord("q"):

            break

    cv2.destroyAllWindows()

    print("=" * 60)
    print("INFERENCE SELESAI")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    run_detection()