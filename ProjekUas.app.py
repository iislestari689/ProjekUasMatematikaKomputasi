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

# Mengambil animasi Lottie
lottie_health = load_lottieurl("https://lottie.host")
lottie_success = load_lottieurl("https://lottie.host")

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

# --- TAMPILAN JUDUL UTAMA BESAR KAPITAL ---
st.markdown(
    """
    <div style="text-align: center; margin-top: -20px; margin-bottom: 10px;">
        <h1 style="font-family: 'Poppins', sans-serif; font-weight: 800; color: #2c3e50; letter-spacing: 3px; font-size: 40px; margin-bottom: 0;">
            📊 KALKULATOR BMI
        </h1>
        <p style="color: #7f8c8d; font-size: 16px; margin-top: 5px; margin-bottom: 5px;">Body Mass Index Calculator</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ====================================================================
# BAGIAN NAMA KELOMPOK DESAIN CANTIK & AESTHETIC (DI ATAS APLIKASI)
# ====================================================================
st.markdown(
    """
    <div style="text-align: center; margin-top: 5px; margin-bottom: 15px;">
        <p style="font-size: 11px; letter-spacing: 2px; color: #57606f; text-transform: uppercase; font-weight: bold; margin-bottom: 2px;">Created By</p>
        <h4 style="font-family: 'Poppins', sans-serif; font-weight: 700; color: #2f3542; margin-top: 0; font-size: 18px; margin-bottom: 15px;">✨ TIM KREATIF KELOMPOK ✨</h4>
    </div>
    """, 
    unsafe_allow_html=True
)

# Pembagian kolom grid untuk list nama anggota kelompok
grid1, grid2 = st.columns(2)
with grid1:
    st.markdown('<div style="background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%); padding: 12px; border-radius: 10px; box-shadow: 0 4px 10px rgba(108, 92, 231, 0.15); text-align: center; margin-bottom: 10px;"><span style="font-size: 18px;">👩‍💻</span><h5 style="margin: 4px 0 0 0; color: white; font-family: \'Poppins\', sans-serif; font-weight: 600; font-size: 14px;">Iis Lestari</h5></div>', unsafe_allow_html=True)
    st.markdown('<div style="background: linear-gradient(135deg, #ff7675 0%, #fab1a0 100%); padding: 12px; border-radius: 10px; box-shadow: 0 4px 10px rgba(255, 118, 117, 0.15); text-align: center; margin-bottom: 10px;"><span style="font-size: 18px;">👨‍💻</span><h5 style="margin: 4px 0 0 0; color: white; font-family: \'Poppins\', sans-serif; font-weight: 600; font-size: 14px;">Asep Triyono</h5></div>', unsafe_allow_html=True)

with grid2:
    st.markdown('<div style="background: linear-gradient(135deg, #2ecc71 0%, #55efc4 100%); padding: 12px; border-radius: 10px; box-shadow: 0 4px 10px rgba(46, 204, 113, 0.15); text-align: center; margin-bottom: 10px;"><span style="font-size: 18px;">👩‍💻</span><h5 style="margin: 4px 0 0 0; color: white; font-family: \'Poppins\', sans-serif; font-weight: 600; font-size: 14px;">Eka Yuslita Dewi</h5></div>', unsafe_allow_html=True)
    st.markdown('<div style="background: linear-gradient(135deg, #e17055 0%, #ffbba0 100%); padding: 12px; border-radius: 10px; box-shadow: 0 4px 10px rgba(225, 112, 85, 0.15); text-align: center; margin-
