import streamlit as st
import os
from pathlib import Path
import base64
import streamlit.components.v1 as components

# 
# 1. CẤU HÌNH & KHỞI TẠO
# 
st.set_page_config(page_title = "Movie Homepage", layout = "wide")

# Định nghĩa đường dẫn
BASE_DIR = Path(os.getcwd()) # Lấy đường dẫn thư mục hiện tại
POSTER_DIR = BASE_DIR / "images"  # Thư mục chứa ảnh

# Hàm hỗ trợ đọc ảnh
@st.cache_data
def get_base64_image(image_path):
    """Đọc file ảnh và chuyển đổi sang chuỗi base64."""
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# 
# 2. CSS CHUNG
# 
# Load Background
bg_path = POSTER_DIR / "BG.jpg"
bg_base64 = get_base64_image(bg_path)
bg_image_rule = ""
if bg_base64:
    bg_image_rule = f"""
    .stApp, [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{bg_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    """

st.markdown(f"""
<style>
    /* --- IMPORT FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Baskervville:ital,wght@0,400..700;1,400..700&family=Courier+Prime:ital,wght@0,400;0,700;1,400;1,700&display=swap');

    /* --- VARIABLES --- */
    :root{{ --bg:#FCFAF5; --ink:#1A1A1A; --lime:#D8FF84; --pink:#FFD6E0; --blue:#D6EFFF; }}

    /* --- BACKGROUND IMAGE --- */
    .stApp, [data-testid="stAppViewContainer"] {{
        background-color: var(--bg) !important;
        {bg_image_rule}
    }}
    /* --- CONTAINER SETTINGS --- */
    .block-container{{ max-width:1400px; padding-top:60px; }}
    [data-testid="stToolbar"] {{ right: 2rem; }} /* Ẩn bớt toolbar */

    /* --- TYPOGRAPHY CLASSES --- */
    .headings-font {{
        font-family: 'Baskervville', serif;
        font-weight: 500; font-size: 40px; color: var(--ink); text-align: center;
    }}
    .subhead-font {{
        font-family: 'Courier Prime', monospace;
        font-weight: 600; font-size: 27px; color: var(--ink); text-align: center;
    }}

    /* --- STREAMLIT BUTTON STYLING (NAV BUTTONS) --- */
    div[data-testid="stVerticalBlock"] button {{
        height: 65px; 
        border: 3px solid var(--ink); 
        border-radius: 20px; 
        background: var(--lime);
        box-shadow: 5px 5px 10px 1px var(--pink); 
        transition: transform .15s ease; 
        width: 100%;
    }}
    div[data-testid="stVerticalBlock"] button > div > p {{
        color: var(--ink); 
        font-family: 'Courier Prime', monospace; 
        font-weight: 500; 
        font-size: 20px;
    }}
    div[data-testid="stVerticalBlock"] button:hover {{ 
        background: var(--lime); 
        box-shadow: 5px 5px 10px 1px var(--pink); 
        transform: scale(1.02); 
        border: 3px solid var(--ink);
        color: var(--ink);
    }}
</style>
""", unsafe_allow_html=True)
    
# 
# 3. HEADER SECTION (LOGO & TEXT)
# 
# Logo
try:
    logo_path = POSTER_DIR / "LOGO.png"
    logo_base64 = get_base64_image(logo_path)
    if logo_base64:
        st.markdown(f"""
            <div style="text-align: center; margin-top: 0px; margin-bottom: -60px;">
                <img src="data:image/jpg;base64,{logo_base64}" width="500"/>
            </div>
        """, unsafe_allow_html=True)
except Exception:
    st.error("Lỗi hiển thị Logo")

# Headings
st.markdown("""
<div class="headings-font" style="margin-top: 50px; margin-bottom: 10px; text-align: center; font-size: 50px; font-weight: 600;">
    When <span style='color: #FFACC0;'>Bag of Words</span> meets <span style='color: #AADEFF;'>Bags of Popcorn</span>
</div>
<div class="subhead-font">This is a web for you to analyze your reviews or find your favorite movies!</div>
""", unsafe_allow_html=True)

