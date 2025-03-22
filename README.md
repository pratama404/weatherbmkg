# 🌦 WeatherBMKG

Aplikasi cuaca berbasis **Streamlit** yang menampilkan data prakiraan cuaca dari BMKG secara real-time.

## 📌 Fitur Utama
- **Menampilkan cuaca terkini** berdasarkan data BMKG
- **Informasi lokasi** (provinsi, kota/kabupaten, kecamatan, desa)
- **Visualisasi cuaca** dalam bentuk kartu informasi
- **Rekomendasi cuaca** berdasarkan kondisi saat ini
- **Tekanan udara, kecepatan angin, visibilitas**, dan parameter lainnya

## 🚀 Instalasi
### 1. Clone Repository
```bash
git clone https://github.com/pratama404/weatherbmkg.git
cd weatherbmkg
```

### 2. Buat Virtual Environment (Opsional)
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate    # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## ▶️ Menjalankan Aplikasi
```bash
streamlit run bmkg.py
```

## 🛠 Konfigurasi API
Pastikan Anda memiliki akses ke API BMKG dan telah menetapkan **URL API** dalam file `bmkg.py`:
```python
url = "https://api.bmkg.go.id/endpoint"
```

## 📌 Struktur Folder
```
weatherbmkg/
│── .venv/               # Virtual environment (opsional)
│── bmkg.py              # Main script untuk Streamlit
│── requirements.txt      # Daftar dependensi
│── README.md            # Dokumentasi proyek
```

## 💡 Kontribusi
Silakan buat **Pull Request** atau laporkan **Issues** jika menemukan bug atau ingin menambahkan fitur baru! 😊

## 📜 Lisensi
Proyek ini dirilis di bawah lisensi **MIT**.

---
✉️ Dibuat oleh [pratama404](https://github.com/pratama404)
