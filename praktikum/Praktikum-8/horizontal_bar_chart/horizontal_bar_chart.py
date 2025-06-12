import matplotlib.pyplot as plt
import numpy as np

# Data Penjualan Smartphone
brands = ['Samsung', 'Apple', 'Xiaomi', 'Oppo', 'Vivo']
sales_2023 = [100, 80, 60, 50, 40]
sales_2024 = [120, 90, 70, 60, 50]
sales_2025 = [140, 100, 80, 70, 60]

plt.barh(brands, sales_2023, color='blue')
plt.title('Penjualan Smartphone 2023')
plt.xlabel('Jumlah Penjualan')
plt.ylabel('Merek Smartphone')
plt.show()