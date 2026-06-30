import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import time
import requests
from streamlit_lottie import st_lottie

# 1. Konfigurasi Halaman & Inisialisasi State di Awal
st.set_page_config(page_title="Kalkulator BMI", page_icon="⚖️", layout="centered")

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Link animasi Lottie publik untuk mempercantik tampilan
lottie_health = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_57tx9b6y.json")
lottie_success = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_at94iw4m.json")

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

def hitung_bmi(berat, tinggi):
    return berat / (tinggi ** 2)

def kategori_bmi(bmi):
    if bmi < 18.5:
        return "Kekurangan berat badan", "#3498db"
    elif 18.5 <= bmi < 25.0:
        return "Berat badan normal", "#2ecc71"
    elif 25.0 <= bmi < 30.0:
        return "Kelebihan berat badan", "#f39c12"
    else:
        return "Obesitas", "#e74c3c"

# --- TAMPILAN JUDUL UTAMA ---
st.title("📊 KALKULATOR BMI")
st.caption("Body Mass Index Calculator")

# ====================================================================
# BAGIAN NAMA KELOMPOK (DI ATAS APLIKASI)
# ====================================================================
st.write("### ✨ TIM KREATIF KELOMPOK ✨")

# Pembagian kolom grid untuk list nama anggota kelompok
grid1, grid2 = st.columns(2)
with grid1:
    st.markdown('👩‍💻 **Iis Lestari**')
    st.markdown('👨‍💻 **Asep Triyono**')
with grid2:
    st.markdown('👩‍💻 **Eka Yuslita Dewi**')
    st.markdown('👩‍💻 **Siti Fatikhatul Mardiyah**')

st.write("---")

# Header Konten Utama
col_title, col_logo = st.columns([3, 1])
with col_title:
    st.subheader("⚖️ Cek Kesehatan Tubuhmu")
    st.write("Masukkan angka di bawah untuk memeriksa kondisi indeks massa tubuh Anda.")
with col_logo:
    if lottie_health:
        st_lottie(lottie_health, height=100, key="main_logo")

# Input Data
col1, col2 = st.columns(2)
with col1:
    berat = st.number_input("Berat badan (kg):", min_value=1.0, value=60.0, step=0.1)
with col2:
    tinggi_cm = st.number_input("Tinggi badan (cm):", min_value=50.0, value=165.0, step=1.0)

# Proses Perhitungan
if st.button("🔍 Hitung BMI", use_container_width=True):
    if tinggi_cm > 0:
        with st.spinner("Menghitung BMI kamu..."):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.003)
                progress_bar.progress(i + 1)
            progress_bar.empty()

        tinggi_m = tinggi_cm / 100
        bmi = hitung_bmi(berat, tinggi_m)
        kategori, warna = kategori_bmi(bmi)
        waktu_cek = datetime.now().strftime("%d-%m-%Y %H:%M")

        st.balloons()

        # Menampilkan Hasil Akhir (Menggunakan komponen asli Streamlit)
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.success(f"**BMI Anda:** {bmi:.2f}")
            st.info(f"**Kategori:** {kategori}")
            st.caption(f"📅 Diperiksa pada: {waktu_cek}")
        with res_col2:
            if lottie_success:
                st_lottie(lottie_success, height=140, key="success_anim")

        # Simpan ke Riwayat Session State
        st.session_state.riwayat.append({
            "waktu": waktu_cek,
            "berat": berat,
            "tinggi_cm": tinggi_cm,
            "bmi": round(bmi, 2),
            "kategori": kategori
        })
    else:
        st.error("Tinggi badan harus lebih dari 0!")

# Bagian Grafik & Tabel Riwayat Pengecekan Berkelanjutan
if st.session_state.riwayat:
    st.write("---")
    st.subheader("📈 Diagram Garis Pengecekan Berkala")

    df = pd.DataFrame(st.session_state.riwayat)
    df["label_pengecekan"] = "Ke-" + (df.index + 1).astype(str) + " (" + df["waktu"] + ")"

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["label_pengecekan"],
        y=df["bmi"],
        mode="lines+markers+text",
        text=df["bmi"],
        textposition="top center",
        line=dict(color="#6c5ce7", width=3, shape="spline"),
        marker=dict(size=12, color="#6c5ce7", line=dict(width=2, color="white")),
        name="Nilai BMI Anda"
    ))

    fig.add_hline(y=18.5, line_dash="dot", line_color="#3498db", annotation_text="Batas Kurus (<18.5)")
    fig.add_hline(y=25.0, line_dash="dot", line_color="#2ecc71", annotation_text="Batas Normal (18.5-25)")
    fig.add_hline(y=30.0, line_dash="dot", line_color="#e74c3c", annotation_text="Batas Obesitas (>30)")

    fig.update_layout(
        xaxis_title="Daftar Riwayat Pengecekan",
        yaxis_title="Nilai Skor BMI",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.6)',
        template="plotly_white",
        height=450,
        margin=dict(l=20, r=20, t=40, b=80)
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("👁️ Lihat Tabel Rincian Data"):
        st.dataframe(df[["waktu", "berat", "tinggi_cm", "bmi", "kategori"]], use_container_width=True)

    if st.button("🗑️ Hapus Semua Riwayat", use_container_width=True):
        st.session_state.riwayat = []
        st.rerun()
