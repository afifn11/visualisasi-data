import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
from PIL import Image
import base64
import datetime
import time

# Tampilan kelompok (WAJIB ADA di setiap skrip)
st.title("Kelompok Visualisasi Data")
st.write("Nama Anggota:")
st.write("- Muhammad Afif Naufal (0110223240)")
st.write("- Ilham Arifin (01102232)")
st.write("- Luthfiyah Syaharani (0110223238)")

# ===== Text Elements =====
st.header("1. Text Elements")

# Title, Header, Subheader
st.title("This is our Title")
st.header("This is our Header")
st.subheader("This is our Sub-header")
st.caption("This is our Caption")

# Plain Text
st.text("Hi,\nPeople\t!!!!!!!!!!")
st.text('Welcome to')
st.text("Streamlit's World")

# Markdown
st.markdown("# Hi,\n# ***People*** \t!!!!!!!!!!")
st.markdown("# Welcome to")
st.markdown("### Streamlit's World")

# LaTeX
st.latex(r'\cos2\theta = 1 - 2\sin^2\theta')
st.latex("""(a+b)^2 = a^2 + b^2 + 2ab""")
st.latex(r'''\frac{\partial}{\partial t} 
= h^2 \left( \frac{\partial^2}{\partial x^2} 
+ \frac{\partial^2}{\partial y^2} 
+ \frac{\partial^2}{\partial z^2} \right)''')

# Display Code
st.subheader("Python Code")
code = '''def hello():
    print("Hello, Streamlit!")'''
st.code(code, language='python')

st.subheader("Java Code")
st.code('''public class GPG {
    public static void main(String args[])
    {
        System.out.println("Hello World");
    }
}''', language='java')

st.subheader("JavaScript Code")
st.code('''<p id="demo"></p>
<script>
try {
    addAlert("Welcome guest!");
}
catch(err) {
    document.getElementById("demo").innerHTML = err.message;
}
</script>''', language='javascript')

# ===== Data Elements =====
st.header("2. Data Elements")

# DataFrame
df = pd.DataFrame(
    np.random.randn(30, 10),
    columns=[f'col_no {i}' for i in range(10)]
)
st.dataframe(df)

# Highlighted DataFrame
st.dataframe(df.style.highlight_min(axis=0))

# Table
st.table(df.head(10))

# Metrics
st.metric(label="Temperature", value="31 °C", delta="1.2 °C")

# Metrics in columns
c1, c2, c3 = st.columns(3)
c1.metric("Rainfall", "100 cm", "10 cm")
c2.metric(label="Population", value="123 Billions", delta="1 Billions", delta_color="inverse")
c3.metric(label="Customers", value=100, delta=10, delta_color="off")
st.metric(label="Speed", value=None, delta=0)
st.metric("Traces", "91456", "-1132649")

# ===== Media Elements =====
st.header("3. Media Elements")

# Single Image (gunakan path yang sesuai)
# st.image("path/to/image.jpg")

# Multiple Images
animal_images = [
    "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7",
    "https://images.unsplash.com/photo-1551963831-b3b1ca40c98e",
    "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13"
]
st.image(animal_images, width=200, caption=["Image 1", "Image 2", "Image 3"])

# Background Image (contoh)
def add_local_background_image(image):
    with open(image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ===== Interactive Elements =====
st.header("4. Interactive Elements")

# Button
st.title('Creating a Button')
button = st.button('Click Here')
if button:
    st.write('You have clicked the Button')
else:
    st.write('You have not clicked the Button')

# Radio Buttons
st.title('Creating Radio Buttons')
gender = st.radio(
    "Select your Gender",
    ('Male', 'Female', 'Others'))
if gender == 'Male':
    st.write('You have selected Male.')
elif gender == 'Female':
    st.write('You have selected Female.')
else:
    st.write('You have selected Others.')

# Check Boxes
st.title('Creating Checkboxes')
st.write('Select your Hobbies:')
check_1 = st.checkbox('Books')
check_2 = st.checkbox('Movies')
check_3 = st.checkbox('Sports')

# Drop-Downs
st.title('Creating Dropdown')
hobby = st.selectbox('Choose your hobby:', ('Books', 'Movies', 'Sports'))
st.write(f'You selected: {hobby}')

# Multiselects
st.title("Multi-Select")
hobbies = st.multiselect(
    'What are your Hobbies',
    ['Reading', 'Cooking', 'Watching Movies/TV Series', 'Playing', 'Drawing', 'Hiking'], 
    ['Reading', 'Playing'])
st.write(f'You selected: {hobbies}')

# Download Buttons
st.title("Download Button")
# Contoh dengan file dummy (ganti dengan path yang sesuai)
# st.download_button(
#     label="Download Image",
#     data=open("path/to/image.jpg", "rb"),
#     file_name="image.jpg",
#     mime='image/jpg'
# )

# Progress Bars
st.title("Progress Bar")
if st.button('Start Progress'):
    download = st.progress(0)
    for percentage in range(100):
        time.sleep(0.05)
        download.progress(percentage+1)
    st.write('Download Complete')

# Spinners
st.title('Spinner')
if st.button('Show Spinner'):
    with st.spinner('Loading...'):
        time.sleep(3)
    st.write('Hello Data Scientists')

# ===== Form Elements =====
st.header("5. Form Elements")

# Text Input
st.title("Text Box")
name = st.text_input("Enter your Name")
st.write("Your Name is ", name)

# Text Input with limit
name = st.text_input("Enter your Name (max 10 chars)", max_chars=10)
password = st.text_input("Enter your password", type='password')

# Text Area
input_text = st.text_area("Enter your Review")
st.write("You entered: \n", input_text)

# Number Input
num = st.number_input("Enter your Number", 0, 10, 5, 2)
st.write("Min. Value is 0, \nMax. value is 10")
st.write("Default Value is 5, \nStep Size value is 2")
st.write("Total value after adding Number entered with step value is:", num)

# Time Input
st.title("Time")
appointment = st.time_input("Select Your Time")
st.write("You selected:", appointment)

# Date Input
st.title("Date")
today = st.date_input("Select Date")
birthday = st.date_input(
    "Select Your Birthday", 
    value=datetime.date(1990, 1, 1),
    min_value=datetime.date(1980, 1, 1),
    max_value=datetime.date(2000, 12, 31)
)

# Color Picker
st.title("Select color")
color_code = st.color_picker("Select your Color", "#00f900")
st.write("Selected color code:", color_code)

# File Upload
st.title("CSV Data")
data_file = st.file_uploader("Upload CSV", type=['csv'])
details = st.button("Check Details")
if details:
    if data_file is not None:
        file_details = {
            "file_name": data_file.name, 
            "file_type": data_file.type,
            "file_size": data_file.size
        }
        st.write(file_details)
        df = pd.read_csv(data_file)
        st.dataframe(df)
    else:
        st.write("No CSV File is Uploaded")

# Form with Submit
st.title("Form with Submit")
with st.form(key='my_form'):
    text_input = st.text_input(label='Enter some text')
    number_input = st.number_input(label='Enter a number')
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    st.write("Form submitted!")
    st.write(f"Text: {text_input}")
    st.write(f"Number: {number_input}")