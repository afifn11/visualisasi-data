import matplotlib.pyplot as plt
import numpy as np

# Data Penjualan Bulanan
moths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
shoes = [150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700]
sandals = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650]
socks = [80, 120, 160, 200, 240, 280, 320, 360, 400, 440, 480, 520]

# multiple area chart
plt.figure(figsize=(10, 6))
plt.fill_between(moths, shoes, color='skyblue', alpha=0.4, label='Shoes Sold')
plt.fill_between(moths, sandals, color='lightgreen', alpha=0.4, label='Sandals Sold')
plt.fill_between(moths, socks, color='lightcoral', alpha=0.4, label='Socks Sold')
plt.title('Multiple Area Chart: Monthly Sales of Shoes, Sandals, and Socks')
plt.xlabel('Months')
plt.ylabel('Number of Items Sold')
plt.legend()
plt.show()


