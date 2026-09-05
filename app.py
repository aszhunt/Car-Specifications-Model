import streamlit as st
import requests
from bs4 import BeautifulSoup

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="🚗 Vehicle Info AI",
    page_icon="🚘",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.main-title {
    font-size: 40px;
    font-weight: bold;
    text-align: center;
    color: #00FFD1;
}
.card {
    background: #1e1e2f;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 0px 15px rgba(0,255,200,0.3);
}
.spec {
    color: #fff;
    font-size: 16px;
}
.price {
    color: #00FF7F;
    font-size: 24px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="main-title">🚘 Vehicle Info AI App</div>', unsafe_allow_html=True)

st.write("🔍 Enter any car, bike, or vehicle name to get specs, price & image")

# ---------- INPUT ----------
vehicle_name = st.text_input("Enter Vehicle Name (e.g. Honda Civic 2024)")

# ---------- FUNCTIONS ----------
def get_vehicle_image(query):
    try:
        url = f"https://source.unsplash.com/800x400/?{query}"
        return url
    except:
        return None

def get_wikipedia_data(query):
    try:
        url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        info = {}

        table = soup.find("table", {"class": "infobox"})
        if table:
            rows = table.find_all("tr")
            for row in rows:
                header = row.find("th")
                value = row.find("td")
                if header and value:
                    info[header.text.strip()] = value.text.strip()

        return info
    except:
        return {}

def estimate_price(vehicle):
    # fallback estimation logic
    if "civic" in vehicle.lower():
        return "$25,000 - $35,000"
    elif "corolla" in vehicle.lower():
        return "$20,000 - $30,000"
    elif "bike" in vehicle.lower():
        return "$500 - $3000"
    else:
        return "Price not available (Estimated)"

# ---------- SEARCH ----------
if st.button("Search 🔎"):
    if vehicle_name.strip() == "":
        st.warning("Please enter a vehicle name")
    else:
        with st.spinner("Fetching data..."):
            image = get_vehicle_image(vehicle_name)
            specs = get_wikipedia_data(vehicle_name)
            price = estimate_price(vehicle_name)

        # ---------- DISPLAY ----------
        col1, col2 = st.columns([1,1])

        with col1:
            st.image(image, use_container_width=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown(f'<div class="price">💰 {price}</div>', unsafe_allow_html=True)

            st.markdown("### ⚙️ Specifications")

            if specs:
                for key, value in list(specs.items())[:10]:
                    st.markdown(f'<div class="spec">✔ {key}: {value}</div>', unsafe_allow_html=True)
            else:
                st.write("No detailed specs found")

            st.markdown('</div>', unsafe_allow_html=True)

        st.success("✅ Data Loaded Successfully")
