import streamlit as st
from streamlit_folium import st_folium
import folium
import geoip2.database
import re
import os

# --- Page Configuration ---
st.set_page_config(page_title="Stellar Network Map", layout="wide")
st.title("🌐 Stellar Node Visualizer (Offline Mode)")
st.markdown("""
This app visualizes Stellar nodes on a map.  
**No Python environment needed!** Just upload your `ipa.txt`.
""")

# --- Constants ---
DB_PATH = 'GeoLite2-City.mmdb'

# --- Functions ---
@st.cache_resource
def load_geoip_reader():
    """Load the GeoLite2 database once and cache it."""
    if os.path.exists(DB_PATH):
        return geoip2.database.Reader(DB_PATH)
    return None

def extract_ips(text):
    """Extract IPv4 addresses using regex."""
    return re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', text)

# --- Sidebar: Upload ---
with st.sidebar:
    st.header("1. Upload Data")
    uploaded_file = st.file_uploader("Upload your ipa.txt", type="txt")
    
    st.divider()
    st.header("2. Map Settings")
    marker_color = st.selectbox("Marker Color", ["blue", "red", "purple", "green", "orange"])

# --- Main Logic ---
reader = load_geoip_reader()

if not reader:
    st.error(f"Database file `{DB_PATH}` not found. Please add it to the repository.")
elif uploaded_file is not None:
    # Process file
    content = uploaded_file.read().decode("utf-8")
    ips = extract_ips(content)
    
    if ips:
        st.success(f"Found {len(ips)} nodes. Processing...")
        
        # Initialize Map
        m = folium.Map(location=[20, 0], zoom_start=2)
        
        count = 0
        for ip in ips:
            try:
                response = reader.city(ip)
                lat = response.location.latitude
                lng = response.location.longitude
                
                if lat and lng:
                    city = response.city.name or "Unknown City"
                    country = response.country.name or "Unknown Country"
                    
                    folium.Marker(
                        location=[lat, lng],
                        popup=f"IP: {ip}<br>Location: {city}, {country}",
                        tooltip=ip,
                        icon=folium.Icon(color=marker_color, icon="server", prefix="fa")
                    ).add_to(m)
                    count += 1
            except:
                # Skip IPs not found in database
                continue
        
        # Show Results
        st.metric("Successfully Mapped", f"{count} nodes")
        st_folium(m, width="100%", height=600)
    else:
        st.warning("No valid IP addresses found in the uploaded file.")
else:
    st.info("👈 Please upload an `ipa.txt` file from the sidebar to begin.")

# --- Footer ---
st.caption("Data source: MaxMind GeoLite2. This product includes GeoLite2 data created by MaxMind.")