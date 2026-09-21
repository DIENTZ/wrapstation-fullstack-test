from pathlib import Path
import shutil
import yaml

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset-yolo"
LABELS_DIR = DATASET_DIR / "labels"
BACKUP_DIR = DATASET_DIR / "labels-segmentation-backup"

OLD_TO_NEW = {
    0: 0,   # Apple
    3: 1,   # Banana
    9: 2,   # Grapes
    6: 3,   # kiwi -> Kiwi
    7: 3,   # Kiwi -> Kiwi
    4: 4,   # Mango
    1: 5,   # orange -> Orange
    2: 5,   # Orange -> Orange
    5: 6,   # Pineapple
    10: 7,  # Sugerapple
    8: 8,   # Watermelon
}

NAMES = [
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

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def polygon_to_box(values):
    coords = list(map(float, values))
    if len(coords) < 6 or len(coords) % 2 != 0:
        raise ValueError("Invalid polygon coordinate count")

    xs = coords[0::2]
    ys = coords[1::2]

    x_min = max(0.0, min(xs))
    x_max = min(1.0, max(xs))
    y_min = max(0.0, min(ys))
    y_max = min(1.0, max(ys))

    width = x_max - x_min
    height = y_max - y_min

    if width <= 0 or height <= 0:
        raise ValueError("Invalid zero-area polygon")

    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2

    return (
        x_center,
        y_center,
        width,
        height,
    )


def repair_label(source, target):
    lines = source.read_text(
        encoding="utf-8",
        errors="ignore"
    ).splitlines()

    output = []

    for line_no, raw in enumerate(lines, start=1):
        line = raw.strip()

        # Empty labels are valid background images.
        if not line:
            continue

        parts = line.split()

        try:
            old_class = int(parts[0])
        except ValueError as exc:
            raise ValueError(
                f"{source}:{line_no}: invalid class id"
            ) from exc

        if old_class not in OLD_TO_NEW:
            raise ValueError(
                f"{source}:{line_no}: unknown class id "
                f"{old_class}. Expected one of "
                f"{sorted(OLD_TO_NEW)}."
            )

        new_class = OLD_TO_NEW[old_class]

        # Existing YOLO detection label.
        if len(parts) == 5:
            values = list(map(float, parts[1:]))
            if not all(0 <= v <= 1 for v in values):
                raise ValueError(
                    f"{source}:{line_no}: coordinate outside 0..1"
                )

            x, y, w, h = values
            if w <= 0 or h <= 0:
                raise ValueError(
                    f"{source}:{line_no}: invalid box size"
                )

        # YOLO segmentation polygon.
        elif len(parts) >= 7 and (len(parts) - 1) % 2 == 0:
            x, y, w, h = polygon_to_box(parts[1:])

        else:
            raise ValueError(
                f"{source}:{line_no}: unsupported label format "
                f"with {len(parts)} tokens"
            )

        output.append(
            f"{new_class} {x:.6f} {y:.6f} "
            f"{w:.6f} {h:.6f}"
        )

    target.write_text(
        "\n".join(output) + ("\n" if output else ""),
        encoding="utf-8"
    )


def main():
    if not LABELS_DIR.exists():
        raise FileNotFoundError(
            f"Labels directory not found: {LABELS_DIR}"
        )

    print("=" * 64)
    print("REPAIR YOLO DATASET")
    print("=" * 64)

    # One-time backup of original segmentation labels.
    if not BACKUP_DIR.exists():
        print(f"Creating backup: {BACKUP_DIR}")
        shutil.copytree(LABELS_DIR, BACKUP_DIR)

    counts = {
        "train": 0,
        "valid": 0,
        "test": 0,
    }

    for split in counts:
        split_dir = LABELS_DIR / split

        if not split_dir.exists():
            raise FileNotFoundError(
                f"Missing labels split: {split_dir}"
            )

        for source in split_dir.glob("*.txt"):
            repair_label(source, source)
            counts[split] += 1

    # Remove stale Ultralytics cache files.
    for cache in LABELS_DIR.rglob("*.cache"):
        cache.unlink()

    data = {
        "path": str(DATASET_DIR.resolve()),
        "train": "images/train",
        "val": "images/valid",
        "test": "images/test",
        "names": {
            i: name
            for i, name in enumerate(NAMES)
        },
    }

    with (DATASET_DIR / "data.yaml").open(
        "w",
        encoding="utf-8"
    ) as f:
        yaml.safe_dump(
            data,
            f,
            sort_keys=False,
            allow_unicode=True
        )

    print("\nRepaired labels:")
    for split, count in counts.items():
        print(f"  {split}: {count}")

    print("\nClasses:")
    for i, name in enumerate(NAMES):
        print(f"  {i}: {name}")

    print("\nREPAIR SELESAI.")
    print("Selanjutnya jalankan:")
    print("  python check_yolo_dataset.py")


if __name__ == "__main__":
    main()
