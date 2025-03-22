import streamlit as st
import requests
import json
import pandas as pd
import datetime, pytz

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Cuaca BMKG", layout="wide")

# # URL API BMKG
# url = "https://cuaca.bmkg.go.id/api/df/v1/forecast/adm?adm1=35&adm2=35.78&adm3=35.78.03&adm4=35.78.03.1001"

# URL CSV wilayah dari GitHub
CSV_URL = "https://raw.githubusercontent.com/kodewilayah/permendagri-72-2019/main/dist/base.csv"

# Load data wilayah dari URL
@st.cache_data
def load_data():
    return pd.read_csv(CSV_URL, dtype=str, names=["kode", "nama"], header=None)

data_wilayah = load_data()
# Menentukan level administratif berdasarkan panjang kode
data_wilayah["level"] = data_wilayah["kode"].apply(lambda x: 
    "provinsi" if len(x) == 2 else
    "kotakab" if len(x) == 5 else
    "kecamatan" if len(x) == 8 else
    "desa" if len(x) == 13 else "lainnya"
)

# Dropdown untuk pemilihan provinsi
provinsi_list = data_wilayah[data_wilayah["level"] == "provinsi"]["nama"].unique()
provinsi = st.sidebar.selectbox("Pilih Provinsi", sorted(provinsi_list))

# Cari kode provinsi berdasarkan nama yang dipilih
kode_provinsi = data_wilayah[(data_wilayah["level"] == "provinsi") & 
                             (data_wilayah["nama"] == provinsi)]["kode"].values[0]

# Dropdown untuk pemilihan Kota/Kabupaten berdasarkan kode provinsi
kotkab_list = data_wilayah[(data_wilayah["level"] == "kotakab") & 
                           (data_wilayah["kode"].str.startswith(kode_provinsi))]["nama"].unique()
kotkab = st.sidebar.selectbox("Pilih Kota/Kabupaten", sorted(kotkab_list))

# Cari kode kotkab
kode_kotkab = data_wilayah[(data_wilayah["level"] == "kotakab") & 
                           (data_wilayah["nama"] == kotkab)]["kode"].values[0]

# Dropdown untuk Kecamatan berdasarkan kode kotkab
kecamatan_list = data_wilayah[(data_wilayah["level"] == "kecamatan") & 
                              (data_wilayah["kode"].str.startswith(kode_kotkab))]["nama"].unique()
kecamatan = st.sidebar.selectbox("Pilih Kecamatan", sorted(kecamatan_list))

# Cari kode kecamatan
kode_kecamatan = data_wilayah[(data_wilayah["level"] == "kecamatan") & 
                              (data_wilayah["nama"] == kecamatan)]["kode"].values[0]

# Dropdown untuk Desa berdasarkan kode kecamatan
desa_list = data_wilayah[(data_wilayah["level"] == "desa") & 
                         (data_wilayah["kode"].str.startswith(kode_kecamatan))]["nama"].unique()
desa = st.sidebar.selectbox("Pilih Desa", sorted(desa_list))

# Cari kode wilayah desa
kode_wilayah_data = data_wilayah[(data_wilayah["level"] == "desa") & 
                                 (data_wilayah["nama"] == desa)]

# Menampilkan hasil kode wilayah
if kode_wilayah_data.empty:
    st.error("⚠️ Data wilayah tidak ditemukan. Coba pilih lokasi lain.")
else:
    kode_wilayah = kode_wilayah_data["kode"].values[0]
    url = f"https://cuaca.bmkg.go.id/api/df/v1/forecast/adm?adm4={kode_wilayah}"
    st.write(f"📌 Kode Wilayah: {kode_wilayah}")
    st.write(f"🌍 API BMKG: {url}")




st.title("🌦 **Dashboard Prakiraan Cuaca BMKG**")
st.write("📡 Data prakiraan cuaca per jam dari BMKG.")

