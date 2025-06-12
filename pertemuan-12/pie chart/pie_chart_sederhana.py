import matplotlib.pyplot as plt

# Data Partisipasi siswa
kegiatan = ['Olahraga', 'Musik', 'Seni', 'Sains', 'Teknologi']
persentase = [25, 15, 20, 30, 10]

# membuat pie chart
plt.pie(persentase, labels=kegiatan, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'])
plt.title('Partisipasi Siswa dalam Kegiatan Ekstrakurikuler')
plt.show()