# 
# 4. DECORATION 1
# 
st1_path = POSTER_DIR / "sticker 3.png"
st2_path = POSTER_DIR / "sticker 5.png"
st3_path = POSTER_DIR / "sticker 17.png"
st4_path = POSTER_DIR / "sticker 10.png"

# Load ảnh
imgs_top = [get_base64_image(p) for p in [st1_path, st2_path, st3_path, st4_path]]

if all(imgs_top):
    st.markdown(f"""
<div style="display: flex; justify-content: center; align-items: flex-end; margin-top: 20px; margin-bottom: -30px; position: relative; z-index: 100; pointer-events: none; gap: 150px;">
    <div style="transform: translateY(30px);">
        <img src="data:image/png;base64,{imgs_top[1]}" style="width: 8vw; height: auto; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));" />
    </div>
    <div style="transform: translateY(-30px) rotate(5deg);">
        <img src="data:image/png;base64,{imgs_top[0]}" style="width: 15vw; height: auto; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));" />
    </div>
    <div style="transform: rotate(-15deg);">
        <img src="data:image/png;base64,{imgs_top[2]}" style="width: 8vw; height: auto; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));" />
    </div>
    <div>
        <img src="data:image/png;base64,{imgs_top[3]}" style="width: 8vw; height: auto; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));" />
    </div>
</div>
""", unsafe_allow_html=True)

# 
# 5. POSTER STACK
# 
poster_files = [f"POSTER {i}.jpg" for i in range(1, 6)]
b64s = [get_base64_image(POSTER_DIR / p) for p in poster_files]

