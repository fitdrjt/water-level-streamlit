import streamlit as st
import pandas as pd
import plotly.express as px

# Fungsi untuk membaca data dari file CSV
def load_data(sheet_name):
    df = pd.read_excel("ireland_water_level_hourly.xlsx", sheet_name=sheet_name)
    df['time'] = pd.to_datetime(df['time'])  
    return df

# Fungsi untuk menampilkan halaman utama
def main_page():
    st.title("🌊 Water Level Monitoring in Ireland 🌊")
    st.write("""
    This project aims to showcase water level data across multiple locations in Ireland, providing users with an intuitive and interactive experience.  

    📍 **Choose from Three Locations:**  
    Dublin, Galway, and Sligo with data sourced from [Digital Ocean Ireland](https://www.digitalocean.ie/Data/DownloadTideData).  

    📈 **Visualize Trends:**  
    Select a location and view time-series graphs to track water level fluctuations over time.  

    📂 **Upload Your Own Data:**  
    Have custom measurements? Easily upload and analyze your own water level data.  

    Dive in and explore the dynamic tides of Ireland! 🌍🌊  
    """)

    # Data lokasi stasiun
    stations = pd.DataFrame({
        'Nama': ["Dublin Port", "Galway Port", "Sligo"],
        'lat': [53.3457, 53.269, 54.3099],
        'lon': [-6.2217, -9.048, -8.582]
    })
    
    st.map(stations)

def location_page(sheet_name):
    st.title(f"Water Level - {sheet_name}")
    df = load_data(sheet_name)
    
    # Pilihan range waktu
    df['time'] = pd.to_datetime(df['time'], errors='coerce')  
    min_date = df['time'].min().date()
    max_date = df['time'].max().date()
    date_range = st.slider("Choose Time!", min_value=min_date, max_value=max_date, value=(min_date, max_date))
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
    start_date = pd.to_datetime(start_date).tz_localize('UTC')
    end_date = pd.to_datetime(end_date).tz_localize('UTC')

    df_filtered = df[(df['time'] >= start_date) & (df['time'] <= end_date)]
    
    # Plot time series
    fig = px.line(
    df_filtered, 
    x='time', 
    y='water level', 
    title=f"Time Series {sheet_name}",
    labels={'time': 'Time', 'water level': 'Water Level (meters)'}  # Rename labels
    )
    st.plotly_chart(fig)
    
    # Menampilkan tabel data
    st.write("### Water Level Data")
    st.dataframe(df_filtered)

def upload_page():
    st.title("Upload Custom Water Level Data")
    uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df['time'] = pd.to_datetime(df['time'])
        
        # Plot time series
        fig = px.line(df, x='time', y='water level', title="Water Level")
        st.plotly_chart(fig)
        
        st.write("### Data Water Level")
        st.dataframe(df)

# Navigasi halaman
st.sidebar.title("Navigasi")
page = st.sidebar.selectbox("Pilih Halaman", ["Main", "Dublin Port", "Galway Port", "Sligo", 
                                              "Visualize Your Own!"])

if page == "Main":
    main_page()
elif page == "Dublin Port":
    location_page("Dublin Port")
elif page == "Galway Port":
    location_page("Galway Port")
elif page == "Sligo":
    location_page("Sligo")
elif page == "Visualize Your Own!":
    upload_page()

st.markdown("""
    <style>
        .stTitle {color: blue;}
    </style>
""", unsafe_allow_html=True)