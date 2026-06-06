# app.py — Netflix-Style Dark Glassmorphism UI

from pathlib import Path
import PIL
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import settings
import helper

# -----------------------------------------------------------
# PAGE SETTINGS
# -----------------------------------------------------------
st.set_page_config(
    page_title="WASM.ai",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------
# NETFLIX-STYLE DARK THEME
# -----------------------------------------------------------
NETFLIX_UI = """
<style>

@import url('https://fonts.googleapis.com/css2?family=Netflix+Sans:wght@300;400;500;700&family=Bebas+Neue&display=swap');

:root {
  --netflix-red: #e50914;
  --netflix-black: #141414;
  --netflix-gray: #2f2f2f;
  --netflix-light: #e5e5e5;
  --text-white: #ffffff;
  --text-gray: #b3b3b3;
  --radius: 8px;
}

/* Force font */
* {
    font-family: 'Netflix Sans', 'Helvetica Neue', Arial, sans-serif !important;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main container - Netflix dark background */
.stApp {
    background: var(--netflix-black) !important;
}

section.main > div {
    background: var(--netflix-black) !important;
    padding: 20px !important;
}

/* Remove default padding issues */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    max-width: 100% !important;
}

/* Remove extra blank spaces */
[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
    gap: 0rem !important;
}

/* Sidebar - Netflix style */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a1a 0%, #0a0a0a 100%) !important;
    border-right: 1px solid #2f2f2f !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}

/* Sidebar text */
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: var(--text-white) !important;
}

[data-testid="stSidebar"] .stMarkdown {
    color: var(--text-white) !important;
}

/* Headers - Netflix style */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-white) !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
}

/* Paragraphs and text */
p, span, div, label {
    color: var(--text-gray) !important;
}

/* RADIO BUTTONS - Netflix button style */
div[data-testid="stRadio"] > div {
    background: transparent !important;
    gap: 8px !important;
    display: flex !important;
    flex-direction: column !important;
}

/* Hide radio circles */
div[data-testid="stRadio"] > div > label > div:first-child {
    display: none !important;
}

/* Radio labels as Netflix buttons */
div[data-testid="stRadio"] > div > label {
    background: var(--netflix-gray) !important;
    border: 2px solid transparent !important;
    padding: 14px 24px !important;
    border-radius: var(--radius) !important;
    margin: 0 !important;
    cursor: pointer !important;
    color: var(--text-white) !important;
    transition: all 0.3s ease !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4) !important;
}

div[data-testid="stRadio"] > div > label:hover {
    background: #3a3a3a !important;
    border: 2px solid rgba(229, 9, 20, 0.5) !important;
    transform: scale(1.02) !important;
}

/* Selected radio */
div[data-testid="stRadio"] > div > label:has(input[type="radio"]:checked) {
    background: var(--netflix-red) !important;
    border: 2px solid var(--netflix-red) !important;
    color: white !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 16px rgba(229, 9, 20, 0.6) !important;
}

div[data-testid="stRadio"] > div > label > div:last-child {
    color: inherit !important;
    font-weight: inherit !important;
}

/* Regular Buttons - Netflix CTA style */
.stButton > button {
    background: var(--netflix-red) !important;
    color: white !important;
    border: none !important;
    padding: 12px 28px !important;
    border-radius: var(--radius) !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 12px rgba(229, 9, 20, 0.4) !important;
    width: 100% !important;
    letter-spacing: 0.5px !important;
}

.stButton > button:hover {
    background: #f40612 !important;
    transform: scale(1.05) !important;
    box-shadow: 0 6px 20px rgba(229, 9, 20, 0.6) !important;
}

/* Select boxes */
div[data-baseweb="select"] > div {
    background: var(--netflix-gray) !important;
    border: 1px solid #444 !important;
    border-radius: var(--radius) !important;
    color: var(--text-white) !important;
}

div[data-baseweb="select"] span {
    color: var(--text-white) !important;
}

/* Dropdown menus */
ul[role="listbox"] {
    background: var(--netflix-gray) !important;
    border: 1px solid #444 !important;
}

ul[role="listbox"] li {
    color: var(--text-white) !important;
    background: var(--netflix-gray) !important;
}

ul[role="listbox"] li:hover {
    background: #3a3a3a !important;
}

/* Text inputs */
input, textarea {
    background: var(--netflix-gray) !important;
    border: 1px solid #444 !important;
    border-radius: var(--radius) !important;
    color: var(--text-white) !important;
    padding: 12px !important;
}

input::placeholder, textarea::placeholder {
    color: #666 !important;
}

input:focus, textarea:focus {
    border: 1px solid var(--netflix-red) !important;
    box-shadow: 0 0 0 2px rgba(229, 9, 20, 0.2) !important;
}

/* Number input */
input[type="number"] {
    background: var(--netflix-gray) !important;
    color: var(--text-white) !important;
}

/* Sliders */
div[data-baseweb="slider"] > div > div {
    background: #444 !important;
}

div[data-baseweb="slider"] div[role="slider"] {
    background: var(--netflix-red) !important;
    box-shadow: 0 2px 8px rgba(229, 9, 20, 0.4) !important;
}

/* Color picker */
input[type="color"] {
    border-radius: var(--radius) !important;
    border: 2px solid #444 !important;
    cursor: pointer !important;
}

/* File uploader */
section[data-testid="stFileUploadDropzone"] {
    background: var(--netflix-gray) !important;
    border: 2px dashed #666 !important;
    border-radius: var(--radius) !important;
}

section[data-testid="stFileUploadDropzone"]:hover {
    border: 2px dashed var(--netflix-red) !important;
}

section[data-testid="stFileUploadDropzone"] span,
section[data-testid="stFileUploadDropzone"] p {
    color: var(--text-white) !important;
}

/* Images */
img {
    border-radius: var(--radius) !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.6) !important;
}

/* Success/Info/Warning - Netflix style */
.stSuccess {
    background: rgba(0, 128, 0, 0.2) !important;
    border-left: 4px solid #00ff00 !important;
    color: #00ff00 !important;
}

.stWarning {
    background: rgba(255, 165, 0, 0.2) !important;
    border-left: 4px solid #ffa500 !important;
    color: #ffa500 !important;
}

.stError {
    background: rgba(229, 9, 20, 0.2) !important;
    border-left: 4px solid var(--netflix-red) !important;
    color: var(--netflix-red) !important;
}

.stInfo {
    background: rgba(58, 122, 254, 0.2) !important;
    border-left: 4px solid #3a7afe !important;
    color: #3a7afe !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: var(--netflix-red) !important;
}

/* Remove extra gaps */
.element-container {
    margin-bottom: 0 !important;
}

/* Column spacing */
div[data-testid="column"] {
    padding: 8px !important;
}

</style>
"""

st.markdown(NETFLIX_UI, unsafe_allow_html=True)

# -----------------------------------------------------------
# NETFLIX-STYLE HEADER
# -----------------------------------------------------------
st.markdown("""
<div style="
    background: linear-gradient(90deg, rgba(229,9,20,1) 0%, rgba(20,20,20,0.95) 100%);
    padding: 40px 30px;
    border-radius: 8px;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.8);
">
    <h1 style="
        font-size: 48px;
        color: white;
        font-weight: 700;
        margin: 0 0 12px 0;
        letter-spacing: -1px;
    ">🌍 WASM.ai</h1>
    <p style="
        font-size: 18px;
        color: #e5e5e5;
        margin: 0;
        font-weight: 300;
    ">Eco-friendly AI • Waste Recognition • 3D Models • Sketch Studio</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------
st.sidebar.markdown("### 🎬 Navigation")
main_mode = st.sidebar.radio(
    "choose_mode",
    ["💰 Sell Waste", "🛒 Buy Items", "✨ Create New"],
    label_visibility="collapsed"
)

# -----------------------------------------------------------
# HELPER: Netflix Card Wrapper - Using container instead
# -----------------------------------------------------------
# Removed HTML helper to avoid raw HTML display issues

# -----------------------------------------------------------
# SELL WASTE
# -----------------------------------------------------------
if main_mode == "💰 Sell Waste":
    st.markdown("## 💰 Sell Your Waste")
    st.write("Connect with nearby verified recycling vendors and turn your waste into cash.")
    st.markdown("---")

    c1, c2 = st.columns([2, 1], gap="medium")

    with c1:
        st.markdown("### Waste Details")
        waste_type = st.selectbox("Waste Type", ["Metal", "Paper", "Plastic", "Glass"])
        qty = st.number_input("Quantity (kg)", 1, 10000, 10)
        location = st.text_input("Pickup Location", "Bengaluru")

    with c2:
        st.markdown("### Vendor Options")
        vendors = {
            "Metal": ["IronHub", "MetalMart", "SteelCycle"],
            "Paper": ["PaperWave", "EcoSheets", "PulpRecycle"],
            "Plastic": ["PlasticPro", "RePlasto", "PolyReborn"],
            "Glass": ["Glassify", "EcoGlass", "ClearCycle"]
        }
        prices = {"Metal": 50, "Paper": 10, "Plastic": 20, "Glass": 5}

        st.write(f"**Price:** ₹{prices[waste_type]}/kg")
        st.write(f"**Estimated Earnings:** ₹{prices[waste_type] * qty}")
        vendor = st.selectbox("Choose Vendor", vendors[waste_type])

        if st.button("🔗 Connect Vendor"):
            st.success(f"✅ {vendor} will contact you within 24 hours!")

# -----------------------------------------------------------
# BUY ITEMS
# -----------------------------------------------------------
elif main_mode == "🛒 Buy Items":
    st.markdown("## 🛒 Buy Eco-Friendly Items")
    st.write("Shop sustainable products made from recycled materials.")
    st.markdown("---")

    items = {
        "Eco Notebook": {"price": 150, "material": "Recycled Paper", "emoji": "📓"},
        "Plastic Organizer": {"price": 299, "material": "Recycled Plastic", "emoji": "🗂️"},
        "Glass Water Bottle": {"price": 499, "material": "Recycled Glass", "emoji": "🍶"},
        "Metal Stand": {"price": 199, "material": "Recycled Metal", "emoji": "🔧"},
        "Bamboo Pen Set": {"price": 249, "material": "Sustainable Bamboo", "emoji": "✒️"},
        "Jute Bag": {"price": 349, "material": "Natural Jute", "emoji": "👜"},
    }

    cols = st.columns(3, gap="medium")
    for idx, (name, info) in enumerate(items.items()):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style="
                background: linear-gradient(145deg, #2f2f2f 0%, #1a1a1a 100%);
                padding: 26px;
                border-radius: 8px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.6);
                border: 1px solid #3a3a3a;
                text-align: center;
                margin-bottom: 20px;
                transition: transform 0.3s ease;
            " onmouseover="this.style.transform='translateY(-8px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="font-size: 56px; margin-bottom: 16px;">{info['emoji']}</div>
                <h4 style="color: white; margin: 8px 0; font-size: 20px;">{name}</h4>
                <p style="color: #b3b3b3; font-size: 14px; margin: 8px 0;">{info['material']}</p>
                <p style="color: #e50914; font-size: 28px; font-weight: 700; margin: 16px 0;">₹{info['price']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("🛒 Add to Cart", key=name)

# -----------------------------------------------------------
# CREATE NEW
# -----------------------------------------------------------
elif main_mode == "✨ Create New":
    st.markdown("## ✨ Create with WASM Tools")
    st.write("Leverage AI-powered tools for waste detection, 3D modeling, and creative sketching.")
    st.markdown("---")

    st.sidebar.markdown("### 🛠 Creative Tools")
    create_mode = st.sidebar.radio(
        "choose_tool",
        ["📸 Waste Detection", "🎨 3D Model Generator", "🖌 Painting & Sketching"],
        label_visibility="collapsed"
    )

    # ----------------------
    # WASTE DETECTION
    # ----------------------
    if create_mode == "📸 Waste Detection":
        st.markdown("### 📸 Waste Detection (YOLOv8)")
        st.write("Upload an image or use your webcam to detect and classify waste materials using AI.")

        confidence = st.sidebar.slider("Detection Confidence", 25, 100, 40) / 100
        model = helper.load_model(Path(settings.DETECTION_MODEL))

        source = st.sidebar.radio("source_choice", ["Image", "Webcam"], label_visibility="collapsed")

        if source == "Image":
            img_file = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"])
            if img_file:
                st.image(img_file)


                if st.button("🔍 Detect Waste"):
                    with st.spinner("Analyzing image..."):
                        img = PIL.Image.open(img_file)
                        res = model.predict(img, conf=confidence)
                        st.image(res[0].plot()[:, :, ::-1])


                        st.success("✅ Detection complete!")
        else:
            helper.play_webcam(confidence, model)

    # ----------------------
    # 3D MODEL GENERATOR
    # ----------------------
    elif create_mode == "🎨 3D Model Generator":
        st.markdown("### 🎨 3D Model Generator")
        st.write("Generate 3D models from waste materials for visualization and design purposes.")

        mat = st.selectbox(
            "Material Type",
            ["Plastic", "Metal", "Glass", "Paper", "Cardboard", "Biodegradable", 
             "Car", "Bridge", "Ship", "Minion"]
        )
        desc = st.text_area("Description (Optional)", placeholder="Describe your 3D model...")

        if st.button("🎯 Generate 3D Model"):
            with st.spinner("Generating 3D model..."):
                helper.generate_3d_model(mat, desc)
                st.success("✅ 3D model generated successfully!")

    # ----------------------
    # PAINTING & SKETCHING
    # ----------------------
    elif create_mode == "🖌 Painting & Sketching":
        st.markdown("### 🖌 Painting & Sketching Panel")
        st.write("Create sketches and drawings for waste management concepts and designs.")

        stroke = st.sidebar.slider("Brush Size", 1, 50, 5)
        color = st.sidebar.color_picker("Brush Color", "#FFFFFF")
        bg = st.sidebar.color_picker("Background Color", "#1a1a1a")
        mode = st.sidebar.radio(
            "drawing_mode",
            ["freedraw", "line", "rect", "circle", "transform"],
            format_func=lambda x: {
                "freedraw": "✏️ Free Draw",
                "line": "📏 Line",
                "rect": "⬜ Rectangle",
                "circle": "⭕ Circle",
                "transform": "🔄 Transform"
            }[x],
            label_visibility="collapsed"
        )

        canvas = st_canvas(
            fill_color="rgba(255,255,255,0)",
            stroke_width=stroke,
            stroke_color=color,
            background_color=bg,
            height=500,
            width=900,
            drawing_mode=mode,
            key="canvas_art",
        )

        if st.button("💾 Save Drawing"):
            if canvas.image_data is not None:
                st.image(canvas.image_data, use_container_width=True)
                st.success("✅ Drawing saved!")
            else:
                st.warning("⚠️ Please draw something first!")