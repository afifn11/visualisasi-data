import streamlit as st
import matplotlib.pyplot as plt
import random

# Data identitas
nama = "Muhammad Afif Naufal"
nim = "0110223240"
prodi = "Teknik Informatika"
peminatan = "Software Engineering"

# Data mata kuliah dan jumlah peserta (acak)
mata_kuliah = ['Agama', 'PPKN', 'RPL', 'Big Data', 'Basis Data', 'Visualisasi Data']
jumlah_peserta = [random.randint(10, 30) for _ in mata_kuliah]

# Warna untuk tiap bagian
colors = ['lightcoral', 'green', 'lightgreen', 'royalblue', 'lightblue', 'red']

# Judul halaman
st.title("Distribusi Jumlah Peserta Perkuliahan")
st.markdown(f"**Nama:** {nama}  \n**NIM:** {nim}  \n**Prodi:** {prodi}  \n**Peminatan:** {peminatan}")

# Membuat grafik pie
fig, ax = plt.subplots(figsize=(2, 2))
ax.pie(jumlah_peserta, labels=mata_kuliah, colors=colors, autopct='%1.1f%%', startangle=140)
ax.set_title("Distribusi Jumlah Peserta Perkuliahan", fontsize=12, fontweight='bold')
ax.axis('equal')

# Tampilkan grafik di Streamlit
st.pyplot(fig)
