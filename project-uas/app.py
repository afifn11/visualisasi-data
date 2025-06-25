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

# Setup halaman dengan konfigurasi responsif
st.set_page_config(
    page_title="Dashboard Kelulusan Mahasiswa", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🎓"
)

# Custom CSS untuk styling responsif
st.markdown("""
<style>
    /* Responsive design untuk semua device */
    .main-header {
        font-size: clamp(1.5rem, 4vw, 2.5rem);
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        padding: 0 1rem;
    }
    
    .team-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    .team-member {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
        padding: 0.5rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        backdrop-filter: blur(10px);
    }
    
    .metric-card {
        background-color: #471396;
        padding: 1rem;
        border-radius: 0.8rem;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .insight-box {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.2);
    }
    
    /* Responsif untuk mobile */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.8rem;
            line-height: 1.2;
        }
        
        .team-member {
            flex-direction: column;
            text-align: center;
        }
        
        .metric-card {
            margin: 0.3rem 0;
            padding: 0.8rem;
        }
        
        .insight-box {
            padding: 1rem;
            font-size: 0.9rem;
        }
    }
    
    /* Animasi hover untuk interaktivitas */
    .team-info:hover {
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    
    /* Responsive charts container */
    .chart-container {
        width: 100%;
        height: auto;
        overflow-x: auto;
    }
    
    /* Sidebar responsif */
    @media (max-width: 768px) {
        .css-1d391kg {
            padding-top: 1rem;
        }
    }
    
    /* Footer styling */
    .footer {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem 1rem;
        border-radius: 1rem;
        text-align: center;
        margin-top: 2rem;
    }
    
    .footer-content {
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Responsive button */
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Header utama dengan informasi kelompok
st.markdown('<h1 class="main-header">🎓 Dashboard Visualisasi Kelulusan Mahasiswa</h1>', unsafe_allow_html=True)

# Informasi tim di bagian atas
st.markdown("""
<div class="team-info">
    <h3 style="text-align: center; margin-bottom: 1rem; font-size: 1.3rem;">
        👥 Kelompok 10 - Proyek Visualisasi Data 2025
    </h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
        <div class="team-member">
            <div style="margin-right: 1rem; font-size: 1.5rem;">👨‍💻</div>
            <div>
                <strong>Muhammad Afif Naufal</strong><br>
                <small>NIM: 0110223240</small>
            </div>
        </div>
        <div class="team-member">
            <div style="margin-right: 1rem; font-size: 1.5rem;">👩‍💻</div>
            <div>
                <strong>Luthfiyah Syaharani</strong><br>
                <small>NIM: 0110223238</small>
            </div>
        </div>
        <div class="team-member">
            <div style="margin-right: 1rem; font-size: 1.5rem;">👨‍💻</div>
            <div>
                <strong>Ilham Arifin</strong><br>
                <small>NIM: 0110223244</small>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

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

    # Main content area - Metrics dengan layout responsif
    st.subheader("📈 Statistik Utama")
    
    # Gunakan container untuk metrics yang responsif
    metrics_container = st.container()
    with metrics_container:
        # Responsive columns - akan menjadi 2 kolom di mobile, 4 di desktop
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>📊 Total Mahasiswa</h4>
                <h2 style="color: #1f77b4; margin: 0;">{}</h2>
                <small>Filter: {}</small>
            </div>
            """.format(len(df_filtered), f"{len(df_filtered) - len(df):+d} dari total"), 
            unsafe_allow_html=True)
        
        with col2:
            if 'ipk' in df_filtered.columns:
                avg_ipk = df_filtered['ipk'].mean()
                st.markdown("""
                <div class="metric-card">
                    <h4>🎯 Rata-rata IPK</h4>
                    <h2 style="color: #1f77b4; margin: 0;">{:.2f}</h2>
                    <small>Δ {:.2f} vs total</small>
                </div>
                """.format(avg_ipk, avg_ipk - df['ipk'].mean()), 
                unsafe_allow_html=True)
        
        with col3:
            if 'jumlah_semester' in df_filtered.columns:
                avg_semester = df_filtered['jumlah_semester'].mean()
                st.markdown("""
                <div class="metric-card">
                    <h4>📅 Rata-rata Semester</h4>
                    <h2 style="color: #1f77b4; margin: 0;">{:.1f}</h2>
                    <small>Δ {:.1f} vs total</small>
                </div>
                """.format(avg_semester, avg_semester - df['jumlah_semester'].mean()), 
                unsafe_allow_html=True)
        
        with col4:
            if 'status_kelulusan' in df_filtered.columns:
                graduation_rate = (df_filtered['status_kelulusan'] == 'Lulus').mean() * 100
                st.markdown("""
                <div class="metric-card">
                    <h4>🎓 Tingkat Kelulusan</h4>
                    <h2 style="color: #1f77b4; margin: 0;">{:.1f}%</h2>
                    <small>Success Rate</small>
                </div>
                """.format(graduation_rate), 
                unsafe_allow_html=True)

    st.markdown("---")

    # 1. Bar Chart: Status Kelulusan vs Faktor Lain
    st.subheader("📊 1. Distribusi Status Kelulusan")
    
    # Responsive layout untuk charts
    chart_col1, chart_col2 = st.columns([1, 1])
    
    with chart_col1:
        if 'status_kelulusan' in df_filtered.columns:
            # Set figure size berdasarkan lebar layar
            fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
            status_counts = df_filtered['status_kelulusan'].value_counts()
            bars = ax_bar.bar(status_counts.index, status_counts.values, 
                             color=sns.color_palette("husl", len(status_counts)))
            ax_bar.set_title("Distribusi Status Kelulusan", fontsize=14, fontweight='bold')
            ax_bar.set_xlabel("Status Kelulusan")
            ax_bar.set_ylabel("Jumlah Mahasiswa")
            
            # Add value labels on bars
            for bar, value in zip(bars, status_counts.values):
                ax_bar.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                           str(value), ha='center', va='bottom', fontweight='bold')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig_bar, use_container_width=True)
    
    with chart_col2:
        # Bar chart dengan breakdown berdasarkan kolom lain
        categorical_cols = df_filtered.select_dtypes(include=['object']).columns
        categorical_cols = [col for col in categorical_cols if col != 'status_kelulusan']
        
        if len(categorical_cols) > 0:
            breakdown_col = st.selectbox("Breakdown berdasarkan:", categorical_cols)
            if breakdown_col and 'status_kelulusan' in df_filtered.columns:
                fig_breakdown, ax_breakdown = plt.subplots(figsize=(10, 6))
                
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
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig_breakdown, use_container_width=True)

    # Insight untuk Bar Chart
    st.markdown("""
    <div class="insight-box">
    <strong>💡 Insight:</strong> Grafik batang menunjukkan distribusi status kelulusan mahasiswa. 
    Perhatikan pola pada breakdown berdasarkan faktor lain untuk mengidentifikasi 
    karakteristik yang mempengaruhi tingkat kelulusan.
    </div>
    """, unsafe_allow_html=True)

    # 2. Scatter Plot: Hubungan antar variabel numerik
    st.subheader("🔵 2. Analisis Korelasi (Scatter Plot)")
    
    numeric_cols = df_filtered.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) >= 2:
        # Responsive selection layout
        select_col1, select_col2 = st.columns(2)
        
        with select_col1:
            x_axis = st.selectbox("Pilih sumbu X:", numeric_cols, key="scatter_x")
        with select_col2:
            y_axis = st.selectbox("Pilih sumbu Y:", 
                                [col for col in numeric_cols if col != x_axis], 
                                key="scatter_y")
        
        if x_axis and y_axis:
            fig_scatter, ax_scatter = plt.subplots(figsize=(12, 8))
            
            if 'status_kelulusan' in df_filtered.columns:
                # Scatter plot dengan color berdasarkan status
                for status in df_filtered['status_kelulusan'].unique():
                    subset = df_filtered[df_filtered['status_kelulusan'] == status]
                    ax_scatter.scatter(subset[x_axis], subset[y_axis], 
                                     label=status, alpha=0.7, s=60)
                ax_scatter.legend(title="Status Kelulusan")
            else:
                ax_scatter.scatter(df_filtered[x_axis], df_filtered[y_axis], 
                                 alpha=0.7, s=60, color='steelblue')
            
            ax_scatter.set_xlabel(x_axis.replace('_', ' ').title(), fontsize=12)
            ax_scatter.set_ylabel(y_axis.replace('_', ' ').title(), fontsize=12)
            ax_scatter.set_title(f"Hubungan {x_axis.replace('_', ' ').title()} vs {y_axis.replace('_', ' ').title()}", 
                               fontsize=14, fontweight='bold')
            
            # Add trend line
            if len(df_filtered[x_axis].dropna()) > 1 and len(df_filtered[y_axis].dropna()) > 1:
                z = np.polyfit(df_filtered[x_axis].dropna(), df_filtered[y_axis].dropna(), 1)
                p = np.poly1d(z)
                ax_scatter.plot(df_filtered[x_axis], p(df_filtered[x_axis]), "r--", alpha=0.8, linewidth=2)
            
            ax_scatter.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig_scatter, use_container_width=True)
            
            # Hitung korelasi
            correlation = df_filtered[x_axis].corr(df_filtered[y_axis])
            st.markdown(f"""
            <div class="insight-box">
            <strong>📈 Korelasi:</strong> {correlation:.3f} 
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
            
            # Create heatmap dengan ukuran responsif
            fig_heatmap, ax_heatmap = plt.subplots(figsize=(12, 10))
            
            # Create mask for upper triangle (optional)
            mask = np.triu(np.ones_like(corr_data, dtype=bool))
            
            sns.heatmap(corr_data, 
                       annot=True, 
                       cmap='RdBu_r', 
                       center=0,
                       square=True,
                       mask=mask,
                       cbar_kws={"shrink": .8},
                       ax=ax_heatmap,
                       fmt='.3f',
                       annot_kws={'fontsize': 10})
            
            ax_heatmap.set_title("Matriks Korelasi Antar Variabel", fontsize=16, fontweight='bold', pad=20)
            plt.tight_layout()
            st.pyplot(fig_heatmap, use_container_width=True)
            
            # Temukan korelasi tertinggi
            corr_pairs = []
            for i in range(len(corr_data.columns)):
                for j in range(i+1, len(corr_data.columns)):
                    corr_pairs.append({
                        'var1': corr_data.columns[i],
                        'var2': corr_data.columns[j],
                        'correlation': corr_data.iloc[i, j]
                    })
            
            if corr_pairs:
                corr_df = pd.DataFrame(corr_pairs)
                corr_df = corr_df.reindex(corr_df['correlation'].abs().sort_values(ascending=False).index)
                
                st.markdown("""
                <div class="insight-box">
                <strong>🔍 Top 3 Korelasi Tertinggi:</strong><br>
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
            
            fig_line, ax_line = plt.subplots(figsize=(12, 8))
            
            # Line plot dengan error bars
            ax_line.errorbar(range(len(trend_data)), trend_data['mean'], 
                           yerr=trend_data['std'], 
                           marker='o', markersize=10, linewidth=3, capsize=8,
                           color='#1f77b4', markerfacecolor='white', markeredgewidth=2)
            
            ax_line.set_xticks(range(len(trend_data)))
            ax_line.set_xticklabels(trend_data['status_kelulusan'], rotation=45, ha='right')
            ax_line.set_ylabel(metric_col.replace('_', ' ').title(), fontsize=12)
            ax_line.set_title(f"Tren {metric_col.replace('_', ' ').title()} berdasarkan Status Kelulusan", 
                            fontsize=14, fontweight='bold')
            ax_line.grid(True, alpha=0.3)
            
            # Add value labels
            for i, (mean_val, std_val) in enumerate(zip(trend_data['mean'], trend_data['std'])):
                ax_line.annotate(f'{mean_val:.2f}±{std_val:.2f}', 
                               (i, mean_val), textcoords="offset points", 
                               xytext=(0,15), ha='center', fontweight='bold',
                               bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
            
            plt.tight_layout()
            st.pyplot(fig_line, use_container_width=True)

    # 5. Pie Chart: Proporsi kategorikal
    st.subheader("🥧 5. Distribusi Proporsi (Pie Chart)")
    
    categorical_cols = df_filtered.select_dtypes(include=['object']).columns.tolist()
    
    if len(categorical_cols) > 0:
        pie_col1, pie_col2 = st.columns([2, 1])
        
        with pie_col2:
            pie_col = st.selectbox("Pilih variabel untuk pie chart:", categorical_cols)
            show_percentage = st.checkbox("Tampilkan persentase", value=True)
        
        if pie_col:
            pie_data = df_filtered[pie_col].value_counts()
            
            with pie_col1:
                fig_pie, ax_pie = plt.subplots(figsize=(10, 10))
                
                # Create pie chart
                colors = sns.color_palette("Set3", len(pie_data))
                wedges, texts, autotexts = ax_pie.pie(pie_data.values, 
                                                     labels=pie_data.index,
                                                     autopct='%1.1f%%' if show_percentage else lambda pct: f'{int(pct/100*len(df_filtered))}',
                                                     startangle=90,
                                                     colors=colors,
                                                     textprops={'fontsize': 11, 'fontweight': 'bold'},
                                                     pctdistance=0.85)
                
                # Make it a donut chart
                centre_circle = plt.Circle((0,0), 0.40, fc='white')
                ax_pie.add_artist(centre_circle)
                
                ax_pie.set_title(f"Distribusi {pie_col.replace('_', ' ').title()}", 
                               fontsize=16, fontweight='bold', pad=20)
                
                # Add center text
                ax_pie.text(0, 0, f'Total\n{len(df_filtered)}', 
                           horizontalalignment='center', verticalalignment='center',
                           fontsize=14, fontweight='bold')
                
                plt.tight_layout()
                st.pyplot(fig_pie, use_container_width=True)
                
            # Summary statistics
            st.markdown(f"""
            <div class="insight-box">
            <strong>📊 Ringkasan {pie_col.replace('_', ' ').title()}:</strong><br>
            • Total kategori: {len(pie_data)}<br>
            • Kategori terbanyak: {pie_data.index[0]} ({pie_data.iloc[0]} mahasiswa)<br>
            • Kategori tersedikit: {pie_data.index[-1]} ({pie_data.iloc[-1]} mahasiswa)
            </div>
            """, unsafe_allow_html=True)

    # Summary dan Insights
    st.markdown("---")
    st.subheader("🎯 Ringkasan dan Rekomendasi")
    
    summary_col1, summary_col2 = st.columns(2)
    
    with summary_col1:
        st.markdown("""
        <div class="insight-box">
        <strong>📈 Key Findings:</strong><br>
        • Analisis 5 jenis visualisasi memberikan perspektif holistik<br>
        • Identifikasi pola dan korelasi antar variabel<br>
        • Pemahaman distribusi dan proporsi data<br>
        • Insight untuk pengambilan keputusan berbasis data
        </div>
        """, unsafe_allow_html=True)
    
    with summary_col2:
        st.markdown("""
        <div class="insight-box">
        <strong>🎯 Rekomendasi:</strong><br>
        • Fokus pada faktor dengan korelasi tinggi<br>
        • Intervensi dini untuk mahasiswa berisiko<br>
        • Optimalisasi program berdasarkan pola data<br>
        • Monitoring berkelanjutan dengan dashboard ini
        </div>
        """, unsafe_allow_html=True)

    # Download hasil analisis
    st.markdown("---")
    if st.button("📊 Generate Summary Report", key="summary_btn"):
        summary_data = {
            'Total_Mahasiswa': len(df_filtered),
            'Rata_rata_IPK': df_filtered['ipk'].mean() if 'ipk' in df_filtered.columns else 'N/A',
            'Rata_rata_Semester': df_filtered['jumlah_semester'].mean() if 'jumlah_semester' in df_filtered.columns else 'N/A',
            'Tingkat_Kelulusan': f"{(df_filtered['status_kelulusan'] == 'Lulus').mean() * 100:.1f}%" if 'status_kelulusan' in df_filtered.columns else 'N/A'
        }
        
        st.json(summary_data)
        st.success("✅ Summary report berhasil di-generate!")

else:
    st.error("❌ Gagal memuat dataset. Pastikan file 'dataset_kelulusan_mahasiswa.csv' tersedia.")

# Footer dengan informasi lengkap
st.markdown("""
<div class="footer">
    <div class="footer-content">
        <h3 style="margin-bottom: 1rem;">🎓 Dashboard Kelulusan Mahasiswa</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1rem 0;">
            <div>
                <strong>📋 Proyek:</strong><br>
                Visualisasi Data 2025
            </div>
            <div>
                <strong>👥 Kelompok 10:</strong><br>
                3 Anggota Tim
            </div>
            <div>
                <strong>🛠️ Teknologi:</strong><br>
                Streamlit, Matplotlib, Seaborn
            </div>
        </div>
        <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.3);">
            <p style="margin: 0.5rem 0;"><strong>🏫 STT Terpadu Nurul Fikri</strong></p>
            <p style="margin: 0.5rem 0;"><strong>📅 Tahun Akademik 2024/2025</strong></p>
            <p style="margin: 0.5rem 0;"><em>💡 "Faktor-Faktor yang Mempengaruhi Kelulusan Mahasiswa di Perguruan Tinggi"</em></p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)