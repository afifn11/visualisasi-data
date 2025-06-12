import matplotlib.pyplot as plt
import numpy as np

# Data Penjualan Bulanan
months = {'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'}
shoes = [150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700]
sandals = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650]

plt.figure(figsize=(10, 6))
plt.fill_between(months, shoes, color='skyblue', alpha=0.4, label='Shoes Sold')
plt.fill_between(months, sandals, color='lightgreen', alpha=0.4, label='Sandals Sold')
plt.title('Kustomisasi Area Chart: Penjualan Bulanan Sepatu dan Sandal')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Terjual')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.show()