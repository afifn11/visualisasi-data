import matplotlib.pyplot as plt

# Data dummy
suhu = [20, 22, 24,26, 28, 30, 32, 34, 36, 38]
penjualan = [50, 60, 70, 80, 90, 100, 110, 130, 180]
# Membuat scatter plot
plt.scatter(suhu, penjualan, color='blue')
plt.title('Hubungan Penjualan Es Krim dan Suhu')
plt.xlabel('Suhu (°C)')
plt.ylabel('Penjualan Es Krim')
# Menampilkan plot
plt.show()