from pathlib import Path
import csv
import shutil


# ============================================================
# PREPARE FRUIT CLASSIFICATION DATASET
# ============================================================
#
# Script ini digunakan untuk membaca dataset buah yang memiliki
# format _classes.csv kemudian mengelompokkan gambar berdasarkan
# kelas buah.
#
# Struktur input:
#
# dataset/
# ├── image/
# │   ├── train/
# │   ├── val/
# │   └── test/
# │
# └── labels/
#     ├── train/
#     │   └── _classes.csv
#     ├── val/
#     │   └── _classes.csv
#     └── test/
#         └── _classes.csv
#
# Output:
#
# dataset-classification/
# ├── train/
# │   ├── Apple/
# │   ├── Banana/
# │   ├── Grapes/
# │   ├── Kiwi/
# │   ├── Mango/
# │   ├── Orange/
# │   ├── Pineapple/
# │   ├── Sugerapple/
# │   └── Watermelon/
# │
# ├── val/
# │   └── ...
# │
# └── test/
#     └── ...
#
# ============================================================


# ============================================================
# KONFIGURASI PATH
# ============================================================

# Folder tempat file prepare_classification.py berada
BASE_DIR = Path(__file__).resolve().parent


# Folder dataset asli
DATASET_DIR = BASE_DIR / "dataset"


# Folder gambar
IMAGE_DIR = DATASET_DIR / "images"


# Folder label CSV
LABEL_DIR = DATASET_DIR / "labels"


# Folder hasil dataset classification
OUTPUT_DIR = BASE_DIR / "dataset-classification"


# ============================================================
# NAMA KELAS BUAH
# ============================================================

