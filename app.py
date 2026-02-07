import streamlit as st
from streamlit_folium import st_folium
import folium
import geocoder
import re

st.set_page_config(page_title="Stellar Peer Map", layout="wide")

#
def get_ips_from_file():
    try:
        with open("ipa.txt", "r") as f:
            data = f.read()
            return re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', data)
    except FileNotFoundError:
        return []

st.title("** Stellar Network Map **")

#
manual_ips = st.sidebar.text_area("Paste IP addresses here (one per line)")
if manual_ips:
    ips = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', manual_ips)
else:
    ips = get_ips_from_file()

if not ips:
    st.warning("No IP addresses found. Please upload or paste data.")
else:
    m = folium.Map(location=[20, 0], zoom_start=2)
    #
    for ip in ips[:50]:  # 
        g = geocoder.ip(ip)
        if g.latlng:
            folium.Marker(
                location=g.latlng,
                popup=f"IP: {ip}",
                icon=folium.Icon(color="blue", icon="server", prefix="fa")
            ).add_to(m)
    
    st_folium(m, width=1000, height=500)