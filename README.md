# Wrapstation Fullstack Test

Repository ini berisi kumpulan implementasi dan pengembangan aplikasi yang mencakup **AI Training, IoT Camera, serta aplikasi Fullstack berbasis CodeIgniter**.

Project ini dibuat sebagai bagian dari technical test dan pengembangan aplikasi dengan beberapa teknologi yang saling berkaitan, mulai dari pemrosesan data dan AI, pengambilan gambar menggunakan kamera, hingga pengelolaan data melalui aplikasi web dan database.

---

## 📌 Project Overview

Repository ini terdiri dari tiga bagian utama:

1. **AI Training**
   - Persiapan project untuk proses training dan inference model AI.
   - Berisi struktur dasar untuk pengembangan model menggunakan Python.

2. **IoT Camera**
   - Aplikasi untuk mengakses webcam secara real-time.
   - Menggunakan Python dan OpenCV.
   - Mendukung pengambilan gambar secara manual maupun burst capture.

3. **CodeIgniter Fullstack Application**
   - Aplikasi web untuk pengelolaan data pengguna, produk, dan transaksi.
   - Menggunakan CodeIgniter 4 dan database MySQL.
   - Menyediakan dashboard serta fitur CRUD.

---

## 🗂️ Project Structure

```text
wrapstation-fullstack-test/
│
├── 01-AI-Training/
│   ├── README.md
│   ├── train.py
│   ├── predict.py
│   ├── requirements.txt
│   └── best.pt
│
├── 02-IoT-Camera/
│   ├── captures/
│   ├── camera.py
│   ├── requirements.txt
│   ├── .gitignore
│   └── README.md
│
├── 03-CodeIgniter/
│   ├── app/
│   │   ├── Controllers/
│   │   ├── Models/
│   │   └── Views/
│   │
│   ├── public/
│   ├── tests/
│   ├── writable/
│   ├── composer.json
│   └── spark
│
├── .gitignore
└── README.md


🤖 01 - AI Training

Folder ini disiapkan untuk kebutuhan pengembangan dan pelatihan model AI menggunakan Python.

Struktur project menyediakan file untuk:

Training model
Prediction / inference
Dependency management
Penyimpanan model hasil training
Teknologi
Python
Machine Learning / AI
Model Training


📷 02 - IoT Camera

IoT Camera merupakan aplikasi berbasis Python untuk mengakses dan mengontrol webcam secara real-time.

Fitur :
Real-time camera preview
Webcam access menggunakan OpenCV
Image capture
Keyboard capture
Burst capture
Konfigurasi resolusi kamera
Automatic image filename
Automatic capture directory

Teknologi:
Python
OpenCV
Tkinter
Pillow

🌐 03 - CodeIgniter Fullstack Application

Bagian ini merupakan aplikasi web fullstack untuk pengelolaan data pengguna, produk, dan transaksi.

Aplikasi dibangun menggunakan CodeIgniter 4 dengan database MySQL.

Fitur Utama
Dashboard

Dashboard menampilkan ringkasan:

Jumlah pengguna
Jumlah produk
Jumlah transaksi
Informasi transaksi terbaru
User Management

Menyediakan fitur:

Menampilkan data pengguna
Menambahkan pengguna
Mengubah pengguna
Menghapus pengguna
Product Management

Menyediakan fitur:

Menampilkan data produk
Menambahkan produk
Mengubah produk
Menghapus produk
Pengelolaan stok produk
Transaction Management

Menyediakan fitur:

Membuat transaksi
Memilih pengguna
Memilih produk
Menentukan jumlah transaksi
Menentukan metode pembayaran
Menghitung total harga
Mengurangi stok secara otomatis
Mengembalikan stok ketika transaksi dihapus

🛠️ Teknologi
Backend
PHP
CodeIgniter 4
Composer
Database
MySQL
Frontend
HTML
CSS
JavaScript
Development Environment
Laragon
Visual Studio Code