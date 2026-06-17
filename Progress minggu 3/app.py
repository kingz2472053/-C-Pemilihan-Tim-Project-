import streamlit as st
import pandas as pd
from data_handler import get_presets, generate_random_candidates, candidates_to_df, df_to_candidates
from visualizer import build_graphviz_tree, plot_benchmark
from algorithm import BranchAndBound

st.set_page_config(page_title="Pemilihan Tim Proyek (B&B)", layout="wide")

st.title("Optimasi Pemilihan Tim Proyek")
st.markdown("Aplikasi seleksi kombinasi $k$ kandidat dari pool $n$ kandidat dengan total biaya minimum menggunakan algoritma **Branch and Bound**.")

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("Konfigurasi Parameter")

# 1. Dataset Selection
dataset_option = st.sidebar.radio(
    "Pilih Sumber Dataset:",
    ["Gunakan Preset", "Generate Acak", "Upload CSV"]
)

candidates = []
k = 5
B = 100_000_000

if dataset_option == "Gunakan Preset":
    presets = get_presets()
    selected_preset = st.sidebar.selectbox("Pilih Preset:", list(presets.keys()))
    preset_data = presets[selected_preset]
    candidates = preset_data["candidates"]
    
    st.sidebar.subheader("Parameter Tim")
    k = st.sidebar.number_input("Ukuran Tim (k)", min_value=1, max_value=len(candidates), value=preset_data["k"])
    B = st.sidebar.number_input("Anggaran Maksimal (B) Rp", min_value=0, value=preset_data["B"], step=1000000)
    st.sidebar.caption(f"Nilai: **Rp {B:,}**".replace(',', '.'))

elif dataset_option == "Generate Acak":
    n_rand = st.sidebar.number_input("Jumlah Kandidat (n)", min_value=12, max_value=100, value=12)
    candidates = generate_random_candidates(n_rand)
    
    st.sidebar.subheader("Parameter Tim")
    k = st.sidebar.number_input("Ukuran Tim (k)", min_value=1, max_value=n_rand, value=5)
    B = st.sidebar.number_input("Anggaran Maksimal (B) Rp", min_value=0, value=100_000_000, step=1000000)
    st.sidebar.caption(f"Nilai: **Rp {B:,}**".replace(',', '.'))

elif dataset_option == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload file CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file, sep=None, engine='python', on_bad_lines='skip')
            candidates = df_to_candidates(df_upload)
            st.sidebar.success(f"Berhasil memuat {len(candidates)} kandidat.")
        except Exception as e:
            st.sidebar.error(f"Error membaca CSV: {e}")
            candidates = get_presets()["Small (n=12, k=5, B=100jt)"]["candidates"]
    else:
        candidates = get_presets()["Small (n=12, k=5, B=100jt)"]["candidates"]
        
    st.sidebar.subheader("Parameter Tim")
    k = st.sidebar.number_input("Ukuran Tim (k)", min_value=1, max_value=max(1, len(candidates)), value=min(5, len(candidates)))
    B = st.sidebar.number_input("Anggaran Maksimal (B) Rp", min_value=0, value=100_000_000, step=1000000)
    st.sidebar.caption(f"Nilai: **Rp {B:,}**".replace(',', '.'))

# --- MAIN CONTENT ---

# Display Dataset
st.subheader(f"Daftar Kandidat (n={len(candidates)})")
df_candidates = candidates_to_df(candidates)

# Show data editor so user can manually tweak if they want
edited_df = st.data_editor(df_candidates, use_container_width=True, hide_index=True, num_rows="dynamic")
updated_candidates = df_to_candidates(edited_df)

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Jalankan Optimasi", type="primary"):
        st.session_state["run_solver"] = True
with col2:
    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Template CSV", data=csv, file_name="kandidat.csv", mime="text/csv")


if st.session_state.get("run_solver", False):
    with st.spinner("Mencari solusi optimal..."):
        bb = BranchAndBound(updated_candidates, k, B)
        result = bb.solve()
    
    st.success("Pencarian Selesai!")
    
    # Tabs for results
    tab1, tab2, tab3 = st.tabs(["Tim Terpilih & Statistik", "Visualisasi Pohon (Graphviz)", "Benchmarking B&B"])
    
    with tab1:
        st.markdown("### Hasil Pemilihan Tim")
        if result.is_feasible:
            team_candidates = [bb.candidates[idx] for idx in result.best_team]
            df_team = candidates_to_df(team_candidates)
            st.table(df_team.set_index("ID"))
            
            total_str = f"Rp {result.best_cost:,}".replace(',', '.')
            sisa_str = f"Rp {B - result.best_cost:,}".replace(',', '.')
            st.info(f"**Total Biaya:** {total_str}  |  **Sisa Anggaran:** {sisa_str}")
            
            # Export Result
            csv_res = df_team.to_csv(index=False).encode('utf-8')
            st.download_button("Export Hasil Tim (CSV)", data=csv_res, file_name="tim_optimal.csv", mime="text/csv")
            
            alts = bb.get_alternative_teams()
            if len(alts) > 1:
                st.warning(f"Ditemukan **{len(alts)}** kombinasi tim alternatif dengan biaya optimal yang persis sama!")
        else:
            st.error("Tidak ada tim yang memenuhi syarat anggaran (B terlalu kecil).")
            
        st.markdown("### Statistik Pencarian Branch & Bound")
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        col_s1.metric("Node Dieksplorasi", f"{result.nodes_explored:,}")
        col_s2.metric("Node Dipangkas (Pruned)", f"{result.nodes_pruned:,}")
        eff = (result.nodes_pruned / max(result.nodes_explored, 1)) * 100
        col_s3.metric("Efisiensi Pruning", f"{eff:.1f}%")
        col_s4.metric("Waktu Komputasi", f"{result.elapsed_sec*1000:.3f} ms")

    with tab2:
        st.markdown("### Visualisasi Pohon Keputusan (State Space Tree)")
        st.markdown("Warna Hijau = Solusi Optimal | Biru = Dieksplorasi | Merah = Dipangkas (Pruned)")
        
        if len(result.tree_nodes) > 100:
            st.warning("Pohon terlalu besar! Hanya menampilkan 100 node pertama untuk mencegah crash pada browser.")
        
        with st.spinner("Menggambar pohon..."):
            dot = build_graphviz_tree(result.tree_nodes, updated_candidates, max_nodes=100)
            
            st.graphviz_chart(dot.source, use_container_width=True)

    with tab3:
        st.markdown("### Perbandingan Performa: Branch & Bound vs Brute Force")
        st.markdown("Mengukur seberapa jauh lebih cepat algoritma B&B dibandingkan mencoba semua kemungkinan kombinasi secara manual.")
        
        if len(updated_candidates) > 24:
            st.warning("n > 24 terlalu besar untuk Brute Force (akan memakan waktu sangat lama). Brute Force dilewati.")
        else:
            with st.spinner("Menjalankan Brute Force untuk benchmarking..."):
                fig = plot_benchmark(updated_candidates, k, B)
                st.pyplot(fig)
