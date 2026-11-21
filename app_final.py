import streamlit as st
import pandas as pd
from datetime import datetime, date
from pathlib import Path
import json

# =========================================================
# MANAGEMENT TOOLS LOSD JAKG
# Database: Google Spreadsheet (gspread) with local CSV fallback
# =========================================================
st.set_page_config(
    page_title="Management Tools | LOSD JAKG",
    page_icon="🧰",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#102B46"
BLUE = "#1769AA"
ORANGE = "#F58220"
BG = "#F3F6FA"
GREEN = "#16845B"
RED = "#C94343"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {{ font-family: Inter, sans-serif; }}
.stApp {{ background: {BG}; }}
section[data-testid="stSidebar"] {{ background: {NAVY}; }}
section[data-testid="stSidebar"] * {{ color: #fff !important; }}
.block-container {{ padding-top: 1.5rem; padding-bottom: 2.5rem; max-width: 1500px; }}
h1, h2, h3 {{ color: {NAVY}; }}
.hero {{
  background: linear-gradient(115deg, {NAVY} 0%, #1D5684 68%, {ORANGE} 100%);
  padding: 26px 30px; border-radius: 18px; color: white; margin-bottom: 22px;
  box-shadow: 0 8px 24px rgba(16,43,70,.14);
}}
.hero h1 {{ color: white !important; margin: 0; font-size: 30px; }}
.hero p {{ color: #EAF2F8 !important; margin: 7px 0 0 0; }}
.kpi {{
  background: white; border: 1px solid #E5EBF1; border-radius: 16px;
  padding: 18px 20px; box-shadow: 0 4px 14px rgba(16,43,70,.06);
  min-height: 116px;
}}
.kpi-label {{ color: #637487; font-size: 13px; font-weight: 600; }}
.kpi-value {{ color: {NAVY}; font-size: 32px; font-weight: 800; margin-top: 5px; }}
.kpi-note {{ color: #8A98A8; font-size: 11px; margin-top: 2px; }}
.section-card {{
 background: white; border: 1px solid #E5EBF1; border-radius: 16px;
 padding: 18px 20px; box-shadow: 0 3px 12px rgba(16,43,70,.04);
}}
div.stButton > button, div.stDownloadButton > button {{
 background: {ORANGE}; color: white; border: 0; border-radius: 10px;
 font-weight: 700; min-height: 42px;
}}
div.stButton > button:hover, div.stDownloadButton > button:hover {{
 background: #DE6D12; color: white; border: 0;
}}
[data-testid="stDataFrame"] {{ background: white; border-radius: 12px; }}
[data-testid="stForm"] {{ background: white; border: 1px solid #E5EBF1; border-radius: 14px; padding: 18px; }}
small {{ color: #718096; }}
</style>
""", unsafe_allow_html=True)

# ------------------ DATA LAYER ------------------
TABLES = {
    "Tools": ["Nama Alat", "Kode", "Stok"],
    "Peminjam": ["Nama Peminjam", "NIPP", "Bagian"],
    "Peminjaman": ["ID Transaksi", "Nama Peminjam", "NIPP", "Nama Alat", "Kode Alat",
                   "Jumlah", "Tanggal Pinjam", "Tanggal Kembali", "Status"],
}
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def local_read(table):
    path = DATA_DIR / f"{table.lower()}.csv"
    if path.exists():
        df = pd.read_csv(path, dtype=str).fillna("")
        for col in TABLES[table]:
            if col not in df.columns:
                df[col] = ""
        return df[TABLES[table]]
    return pd.DataFrame(columns=TABLES[table])

def local_write(table, df):
    df.reindex(columns=TABLES[table]).fillna("").to_csv(
        DATA_DIR / f"{table.lower()}.csv", index=False, encoding="utf-8-sig"
    )

@st.cache_resource
def get_gspread_client():
    import gspread
    from google.oauth2.service_account import Credentials
    secrets = st.secrets
    if "gcp_service_account" not in secrets or "spreadsheet" not in secrets:
        return None
    creds_info = dict(secrets["gcp_service_account"])
    scopes = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open_by_key(str(secrets["spreadsheet"]["id"]))

def read_table(table):
    try:
        book = get_gspread_client()
        if book is None:
            return local_read(table), "local"
        try:
            ws = book.worksheet(table)
        except Exception:
            ws = book.add_worksheet(title=table, rows=1000, cols=len(TABLES[table]))
            ws.append_row(TABLES[table])
        values = ws.get_all_records()
        df = pd.DataFrame(values)
        for col in TABLES[table]:
            if col not in df.columns:
                df[col] = ""
        return df[TABLES[table]].fillna("").astype(str), "google"
    except Exception as exc:
        st.session_state["db_error"] = str(exc)
        return local_read(table), "local"

def write_table(table, df):
    df = df.reindex(columns=TABLES[table]).fillna("").astype(str)
    try:
        book = get_gspread_client()
        if book is None:
            local_write(table, df)
            return "local"
        try:
            ws = book.worksheet(table)
        except Exception:
            ws = book.add_worksheet(title=table, rows=1000, cols=len(TABLES[table]))
        ws.clear()
        ws.update([TABLES[table]] + df.values.tolist(), value_input_option="USER_ENTERED")
        local_write(table, df)
        return "google"
    except Exception as exc:
        st.session_state["db_error"] = str(exc)
        local_write(table, df)
        raise RuntimeError(f"Gagal menyimpan ke Google Spreadsheet: {exc}") from exc

def refresh_data():
    st.cache_data.clear()
    st.rerun()

tools, db_tools = read_table("Tools")
borrowers, db_borrowers = read_table("Peminjam")
loans, db_loans = read_table("Peminjaman")
db_mode = "Google Spreadsheet" if "google" in (db_tools, db_borrowers, db_loans) else "Penyimpanan lokal (CSV)"

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.markdown("<div style='text-align:center;font-size:48px'>🧰</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-weight:800;font-size:18px'>MANAGEMENT TOOLS</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:12px;opacity:.85'>DEPO GERBONG JAKARTA GUDANG<br>LOSD JAKG</div>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("NAVIGASI", [
        "Dashboard", "Data Master Tools", "Data Peminjam",
        "Peminjaman Tools", "Pengembalian Tools", "Riwayat Peminjaman", "Laporan"
    ], label_visibility="visible")
    st.markdown("---")
    st.caption(f"Database aktif: {db_mode}")
    if st.button("🔄 Muat Ulang Data", use_container_width=True):
        refresh_data()
    st.markdown("---")
    st.caption("Utamakan keselamatan kerja • Kembalikan tools setelah digunakan")

# ------------------ HEADER ------------------
st.markdown("""
<div class="hero">
  <h1>Management Tools LOSD JAKG</h1>
  <p>Sistem informasi pengelolaan inventaris, peminjaman, dan pengembalian peralatan kerja.</p>
</div>
""", unsafe_allow_html=True)

if db_mode != "Google Spreadsheet":
    st.warning("Aplikasi saat ini berjalan dengan penyimpanan CSV lokal. Hubungkan Google Spreadsheet melalui file secrets.toml agar data tersimpan terpusat.")
if st.session_state.get("db_error"):
    st.error("Koneksi database: " + st.session_state["db_error"])

# Helpers
def save_and_reload(table, df, success_msg):
    try:
        mode = write_table(table, df)
        st.success(success_msg + (" (Google Spreadsheet)" if mode == "google" else " (CSV lokal)"))
        st.cache_data.clear()
        st.rerun()
    except RuntimeError as err:
        st.error(str(err))

def metric_card(label, value, note, icon):
    st.markdown(f"""<div class="kpi"><div class="kpi-label">{icon} &nbsp;{label}</div>
    <div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>""", unsafe_allow_html=True)

# ------------------ PAGES ------------------
if menu == "Dashboard":
    st.subheader("Ringkasan Inventaris")
    total_types = len(tools)
    total_stock = pd.to_numeric(tools["Stok"], errors="coerce").fillna(0).sum() if len(tools) else 0
    active = loans[loans["Status"].str.lower() == "dipinjam"] if len(loans) else loans
    borrowed = pd.to_numeric(active["Jumlah"], errors="coerce").fillna(0).sum() if len(active) else 0
    available = max(int(total_stock - borrowed), 0)
    cols = st.columns(4)
    with cols[0]: metric_card("Jenis Tools", total_types, "Jenis alat terdaftar", "🧰")
    with cols[1]: metric_card("Total Stok", int(total_stock), "Unit terdata", "📦")
    with cols[2]: metric_card("Sedang Dipinjam", int(borrowed), "Unit belum kembali", "📤")
    with cols[3]: metric_card("Tersedia", available, "Perkiraan unit tersedia", "✅")
    st.write("")
    left, right = st.columns([1.25, 1])
    with left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### Status Peminjaman")
        if len(loans):
            status_counts = loans["Status"].value_counts().rename_axis("Status").reset_index(name="Jumlah")
            st.bar_chart(status_counts.set_index("Status"))
        else:
            st.info("Belum ada transaksi peminjaman.")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### Informasi Sistem")
        st.write(f"**Database:** {db_mode}")
        st.write(f"**Jumlah peminjam terdaftar:** {len(borrowers)}")
        st.write(f"**Total transaksi:** {len(loans)}")
        st.write(f"**Transaksi aktif:** {len(active)}")
        st.markdown("</div>", unsafe_allow_html=True)
    st.caption("Pastikan data stok dan transaksi diperbarui setiap terjadi peminjaman atau pengembalian.")

elif menu == "Data Master Tools":
    st.subheader("📦 Data Master Tools")
    with st.expander("＋ Tambah Tools Baru", expanded=False):
        with st.form("add_tool", clear_on_submit=True):
            c1, c2, c3 = st.columns([2, 1, 1])
            nama = c1.text_input("Nama Alat")
            kode = c2.text_input("Kode Alat")
            stok = c3.number_input("Stok Awal", min_value=0, step=1)
            submitted = st.form_submit_button("Simpan Tools", use_container_width=True)
            if submitted:
                if not nama.strip() or not kode.strip():
                    st.error("Nama alat dan kode wajib diisi.")
                elif (tools["Kode"].str.casefold() == kode.strip().casefold()).any():
                    st.error("Kode alat sudah digunakan.")
                else:
                    new = pd.concat([tools, pd.DataFrame([{"Nama Alat": nama.strip(), "Kode": kode.strip(), "Stok": str(stok)}])], ignore_index=True)
                    save_and_reload("Tools", new, "Tools berhasil ditambahkan.")
    search = st.text_input("🔎 Cari nama alat atau kode")
    shown = tools.copy()
    if search:
        shown = shown[shown.apply(lambda r: search.lower() in " ".join(r.astype(str)).lower(), axis=1)]
    st.dataframe(shown, use_container_width=True, hide_index=True)
    if len(shown):
        with st.expander("✏️ Edit atau Hapus Tools"):
            selected_code = st.selectbox("Pilih kode alat", shown["Kode"].tolist())
            item = tools[tools["Kode"] == selected_code].iloc[0]
            with st.form("edit_tool"):
                enama = st.text_input("Nama Alat", item["Nama Alat"])
                estok = st.number_input("Stok", min_value=0, value=max(0, int(float(item["Stok"] or 0))))
                c1, c2 = st.columns(2)
                update = c1.form_submit_button("Simpan Perubahan", use_container_width=True)
                delete = c2.form_submit_button("Hapus Tools", use_container_width=True)
                if update:
                    tools.loc[tools["Kode"] == selected_code, "Nama Alat"] = enama.strip()
                    tools.loc[tools["Kode"] == selected_code, "Stok"] = str(estok)
                    save_and_reload("Tools", tools, "Perubahan tools tersimpan.")
                if delete:
                    active_tool = loans[(loans["Kode Alat"] == selected_code) & (loans["Status"] == "Dipinjam")]
                    if len(active_tool):
                        st.error("Tools tidak dapat dihapus karena masih memiliki transaksi aktif.")
                    else:
                        save_and_reload("Tools", tools[tools["Kode"] != selected_code], "Tools berhasil dihapus.")

elif menu == "Data Peminjam":
    st.subheader("👤 Data Peminjam")
    with st.expander("＋ Tambah Peminjam", expanded=False):
        with st.form("add_borrower", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            nama = c1.text_input("Nama Peminjam")
            nipp = c2.text_input("NIPP")
            bagian = c3.text_input("Bagian")
            submitted = st.form_submit_button("Simpan Peminjam", use_container_width=True)
            if submitted:
                if not nama.strip() or not nipp.strip():
                    st.error("Nama dan NIPP wajib diisi.")
                elif (borrowers["NIPP"] == nipp.strip()).any():
                    st.error("NIPP sudah terdaftar.")
                else:
                    new = pd.concat([borrowers, pd.DataFrame([{"Nama Peminjam": nama.strip(), "NIPP": nipp.strip(), "Bagian": bagian.strip()}])], ignore_index=True)
                    save_and_reload("Peminjam", new, "Data peminjam berhasil ditambahkan.")
    st.dataframe(borrowers, use_container_width=True, hide_index=True)
    if len(borrowers):
        with st.expander("Hapus Data Peminjam"):
            nipp_del = st.selectbox("Pilih NIPP", borrowers["NIPP"].tolist())
            if st.button("Hapus Peminjam", type="secondary"):
                name_del = borrowers.loc[borrowers["NIPP"] == nipp_del, "Nama Peminjam"].iloc[0]
                active_borrower = loans[(loans["NIPP"] == nipp_del) & (loans["Status"] == "Dipinjam")]
                if len(active_borrower):
                    st.error("Peminjam masih memiliki tools yang belum dikembalikan.")
                else:
                    save_and_reload("Peminjam", borrowers[borrowers["NIPP"] != nipp_del], f"Data {name_del} dihapus.")

elif menu == "Peminjaman Tools":
    st.subheader("📤 Peminjaman Tools")
    if borrowers.empty or tools.empty:
        st.warning("Data peminjam dan data tools harus tersedia sebelum transaksi.")
    else:
        with st.form("borrow_form"):
            borrower_options = {f'{r["Nama Peminjam"]} | NIPP {r["NIPP"]}': r for _, r in borrowers.iterrows()}
            selected_borrower = st.selectbox("Pilih Peminjam", list(borrower_options))
            selected_tools = st.multiselect("Pilih Tools (bisa lebih dari satu)", [
                f'{r["Nama Alat"]} | {r["Kode"]} | stok {r["Stok"]}' for _, r in tools.iterrows()
                if int(float(r["Stok"] or 0)) > 0
            ])
            quantities = {}
            for choice in selected_tools:
                code = choice.split("|")[1].strip()
                stock = int(float(tools.loc[tools["Kode"] == code, "Stok"].iloc[0]))
                quantities[code] = st.number_input(f"Jumlah - {choice}", min_value=1, max_value=stock, value=1, step=1, key=f"borrow_{code}")
            submit = st.form_submit_button("Konfirmasi Peminjaman", use_container_width=True)
            if submit:
                if not selected_tools:
                    st.error("Pilih minimal satu tools.")
                else:
                    borrower = borrower_options[selected_borrower]
                    updated_tools = tools.copy()
                    new_loans = loans.copy()
                    for code, qty in quantities.items():
                        idx = updated_tools.index[updated_tools["Kode"] == code][0]
                        stock = int(float(updated_tools.at[idx, "Stok"] or 0))
                        if qty > stock:
                            st.error(f"Stok {code} tidak mencukupi.")
                            st.stop()
                        updated_tools.at[idx, "Stok"] = str(stock - qty)
                        tool = updated_tools.loc[idx]
                        new_loans.loc[len(new_loans)] = [
                            datetime.now().strftime("%Y%m%d%H%M%S") + "-" + code,
                            borrower["Nama Peminjam"], borrower["NIPP"], tool["Nama Alat"], code,
                            str(qty), date.today().isoformat(), "", "Dipinjam"
                        ]
                    try:
                        write_table("Tools", updated_tools)
                        write_table("Peminjaman", new_loans)
                        st.cache_data.clear()
                        st.success("Transaksi peminjaman berhasil disimpan.")
                        st.rerun()
                    except RuntimeError as err:
                        st.error(str(err))

elif menu == "Pengembalian Tools":
    st.subheader("📥 Pengembalian Tools")
    active = loans[loans["Status"] == "Dipinjam"].copy()
    if active.empty:
        st.info("Tidak ada tools yang sedang dipinjam.")
    else:
        active["Pilihan"] = active.apply(lambda r: f'{r["ID Transaksi"]} | {r["Nama Peminjam"]} | {r["Nama Alat"]} | jumlah {r["Jumlah"]}', axis=1)
        chosen = st.multiselect("Pilih transaksi yang akan dikembalikan", active["Pilihan"].tolist())
        if st.button("Proses Pengembalian", use_container_width=True, disabled=not chosen):
            updated_loans = loans.copy()
            updated_tools = tools.copy()
            for choice in chosen:
                transaction_id = choice.split("|")[0].strip()
                row_idx = updated_loans.index[updated_loans["ID Transaksi"] == transaction_id][0]
                transaction = updated_loans.loc[row_idx]
                updated_loans.at[row_idx, "Status"] = "Dikembalikan"
                updated_loans.at[row_idx, "Tanggal Kembali"] = date.today().isoformat()
                code = transaction["Kode Alat"]
                tool_idx = updated_tools.index[updated_tools["Kode"] == code]
                if len(tool_idx):
                    idx = tool_idx[0]
                    current_stock = int(float(updated_tools.at[idx, "Stok"] or 0))
                    updated_tools.at[idx, "Stok"] = str(current_stock + int(float(transaction["Jumlah"] or 0)))
            try:
                write_table("Tools", updated_tools)
                write_table("Peminjaman", updated_loans)
                st.cache_data.clear()
                st.success(f"{len(chosen)} transaksi berhasil dikembalikan.")
                st.rerun()
            except RuntimeError as err:
                st.error(str(err))

elif menu == "Riwayat Peminjaman":
    st.subheader("📋 Riwayat Peminjaman")
    c1, c2, c3 = st.columns([1, 1, 1])
    start = c1.date_input("Dari tanggal", value=None)
    end = c2.date_input("Sampai tanggal", value=None)
    status = c3.selectbox("Status", ["Semua", "Dipinjam", "Dikembalikan"])
    shown = loans.copy()
    if start and end:
        shown = shown[(shown["Tanggal Pinjam"] >= start.isoformat()) & (shown["Tanggal Pinjam"] <= end.isoformat())]
    elif start:
        shown = shown[shown["Tanggal Pinjam"] >= start.isoformat()]
    elif end:
        shown = shown[shown["Tanggal Pinjam"] <= end.isoformat()]
    if status != "Semua":
        shown = shown[shown["Status"] == status]
    st.dataframe(shown.drop(columns=["ID Transaksi"], errors="ignore"), use_container_width=True, hide_index=True)
    st.caption(f"Menampilkan {len(shown)} transaksi.")

elif menu == "Laporan":
    st.subheader("📊 Laporan Peminjaman")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Transaksi", len(loans))
    c2.metric("Masih Dipinjam", int((loans["Status"] == "Dipinjam").sum()) if len(loans) else 0)
    c3.metric("Sudah Kembali", int((loans["Status"] == "Dikembalikan").sum()) if len(loans) else 0)
    st.dataframe(loans, use_container_width=True, hide_index=True)
    csv_bytes = loans.to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇️ Download Laporan CSV", csv_bytes, "laporan_peminjaman_losd_jakg.csv", "text/csv", use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align:right;color:#8190A0;font-size:12px'>Management Tools LOSD JAKG • Dikembangkan untuk operasional Depo Gerbong Jakarta Gudang</div>", unsafe_allow_html=True)
