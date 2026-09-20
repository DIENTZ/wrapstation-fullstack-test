from pathlib import Path
import shutil
import tempfile

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset-yolo"

SPLITS = [
    "train",
    "valid",
    "test",
]

BACKUP_DIR = DATASET_DIR / "labels-segmentation-backup"

MIN_COORDINATES = 6  # minimal 3 titik polygon


def convert_line(line, label_path, line_number):
    parts = line.strip().split()

    if not parts:
        return None

    if len(parts) < 1:
        raise ValueError(
            f"{label_path.name}, baris {line_number}: "
            "baris kosong/tidak valid."
        )

    try:
        class_id = int(parts[0])
    except ValueError:
        raise ValueError(
            f"{label_path.name}, baris {line_number}: "
            f"class_id tidak valid: {parts[0]}"
        )

    coordinates = []

    for value in parts[1:]:
        try:
            coordinates.append(float(value))
        except ValueError:
            raise ValueError(
                f"{label_path.name}, baris {line_number}: "
                f"koordinat tidak valid: {value}"
            )

    if len(coordinates) < MIN_COORDINATES:
        raise ValueError(
            f"{label_path.name}, baris {line_number}: "
            f"polygon membutuhkan minimal 3 titik."
        )

    if len(coordinates) % 2 != 0:
        raise ValueError(
            f"{label_path.name}, baris {line_number}: "
            f"jumlah koordinat polygon harus genap, "
            f"ditemukan {len(coordinates)}."
        )

    xs = coordinates[0::2]
    ys = coordinates[1::2]

    for value in xs + ys:
        if value < 0 or value > 1:
            raise ValueError(
                f"{label_path.name}, baris {line_number}: "
                f"koordinat berada di luar range 0-1."
            )

    xmin = min(xs)
    xmax = max(xs)
    ymin = min(ys)
    ymax = max(ys)

    width = xmax - xmin
    height = ymax - ymin

    if width <= 0 or height <= 0:
        raise ValueError(
            f"{label_path.name}, baris {line_number}: "
            "bounding box memiliki ukuran 0."
        )

    x_center = (xmin + xmax) / 2
    y_center = (ymin + ymax) / 2

    return (
        f"{class_id} "
        f"{x_center:.10f} "
        f"{y_center:.10f} "
        f"{width:.10f} "
        f"{height:.10f}"
    )


def process_split(split):
    source_dir = DATASET_DIR / "labels" / split
    backup_dir = BACKUP_DIR / split

    if not source_dir.exists():
        raise FileNotFoundError(
            f"Folder label tidak ditemukan:\n{source_dir}"
        )

    label_files = sorted(source_dir.glob("*.txt"))

    print("=" * 70)
    print(f"CONVERT SPLIT: {split.upper()}")
    print("=" * 70)
    print(f"Label ditemukan: {len(label_files)}")

    # Validasi semua file terlebih dahulu
    converted_files = {}

    for label_path in label_files:

        lines = label_path.read_text(
            encoding="utf-8"
        ).splitlines()

        converted_lines = []

        for line_number, line in enumerate(lines, start=1):

            if not line.strip():
                continue

            converted = convert_line(
                line,
                label_path,
                line_number
            )

            if converted:
                converted_lines.append(converted)

        if not converted_lines:
            raise ValueError(
                f"Label kosong setelah konversi:\n{label_path}"
            )

        converted_files[label_path] = converted_lines

    print("[OK] Semua label berhasil dianalisis.")

    # Backup
    backup_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    for label_path in label_files:

        backup_path = backup_dir / label_path.name

        shutil.copy2(
            label_path,
            backup_path
        )

    print(
        f"[OK] Backup dibuat di:\n{backup_dir}"
    )

    # Tulis hasil conversion
    for label_path, converted_lines in converted_files.items():

        label_path.write_text(
            "\n".join(converted_lines) + "\n",
            encoding="utf-8"
        )

    print(
        f"[OK] {len(converted_files)} label berhasil "
        "diubah menjadi YOLO Detection."
    )
    print()


def main():

    print("=" * 70)
    print("WRAPSTATION - SEGMENTATION TO DETECTION")
    print("=" * 70)
    print()

    if not DATASET_DIR.exists():
        raise FileNotFoundError(
            f"Dataset tidak ditemukan:\n{DATASET_DIR}"
        )

    for split in SPLITS:
        process_split(split)

    print("=" * 70)
    print("KONVERSI SELESAI")
    print("=" * 70)
    print()
    print("Semua label sekarang menggunakan format:")
    print("class_id x_center y_center width height")
    print()
    print("Backup segmentation tersedia di:")
    print(BACKUP_DIR)


if __name__ == "__main__":
    main()