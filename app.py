import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="🚗 Vehicle Info AI (PK)",
    page_icon="🚘",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
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
st.markdown('<div class="main-title">🚘 Vehicle Info AI App (Pakistan Edition)</div>', unsafe_allow_html=True)
st.write("🔍 Enter any car, bike, or vehicle name to get specs, price in PKR & image")

# ---------- INPUT ----------
vehicle_name = st.text_input("Enter Vehicle Name (e.g. Toyota Corolla 2026)")

# ---------- FUNCTIONS ----------
def get_vehicle_image(query):
    """Fetches a free stock vehicle image via Wikimedia Commons."""
    try:
        search_url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrlimit=1&prop=imageinfo&iiprop=url&format=json"
        headers = {"User-Agent": "VehicleInfoAIApp/1.0 (contact@example.com)"}
        response = requests.get(search_url, headers=headers, timeout=5)
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_info in pages.items():
            imageinfo = page_info.get("imageinfo", [])
            if imageinfo:
                return imageinfo[0].get("url")
    except Exception:
        pass
    
    # Fallback image URL
    return "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=800&q=80"

def get_wikipedia_data(query):
    try:
        # Search Wikipedia for the closest article match
        search_api = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json"
        headers = {"User-Agent": "VehicleInfoAIApp/1.0 (contact@example.com)"}
        res = requests.get(search_api, headers=headers, timeout=5)
        search_data = res.json()
        
        search_results = search_data.get("query", {}).get("search", [])
        if not search_results:
            return {}
            
        page_title = search_results[0]["title"]
        
        # Fetch Wikipedia page content
        url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(page_title.replace(' ', '_'))}"
        page_res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(page_res.text, "html.parser")

        info = {}
        # Look for infobox tables or general tables
        table = soup.find("table", {"class": ["infobox", "vevent"]})
        if not table:
            table = soup.find("table", {"class": "infobox"})
            
        if table:
            rows = table.find_all("tr")
            for row in rows:
                header = row.find("th")
                value = row.find("td")
                if header and value:
                    key_text = header.text.strip().replace("\n", " ")
                    val_text = value.text.strip().replace("\n", " ")
                    if key_text and val_text:
                        info[key_text] = val_text

        return info
    except Exception:
        return {}

def estimate_price_pkr(vehicle):
    v = vehicle.lower()
    # Approximate PKR estimates based on market trends
    if "corolla" in v:
        return "PKR 7,500,000 - 9,500,000 (Estimated)"
    elif "civic" in v:
        return "PKR 8,500,000 - 11,000,000 (Estimated)"
    elif "alto" in v or "cultus" in v:
        return "PKR 2,500,000 - 4,500,000 (Estimated)"
    elif "swift" in v:
        return "PKR 4,300,000 - 5,500,000 (Estimated)"
    elif "tesla" in v:
        return "PKR 25,000,000+ (Import Estimated)"
    elif "bike" in v or "motorcycle" in v or "cg 125" in v:
        return "PKR 180,000 - 350,000 (Estimated)"
    else:
        return "PKR 5,000,000 - 10,000,000 (General Estimate)"

# ---------- SEARCH ----------
if st.button("Search 🔎"):
    if vehicle_name.strip() == "":
        st.warning("Please enter a vehicle name")
    else:
        with st.spinner("Fetching vehicle data, specs, and price in PKR..."):
            image = get_vehicle_image(vehicle_name)
            specs = get_wikipedia_data(vehicle_name)
            price = estimate_price_pkr(vehicle_name)

        # ---------- DISPLAY ----------
        col1, col2 = st.columns([1, 1])

        with col1:
            if image:
                st.image(image, use_container_width=True, caption=vehicle_name)
            else:
                st.info("No image found.")

        with col2:
            st.markdown('<div class="card">', unsafe_allowed_html=True if "unsafe_allow_html" in dir(st) else True)
            st.markdown(f'<div class="price">💰 {price}</div>', unsafe_allow_html=True)
            st.markdown("### ⚙️ Specifications")

            if specs:
                for key, value in list(specs.items())[:12]:
                    st.markdown(f'<div class="spec">✔ **{key}**: {value}</div>', unsafe_allow_html=True)
            else:
                st.write("No detailed specs found on Wikipedia for this exact query. Try adding a broader or official model name.")

            st.markdown('</div>', unsafe_allow_html=True)

        st.success("✅ Data Loaded Successfully")
