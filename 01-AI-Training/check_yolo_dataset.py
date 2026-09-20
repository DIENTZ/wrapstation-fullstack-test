from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset-yolo"

IMAGE_DIR = DATASET_DIR / "images"
LABEL_DIR = DATASET_DIR / "labels"

SPLITS = {
    "train": "train",
    "val": "valid",
    "test": "test",
}

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
}


def get_images(folder):
    if not folder.exists():
        return []

    return [
        file
        for file in folder.iterdir()
        if file.is_file()
        and file.suffix.lower() in IMAGE_EXTENSIONS
    ]


def validate_label_file(label_path, number_of_classes):
    errors = []

    try:
        lines = label_path.read_text(
            encoding="utf-8"
        ).splitlines()

    except Exception as error:
        return [f"Gagal membaca file: {error}"]

    if not lines:
        return ["File label kosong."]

    for line_number, line in enumerate(lines, start=1):

        line = line.strip()

        if not line:
            continue

        parts = line.split()

        # YOLO Detection harus 5 nilai
        if len(parts) != 5:
            errors.append(
                f"Baris {line_number}: "
                f"harus 5 nilai, ditemukan {len(parts)}"
            )
            continue

        try:
            class_id = int(parts[0])

            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])

        except ValueError:
            errors.append(
                f"Baris {line_number}: "
                "nilai bukan angka yang valid."
            )
            continue

        if class_id < 0 or class_id >= number_of_classes:
            errors.append(
                f"Baris {line_number}: "
                f"class_id {class_id} di luar range."
            )

        coordinates = [
            x_center,
            y_center,
            width,
            height,
        ]

        for value in coordinates:

            if value < 0 or value > 1:

                errors.append(
                    f"Baris {line_number}: "
                    "koordinat harus berada antara 0 dan 1."
                )

                break

        if width <= 0:
            errors.append(
                f"Baris {line_number}: width harus > 0."
            )

        if height <= 0:
            errors.append(
                f"Baris {line_number}: height harus > 0."
            )

    return errors


def check_split(
    name,
    folder_name,
    number_of_classes
):

    print("=" * 70)
    print(f"CHECK DATASET: {name.upper()}")
    print("=" * 70)

    image_dir = IMAGE_DIR / folder_name
    label_dir = LABEL_DIR / folder_name

    print(f"Image folder : {image_dir}")
    print(f"Label folder : {label_dir}")
    print()

    if not image_dir.exists():

        print(
            "[ERROR] Folder image tidak ditemukan."
        )

        return False

    if not label_dir.exists():

        print(
            "[ERROR] Folder label tidak ditemukan."
        )

        return False

    images = get_images(image_dir)

    label_files = list(
        label_dir.glob("*.txt")
    )

    print(
        f"Jumlah gambar : {len(images)}"
    )

    print(
        f"Jumlah label  : {len(label_files)}"
    )

    print()

    missing_labels = []

    invalid_labels = []

    for image in images:

        label_path = (
            label_dir
            / f"{image.stem}.txt"
        )

        if not label_path.exists():

            missing_labels.append(
                image.name
            )

            continue

        errors = validate_label_file(
            label_path,
            number_of_classes
        )

        if errors:

            invalid_labels.append(
                (
                    image.name,
                    errors
                )
            )

    print(
        f"Label hilang      : "
        f"{len(missing_labels)}"
    )

    print(
        f"Label tidak valid : "
        f"{len(invalid_labels)}"
    )

    if missing_labels:

        print(
            "\nContoh label yang hilang:"
        )

        for filename in missing_labels[:5]:

            print(
                f"  - {filename}"
            )

    if invalid_labels:

        print(
            "\nContoh label tidak valid:"
        )

        for filename, errors in invalid_labels[:5]:

            print(
                f"\n  {filename}"
            )

            for error in errors[:5]:

                print(
                    f"    - {error}"
                )

    success = (
        len(images) > 0
        and len(missing_labels) == 0
        and len(invalid_labels) == 0
    )

    if success:

        print(
            "\n[OK] Dataset split valid."
        )

    else:

        print(
            "\n[ERROR] Dataset split belum valid."
        )

    print()

    return success


def main():

    print("=" * 70)
    print("WRAPSTATION - YOLO DATASET VALIDATOR")
    print("=" * 70)
    print()

    if not DATASET_DIR.exists():

        raise FileNotFoundError(
            f"Dataset tidak ditemukan:\n"
            f"{DATASET_DIR}"
        )

    # 11 class sesuai data.yaml saat ini
    number_of_classes = 11

    results = []

    for name, folder_name in SPLITS.items():

        result = check_split(
            name,
            folder_name,
            number_of_classes
        )

        results.append(result)

    print("=" * 70)
    print("HASIL AKHIR")
    print("=" * 70)

    if all(results):

        print(
            "[OK] SEMUA DATASET VALID."
        )

        print(
            "[OK] Dataset siap untuk training."
        )

    else:

        print(
            "[ERROR] Dataset masih bermasalah."
        )


if __name__ == "__main__":
    main()