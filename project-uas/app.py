import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib style
plt.style.use('default')
sns.set_palette("husl")

# Setup halaman
st.set_page_config(
    page_title="Dashboard Kelulusan Mahasiswa", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .insight-box {
        background-color: #471396;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🎓 Dashboard Visualisasi Kelulusan Mahasiswa</h1>', unsafe_allow_html=True)

# Load dan preprocessing data
@st.cache_data
def load_and_process_data():
    try:
        df = pd.read_csv("dataset_kelulusan_mahasiswa.csv")
        
        # Normalisasi nama kolom
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")
        
        # Handle missing values
        df = df.dropna()
        
        # Pastikan tipe data benar
        numeric_cols = ['ipk', 'jumlah_cuti_akademik', 'jumlah_semester']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Handle kolom IPS jika ada
        ips_cols = [col for col in df.columns if 'ips' in col.lower()]
        for col in ips_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data
df = load_and_process_data()

if df is not None:
    # Sidebar: Info dataset dan filter
    with st.sidebar:
        st.header("📊 Info Dataset")
        st.info(f"Total Data: {len(df)} mahasiswa")
        
        st.subheader("📁 Kolom Dataset")
        with st.expander("Lihat semua kolom"):
            for i, col in enumerate(df.columns.tolist(), 1):
                st.write(f"{i}. {col}")
        
        st.header("🎯 Filter Data")
        
        # Filter status kelulusan
        if 'status_kelulusan' in df.columns:
            status_options = df['status_kelulusan'].unique()
            selected_status = st.multiselect(
                "Status Kelulusan", 
                options=status_options, 
                default=status_options
            )
            df_filtered = df[df['status_kelulusan'].isin(selected_status)]
        else:
            df_filtered = df.copy()
            st.warning("Kolom 'status_kelulusan' tidak ditemukan")
        
        # Filter IPK range jika ada
        if 'ipk' in df.columns:
            ipk_min, ipk_max = float(df['ipk'].min()), float(df['ipk'].max())
            ipk_range = st.slider(
                "Range IPK", 
                min_value=ipk_min, 
                max_value=ipk_max, 
                value=(ipk_min, ipk_max),
                step=0.1
            )
            df_filtered = df_filtered[
                (df_filtered['ipk'] >= ipk_range[0]) & 
                (df_filtered['ipk'] <= ipk_range[1])
            ]

    # Main content area
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Mahasiswa", 
            value=len(df_filtered),
            delta=f"{len(df_filtered) - len(df)} dari filter"
        )
    
    with col2:
        if 'ipk' in df_filtered.columns:
            avg_ipk = df_filtered['ipk'].mean()
            st.metric(
                label="Rata-rata IPK", 
                value=f"{avg_ipk:.2f}",
                delta=f"{avg_ipk - df['ipk'].mean():.2f} vs total"
            )
    
    with col3:
        if 'jumlah_semester' in df_filtered.columns:
            avg_semester = df_filtered['jumlah_semester'].mean()
            st.metric(
                label="Rata-rata Semester", 
                value=f"{avg_semester:.1f}",
                delta=f"{avg_semester - df['jumlah_semester'].mean():.1f} vs total"
            )
    
    with col4:
        if 'status_kelulusan' in df_filtered.columns:
            graduation_rate = (df_filtered['status_kelulusan'] == 'Lulus').mean() * 100
            st.metric(
                label="Tingkat Kelulusan", 
                value=f"{graduation_rate:.1f}%"
            )

    st.markdown("---")

    # 1. Bar Chart: Status Kelulusan vs Faktor Lain
    st.subheader("📊 1. Distribusi Status Kelulusan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'status_kelulusan' in df_filtered.columns:
            fig_bar, ax_bar = plt.subplots(figsize=(8, 5))
            status_counts = df_filtered['status_kelulusan'].value_counts()
            bars = ax_bar.bar(status_counts.index, status_counts.values, 
                             color=sns.color_palette("husl", len(status_counts)))
            ax_bar.set_title("Distribusi Status Kelulusan", fontsize=14, fontweight='bold')
            ax_bar.set_xlabel("Status Kelulusan")
            ax_bar.set_ylabel("Jumlah Mahasiswa")
            
            # Add value labels on bars
            for bar, value in zip(bars, status_counts.values):
                ax_bar.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                           str(value), ha='center', va='bottom')
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig_bar)
    
    with col2:
        # Bar chart dengan breakdown berdasarkan kolom lain
        categorical_cols = df_filtered.select_dtypes(include=['object']).columns
        categorical_cols = [col for col in categorical_cols if col != 'status_kelulusan']
        
        if len(categorical_cols) > 0:
            breakdown_col = st.selectbox("Breakdown berdasarkan:", categorical_cols)
            if breakdown_col and 'status_kelulusan' in df_filtered.columns:
                fig_breakdown, ax_breakdown = plt.subplots(figsize=(8, 5))
                
                # Create crosstab for grouped bar chart
                crosstab_data = pd.crosstab(df_filtered['status_kelulusan'], df_filtered[breakdown_col])
                crosstab_data.plot(kind='bar', ax=ax_breakdown, 
                                 color=sns.color_palette("Set2", len(crosstab_data.columns)))
                
                ax_breakdown.set_title(f"Status Kelulusan vs {breakdown_col.replace('_', ' ').title()}", 
                                     fontsize=14, fontweight='bold')
                ax_breakdown.set_xlabel("Status Kelulusan")
                ax_breakdown.set_ylabel("Jumlah Mahasiswa")
                ax_breakdown.legend(title=breakdown_col.replace('_', ' ').title(), 
                                  bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig_breakdown)

    # Insight untuk Bar Chart
    st.markdown("""
    <div class="insight-box">
    <b>💡 Insight:</b> Grafik batang menunjukkan distribusi status kelulusan mahasiswa. 
    Perhatikan pola pada breakdown berdasarkan faktor lain untuk mengidentifikasi 
    karakteristik yang mempengaruhi tingkat kelulusan.
    </div>
    """, unsafe_allow_html=True)

    # 2. Scatter Plot: Hubungan antar variabel numerik
    st.subheader("🔵 2. Analisis Korelasi (Scatter Plot)")
    
    numeric_cols = df_filtered.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) >= 2:
        col1, col2 = st.columns(2)
        
        with col1:
            x_axis = st.selectbox("Pilih sumbu X:", numeric_cols, key="scatter_x")
        with col2:
            y_axis = st.selectbox("Pilih sumbu Y:", 
                                [col for col in numeric_cols if col != x_axis], 
                                key="scatter_y")
        
        if x_axis and y_axis:
            fig_scatter, ax_scatter = plt.subplots(figsize=(10, 6))
            
            if 'status_kelulusan' in df_filtered.columns:
                # Scatter plot dengan color berdasarkan status
                for status in df_filtered['status_kelulusan'].unique():
                    subset = df_filtered[df_filtered['status_kelulusan'] == status]
                    ax_scatter.scatter(subset[x_axis], subset[y_axis], 
                                     label=status, alpha=0.7, s=50)
                ax_scatter.legend(title="Status Kelulusan")
            else:
                ax_scatter.scatter(df_filtered[x_axis], df_filtered[y_axis], 
                                 alpha=0.7, s=50, color='steelblue')
            
            ax_scatter.set_xlabel(x_axis.replace('_', ' ').title())
            ax_scatter.set_ylabel(y_axis.replace('_', ' ').title())
            ax_scatter.set_title(f"Hubungan {x_axis.replace('_', ' ').title()} vs {y_axis.replace('_', ' ').title()}", 
                               fontsize=14, fontweight='bold')
            
            # Add trend line
            z = np.polyfit(df_filtered[x_axis].dropna(), df_filtered[y_axis].dropna(), 1)
            p = np.poly1d(z)
            ax_scatter.plot(df_filtered[x_axis], p(df_filtered[x_axis]), "r--", alpha=0.8, linewidth=2)
            
            plt.tight_layout()
            st.pyplot(fig_scatter)
            
            # Hitung korelasi
            correlation = df_filtered[x_axis].corr(df_filtered[y_axis])
            st.markdown(f"""
            <div class="insight-box">
            <b>📈 Korelasi:</b> {correlation:.3f} 
            {"(Korelasi kuat)" if abs(correlation) > 0.7 else 
             "(Korelasi sedang)" if abs(correlation) > 0.3 else "(Korelasi lemah)"}
            </div>
            """, unsafe_allow_html=True)

    # 3. Heatmap: Matriks Korelasi
    st.subheader("🔥 3. Matriks Korelasi (Heatmap)")
    
    if len(numeric_cols) >= 2:
        # Pilih kolom untuk analisis korelasi
        selected_cols = st.multiselect(
            "Pilih variabel untuk analisis korelasi:",
            numeric_cols,
            default=numeric_cols[:min(6, len(numeric_cols))]  # Max 6 kolom
        )
        
        if len(selected_cols) >= 2:
            corr_data = df_filtered[selected_cols].corr()
            
            # Create heatmap dengan matplotlib/seaborn
            fig_heatmap, ax_heatmap = plt.subplots(figsize=(10, 8))
            
            # Create mask for upper triangle (optional)
            mask = np.triu(np.ones_like(corr_data, dtype=bool))
            
            sns.heatmap(corr_data, 
                       annot=True, 
                       cmap='RdBu_r', 
                       center=0,
                       square=True,
                       mask=mask,
                       cbar_kws={"shrink": .8},
                       ax=ax_heatmap)
            
            ax_heatmap.set_title("Matriks Korelasi Antar Variabel", fontsize=14, fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig_heatmap)
            
            # Temukan korelasi tertinggi
            corr_pairs = []
            for i in range(len(corr_data.columns)):
                for j in range(i+1, len(corr_data.columns)):
                    corr_pairs.append({
                        'var1': corr_data.columns[i],
                        'var2': corr_data.columns[j],
                        'correlation': corr_data.iloc[i, j]
                    })
            
            corr_df = pd.DataFrame(corr_pairs)
            corr_df = corr_df.reindex(corr_df['correlation'].abs().sort_values(ascending=False).index)
            
            st.markdown("""
            <div class="insight-box">
            <b>🔍 Top 3 Korelasi Tertinggi:</b>
            """, unsafe_allow_html=True)
            
            for i, row in corr_df.head(3).iterrows():
                st.write(f"• {row['var1']} ↔ {row['var2']}: {row['correlation']:.3f}")
            
            st.markdown("</div>", unsafe_allow_html=True)

    # 4. Line Chart: Tren berdasarkan kategori
    st.subheader("📈 4. Analisis Tren (Line Chart)")
    
    if 'status_kelulusan' in df_filtered.columns and len(numeric_cols) > 0:
        metric_col = st.selectbox("Pilih metrik untuk analisis tren:", numeric_cols)
        
        if metric_col:
            # Tren berdasarkan status kelulusan
            trend_data = df_filtered.groupby('status_kelulusan')[metric_col].agg(['mean', 'std', 'count']).reset_index()
            
            fig_line, ax_line = plt.subplots(figsize=(10, 6))
            
            # Line plot dengan error bars
            ax_line.errorbar(range(len(trend_data)), trend_data['mean'], 
                           yerr=trend_data['std'], 
                           marker='o', markersize=8, linewidth=2, capsize=5)
            
            ax_line.set_xticks(range(len(trend_data)))
            ax_line.set_xticklabels(trend_data['status_kelulusan'], rotation=45)
            ax_line.set_ylabel(metric_col.replace('_', ' ').title())
            ax_line.set_title(f"Tren {metric_col.replace('_', ' ').title()} berdasarkan Status Kelulusan", 
                            fontsize=14, fontweight='bold')
            ax_line.grid(True, alpha=0.3)
            
            # Add value labels
            for i, (mean_val, std_val) in enumerate(zip(trend_data['mean'], trend_data['std'])):
                ax_line.annotate(f'{mean_val:.2f}±{std_val:.2f}', 
                               (i, mean_val), textcoords="offset points", 
                               xytext=(0,10), ha='center')
            
            plt.tight_layout()
            st.pyplot(fig_line)

    # 5. Pie Chart: Proporsi kategorikal
    st.subheader("🥧 5. Distribusi Proporsi (Pie Chart)")
    
    categorical_cols = df_filtered.select_dtypes(include=['object']).columns.tolist()
    
    if len(categorical_cols) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            pie_col = st.selectbox("Pilih variabel untuk pie chart:", categorical_cols)
        
        if pie_col:
            pie_data = df_filtered[pie_col].value_counts()
            
            with col2:
                show_percentage = st.checkbox("Tampilkan persentase", value=True)
            
            fig_pie, ax_pie = plt.subplots(figsize=(8, 8))
            
            # Create pie chart
            colors = sns.color_palette("Set3", len(pie_data))
            wedges, texts, autotexts = ax_pie.pie(pie_data.values, 
                                                 labels=pie_data.index,
                                                 autopct='%1.1f%%' if show_percentage else lambda pct: f'{int(pct/100*len(df_filtered))}',
                                                 startangle=90,
                                                 colors=colors,
                                                 textprops={'fontsize': 10})
            
            # Make it a donut chart
            centre_circle = plt.Circle((0,0), 0.40, fc='white')
            ax_pie.add_artist(centre_circle)
            
            ax_pie.set_title(f"Distribusi {pie_col.replace('_', ' ').title()}", 
                           fontsize=14, fontweight='bold', pad=20)
            
            # Add center text
            ax_pie.text(0, 0, f'Total\n{len(df_filtered)}', 
                       horizontalalignment='center', verticalalignment='center',
                       fontsize=12, fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig_pie)
            
            # Summary statistics
            st.markdown(f"""
            <div class="insight-box">
            <b>📊 Ringkasan {pie_col.replace('_', ' ').title()}:</b><br>
            • Total kategori: {len(pie_data)}<br>
            • Kategori terbanyak: {pie_data.index[0]} ({pie_data.iloc[0]} mahasiswa)<br>
            • Kategori tersedikit: {pie_data.index[-1]} ({pie_data.iloc[-1]} mahasiswa)
            </div>
            """, unsafe_allow_html=True)

    # Summary dan Insights
    st.markdown("---")
    st.subheader("🎯 Ringkasan dan Rekomendasi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box">
        <b>📈 Key Findings:</b><br>
        • Analisis 5 jenis visualisasi memberikan perspektif holistik<br>
        • Identifikasi pola dan korelasi antar variabel<br>
        • Pemahaman distribusi dan proporsi data<br>
        • Insight untuk pengambilan keputusan berbasis data
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
        <b>🎯 Rekomendasi:</b><br>
        • Fokus pada faktor dengan korelasi tinggi<br>
        • Intervensi dini untuk mahasiswa berisiko<br>
        • Optimalisasi program berdasarkan pola data<br>
        • Monitoring berkelanjutan dengan dashboard ini
        </div>
        """, unsafe_allow_html=True)

    # Download hasil analisis
    st.markdown("---")
    if st.button("📊 Generate Summary Report"):
        summary_data = {
            'Total_Mahasiswa': len(df_filtered),
            'Rata_rata_IPK': df_filtered['ipk'].mean() if 'ipk' in df_filtered.columns else 'N/A',
            'Rata_rata_Semester': df_filtered['jumlah_semester'].mean() if 'jumlah_semester' in df_filtered.columns else 'N/A',
        }
        
        st.json(summary_data)
        st.success("✅ Summary report berhasil di-generate!")

else:
    st.error("❌ Gagal memuat dataset. Pastikan file 'dataset_kelulusan_mahasiswa.csv' tersedia.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><b>🎓 Dashboard Kelulusan Mahasiswa</b></p>
    <p>Kelompok 10 [Muhammad Afif Naufal - Luthfiyah Syaharani - Ilham Arifin] | Proyek Visualisasi Data 2025</p>
    <p><i>Powered by Streamlit, Plotly & Python</i></p>
</div>
""", unsafe_allow_html=True)