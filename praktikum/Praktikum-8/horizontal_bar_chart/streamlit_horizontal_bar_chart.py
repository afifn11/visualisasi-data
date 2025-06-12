import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Penjualan Smartphone Berdasarkan Merrek")
st.subheader("Horizontal Bar Chart Sederhana")

# Data Penjualan Smartphone
brands = ['Samsung', 'Apple', 'Xiaomi', 'Oppo', 'Vivo']
sales_2023 = [100, 80, 60, 50, 40]

# Membuat Horizontal Bar Chart
fig, ax = plt.subplots()
y = np.arange(len(brands))
ax.barh(y, sales_2023, color=colors)
ax.set_yticks(y)
ax.set_yticklabels(brands)
ax.set_xlabel('Jumlah Penjualan')
ax.set_ylabel('Merek Smartphone')
ax.set_title('Penjualan Smartphone 2023')

# Warna berbeda untuk setiap bar
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

fig, ax = plt.subplots()
ax.barh(y, sales_2023, color=colors)

# Menambahkan nilai pada setiap bar
for i, v in enumerate(sales_2023):
    ax.text(v + 1, i, str(v), color='black', va='center')



# Menampilkan chart di Streamlit
st.pyplot(fig)