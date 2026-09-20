from pathlib import Path
import shutil
import sys

BASE_DIR = Path(__file__).resolve().parent
DATASET = BASE_DIR / "dataset-yolo"
LABELS = DATASET / "labels"
BACKUP = DATASET / "labels-segmentation-backup"
SPLITS = ("train", "valid", "test")
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
NUM_CLASSES = 11

def fail(msg):
    print(f"[ERROR] {msg}")
    sys.exit(1)

def convert_line(line, path, line_no):
    p = line.strip().split()
    if not p:
        return None
    try:
        cls = int(p[0])
        vals = [float(x) for x in p[1:]]
    except ValueError:
        raise ValueError(f"{path.name}:{line_no} bukan angka yang valid")

    if not 0 <= cls < NUM_CLASSES:
        raise ValueError(f"{path.name}:{line_no} class_id={cls} di luar 0..{NUM_CLASSES-1}")

    if len(vals) == 4:
        x, y, w, h = vals
    else:
        if len(vals) < 6 or len(vals) % 2 != 0:
            raise ValueError(f"{path.name}:{line_no} jumlah koordinat polygon tidak valid: {len(vals)}")
        if any(v < 0 or v > 1 for v in vals):
            raise ValueError(f"{path.name}:{line_no} koordinat polygon harus 0..1")
        xs = vals[0::2]
        ys = vals[1::2]
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)
        x = (xmin + xmax) / 2.0
        y = (ymin + ymax) / 2.0
        w = xmax - xmin
        h = ymax - ymin

    if not all(0 <= v <= 1 for v in (x, y, w, h)):
        raise ValueError(f"{path.name}:{line_no} bbox di luar 0..1")
    if w <= 0 or h <= 0:
        raise ValueError(f"{path.name}:{line_no} bbox width/height <= 0")

    return f"{cls} {x:.10f} {y:.10f} {w:.10f} {h:.10f}"

def process_split(split):
    src = LABELS / split
    backup = BACKUP / split
    if not src.exists():
        fail(f"Folder label tidak ditemukan: {src}")

    files = sorted(src.glob("*.txt"))
    if not files:
        fail(f"Tidak ada label .txt di {src}")

    backup.mkdir(parents=True, exist_ok=True)
    converted = 0

    for path in files:
        original = path.read_text(encoding="utf-8")
        out = []
        for no, line in enumerate(original.splitlines(), 1):
            if line.strip():
                out.append(convert_line(line, path, no))
        if not out:
            fail(f"Label kosong: {path}")

        backup_path = backup / path.name
        if not backup_path.exists():
            shutil.copy2(path, backup_path)

        path.write_text("\n".join(out) + "\n", encoding="utf-8")
        converted += 1

    return converted

def validate_split(split):
    img_dir = DATASET / "images" / split
    lbl_dir = LABELS / split
    if not img_dir.exists():
        fail(f"Folder image tidak ditemukan: {img_dir}")

    images = sorted(p for p in img_dir.iterdir()
                    if p.is_file() and p.suffix.lower() in IMAGE_EXTS)
    labels = sorted(lbl_dir.glob("*.txt"))
    missing = []
    invalid = []

    for image in images:
        label = lbl_dir / f"{image.stem}.txt"
        if not label.exists():
            missing.append(image.name)
            continue

        for no, line in enumerate(label.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                invalid.append(f"{label.name}:{no} kosong")
                continue
            p = line.split()
            if len(p) != 5:
                invalid.append(f"{label.name}:{no} harus 5 nilai, ditemukan {len(p)}")
                continue
            try:
                cls = int(p[0])
                vals = [float(v) for v in p[1:]]
            except ValueError:
                invalid.append(f"{label.name}:{no} bukan angka")
                continue
            if not 0 <= cls < NUM_CLASSES:
                invalid.append(f"{label.name}:{no} class_id {cls} di luar range")
                continue
            if not all(0 <= v <= 1 for v in vals):
                invalid.append(f"{label.name}:{no} koordinat di luar 0..1")
                continue
            if vals[2] <= 0 or vals[3] <= 0:
                invalid.append(f"{label.name}:{no} width/height tidak valid")

    print(f"{split.upper():5} | images={len(images):4} labels={len(labels):4} "
          f"missing={len(missing):3} invalid={len(invalid):3}")
    if missing:
        print("  Missing:", missing[:3])
    if invalid:
        print("  Invalid:", invalid[:3])
    return not missing and not invalid and len(images) == len(labels)

def main():
    print("=" * 72)
    print("WRAPSTATION - FIX YOLO SEGMENTATION -> DETECTION")
    print("=" * 72)

    if not DATASET.exists():
        fail(f"dataset-yolo tidak ditemukan: {DATASET}")

    print("\n[1/4] Backup + convert label...")
    for split in SPLITS:
        n = process_split(split)
        print(f"[OK] {split}: {n} label diproses")

    print("\n[2/4] Hapus cache YOLO...")
    removed = 0
    for p in LABELS.rglob("*.cache"):
        try:
            p.unlink()
            removed += 1
        except OSError as e:
            print(f"[WARNING] Tidak bisa hapus {p}: {e}")
    print(f"[OK] Cache dihapus: {removed}")

    print("\n[3/4] Validasi final...")
    results = [validate_split(split) for split in SPLITS]

    print("\n[4/4] HASIL")
    print("-" * 72)
    if all(results):
        print("[OK] DATASET SUDAH VALID.")
        print("[OK] Semua label sekarang YOLO Detection (5 nilai).")
        print("[OK] Missing label = 0.")
        print("[OK] Invalid label = 0.")
        print(f"[OK] Backup label asli: {BACKUP}")
        print("\nLangkah berikutnya:")
        print("  python check_yolo_dataset.py")
        print("  python predict.py")
        print("  (training ulang hanya jika ingin meningkatkan akurasi)")
        return 0

    print("[ERROR] Dataset masih bermasalah. Jangan training dulu.")
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