CLASS_NAMES = [
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


# ============================================================
# FUNGSI MENENTUKAN KELAS GAMBAR
# ============================================================

def get_class_from_row(row):
    """
    Menentukan kelas gambar berdasarkan isi satu baris CSV.

    Contoh data CSV:

    filename,Apple,Banana,Grapes,Kiwi,Mango,Orange,Pineapple,Sugerapple,Watermelon

    image.jpg,0,0,1,0,0,0,0,0,0

    Maka hasilnya:

    Grapes
    """

    # --------------------------------------------------------
    # Bersihkan nama kolom dan nilai CSV
    # --------------------------------------------------------

    cleaned_row = {}

    for key, value in row.items():

        # Abaikan key kosong
        if key is None:
            continue

        # Bersihkan nama kolom
        clean_key = str(key).strip()

        # Bersihkan nilai
        clean_value = str(value).strip()

        cleaned_row[clean_key] = clean_value

    # --------------------------------------------------------
    # Periksa setiap kelas
    # --------------------------------------------------------

    for class_name in CLASS_NAMES:

        # Ambil nilai berdasarkan nama kelas
        value = cleaned_row.get(class_name)

        # Jika kolom tidak ada
        if value is None:
            continue

        # Bersihkan nilai
        value = str(value).strip()

        # ----------------------------------------------------
        # Format normal
        # ----------------------------------------------------

        if value == "1":
            return class_name

        # ----------------------------------------------------
        # Antisipasi format 1.0
        # ----------------------------------------------------

        try:

            numeric_value = float(value)

            if numeric_value == 1:
                return class_name

        except ValueError:

            pass

    # Jika tidak ada kelas yang ditemukan
    return None


# ============================================================
# FUNGSI MEMBUAT FOLDER OUTPUT
# ============================================================

def create_directories():
    """
    Membuat seluruh folder dataset classification.
    """

    print("=" * 60)
    print("MEMBUAT FOLDER DATASET CLASSIFICATION")
    print("=" * 60)

    # --------------------------------------------------------
    # Buat folder train, val, test
    # --------------------------------------------------------

    for split_name in [
        "train",
        "val",
        "test"
    ]:

        # ----------------------------------------------------
        # Buat folder untuk setiap kelas
        # ----------------------------------------------------

        for class_name in CLASS_NAMES:

            folder = (
                OUTPUT_DIR
                / split_name
                / class_name
            )

            folder.mkdir(
                parents=True,
                exist_ok=True
            )

    print()
    print("Folder output berhasil dibuat:")
    print(OUTPUT_DIR)
    print()


# ============================================================
# FUNGSI MEMPROSES DATASET
# ============================================================

def prepare_split(
    split_name,
    image_dir,
    csv_path
):
    """
    Memproses satu bagian dataset:

    train
    val
    test

    CSV digunakan untuk menentukan kelas setiap gambar.
    """

    print("=" * 60)
    print(
        f"MEMPROSES DATASET: "
        f"{split_name.upper()}"
    )
    print("=" * 60)

    # --------------------------------------------------------
    # CEK FOLDER GAMBAR
    # --------------------------------------------------------

    if not image_dir.exists():

        raise FileNotFoundError(
            f"Folder gambar tidak ditemukan:\n"
            f"{image_dir}"
        )

    # --------------------------------------------------------
    # CEK FILE CSV
    # --------------------------------------------------------

    if not csv_path.exists():

        raise FileNotFoundError(
            f"CSV tidak ditemukan:\n"
            f"{csv_path}"
        )

    # --------------------------------------------------------
    # COUNTER
    # --------------------------------------------------------

    copied = 0
    skipped = 0

    # Digunakan untuk menampilkan contoh data CSV
    first_row = True

    # ========================================================
    # BUKA CSV
    # ========================================================

    with csv_path.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        # ----------------------------------------------------
        # Baca CSV
        # ----------------------------------------------------

        reader = csv.DictReader(file)

        # ----------------------------------------------------
        # CEK HEADER
        # ----------------------------------------------------

        if not reader.fieldnames:

            raise ValueError(
                f"Header CSV tidak ditemukan:\n"
                f"{csv_path}"
            )

        # ----------------------------------------------------
        # Tampilkan header asli
        # ----------------------------------------------------

        print()
        print("HEADER ASLI CSV:")
        print(reader.fieldnames)
        print()

        # ----------------------------------------------------
        # Bersihkan nama header
        # ----------------------------------------------------

        headers = [
            str(header).strip()
            for header in reader.fieldnames
            if header
        ]

        print("KOLOM CSV SETELAH DIBERSIHKAN:")
        print(headers)
        print()

        # ----------------------------------------------------
        # Cek kolom kelas
        # ----------------------------------------------------

        print("PEMERIKSAAN KOLOM KELAS:")

        for class_name in CLASS_NAMES:

            if class_name in headers:

                print(
                    f"[OK] {class_name}"
                )

            else:

                print(
                    f"[WARNING] "
                    f"Kolom tidak ditemukan: "
                    f"{class_name}"
                )

        print()

        # ====================================================
        # BACA SETIAP BARIS CSV
        # ====================================================

        for row in reader:

            # ------------------------------------------------
            # Tampilkan satu contoh baris
            # ------------------------------------------------

            if first_row:

                print("CONTOH DATA CSV:")

                print(row)

                print()

                first_row = False

            # ------------------------------------------------
            # Ambil nama file
            # ------------------------------------------------

            filename = row.get("filename")

            # ------------------------------------------------
            # Bersihkan nama file
            # ------------------------------------------------

            if filename:

                filename = filename.strip()

            # ------------------------------------------------
            # Jika filename kosong
            # ------------------------------------------------

            if not filename:

                print(
                    "[SKIP] Filename kosong"
                )

                skipped += 1

                continue

            # ------------------------------------------------
            # Tentukan kelas
            # ------------------------------------------------

            class_name = get_class_from_row(row)

            # ------------------------------------------------
            # Jika kelas tidak ditemukan
            # ------------------------------------------------

            if not class_name:

                print(
                    "[SKIP] Kelas tidak ditemukan: "
                    f"{filename}"
                )

                skipped += 1

                continue

            # ------------------------------------------------
            # Lokasi gambar asli
            # ------------------------------------------------

            source = image_dir / filename

            # ------------------------------------------------
            # Cek apakah gambar tersedia
            # ------------------------------------------------

            if not source.exists():

                print(
                    "[SKIP] Gambar tidak ditemukan: "
                    f"{filename}"
                )

                skipped += 1

                continue

            # ------------------------------------------------
            # Lokasi tujuan
            # ------------------------------------------------

            destination = (
                OUTPUT_DIR
                / split_name
                / class_name
                / filename
            )

            # ------------------------------------------------
            # Buat folder tujuan
            # ------------------------------------------------

            destination.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            # ------------------------------------------------
            # Salin gambar
            # ------------------------------------------------

            shutil.copy2(
                source,
                destination
            )

            # ------------------------------------------------
            # Tambahkan counter
            # ------------------------------------------------

            copied += 1

    # ========================================================
    # HASIL PROSES
    # ========================================================

    print()
    print("-" * 60)
    print(
        f"HASIL DATASET {split_name.upper()}"
    )
    print("-" * 60)

    print(
        f"Gambar berhasil diproses : "
        f"{copied}"
    )

    print(
        f"Gambar dilewati           : "
        f"{skipped}"
    )

    print()


# ============================================================
# FUNGSI MENAMPILKAN RINGKASAN DATASET
# ============================================================

def show_dataset_summary():
    """
    Menampilkan jumlah gambar pada setiap kelas.
    """

    print("=" * 60)
    print("RINGKASAN DATASET")
    print("=" * 60)

    # --------------------------------------------------------
    # Periksa train, val, test
    # --------------------------------------------------------

    for split_name in [
        "train",
        "val",
        "test"
    ]:

        split_dir = (
            OUTPUT_DIR
            / split_name
        )

        print()
        print(
            f"[{split_name.upper()}]"
        )

        total = 0

        # ----------------------------------------------------
        # Periksa setiap kelas
        # ----------------------------------------------------

        for class_name in CLASS_NAMES:

            class_dir = (
                split_dir
                / class_name
            )

            # Jika folder tidak ada
            if not class_dir.exists():

                count = 0

            else:

                count = sum(
                    1
                    for file in class_dir.iterdir()
                    if file.is_file()
                )

            print(
                f"{class_name:12} : "
                f"{count}"
            )

            total += count

        print(
            f"{'TOTAL':12} : "
            f"{total}"
        )

    print()


# ============================================================
# FUNGSI UTAMA
# ============================================================

def main():

    print()
    print("=" * 60)
    print("PREPARE FRUIT CLASSIFICATION DATASET")
    print("=" * 60)
    print()

    # --------------------------------------------------------
    # Tampilkan lokasi
    # --------------------------------------------------------

    print("BASE DIRECTORY:")
    print(BASE_DIR)
    print()

    print("DATASET DIRECTORY:")
    print(DATASET_DIR)
    print()

    print("IMAGE DIRECTORY:")
    print(IMAGE_DIR)
    print()

    print("LABEL DIRECTORY:")
    print(LABEL_DIR)
    print()

    print("OUTPUT DIRECTORY:")
    print(OUTPUT_DIR)
    print()

    # ========================================================
    # CEK DATASET UTAMA
    # ========================================================

    if not DATASET_DIR.exists():

        raise FileNotFoundError(
            "Folder dataset tidak ditemukan:\n"
            f"{DATASET_DIR}"
        )

    # ========================================================
    # CEK FOLDER IMAGE
    # ========================================================

    if not IMAGE_DIR.exists():

        raise FileNotFoundError(
            "Folder image tidak ditemukan:\n"
            f"{IMAGE_DIR}"
        )

    # ========================================================
    # CEK FOLDER LABEL
    # ========================================================

    if not LABEL_DIR.exists():

        raise FileNotFoundError(
            "Folder labels tidak ditemukan:\n"
            f"{LABEL_DIR}"
        )

    # ========================================================
    # BUAT FOLDER OUTPUT
    # ========================================================

    create_directories()

    # ========================================================
    # PROSES TRAIN
    # ========================================================

    train_image_dir = (
        IMAGE_DIR
        / "train"
    )

    train_csv = (
        LABEL_DIR
        / "train"
        / "_classes.csv"
    )

    prepare_split(
        split_name="train",
        image_dir=train_image_dir,
        csv_path=train_csv
    )

    # ========================================================
    # PROSES VALIDATION
    # ========================================================

    val_image_dir = (
        IMAGE_DIR
        / "val"
    )

    val_csv = (
        LABEL_DIR
        / "val"
        / "_classes.csv"
    )

    prepare_split(
        split_name="val",
        image_dir=val_image_dir,
        csv_path=val_csv
    )

    # ========================================================
    # PROSES TEST
    # ========================================================

    test_image_dir = (
        IMAGE_DIR
        / "test"
    )

    test_csv = (
        LABEL_DIR
        / "test"
        / "_classes.csv"
    )

    prepare_split(
        split_name="test",
        image_dir=test_image_dir,
        csv_path=test_csv
    )

    # ========================================================
    # TAMPILKAN RINGKASAN
    # ========================================================

    show_dataset_summary()

    # ========================================================
    # SELESAI
    # ========================================================

    print("=" * 60)
    print("PREPARE DATASET SELESAI")
    print("=" * 60)
    print()

    print(
        "Dataset classification tersedia di:"
    )

    print(OUTPUT_DIR)

    print()

    print(
        "Struktur output:"
    )

    print()
    print("dataset-classification/")
    print("│")
    print("├── train/")
    print("│   ├── Apple/")
    print("│   ├── Banana/")
    print("│   ├── Grapes/")
    print("│   ├── Kiwi/")
    print("│   ├── Mango/")
    print("│   ├── Orange/")
    print("│   ├── Pineapple/")
    print("│   ├── Sugerapple/")
    print("│   └── Watermelon/")
    print("│")
    print("├── val/")
    print("│   ├── Apple/")
    print("│   ├── Banana/")
    print("│   ├── Grapes/")
    print("│   ├── Kiwi/")
    print("│   ├── Mango/")
    print("│   ├── Orange/")
    print("│   ├── Pineapple/")
    print("│   ├── Sugerapple/")
    print("│   └── Watermelon/")
    print("│")
    print("└── test/")
    print("    ├── Apple/")
    print("    ├── Banana/")
    print("    ├── Grapes/")
    print("    ├── Kiwi/")
    print("    ├── Mango/")
    print("    ├── Orange/")
    print("    ├── Pineapple/")
    print("    ├── Sugerapple/")
    print("    └── Watermelon/")
    print()

    print(
        "Jangan menjalankan train.py "
        "sebelum hasil dataset diperiksa."
    )

    print()


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()