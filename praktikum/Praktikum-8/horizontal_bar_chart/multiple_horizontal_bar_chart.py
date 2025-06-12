import matplotlib.pyplot as plt
import numpy as np

# Data Penjualan Smartphone
brands = ['Samsung', 'Apple', 'Xiaomi', 'Oppo', 'Vivo']
sales_2023 = [100, 80, 60, 50, 40]
sales_2024 = [90, 70, 65, 55, 45]
sales_2025 = [110, 85, 75, 65, 55]

y_pos = np.arange(len(brands))
plt.barh(y_pos - 0.2, sales_2023, height=0.2, color='blue', label='2023')
plt.barh(y_pos + sales_2024, height=0.2, color='orange', label='2024')
plt.yticks(y_pos, brands)
plt.title('Perbandingan Penjualan Smartphone 2023-2025')
plt.xlabel('Jumlah Penjualan')
plt.ylabel('Merek Smartphone')
plt.legend()
plt.show()