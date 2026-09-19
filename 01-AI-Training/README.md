# AI Training - Fruit Object Detection

Bagian ini merupakan implementasi soal AI Training pada technical test
Full Stack Developer - Wrapstation.

## Deskripsi

Sistem ini merupakan Object Detection berbasis YOLO yang digunakan untuk
mendeteksi dan mengklasifikasikan objek buah pada gambar.

Dataset yang digunakan:

Fruits by YOLO - Fruits Detection

https://www.kaggle.com/datasets/kapturovalexander/fruits-by-yolo-fruits-detection

Dataset memiliki 9 kelas:

- Apple
- Banana
- Grapes
- Kiwi
- Mango
- Orange
- Pineapple
- Sugerapple
- Watermelon

## Teknologi

- Python
- Ultralytics YOLO
- OpenCV
- PyYAML
- Pillow

## Struktur Folder

```text
01-AI-Training/
│
├── dataset/
│   ├── image/
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   │
│   ├── labels/
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   │
│   └── data.yaml
│
├── best.pt
├── train.py
├── predict.py
├── requirements.txt
└── README.md
```