# Chỉ hiển thị nếu load đủ 5 poster
if all(b64s):
    html_poster_stack = f"""
    <div class="poster-stack">
      <div class="card card-1"><img src="data:image/jpeg;base64,{b64s[0]}" /></div>
      <div class="card card-2"><img src="data:image/jpeg;base64,{b64s[1]}" /></div>
      <div class="card card-3"><img src="data:image/jpeg;base64,{b64s[2]}" /></div>
      <div class="card card-4"><img src="data:image/jpeg;base64,{b64s[3]}" /></div>
      <div class="card card-5"><img src="data:image/jpeg;base64,{b64s[4]}" /></div>

      <div class="badge badge-1">96% Positive 😊</div>
      <div class="badge badge-3">Mind-twisted 🤩</div>
      <div class="badge badge-5">AMAZING 😱!!!!</div>
    </div>

    <style>
     .poster-stack {{
        position: relative;
        width: 100%;
        max-width: 1400px;
        height: clamp(400px, 55vw, 650px);
        margin: clamp(40px, 5vw, 80px) auto 0 auto;
        overflow: visible;
    }}
    .poster-stack .card {{
        position: absolute;
        top: 5%;
        width: clamp(130px, 22vw, 310px);
        aspect-ratio: 2/3;
        border-radius: 16px;
        overflow: hidden;
        border: 3px solid #1A1A1A;
        box-shadow: 0 18px 30px rgba(0,0,0,0.25);
        transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s ease;
    }}
    .poster-stack .card img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .poster-stack .card-1:hover {{ 
    transform: translateX(0) scale(1.3) rotate(var(--rot)); 
    z-index: 50; 
    box-shadow: 0 25px 50px rgba(0,0,0,0.4);
    }}
    .poster-stack .card-2:hover {{ 
    transform: translateX(-15%) scale(1.3) rotate(var(--rot)); 
    z-index: 50; 
    box-shadow: 0 25px 50px rgba(0,0,0,0.4);
    }}
    .poster-stack .card-3:hover {{ 
    transform: translateX(-50%) scale(1.3) rotate(var(--rot)); 
    z-index: 50; 
    box-shadow: 0 25px 50px rgba(0,0,0,0.4);
    }}
    .poster-stack .card-4:hover {{ 
    transform: translateX(-85%) scale(1.3) rotate(var(--rot)); 
    z-index: 50; 
    box-shadow: 0 25px 50px rgba(0,0,0,0.4);
    }}
    .poster-stack .card-5:hover {{ 
    transform: translateX(0) scale(1.3) rotate(var(--rot)); 
    z-index: 50; 
    box-shadow: 0 25px 50px rgba(0,0,0,0.4);
    }}
    /* Positions */
    .poster-stack .card-1 {{ left: 5%;  transform: translateX(0)     rotate(-12deg); --rot:-12deg; z-index:5; }}
    .poster-stack .card-2 {{ left: 25%; transform: translateX(-15%)  rotate(-6deg);  --rot:-6deg;  z-index:7; }}
    .poster-stack .card-3 {{ left: 50%; transform: translateX(-50%)  rotate(0deg);   --rot:0deg;   z-index:9; }}
    .poster-stack .card-4 {{ left: 75%; transform: translateX(-85%)  rotate(6deg);   --rot:6deg;   z-index:7; }}
    .poster-stack .card-5 {{ right: 5%; transform: translateX(0)     rotate(12deg);  --rot:12deg;  z-index:5; }}

    /* Badges */
    .poster-stack .badge {{
        position: absolute;
        padding: clamp(10px, 1.5vw, 18px) clamp(16px, 2vw, 30px);
        border-radius: 16px;
        border: 3px solid #1A1A1A;
        font-family: 'Courier Prime', monospace;
        font-weight: 700; color: #1A1A1A; z-index: 60;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        font-size: clamp(14px, 1.5vw, 24px); white-space: nowrap;
    }}
    .poster-stack .badge-1 {{ left: 8%; bottom: 25%; background: #D6EFFF; transform: translateY(-50%) rotate(-3deg); }}
    .poster-stack .badge-3 {{ left: 50%; bottom: 88%; background: #FFD6E0; transform: translateX(-50%) translateY(-30%) rotate(-2deg); }}
    .poster-stack .badge-5 {{ right: 8%; bottom: 25%; background: #D6EFFF; transform: translateY(-50%) rotate(0deg); }}

    @media (max-width: 600px) {{
        .poster-stack {{ height: 380px; }}
        .poster-stack .card-1 {{ left: 0%; }}
        .poster-stack .card-2 {{ left: 20%; }}
        .poster-stack .card-3 {{ left: 50%; }}
        .poster-stack .card-4 {{ left: 80%; }}
        .poster-stack .card-5 {{ right: 0%; }}
    }}
    </style>
    """
    components.html(html_poster_stack, height=650, scrolling=False)
else:
    st.warning("Chưa load đủ ảnh poster. Vui lòng kiểm tra thư mục images.")

# 
# 6. DECORATION 2
# 
st5_path = POSTER_DIR / "sticker 11.png" # Cinema
st6_path = POSTER_DIR / "sticker 19.png" # Planet
st7_path = POSTER_DIR / "sticker 20.png" # Clapper

imgs_bot = [get_base64_image(p) for p in [st5_path, st6_path, st7_path]]

if all(imgs_bot):
    st.markdown(f"""
<div style="display: flex; justify-content: center; align-items: flex-end; position: relative; z-index: 100; pointer-events: none; gap: 100px; margin-top: -100px; margin-bottom: 60px;">
    <div style="transform: translateY(-50px);">
        <img src="data:image/png;base64,{imgs_bot[1]}" style="width: 12vw; height: auto; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));" />
    </div>
    <div style="transform: translateY(20px);">
        <img src="data:image/png;base64,{imgs_bot[0]}" style="width: 25vw; height: auto; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));" />
    </div>
    <div style="transform: rotate(15deg);">
        <img src="data:image/png;base64,{imgs_bot[2]}" style="width: 12vw; height: auto; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));" />
    </div>
</div>
""", unsafe_allow_html=True)

# 
# 7. NAVIGATION BUTTONS (FOOTER)
# 
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Your Next Favourite Movies", use_container_width=True):
        st.switch_page("pages/recommendations.py")            

with col2:
    if st.button("Analyze Your Reviews", use_container_width=True):
        st.switch_page("pages/review.py")
