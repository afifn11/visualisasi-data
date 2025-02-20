import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Judul aplikasi
st.title("Visualisasi Data dengan Streamlit")

# Contoh data
np.random.seed(42)
data = pd.DataFrame({
    'Kategori': ['A', 'B', 'C', 'D', 'E'],
    'Nilai': np.random.randint(10, 100, 5)
})

# Menampilkan DataFrame
st.write("### Data:")
st.dataframe(data)

# Membuat visualisasi
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='Kategori', y='Nilai', hue='Kategori', data=data, palette='viridis', ax=ax, legend=False)
ax.set_title('Visualisasi Data dengan Bar Plot')
ax.set_xlabel('Kategori')
ax.set_ylabel('Nilai')

# Menampilkan plot di Streamlit
st.pyplot(fig)
