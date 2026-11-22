












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

Anda telah mencapai batas analisis data. Tingkatkan ke ChatGPT Plus atau coba lagi besok setelah 16.45.




