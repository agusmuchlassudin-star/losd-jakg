import streamlit as st
# --- OBAT BIAR TABEL & TANGGAL TERANG LAGI ---
st.markdown("""
<style>
/* Kotak tanggal & semua input jadi putih, tulisan item */
input, .stDateInput input, .stTextInput input, .stSelectbox div {
  background-color: #FFFFFF !important;
  color: #000000 !important;
  -webkit-text-fill-color: #000000 !important;
}
/* Label Dari Tanggal / Sampai Tanggal jadi item terang */
label, .stDateInput label {
  color: #000000 !important;
}
/* Tabel Riwayat jadi putih, tulisan item */
div[data-testid="stDataFrame"] *, div[data-testid="stTable"] * {
  background-color: #FFFFFF !important;
  color: #000000 !important;
  -webkit-text-fill-color: #000000 !important;
}
/* Judul kolom tabel tetep biru dongker, tulisan putih biar cakep */
div[data-testid="stDataFrame"] thead th, div[data-testid="stDataFrame"] [role="columnheader"] {
  background-color: #0F2A44 !important;
  color: #FFFFFF !important;
  -webkit-text-fill-color: #FFFFFF !important;
}
/* Tombol Cari & Tampilkan Semua tetep oren */
button {
  color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)
import csv
import os
from datetime import datetime, date

st.set_page_config(page_title="Management Tools LOSD JAKG", page_icon="logo.png.jpg", layout="wide")
# --- HEADER MEMANJANG BALIK LAGI ---
if os.path.exists("header.png.jpg"):
    st.image("logo.png", use_container_width=True)

  # --- RUNNING TEXT STYLE CANTIK V3 PALING ATAS - JAKG ---
st.markdown("""
<style>
.jakg-box-v3 {
  overflow: hidden;
  background: linear-gradient(90deg, #0F2A44 0%, #1A4A7A 50%, #FF6B00 100%) !important;
  border: 2px solid #FFCC00 !important;
  border-radius: 12px !important;
  padding: 14px 0px !important;
  box-shadow: 0px 4px 12px rgba(0,0,0,0.4) !important;
  white-space: nowrap !important;
}
.jakg-track-v3 {
  display: inline-flex !important;
  white-space: nowrap !important;
  animation: jakg-jalan-v3 60s linear infinite !important;
}
.jakg-track-v3 span {
  color: #FFEB00 !important;
  -webkit-text-fill-color: #FFEB00 !important;
  font-size: 24px !important;
  font-weight: 900 !important;
  font-family: Arial, sans-serif !important;
  letter-spacing: 1px !important;
  text-shadow: 0px 0px 10px #FFEB00, 2px 2px 3px black !important;
  padding-right: 80px !important;
}
@keyframes jakg-jalan-v3 {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
</style>
<div class="jakg-box-v3"><div class="jakg-track-v3">
<span style="color:#FFEB00 !important; -webkit-text-fill-color:#FFEB00 !important;">SELAMAT DATANG DI MANAGEMENT TOOLS LOSD JAKG &nbsp; ✦ &nbsp; UTAMAKAN KESELAMATAN KERJA &nbsp; ✦ &nbsp; KEMBALIKAN TOOLS SETELAH DIPAKAI &nbsp; ✦ &nbsp; LOSD JAKG - SIAP, SELAMAT, MELAYANI &nbsp; ✦ &nbsp;</span>
<span style="color:#FFEB00 !important; -webkit-text-fill-color:#FFEB00 !important;">SELAMAT DATANG DI MANAGEMENT TOOLS LOSD JAKG &nbsp; ✦ &nbsp; UTAMAKAN KESELAMATAN KERJA &nbsp; ✦ &nbsp; KEMBALIKAN TOOLS SETELAH DIPAKAI &nbsp; ✦ &nbsp; LOSD JAKG - SIAP, SELAMAT, MELAYANI &nbsp; ✦ &nbsp;</span>
</div></div>
""", unsafe_allow_html=True)
# --- LOGO BARU DI DEPAN / SIDEBAR ---
LOGO_KAI = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Logo_PT_Kereta_Api_Indonesia_%28Persero%29_2020.svg/500px-Logo_PT_Kereta_Api_Indonesia_%28Persero%29_2020.svg.png"

# --- LOGO KAI DITENGAH SIDEBAR ---
c_kiri, c_tengah, c_kanan = st.sidebar.columns([1, 2, 1])
with c_tengah:
    st.image(LOGO_KAI, width=170)
st.sidebar.markdown("<p style='text-align:center; color:white; font-size:13px; font-weight:bold;'>Depo Gerbong Jakarta Gudang<br>LOSD JAKG</p>", unsafe_allow_html=True)
st.sidebar.markdown("### 🎵 Mars KAI")
st.sidebar.video("https://www.youtube.com/watch?v=zL9s0WoVHgA")
st.sidebar.markdown("---")


st.markdown("""
<style>
    .stApp { background-color: #F0F2F6; }
    h1 { color: #0F2A44 !important; text-align: center !important; }
    .stApp p, .stApp label, .stApp span, .stApp div { color: #0F2A44 !important; }
    div[data-testid="stMetric"] { background-color: white !important; padding: 15px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); border-top: 4px solid #0066CC; }
    .stButton > button { background-color: #FF6B00 !important; color: white !important; border: none !important; border-radius: 10px !important; font-weight: bold !important; width: 100%; }
    .stButton > button * { color: white !important; }
    section[data-testid="stSidebar"] { background-color: #0F2A44 !important; }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] span { color: white !important; }
    input { color: black !important; background-color: white !important; }
</style>
""", unsafe_allow_html=True)

def baca_csv(nama_file, kolom):
    if not os.path.exists(nama_file):
        with open(nama_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=kolom); writer.writeheader()
        return []
    with open(nama_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader if any(row.values())]

def simpan_csv(nama_file, kolom, data):
    with open(nama_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=kolom); writer.writeheader(); writer.writerows(data)

def tambah_data(nama_file, kolom, baris_baru):
    data = baca_csv(nama_file, kolom); data.append(baris_baru); simpan_csv(nama_file, kolom, data)

KOLOM_TOOLS = ["Nama Alat", "Kode", "Stok"]
KOLOM_PEMINJAM = ["Nama Peminjam", "NIPP", "Bagian"]
KOLOM_PINJAM = ["Nama Peminjam", "Nama Alat", "Jumlah", "Tanggal Pinjam", "Status"]

LIST_ALAT_LO = ["Tang Buaya Bengkok 10","Xing Bo","Preasure Sprayer","Bearing Sparator","Thermometer","Insulation Tester / Tes Pen","Air Duster","Flaring Tools","Waterpas 600mm","Kunci Pas Ring Ratchet 36","Gerinda Tangan","Bor Tangan","Pompa","Mesin Amplas","Jig Saw","Dongkrak Simplex 10T","Dongkrak Simplex 5T","Dongkrak Hidrolik 30T","Dongkrak Hidrolik 10T","Box MCB Plastik","S21 Portable","Rambu Perawatan Genset","Rambu Perawatan PB / Perbaikan","Rambu Perawatan P3","Rambu Perawatan P6","Rambu Perawatan P12","Spray Gun F75","Kaca Mata Safety","Kaca Mata Las","Rompi Kolong","Kunci Inggris","Kunci Pipa","Tang Kombinasi","Tang Potong","Snapring Straight","Snapring Curved","Pahat","Palu Kecil","Palu Besar","Palu Besar 5 Kg","Linggis","Gagang Kunci Shock 3/4","Ragum","Box Impack","Vacum Cleaner Milwaukee","Back To Back","Kunci Momen","Kunci Momen Kecil Uk 1/2","Diameter Roda","Blok Kalibrasi","Crack Detector","Sarung Tangan Las","Goseave / Baju Las","Kawat Las RB & LB","Topeng Las","Mesin Las","Kabel Roll","Gerinda Cutting","Crimping Hidrolik","Kunci Sok 1 Set 60 Pc (SATA)","Impack 1/2","Stopwatch","Clearence","Meteran 7.5 m","Sigmat","Manometer","Mal Knuckle","Obeng (+)","Obeng (-)","Obeng Ketok","Kunci (L) Bintang","Kunci (L)","Mata Bor 4.0","Mata Bor 4.5","Mata Bor 5.0","Mata Bor 8.0","Mata Bor 10.0","Mata Bor 16","Mata Bor Beton","Kunci Shock","Gergaji Besi","Metrix","Cidi Met","Kepala Snei","Box Senai 1 Set","Mesin Senai","Mistar Panjang","Mistar Siku","Semboyan 21 Malam Portebel","Box S21","Kape","Sikat Kawat","Stang Sealler Botol Manual","Stang Sealler Botol Milwaukee","Senter","Senter Kepala Milwaukee","Senter Kepala Sunrei","Aki 60A","Tang Krimping / Skun","Gunting Potong","Tang Ripet","Bateray Tester","Tang Amper","Merger","Multimeter Digital 101","Kabel Kopler Panjang","Kabel Kopler","Karet List Kaca U","Selang Kawat","Manipol Gauge AC","Kunci T 10","Kunci T 12","Kunci T 13","Kunci T 17","Kunci T 19","Charger Accu","Tekel","Kunci Ring Pas 16","Kunci Ring Pas 17","Kunci Ring Pas 19","Kunci Ring Pas 22","Kunci Ring Pas 23","Kunci Ring Pas 24","Kunci Ring Pas 26","Kunci Ring Pas 27","Kunci Ring Pas 28","Kunci Ring Pas 29","Kunci Ring Pas 30","Kunci Ring Pas 32","Kunci Ring Pas 34","Kunci Ring Pas 36","Kunci Ring Pas 38","Kunci Ring 20,22","Kunci Ring 21,23","Kunci Ring 24,27","Kunci Ring 25,28","Kunci Ring 30,32","Kunci Pas 14,17","Kunci Pas 16,17","Kunci Pas 21-23","Kunci Pas 25-28","Kunci Pas 30-32","Kunci Ring Pas Ratchet 8,10,12,13,14,16,17,19,24","Kunci L Set Model T 2.5,3,4,5,6,8,10","Mesin Gerinda Portebel","Bor Tangan Portebel","Bor Duduk","Bateray Milwaukee","Bateray Bor Portable","Tangga Kecil","Rapid Charger Milwaukee","Beri","Heavy Duty Nut Splitter","Cordless Portable","Impack 3/4","Kunci Ring 30/32","Kunci Ring 28/25","Kunci Ring 27/24","Kunci Ring 23/21","Kunci Ring 22/20","Kunci Ring 8/9","Kunci Ring 7/6","Kunci Ring Pas 23","Kunci Ring Pas 22","Kunci Pas 26/24","Kunci Pas 23/21","Kunci Pas 15/14","Kunci T 17"]

if not os.path.exists("tools.csv") or len(baca_csv("tools.csv", KOLOM_TOOLS)) == 0:
    data_awal_tools = [{"Nama Alat": nama_alat, "Kode": f"TL-{i:03d}", "Stok": "1"} for i, nama_alat in enumerate(LIST_ALAT_LO, start=1)]
    simpan_csv("tools.csv", KOLOM_TOOLS, data_awal_tools)

if not os.path.exists("peminjam.csv") or len(baca_csv("peminjam.csv", KOLOM_PEMINJAM)) == 0:
    simpan_csv("peminjam.csv", KOLOM_PEMINJAM, [{"Nama Peminjam": "agus", "NIPP": "12345", "Bagian": "Teknik"},{"Nama Peminjam": "Budi", "NIPP": "12346", "Bagian": "Listrik"},{"Nama Peminjam": "Siti", "NIPP": "12347", "Bagian": "Mekanik"}])

st.sidebar.title("MENU UTAMA")
menu = st.sidebar.radio("Pilih Menu:", ["Dashboard", "Data Master Tools", "Data Peminjam", "Peminjaman Tools", "Pengembalian Tools", "Riwayat Peminjaman", "Laporan"])
tools = baca_csv("tools.csv", KOLOM_TOOLS)
for t in tools:
    if "Tang Buaya" in t.get("Nama Alat", ""): t["Stok"] = "1"
simpan_csv("tools.csv", KOLOM_TOOLS, tools)
peminjam = baca_csv("peminjam.csv", KOLOM_PEMINJAM)
riwayat = baca_csv("peminjaman.csv", KOLOM_PINJAM)

# --- TEMA ADEM - GAK SILAU ---
st.markdown("""<style>
section[data-testid="stSidebar"] { background-color: #0F2A44 !important; }
section[data-testid="stSidebar"] * { color: #FFFFFF !important; background-color: #0F2A44 !important; }
section[data-testid="stMain"] { background-color: #DCE6EC !important; }
section[data-testid="stMain"] * { color: #1A1A1A !important; }
div[data-testid="stAppViewBlockContainer"] { background-color: #EAF0F4 !important; border-radius: 12px; padding: 20px !important; }
input { color: #000000 !important; background-color: #FFFFFF !important; }
button { background-color: #FF7A00 !important; color: #FFFFFF !important; }
</style>""", unsafe_allow_html=True)

def tampilkan_list(data, format_func):
    if not data: st.info("Belum ada data.")
    else:
        for item in data: st.write("• " + format_func(item)); st.write("---")

if menu == "Dashboard":
    # --- DASHBOARD CANTIK ALA KAI ---
  st.markdown("""
  <style>
  .kpi-card { background: white; border-radius: 16px; padding: 18px 20px; box-shadow: 0 4px 18px rgba(0,0,0,0.08); border-top: 5px solid #0F2A44; }
  .kpi-blue { border-top-color: #1A4B8F; }
  .kpi-orange { border-top-color: #F7941D; }
  .kpi-red { border-top-color: #E53935; }
  .kpi-green { border-top-color: #2E9E5B; }
  .kpi-label { font-size: 13px; color: #666; font-weight: 600; }
  .kpi-value { font-size: 38px; font-weight: 800; color: #0F2A44; margin: 2px 0; }
  .kpi-icon { font-size: 28px; float: right; }
  .kpi-sub { font-size: 12px; color: #999; }
  </style>
  """, unsafe_allow_html=True)
  
  st.markdown("### 📊 Dashboard Monitoring Tools")
  st.write("Sistem Informasi Pengelolaan Alat dan Inventaris - Dipo Gerbong Jakarta Gudang")
  
  total_jenis = len(tools); total_stok = sum(int(t.get("Stok", 0) or 0) for t in tools) if tools else 0
  sedang_dipinjam = sum(int(r.get("Jumlah", 0) or 0) for r in riwayat if r.get("Status") == "Dipinjam") if riwayat else 0
  tersedia = total_stok - sedang_dipinjam
  
  c1, c2, c3, c4 = st.columns(4)
  with c1:
      st.markdown(f"""<div class="kpi-card kpi-blue"><div><span class="kpi-label">Total Jenis Alat</span><span class="kpi-icon">🧰</span></div><div class="kpi-value">{total_jenis}</div><div class="kpi-sub">Jenis alat terdaftar</div></div>""", unsafe_allow_html=True)
  with c2:
      st.markdown(f"""<div class="kpi-card kpi-orange"><div><span class="kpi-label">Total Stok</span><span class="kpi-icon">📦</span></div><div class="kpi-value">{total_stok}</div><div class="kpi-sub">Total unit di gudang</div></div>""", unsafe_allow_html=True)
  with c3:
      st.markdown(f"""<div class="kpi-card kpi-red"><div><span class="kpi-label">Sedang Dipinjam</span><span class="kpi-icon">🔧</span></div><div class="kpi-value">{sedang_dipinjam}</div><div class="kpi-sub">Alat sedang keluar</div></div>""", unsafe_allow_html=True)
  with c4:
      st.markdown(f"""<div class="kpi-card kpi-green"><div><span class="kpi-label">Tersedia</span><span class="kpi-icon">✅</span></div><div class="kpi-value">{tersedia}</div><div class="kpi-sub">Siap dipinjam</div></div>""", unsafe_allow_html=True)
  
  st.markdown("---")
  st.info("👋 Selamat datang di Sistem Peminjaman Tools - Dipo Gerbong Jakarta Gudang")
elif menu == "Data Master Tools":
    st.title("📦 Data Master Tools"); st.subheader("Tambah Alat Baru")
    with st.form("form_alat"):
        nama = st.text_input("Nama Alat"); kode = st.text_input("Kode Alat"); stok = st.number_input("Stok", min_value=0, step=1); simpan = st.form_submit_button("Simpan Alat")
        if simpan:
            if nama and kode: tambah_data("tools.csv", KOLOM_TOOLS, {"Nama Alat": nama, "Kode": kode, "Stok": str(int(stok))}); st.success(f"Alat {nama} berhasil ditambahkan!"); st.rerun()
            else: st.error("Nama dan Kode wajib diisi!")
    st.write("---"); st.subheader("Daftar Alat"); cari_alat = st.text_input("🔍 Cari Alat", placeholder="Ketik misal: Dongkrak, Kunci, Tang...")
    tools_tampil = [t for t in tools if cari_alat.lower() in t.get("Nama Alat","").lower()] if cari_alat else tools
    if cari_alat: st.write(f"Ditemukan {len(tools_tampil)} alat")
    if not tools_tampil: st.info("Belum ada data.")
    else:
        for idx, t in enumerate(tools_tampil):
            col_tulis, col_hapus = st.columns([4, 1])
            with col_tulis: st.write(f"🔧 {t.get('Nama Alat','-')} | Kode: {t.get('Kode','-')} | Stok: {t.get('Stok','0')}")
            with col_hapus:
                if st.button("🗑️ Hapus", key=f"hapus_alat_{t.get('Kode','')}_{idx}"):
                    nama_hapus = t.get("Nama Alat")
                    if any(r.get("Nama Alat") == nama_hapus and r.get("Status") == "Dipinjam" for r in riwayat): st.error(f"Gak bisa hapus {nama_hapus}, masih ada yang pinjam!")
                    else: simpan_csv("tools.csv", KOLOM_TOOLS, [x for x in tools if x != t]); st.success(f"Alat {nama_hapus} berhasil dihapus!"); st.rerun()
            st.write("---")
elif menu == "Data Peminjam":
    st.title("👤 Data Peminjam"); st.subheader("Tambah Peminjam Baru")
    with st.form("form_peminjam"):
        nama_p = st.text_input("Nama Peminjam"); nipp = st.text_input("NIPP"); bagian = st.text_input("Bagian"); simpan_p = st.form_submit_button("Simpan Peminjam")
        if simpan_p:
            if nama_p and nipp: tambah_data("peminjam.csv", KOLOM_PEMINJAM, {"Nama Peminjam": nama_p, "NIPP": nipp, "Bagian": bagian}); st.success(f"Peminjam {nama_p} berhasil ditambahkan!"); st.rerun()
            else: st.error("Nama Peminjam dan NIPP wajib diisi!")
    st.write("---"); st.subheader("Daftar Peminjam")
    if not peminjam: st.info("Belum ada data.")
    else:
        for idx, p in enumerate(peminjam):
            col_tulis, col_hapus = st.columns([4, 1])
            with col_tulis: st.write(f"👤 {p.get('Nama Peminjam','-')} | NIPP: {p.get('NIPP','-')} | Bagian: {p.get('Bagian','-')}")
            with col_hapus:
                if st.button("🗑️ Hapus", key=f"hapus_peminjam_{idx}"):
                    nama_hapus = p.get("Nama Peminjam")
                    if any(r.get("Nama Peminjam") == nama_hapus and r.get("Status") == "Dipinjam" for r in riwayat): st.error(f"Gak bisa hapus {nama_hapus}, masih ada pinjaman!")
                    else: simpan_csv("peminjam.csv", KOLOM_PEMINJAM, [x for x in peminjam if x != p]); st.success(f"Peminjam {nama_hapus} berhasil dihapus!"); st.rerun()
            st.write("---")
elif menu == "Peminjaman Tools":
    st.title("📤 Peminjaman Tools"); st.write("Bisa pinjam lebih dari 1 alat sekaligus!")
    if not peminjam: st.warning("Belum ada data peminjam. Tambah dulu di menu Data Peminjam.")
    elif not tools: st.warning("Belum ada data alat.")
    else:
        nama_pilih = st.selectbox("Pilih Peminjam", [p.get("Nama Peminjam","-") for p in peminjam])
        daftar_alat = [f"{t.get('Nama Alat','-')} (Stok: {t.get('Stok','0')})" for t in tools]
        alat_terpilih = st.multiselect("Pilih Alat (Bisa Lebih Dari 1)", daftar_alat); jumlah_per_alat = {}
        if alat_terpilih:
            st.write("---"); st.subheader("Atur Jumlah Tiap Alat:")
            for a in alat_terpilih:
                nama_alat_bersih = a.split(" (Stok:")[0]; jumlah_per_alat[nama_alat_bersih] = st.number_input(f"Jumlah {nama_alat_bersih}", min_value=1, step=1, key=f"jml_{nama_alat_bersih}")
            if st.button("Pinjam Semua Alat"):
                gagal = []
                for nama_alat, jml in jumlah_per_alat.items():
                    stok_alat = next((t for t in tools if t.get("Nama Alat") == nama_alat), None)
                    if not stok_alat or int(stok_alat.get("Stok", 0) or 0) < jml: gagal.append(nama_alat)
                if gagal: st.error(f"Stok tidak cukup untuk: {', '.join(gagal)}")
                else:
                    for nama_alat, jml in jumlah_per_alat.items():
                        for t in tools:
                            if t.get("Nama Alat") == nama_alat: t["Stok"] = str(int(t.get("Stok", 0) or 0) - int(jml))
                        tambah_data("peminjaman.csv", KOLOM_PINJAM, {"Nama Peminjam": nama_pilih, "Nama Alat": nama_alat, "Jumlah": str(int(jml)), "Tanggal Pinjam": datetime.now().strftime("%Y-%m-%d"), "Status": "Dipinjam"})
                    simpan_csv("tools.csv", KOLOM_TOOLS, tools); st.success(f"Berhasil meminjam {len(jumlah_per_alat)} alat!"); st.rerun()
        else: st.info("Pilih minimal 1 alat dulu di atas 👆")
elif menu == "Pengembalian Tools":
    st.title("📥 Pengembalian Tools"); st.write("Bisa kembalikan banyak alat sekaligus!")
    masih_pinjam = [r for r in riwayat if r.get("Status") == "Dipinjam"]
    if not masih_pinjam: st.info("Tidak ada alat yang sedang dipinjam.")
    else:
        opsi = [f"{i} - {r.get('Nama Peminjam','-')} - {r.get('Nama Alat','-')} - {r.get('Jumlah','0')} - {r.get('Tanggal Pinjam','-')}" for i, r in enumerate(masih_pinjam)]
        dipilih = st.multiselect("Centang alat yang mau dikembalikan (Bisa Banyak)", opsi)
        if dipilih:
            if st.button("Kembalikan Semua Yang Dipilih"):
                for pil in dipilih:
                    idx = int(pil.split(" - ")[0]); item = masih_pinjam[idx]
                    for r in riwayat:
                        if r == item and r.get("Status") == "Dipinjam": r["Status"] = "Dikembalikan"; break
                    for t in tools:
                        if t.get("Nama Alat") == item.get("Nama Alat"): t["Stok"] = str(int(t.get("Stok", 0) or 0) + int(item.get("Jumlah", 0) or 0))
                simpan_csv("peminjaman.csv", KOLOM_PINJAM, riwayat); simpan_csv("tools.csv", KOLOM_TOOLS, tools); st.success(f"Berhasil mengembalikan {len(dipilih)} alat!"); st.rerun()
        else: st.info("Centang dulu alatnya di atas 👆")

elif menu == "Riwayat Peminjaman":
    st.title("📋 Riwayat Peminjaman"); st.subheader("🔍 Cari Berdasarkan Tanggal")
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1: tgl_dari = st.date_input("Dari Tanggal", value=None)
    with col2: tgl_sampai = st.date_input("Sampai Tanggal", value=None)
    with col3: st.write(" "); st.write(" "); cari = st.button("🔍 Cari")
    if st.button("Tampilkan Semua"): st.rerun()
    riwayat_tampil = riwayat
    if tgl_dari and tgl_sampai:
        riwayat_tampil = []
        for r in riwayat:
            try:
                tgl_data = datetime.strptime(r.get("Tanggal Pinjam",""), "%Y-%m-%d").date()
                if tgl_dari <= tgl_data <= tgl_sampai: riwayat_tampil.append(r)
            except: pass
        st.success(f"Ditemukan {len(riwayat_tampil)} data dari {tgl_dari} sampai {tgl_sampai}")
    st.write("---"); tampilkan_list(riwayat_tampil, lambda r: f"{r.get('Nama Peminjam','-')} pinjam {r.get('Nama Alat','-')} ({r.get('Jumlah','0')}) - {r.get('Tanggal Pinjam','-')} - {r.get('Status','-')}")
elif menu == "Laporan":
    st.title("📊 Laporan"); st.write(f"Total Transaksi: {len(riwayat)}")
    tampilkan_list(riwayat, lambda r: f"{r.get('Nama Peminjam','-')} | {r.get('Nama Alat','-')} | {r.get('Jumlah','0')} | {r.get('Tanggal Pinjam','-')} | {r.get('Status','-')}")
    if riwayat:
        csv_text = "Nama Peminjam,Nama Alat,Jumlah,Tanggal Pinjam,Status\n"
        for r in riwayat: csv_text += f"{r.get('Nama Peminjam','-')},{r.get('Nama Alat','-')},{r.get('Jumlah','0')},{r.get('Tanggal Pinjam','-')},{r.get('Status','-')}\n"
        st.download_button("Download Laporan CSV", csv_text, "laporan_peminjaman.csv", "text/csv")
st.markdown("---")
st.markdown("<p style='text-align: right; font-size: 12px; color: grey;'>by: Agus Muchlassudin Effendhi</p>", unsafe_allow_html=True)
