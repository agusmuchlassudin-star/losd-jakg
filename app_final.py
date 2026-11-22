import streamlit as st
import pandas as pd
import csv
import os
from datetime import datetime, date
from io import BytesIO

# =========================================================
# KONFIGURASI APLIKASI
# =========================================================
st.set_page_config(
    page_title="Management Tools LOSD JAKG",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

APP_TITLE = "MANAGEMENT TOOLS"
APP_SUBTITLE = "LOSD JAKARTA GUDANG · SISTEM INVENTARIS & PEMINJAMAN TOOLS"
LOGO_KAI = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Logo_PT_Kereta_Api_Indonesia_%28Persero%29_2020.svg/500px-Logo_PT_Kereta_Api_Indonesia_%28Persero%29_2020.svg.png"
MARS_KAI_URL = "https://www.youtube.com/watch?v=zL9s0WoVHgA"

KOLOM_TOOLS = ["Nama Alat", "Kode", "Stok"]
KOLOM_PEMINJAM = ["Nama Peminjam", "NIPP", "Bagian"]
KOLOM_PINJAM = ["Nama Peminjam", "Nama Alat", "Jumlah", "Tanggal Pinjam", "Status"]

LIST_ALAT_LO = ['Tang Buaya Bengkok 10', 'Xing Bo', 'Preasure Sprayer', 'Bearing Sparator', 'Thermometer', 'Insulation Tester / Tes Pen', 'Air Duster', 'Flaring Tools', 'Waterpas 600mm', 'Kunci Pas Ring Ratchet 36', 'Gerinda Tangan', 'Bor Tangan', 'Pompa', 'Mesin Amplas', 'Jig Saw', 'Dongkrak Simplex 10T', 'Dongkrak Simplex 5T', 'Dongkrak Hidrolik 30T', 'Dongkrak Hidrolik 10T', 'Box MCB Plastik', 'S21 Portable', 'Rambu Perawatan Genset', 'Rambu Perawatan PB / Perbaikan', 'Rambu Perawatan P3', 'Rambu Perawatan P6', 'Rambu Perawatan P12', 'Spray Gun F75', 'Kaca Mata Safety', 'Kaca Mata Las', 'Rompi Kolong', 'Kunci Inggris', 'Kunci Pipa', 'Tang Kombinasi', 'Tang Potong', 'Snapring Straight', 'Snapring Curved', 'Pahat', 'Palu Kecil', 'Palu Besar', 'Palu Besar 5 Kg', 'Linggis', 'Gagang Kunci Shock 3/4', 'Ragum', 'Box Impack', 'Vacum Cleaner Milwaukee', 'Back To Back', 'Kunci Momen', 'Kunci Momen Kecil Uk 1/2', 'Diameter Roda', 'Blok Kalibrasi', 'Crack Detector', 'Sarung Tangan Las', 'Goseave / Baju Las', 'Kawat Las RB & LB', 'Topeng Las', 'Mesin Las', 'Kabel Roll', 'Gerinda Cutting', 'Crimping Hidrolik', 'Kunci Sok 1 Set 60 Pc (SATA)', 'Impack 1/2', 'Stopwatch', 'Clearence', 'Meteran 7.5 m', 'Sigmat', 'Manometer', 'Mal Knuckle', 'Obeng (+)', 'Obeng (-)', 'Obeng Ketok', 'Kunci (L) Bintang', 'Kunci (L)', 'Mata Bor 4.0', 'Mata Bor 4.5', 'Mata Bor 5.0', 'Mata Bor 8.0', 'Mata Bor 10.0', 'Mata Bor 16', 'Mata Bor Beton', 'Kunci Shock', 'Gergaji Besi', 'Metrix', 'Cidi Met', 'Kepala Snei', 'Box Senai 1 Set', 'Mesin Senai', 'Mistar Panjang', 'Mistar Siku', 'Semboyan 21 Malam Portebel', 'Box S21', 'Kape', 'Sikat Kawat', 'Stang Sealler Botol Manual', 'Stang Sealler Botol Milwaukee', 'Senter', 'Senter Kepala Milwaukee', 'Senter Kepala Sunrei', 'Aki 60A', 'Tang Krimping / Skun', 'Gunting Potong', 'Tang Ripet', 'Bateray Tester', 'Tang Amper', 'Merger', 'Multimeter Digital 101', 'Kabel Kopler Panjang', 'Kabel Kopler', 'Karet List Kaca U', 'Selang Kawat', 'Manipol Gauge AC', 'Kunci T 10', 'Kunci T 12', 'Kunci T 13', 'Kunci T 17', 'Kunci T 19', 'Charger Accu', 'Tekel', 'Kunci Ring Pas 16', 'Kunci Ring Pas 17', 'Kunci Ring Pas 19', 'Kunci Ring Pas 22', 'Kunci Ring Pas 23', 'Kunci Ring Pas 24', 'Kunci Ring Pas 26', 'Kunci Ring Pas 27', 'Kunci Ring Pas 28', 'Kunci Ring Pas 29', 'Kunci Ring Pas 30', 'Kunci Ring Pas 32', 'Kunci Ring Pas 34', 'Kunci Ring Pas 36', 'Kunci Ring Pas 38', 'Kunci Ring 20,22', 'Kunci Ring 21,23', 'Kunci Ring 24,27', 'Kunci Ring 25,28', 'Kunci Ring 30,32', 'Kunci Pas 14,17', 'Kunci Pas 16,17', 'Kunci Pas 21-23', 'Kunci Pas 25-28', 'Kunci Pas 30-32', 'Kunci Ring Pas Ratchet 8,10,12,13,14,16,17,19,24', 'Kunci L Set Model T 2.5,3,4,5,6,8,10', 'Mesin Gerinda Portebel', 'Bor Tangan Portebel', 'Bor Duduk', 'Bateray Milwaukee', 'Bateray Bor Portable', 'Tangga Kecil', 'Rapid Charger Milwaukee', 'Beri', 'Heavy Duty Nut Splitter', 'Cordless Portable', 'Impack 3/4', 'Kunci Ring 30/32', 'Kunci Ring 28/25', 'Kunci Ring 27/24', 'Kunci Ring 23/21', 'Kunci Ring 22/20', 'Kunci Ring 8/9', 'Kunci Ring 7/6', 'Kunci Ring Pas 23', 'Kunci Ring Pas 22', 'Kunci Pas 26/24', 'Kunci Pas 23/21', 'Kunci Pas 15/14', 'Kunci T 17']

# =========================================================
# TEMA DARK KAI: NAVY, BLUE, ORANGE
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #081a2d;
    --navy-2: #102b49;
    --blue: #174d7d;
    --blue-light: #2476ad;
    --orange: #f28c28;
    --orange-light: #ffad55;
    --surface: #13283e;
    --surface-2: #192f47;
    --line: rgba(185, 205, 226, .15);
    --text: #edf4fb;
    --muted: #a9bbce;
}
html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stApp {
    background:
      radial-gradient(circle at 85% 0%, rgba(36,118,173,.16), transparent 28%),
      linear-gradient(145deg, #071625 0%, #0b1e32 55%, #102b43 100%);
    color: var(--text);
}
[data-testid="stHeader"] { background: rgba(7,22,37,.88); }
[data-testid="stToolbar"] { right: 1rem; }
[data-testid="stAppViewContainer"] .main .block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071729 0%, #102d4b 58%, #0c2238 100%);
    border-right: 1px solid rgba(255,255,255,.08);
}
[data-testid="stSidebar"] * { color: #edf4fb; }
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 12px;
    padding: 10px 12px;
    margin: 4px 0;
    transition: .2s ease;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(242,140,40,.16);
    border-color: rgba(242,140,40,.45);
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p { font-weight: 600; }
h1, h2, h3, h4, p, label, .stMarkdown, [data-testid="stCaptionContainer"] {
    color: var(--text) !important;
}
h1 { font-weight: 800 !important; letter-spacing: -.7px; }
h2, h3 { font-weight: 750 !important; }
small, .stCaption, [data-testid="stCaptionContainer"] { color: var(--muted) !important; }
hr { border-color: var(--line) !important; }
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #17334f, #10263d);
    border: 1px solid var(--line);
    border-top: 3px solid var(--orange);
    border-radius: 16px;
    padding: 17px 18px;
    box-shadow: 0 10px 26px rgba(0,0,0,.18);
}
div[data-testid="stMetric"] label { color: #b8c9d9 !important; font-weight: 600; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #fff !important; font-weight: 800;
}
div[data-testid="stForm"], div[data-testid="stExpander"] {
    background: rgba(19,40,62,.88);
    border: 1px solid var(--line);
    border-radius: 16px;
}
div[data-testid="stForm"] { padding: 18px; }
div[data-testid="stExpander"] summary { color: var(--text) !important; font-weight: 650; }
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] div[data-baseweb="select"],
[data-testid="stMultiSelect"] div[data-baseweb="select"] {
    background: #f5f8fc !important;
    color: #10243a !important;
    border-radius: 10px !important;
}
[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder { color: #64788d !important; }
[data-testid="stSelectbox"] [data-baseweb="select"] *,
[data-testid="stMultiSelect"] [data-baseweb="select"] * { color: #10243a !important; }
[data-testid="stDateInput"] button { color: #10243a !important; }
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] button {
    background: linear-gradient(100deg, #e97816, #f59b38) !important;
    color: white !important;
    border: 0 !important;
    border-radius: 11px !important;
    font-weight: 750 !important;
    min-height: 42px;
    box-shadow: 0 6px 16px rgba(242,140,40,.2);
    transition: .18s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover,
[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-1px);
    box-shadow: 0 9px 20px rgba(242,140,40,.32);
}
button[kind="secondary"] {
    background: #203a54 !important;
    color: white !important;
    border: 1px solid var(--line) !important;
}
[data-testid="stDataFrame"], [data-testid="stTable"] {
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
}
[data-testid="stAlert"] { border-radius: 12px; }
.jakg-hero {
    position: relative; overflow: hidden;
    background: linear-gradient(112deg, #0b2036 0%, #174a76 66%, #e97816 145%);
    border: 1px solid rgba(255,255,255,.13);
    border-radius: 22px;
    padding: 25px 28px;
    margin: 2px 0 18px 0;
    box-shadow: 0 14px 35px rgba(0,0,0,.25);
}
.jakg-hero:after {
    content: "🚆"; position: absolute; right: 28px; top: 12px;
    font-size: 74px; opacity: .13; transform: rotate(-8deg);
}
.jakg-eyebrow {
    color: #ffbd75; font-size: 11px; font-weight: 800;
    letter-spacing: 2px; text-transform: uppercase;
}
.jakg-title {
    color: white; font-size: clamp(23px, 3vw, 34px);
    font-weight: 850; line-height: 1.15; margin: 7px 0;
}
.jakg-subtitle { color: #d5e5f3; font-size: 13px; }
.jakg-ticker {
    overflow: hidden; white-space: nowrap; border-radius: 11px;
    background: linear-gradient(90deg,#102b49,#174d7d,#a95012);
    border: 1px solid rgba(255,177,95,.5);
    padding: 10px 0; margin: 12px 0 22px;
}
.jakg-ticker-track {
    display: inline-flex; animation: ticker 48s linear infinite;
}
.jakg-ticker-track span {
    color: #ffe2bd; font-size: 13px; font-weight: 800;
    letter-spacing: .7px; padding-right: 55px;
}
@keyframes ticker { from {transform:translateX(0)} to {transform:translateX(-50%)} }
.section-heading {
    display:flex; align-items:center; gap:10px;
    padding: 10px 0 12px; margin: 8px 0 12px;
    border-bottom: 1px solid var(--line);
    color:#fff; font-size:18px; font-weight:800;
}
.section-dot { width:5px; height:22px; background:var(--orange); border-radius:5px; }
.kpi-grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:14px; }
.kpi-card {
    position:relative; overflow:hidden; min-height:132px;
    padding:18px; border-radius:17px;
    background:linear-gradient(145deg,#183752,#10273e);
    border:1px solid rgba(255,255,255,.10);
    box-shadow:0 9px 22px rgba(0,0,0,.18);
}
.kpi-card:after {
    content:""; position:absolute; width:95px; height:95px;
    border-radius:50%; right:-28px; bottom:-42px;
    background:rgba(255,255,255,.045);
}
.kpi-label { color:#b8cadd; font-size:12px; font-weight:700; }
.kpi-value { color:#fff; font-size:35px; font-weight:850; margin:8px 0 2px; }
.kpi-note { color:#91a9bf; font-size:11px; }
.kpi-icon { float:right; font-size:26px; }
.kpi-orange { border-top:3px solid #f28c28; }
.kpi-blue { border-top:3px solid #3b91cf; }
.kpi-green { border-top:3px solid #31b38b; }
.kpi-red { border-top:3px solid #dc6b66; }
@media(max-width:850px) { .kpi-grid {grid-template-columns:repeat(2,minmax(0,1fr));} }
@media(max-width:520px) { .kpi-grid {grid-template-columns:1fr;} }
.footer {
    color:#8197ad; text-align:right; font-size:11px;
    border-top:1px solid var(--line); padding-top:14px; margin-top:28px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# UTILITAS DATA CSV
# =========================================================
def baca_csv(nama_file, kolom):
    if not os.path.exists(nama_file):
        with open(nama_file, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=kolom).writeheader()
        return []
    with open(nama_file, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        hasil = []
        for row in reader:
            if row and any(str(v or "").strip() for v in row.values()):
                hasil.append({k: row.get(k, "") or "" for k in kolom})
        return hasil

def simpan_csv(nama_file, kolom, data):
    with open(nama_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=kolom)
        writer.writeheader()
        writer.writerows([{k: item.get(k, "") for k in kolom} for item in data])

def tambah_data(nama_file, kolom, baris_baru):
    data = baca_csv(nama_file, kolom)
    data.append(baris_baru)
    simpan_csv(nama_file, kolom, data)

def angka(nilai):
    try:
        return int(float(str(nilai or "0").replace(",", ".")))
    except (ValueError, TypeError):
        return 0

def rupiah_tanggal(nilai):
    try:
        return datetime.strptime(nilai, "%Y-%m-%d").strftime("%d-%m-%Y")
    except (ValueError, TypeError):
        return nilai or "-"

# =========================================================
# INISIALISASI DATA
# =========================================================
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRV6iCRsvA3S8uCNNdNbvvrWnFxKxRoepGrZGL_3bWswWttq8ECPGMDNTL8UhqgTyeOcfkm6gkTODEJ/pub?gid=1373973017&single=true&output=csv"

def data_awal_tools():
    try:
        df_sheet = pd.read_csv(SHEET_URL)
        df_sheet.columns = [str(c).strip() for c in df_sheet.columns]
        kandidat = [c for c in df_sheet.columns if "nama" in c.lower() or "alat" in c.lower()]
        if kandidat:
            nama_alat = df_sheet[kandidat[0]].dropna().astype(str).str.strip().tolist()
            nama_alat = [x for x in nama_alat if x and x.lower() != "nan"]
            if nama_alat:
                return [{"Nama Alat": n, "Kode": f"TL-{i:03d}", "Stok": "1"}
                        for i, n in enumerate(nama_alat, 1)]
    except Exception:
        pass
    return [{"Nama Alat": n, "Kode": f"TL-{i:03d}", "Stok": "1"}
            for i, n in enumerate(LIST_ALAT_LO, 1)]

if not os.path.exists("tools.csv") or not baca_csv("tools.csv", KOLOM_TOOLS):
    simpan_csv("tools.csv", KOLOM_TOOLS, data_awal_tools())

if not os.path.exists("peminjam.csv") or not baca_csv("peminjam.csv", KOLOM_PEMINJAM):
    simpan_csv("peminjam.csv", KOLOM_PEMINJAM, [
        {"Nama Peminjam": "agus", "NIPP": "12345", "Bagian": "Teknik"},
        {"Nama Peminjam": "Budi", "NIPP": "12346", "Bagian": "Listrik"},
        {"Nama Peminjam": "Siti", "NIPP": "12347", "Bagian": "Mekanik"},
    ])

tools = baca_csv("tools.csv", KOLOM_TOOLS)
peminjam = baca_csv("peminjam.csv", KOLOM_PEMINJAM)
riwayat = baca_csv("peminjaman.csv", KOLOM_PINJAM)

# =========================================================
# SIDEBAR & HEADER
# =========================================================
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:10px 0 4px'>", unsafe_allow_html=True)
    st.image(LOGO_KAI, width=155)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-weight:800;font-size:14px;line-height:1.6'>DEPO GERBONG JAKARTA GUDANG<br><span style='color:#ffad55'>LOSD JAKG</span></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### ☰ MENU UTAMA")
    menu = st.radio(
        "Navigasi aplikasi",
        ["Dashboard", "Data Master Tools", "Data Peminjam", "Peminjaman Tools",
         "Pengembalian Tools", "Riwayat Peminjaman", "Laporan"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("<div style='font-size:11px;color:#a9bbce;text-align:center'>SIAP · SELAMAT · MELAYANI</div>", unsafe_allow_html=True)
    with st.expander("🎵 Mars KAI"):
        st.video(MARS_KAI_URL)

st.markdown(f"""
<div class="jakg-hero">
  <div class="jakg-eyebrow">DEPO GERBONG JAKARTA GUDANG · LOSD JAKG</div>
  <div class="jakg-title">{APP_TITLE}</div>
  <div class="jakg-subtitle">{APP_SUBTITLE}</div>
</div>
<div class="jakg-ticker"><div class="jakg-ticker-track">
  <span>SELAMAT DATANG DI MANAGEMENT TOOLS LOSD JAKG ✦ UTAMAKAN KESELAMATAN KERJA ✦ KEMBALIKAN TOOLS SETELAH DIPAKAI ✦ SIAP, SELAMAT, MELAYANI ✦</span>
  <span>SELAMAT DATANG DI MANAGEMENT TOOLS LOSD JAKG ✦ UTAMAKAN KESELAMATAN KERJA ✦ KEMBALIKAN TOOLS SETELAH DIPAKAI ✦ SIAP, SELAMAT, MELAYANI ✦</span>
</div></div>
""", unsafe_allow_html=True)

def judul_bagian(teks):
    st.markdown(f'<div class="section-heading"><span class="section-dot"></span>{teks}</div>', unsafe_allow_html=True)

def tampilkan_list(data, format_func):
    if not data:
        st.info("Belum ada data.")
        return
    for item in data:
        st.markdown(
            f"<div style='padding:12px 15px;margin:6px 0;background:#142c43;"
            f"border:1px solid rgba(255,255,255,.08);border-radius:11px;color:#eaf2fa'>"
            f"{format_func(item)}</div>",
            unsafe_allow_html=True
        )

# =========================================================
# DASHBOARD
# =========================================================
if menu == "Dashboard":
    judul_bagian("Dashboard Monitoring Tools")
    st.caption("Ringkasan inventaris, ketersediaan, dan aktivitas peminjaman.")

    total_jenis = len(tools)
    total_stok = sum(angka(t.get("Stok")) for t in tools)
    sedang_dipinjam = sum(angka(r.get("Jumlah")) for r in riwayat if r.get("Status") == "Dipinjam")
    tersedia = max(total_stok - sedang_dipinjam, 0)
    total_peminjam = len(peminjam)
    total_transaksi = len(riwayat)

    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card kpi-blue"><span class="kpi-icon">🧰</span>
        <div class="kpi-label">TOTAL JENIS ALAT</div><div class="kpi-value">{total_jenis:,}</div>
        <div class="kpi-note">Jenis alat terdaftar</div></div>
      <div class="kpi-card kpi-orange"><span class="kpi-icon">📦</span>
        <div class="kpi-label">TOTAL STOK</div><div class="kpi-value">{total_stok:,}</div>
        <div class="kpi-note">Unit tercatat di gudang</div></div>
      <div class="kpi-card kpi-red"><span class="kpi-icon">🔧</span>
        <div class="kpi-label">SEDANG DIPINJAM</div><div class="kpi-value">{sedang_dipinjam:,}</div>
        <div class="kpi-note">Unit sedang digunakan</div></div>
      <div class="kpi-card kpi-green"><span class="kpi-icon">✅</span>
        <div class="kpi-label">TERSEDIA</div><div class="kpi-value">{tersedia:,}</div>
        <div class="kpi-note">Unit siap dipinjam</div></div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("👤 Data Peminjam", f"{total_peminjam:,}")
    with c2:
        st.metric("🧾 Total Transaksi", f"{total_transaksi:,}")

    judul_bagian("Aktivitas Peminjaman Terbaru")
    if riwayat:
        terbaru = sorted(riwayat, key=lambda x: x.get("Tanggal Pinjam", ""), reverse=True)[:8]
        st.dataframe(pd.DataFrame(terbaru), use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada aktivitas peminjaman.")

# =========================================================
# DATA MASTER TOOLS
# =========================================================
elif menu == "Data Master Tools":
    judul_bagian("Data Master Tools")
    with st.expander("➕ Tambah alat baru", expanded=True):
        with st.form("form_alat", clear_on_submit=True):
            a, b, c = st.columns([3, 2, 1])
            with a:
                nama = st.text_input("Nama alat", placeholder="Contoh: Kunci Ring Pas")
            with b:
                kode = st.text_input("Kode alat", placeholder="Contoh: TL-169")
            with c:
                stok = st.number_input("Stok awal", min_value=0, step=1)
            simpan = st.form_submit_button("Simpan Alat", use_container_width=True)
        if simpan:
            if not nama.strip() or not kode.strip():
                st.error("Nama dan kode alat wajib diisi.")
            elif any(t.get("Kode", "").lower() == kode.strip().lower() for t in tools):
                st.error("Kode alat sudah digunakan. Gunakan kode yang berbeda.")
            else:
                tools.append({"Nama Alat": nama.strip(), "Kode": kode.strip().upper(), "Stok": str(int(stok))})
                simpan_csv("tools.csv", KOLOM_TOOLS, tools)
                st.success(f"Alat {nama} berhasil ditambahkan.")
                st.rerun()

    judul_bagian("Daftar Inventaris")
    cari_alat = st.text_input("🔎 Cari nama alat atau kode", placeholder="Ketik Dongkrak, Kunci, TL-001, dan lainnya")
    tools_tampil = [t for t in tools if cari_alat.lower() in (t.get("Nama Alat", "") + " " + t.get("Kode", "")).lower()] if cari_alat else tools
    if tools_tampil:
        st.caption(f"Menampilkan {len(tools_tampil)} dari {len(tools)} jenis alat.")
        for idx, tool in enumerate(tools_tampil):
            kode_tool = tool.get("Kode", "")
            with st.container(border=True):
                x, y, z, q = st.columns([4, 1.3, 1.2, 1.2])
                x.markdown(f"**{tool.get('Nama Alat','-')}**")
                x.caption(kode_tool)
                y.metric("Stok", angka(tool.get("Stok")))
                if z.button("✏️ Edit", key=f"edit_{kode_tool}_{idx}", use_container_width=True):
                    st.session_state["edit_kode"] = kode_tool
                if q.button("🗑️ Hapus", key=f"hapus_{kode_tool}_{idx}", use_container_width=True):
                    sedang = any(r.get("Nama Alat") == tool.get("Nama Alat") and r.get("Status") == "Dipinjam" for r in riwayat)
                    if sedang:
                        st.error("Alat masih tercatat sedang dipinjam dan tidak dapat dihapus.")
                    else:
                        tools = [t for t in tools if t.get("Kode") != kode_tool]
                        simpan_csv("tools.csv", KOLOM_TOOLS, tools)
                        st.success("Data alat dihapus.")
                        st.rerun()

    if st.session_state.get("edit_kode"):
        target = next((t for t in tools if t.get("Kode") == st.session_state["edit_kode"]), None)
        if target:
            judul_bagian(f"Edit Alat · {target.get('Kode')}")
            with st.form("form_edit_alat"):
                nama_edit = st.text_input("Nama alat", value=target.get("Nama Alat", ""))
                stok_edit = st.number_input("Stok", min_value=0, value=angka(target.get("Stok")), step=1)
                simpan_edit = st.form_submit_button("Simpan Perubahan")
            a, b = st.columns(2)
            if simpan_edit:
                target["Nama Alat"] = nama_edit.strip()
                target["Stok"] = str(int(stok_edit))
                simpan_csv("tools.csv", KOLOM_TOOLS, tools)
                del st.session_state["edit_kode"]
                st.success("Perubahan berhasil disimpan.")
                st.rerun()
            if b.button("Batalkan edit"):
                del st.session_state["edit_kode"]
                st.rerun()

# =========================================================
# DATA PEMINJAM
# =========================================================
elif menu == "Data Peminjam":
    judul_bagian("Data Peminjam")
    with st.expander("➕ Tambah peminjam baru", expanded=True):
        with st.form("form_peminjam", clear_on_submit=True):
            a, b, c = st.columns(3)
            with a:
                nama_p = st.text_input("Nama peminjam")
            with b:
                nipp = st.text_input("NIPP")
            with c:
                bagian = st.text_input("Bagian")
            simpan_p = st.form_submit_button("Simpan Peminjam", use_container_width=True)
        if simpan_p:
            if not nama_p.strip() or not nipp.strip():
                st.error("Nama peminjam dan NIPP wajib diisi.")
            elif any(p.get("NIPP") == nipp.strip() for p in peminjam):
                st.error("NIPP sudah terdaftar.")
            else:
                peminjam.append({"Nama Peminjam": nama_p.strip(), "NIPP": nipp.strip(), "Bagian": bagian.strip()})
                simpan_csv("peminjam.csv", KOLOM_PEMINJAM, peminjam)
                st.success(f"Peminjam {nama_p} berhasil ditambahkan.")
                st.rerun()

    judul_bagian("Daftar Peminjam")
    if peminjam:
        for i, p in enumerate(peminjam):
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([3, 1.5, 2, 1])
                c1.markdown(f"**👤 {p.get('Nama Peminjam','-')}**")
                c2.caption(f"NIPP: {p.get('NIPP','-')}")
                c3.caption(f"Bagian: {p.get('Bagian','-')}")
                if c4.button("Hapus", key=f"hapus_peminjam_{i}"):
                    aktif = any(r.get("NIPP") == p.get("NIPP") and r.get("Status") == "Dipinjam" for r in riwayat)
                    if aktif:
                        st.error(f"{p.get('Nama Peminjam')} masih memiliki pinjaman aktif.")
                    else:
                        peminjam = [x for x in peminjam if x.get("NIPP") != p.get("NIPP")]
                        simpan_csv("peminjam.csv", KOLOM_PEMINJAM, peminjam)
                        st.success("Data peminjam dihapus.")
                        st.rerun()
    else:
        st.info("Belum ada data peminjam.")

# =========================================================
# PEMINJAMAN TOOLS
# =========================================================
elif menu == "Peminjaman Tools":
    judul_bagian("Peminjaman Tools")
    st.caption("Pilih peminjam, pilih satu atau beberapa alat, lalu tentukan jumlah setiap alat.")
    alat_tersedia = [t for t in tools if angka(t.get("Stok")) > 0]
    if not peminjam:
        st.warning("Belum ada data peminjam. Tambahkan melalui menu Data Peminjam.")
    elif not alat_tersedia:
        st.warning("Tidak ada stok alat yang tersedia untuk dipinjam.")
    else:
        nama_pilih = st.selectbox("Pilih peminjam", [p.get("Nama Peminjam", "-") for p in peminjam])
        opsi_alat = {
            f"{t.get('Kode')} · {t.get('Nama Alat')} (stok: {angka(t.get('Stok'))})": t
            for t in alat_tersedia
        }
        alat_dipilih = st.multiselect("Pilih alat (dapat lebih dari satu)", list(opsi_alat.keys()))
        jumlah_per_alat = {}
        if alat_dipilih:
            judul_bagian("Jumlah yang Dipinjam")
            cols = st.columns(2)
            for i, pilihan in enumerate(alat_dipilih):
                tool = opsi_alat[pilihan]
                with cols[i % 2]:
                    jumlah_per_alat[pilihan] = st.number_input(
                        f"{tool.get('Nama Alat')} · Maksimal {angka(tool.get('Stok'))}",
                        min_value=1, max_value=angka(tool.get("Stok")), value=1,
                        step=1, key=f"jumlah_{tool.get('Kode')}"
                    )
            if st.button("📤 PROSES PEMINJAMAN", type="primary", use_container_width=True):
                tanggal_pinjam = date.today().strftime("%Y-%m-%d")
                for pilihan in alat_dipilih:
                    tool = opsi_alat[pilihan]
                    jumlah = int(jumlah_per_alat[pilihan])
                    tool["Stok"] = str(angka(tool.get("Stok")) - jumlah)
                    riwayat.append({
                        "Nama Peminjam": nama_pilih,
                        "Nama Alat": tool.get("Nama Alat", ""),
                        "Jumlah": str(jumlah),
                        "Tanggal Pinjam": tanggal_pinjam,
                        "Status": "Dipinjam"
                    })
                simpan_csv("tools.csv", KOLOM_TOOLS, tools)
                simpan_csv("peminjaman.csv", KOLOM_PINJAM, riwayat)
                st.success(f"Berhasil memproses peminjaman {len(alat_dipilih)} jenis alat.")
                st.rerun()
        else:
            st.info("Pilih minimal satu alat untuk melanjutkan.")

# =========================================================
# PENGEMBALIAN TOOLS
# =========================================================
elif menu == "Pengembalian Tools":
    judul_bagian("Pengembalian Tools")
    masih_pinjam = [(i, r) for i, r in enumerate(riwayat) if r.get("Status") == "Dipinjam"]
    if not masih_pinjam:
        st.success("Semua alat sudah dikembalikan. Tidak ada pinjaman aktif.")
    else:
        opsi_kembali = {
            f"{i} · {r.get('Nama Peminjam','-')} · {r.get('Nama Alat','-')} · {r.get('Jumlah','0')} unit · {rupiah_tanggal(r.get('Tanggal Pinjam',''))}": (i, r)
            for i, r in masih_pinjam
        }
        dipilih = st.multiselect("Pilih alat yang akan dikembalikan", list(opsi_kembali.keys()))
        if dipilih and st.button("📥 PROSES PENGEMBALIAN", type="primary", use_container_width=True):
            for label in dipilih:
                idx, item = opsi_kembali[label]
                riwayat[idx]["Status"] = "Dikembalikan"
                tool = next((t for t in tools if t.get("Nama Alat") == item.get("Nama Alat")), None)
                if tool:
                    tool["Stok"] = str(angka(tool.get("Stok")) + angka(item.get("Jumlah")))
            simpan_csv("peminjaman.csv", KOLOM_PINJAM, riwayat)
            simpan_csv("tools.csv", KOLOM_TOOLS, tools)
            st.success(f"Berhasil mengembalikan {len(dipilih)} transaksi alat.")
            st.rerun()

# =========================================================
# RIWAYAT PEMINJAMAN
# =========================================================
elif menu == "Riwayat Peminjaman":
    judul_bagian("Riwayat Peminjaman")
    a, b, c = st.columns([2, 2, 1])
    with a:
        tgl_dari = st.date_input("Dari tanggal", value=None, key="riwayat_dari")
    with b:
        tgl_sampai = st.date_input("Sampai tanggal", value=None, key="riwayat_sampai")
    with c:
        status_filter = st.selectbox("Status", ["Semua", "Dipinjam", "Dikembalikan"])
    hasil = riwayat.copy()
    if tgl_dari and tgl_sampai:
        hasil = [
            r for r in hasil
            if r.get("Tanggal Pinjam") and
            tgl_dari <= datetime.strptime(r["Tanggal Pinjam"], "%Y-%m-%d").date() <= tgl_sampai
        ]
    if status_filter != "Semua":
        hasil = [r for r in hasil if r.get("Status") == status_filter]
    st.caption(f"Ditemukan {len(hasil)} transaksi.")
    if hasil:
        df_riwayat = pd.DataFrame(hasil)
        df_riwayat["Tanggal Pinjam"] = df_riwayat["Tanggal Pinjam"].apply(rupiah_tanggal)
        st.dataframe(df_riwayat, use_container_width=True, hide_index=True)
    else:
        st.info("Tidak ada transaksi pada filter tersebut.")

# =========================================================
# LAPORAN
# =========================================================
elif menu == "Laporan":
    judul_bagian("Laporan Peminjaman Tools")
    total = len(riwayat)
    aktif = sum(1 for r in riwayat if r.get("Status") == "Dipinjam")
    kembali = sum(1 for r in riwayat if r.get("Status") == "Dikembalikan")
    a, b, c = st.columns(3)
    a.metric("Total Transaksi", total)
    b.metric("Masih Dipinjam", aktif)
    c.metric("Sudah Dikembalikan", kembali)

    if riwayat:
        df_laporan = pd.DataFrame(riwayat)
        st.dataframe(df_laporan, use_container_width=True, hide_index=True)
        csv_data = df_laporan.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "⬇️ Unduh Laporan CSV", csv_data,
            file_name=f"laporan_peminjaman_{date.today()}.csv",
            mime="text/csv"
        )
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_laporan.to_excel(writer, index=False, sheet_name="Laporan Peminjaman")
        st.download_button(
            "⬇️ Unduh Laporan Excel", buffer.getvalue(),
            file_name=f"laporan_peminjaman_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("Belum ada data transaksi untuk dilaporkan.")

st.markdown("<div class='footer'>MANAGEMENT TOOLS LOSD JAKG · SIAP, SELAMAT, MELAYANI</div>", unsafe_allow_html=True)
