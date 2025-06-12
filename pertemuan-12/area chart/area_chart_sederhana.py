import matplotlib.pyplot as plt
import numpy as np

# Data Penjualan Bulanan
months = np.array(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
shoes = np.array([150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700])

# Membuat Area Chart
plt.figure(figsize=(10, 6))
plt.fill_between(months, shoes, color='skyblue', alpha=0.4)
plt.title('Basic Area Chart: Monthly Shoe Sales')
plt.xlabel('Months')
plt.ylabel('Number of Shoes Sold')
plt.legend('Units Sold')
plt.show()