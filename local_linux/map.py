import folium
import geocoder
import re
import os

# 1. Prepare the list of IP addresses
# If you have a file saved from the command:
# docker exec mainnet stellar-core http-command peers | grep address > ips.txt
raw_data = [
    '"address": "1.2.3.4:11625"',  # Example format from Stellar-core
    '"address": "5.6.7.8:11625"'
]
raw_data = [
    '"address": "1.2.3.4"',  # Example format from Stellar-core
    '"address": "5.6.7.8"'
]
os.system("docker exec mainnet stellar-core http-command peers | grep address >> ipa.txt")


peers_ips = []
with open("ipa.txt", "r") as f:
    for line in f:
        match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
        if match:
            peers_ips.append(match.group(1))

raw_data = []
for ip in peers_ips:
  raw_data.append('"address": "' + ip + '",')



# Extract only IP addresses using Regex (removing port numbers)
peers_ips = []
for entry in raw_data:
    match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', entry)
    if match:
        peers_ips.append(match.group(1))

# 2. Initialize the World Map
m = folium.Map(location=[20, 0], zoom_start=2)

print("Fetching coordinates for IP addresses...")

# 3. Geocode and Mark each IP
for ip in peers_ips:
    # Get geolocation data based on IP
    g = geocoder.ip(ip)
    
    if g.latlng:
        # Add a marker to the map
        folium.Marker(
            location=g.latlng,
            popup=f"IP: {ip}<br>Location: {g.city}, {g.country}",
            tooltip=f"Peer: {ip}",
            icon=folium.Icon(color="blue", icon="server", prefix="fa")
        ).add_to(m)
        print(f"Success: {ip} found in {g.city}")
    else:
        print(f"Warning: Could not resolve location for {ip}")

# 4. Export to HTML
m.save("stellar_peers_map.html")
print("Process complete! Open 'stellar_peers_map.html' in your browser.")