# Fungsi untuk menampilkan kartu cuaca
def display_weather_card(title, value, description, color):
    st.markdown(
        f"""
        <div style="
            background-color:{color}; 
            padding:15px; 
            border-radius:10px; 
            text-align:center; 
            color:white;
            font-size:18px;
            margin-bottom:10px;
        ">
            <h4>{title}</h4>
            <h2>{value}</h2>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Mapping kondisi cuaca ke emoji
weather_icons = {
    "Berawan": "☁️",
    "Cerah": "☀️",
    "Hujan": "🌧️",
    "Petir": "🌩️",
    "Kabut": "🌫️",
    "Hujan Ringan": "🌦️"
}

weather_recommendations = {
    "Berawan": "🌃 Cocok untuk jalan-jalan ringan. Jangan lupa jaket!",
    "Cerah": "🌴 Waktu yang sempurna untuk aktivitas luar ruangan! Pakai sunscreen ya!",
    "Hujan": "🌫️ Bawa payung dan pakai jaket tahan air jika keluar rumah!",
    "Petir": "💨 Hindari berada di luar rumah atau dekat benda logam!",
    "Kabut": "🌁 Berkendara hati-hati, jarak pandang bisa berkurang!",
    "Hujan Ringan": "💧 Pakai jaket ringan dan bawa payung kecil!"
}


try:
    # Mengambil data dari API
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Cek apakah data tersedia
    if 'data' in data:
        for item in data['data']:
            lokasi = item.get('lokasi', {})
            cuaca = item.get('cuaca', [])

            # Menampilkan informasi lokasi di sidebar
            with st.sidebar:
                st.header("📍 **Lokasi**")
                st.write(f"**Provinsi:** {lokasi.get('provinsi', 'Tidak tersedia')}")
                st.write(f"**Kota/Kabupaten:** {lokasi.get('kotkab', 'Tidak tersedia')}")
                st.write(f"**Kecamatan:** {lokasi.get('kecamatan', 'Tidak tersedia')}")
                st.write(f"**Desa:** {lokasi.get('desa', 'Tidak tersedia')}")
                st.write(f"🌍 **Longitude:** {lokasi.get('lon', 'Tidak tersedia')}")
                st.write(f"🌍 **Latitude:** {lokasi.get('lat', 'Tidak tersedia')}")

            # Menampilkan parameter cuaca dalam kotak-kotak
            if cuaca:
                st.subheader("🌡 **Kondisi Cuaca Saat Ini**")
                forecast = cuaca[0][0]  # Mengambil data pertama

                # Ambil deskripsi cuaca dan emoji
                weather_desc = forecast.get('weather_desc', 'Tidak tersedia')
                weather_emoji = weather_icons.get(weather_desc, "❓")
                recommendation = weather_recommendations.get(weather_desc, "❓ Tidak ada rekomendasi tersedia.")

                col1, col2, col3 = st.columns(3)
                with col1:
                    display_weather_card("🌡 Suhu Udara", f"{forecast.get('t', 'Tidak tersedia')}°C", "Suhu rata-rata udara.", "#FF5733")
                    display_weather_card("☁️ Total Awan", f"{forecast.get('tcc', 'Tidak tersedia')}%", "Persentase tutupan awan.", "#4A90E2")
                    display_weather_card("💦 Kelembapan", f"{forecast.get('hu', 'Tidak tersedia')}%", "Persentase kadar air di udara.", "#2ECC71")
                    display_weather_card("⛅ Cuaca", f"{weather_emoji} {weather_desc}", "Kondisi cuaca saat ini.", "#2ECC71")

                with col2:
                    display_weather_card("🌡 Suhu Permukaan", f"{forecast.get('tp', 'Tidak tersedia')}°C", "Suhu di permukaan tanah.", "#33A1FF")
                    display_weather_card("🌬 Kecepatan Angin", f"{forecast.get('ws', 'Tidak tersedia')} m/s", "Laju angin saat ini.", "#F39C12")
                    display_weather_card("🔭 Visibilitas", f"{forecast.get('vs', 'Tidak tersedia')} meter", "Jarak pandang akibat kabut, hujan, dsb.", "#8E44AD")
                    display_weather_card("🕒 Waktu Lokal", f"{forecast.get('local_datetime', 'Tidak tersedia')}", "Waktu saat ini di lokasi.", "#8E44AD")

                with col3:
                    display_weather_card("🧭 Arah Angin", f"{forecast.get('wd', 'Tidak tersedia')}°", "Arah datangnya angin.", "#D35400")
                    display_weather_card("🌪 Tekanan Udara", f"{forecast.get('press', 'Tidak tersedia')} hPa", "Tekanan atmosfer di lokasi.", "#A569BD")
                    display_weather_card("⏳ Indeks Waktu", f"{forecast.get('time_index', 'Tidak tersedia')}", "Rentang waktu prakiraan.", "#5D6D7E")
                    display_weather_card("\U0001F4A1 Rekomendasi", recommendation, "Saran berdasarkan cuaca.", "#3498DB")


                # Menampilkan prakiraan cuaca per jam
                st.subheader("⏳ **Prakiraan Cuaca Per Jam**")

                # Konversi data ke DataFrame
                df = pd.DataFrame(cuaca[0])
                df["datetime"] = pd.to_datetime(df["datetime"])

                # Filter data dari waktu saat ini hingga jam 23:00
                now = datetime.datetime.now(pytz.utc)
                df = df[df["datetime"] >= now]  # Ambil data dari waktu sekarang
                df = df[df["datetime"].dt.hour <= 23]  # Hanya sampai jam 23:00
                
                # Menampilkan grafik cuaca
                st.write("📈 **Grafik Suhu Udara per Jam**")
                st.line_chart(df.set_index("datetime")["t"])

                st.write("💨 **Grafik Kecepatan Angin per Jam**")
                st.line_chart(df.set_index("datetime")["ws"])

                st.write("💦 **Grafik Kelembapan Udara per Jam**")
                st.line_chart(df.set_index("datetime")["hu"])

                st.subheader("📋 **Data Cuaca Per Jam**")
                df = df.sort_values(by="datetime")

                # Rename kolom agar lebih mudah dibaca
                df.rename(columns={
                    "datetime": "Tanggal & Waktu",
                    "t": "Suhu Udara (°C)",
                    "tcc": "Total Awan (%)",
                    "tp": "Suhu Permukaan (°C)",
                    "desc_id": "Deskripsi Cuaca (ID)",
                    "desc_en": "Deskripsi Cuaca (EN)",
                    "wd": "Arah Angin",
                    "ws": "Kecepatan Angin (m/s)",
                    "hu": "Kelembapan (%)",
                    "vs": "Visibilitas (m)",
                    "desc_vs": "Deskripsi Visibilitas",
                    "time_index": "Rentang Waktu",
                    "analysis_time": "Tanggal Analisis",
                    "icon": "URL Ikon Cuaca",
                    "utc_time": "Waktu UTC",
                    "local_time": "Waktu Lokal"
                }, inplace=True)
                
                st.dataframe(df)

            else:
                st.warning("⚠️ Data cuaca tidak tersedia.")

    else:
        st.warning("⚠️ Data tidak tersedia atau format tidak sesuai.")

except requests.exceptions.RequestException as e:
    st.error(f"❌ Terjadi kesalahan saat mengambil data: {e}")
except json.JSONDecodeError:
    st.error("❌ Gagal memproses data JSON.")
