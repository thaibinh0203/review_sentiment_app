import streamlit as st
import os
from pathlib import Path
import base64
import streamlit.components.v1 as components

# 1. CẤU HÌNH
st.set_page_config(page_title = "Movie Homepage", layout = "wide")

# 2. ĐỊNH NGHĨA ĐƯỜNG DẪN & HÀM HỖ TRỢ
BASE_DIR = Path(os.getcwd()) # Lấy đường dẫn thư mục hiện tại
POSTER_DIR = BASE_DIR / "images"  # Thư mục chứa ảnh

@st.cache_data
def get_base64_image(image_path):
    """Đọc file ảnh và chuyển đổi sang chuỗi base64."""
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# 3. BACKGROUND
bg_path = POSTER_DIR / "BG.jpg"
bg_base64 = get_base64_image(bg_path)

if bg_base64:
    st.markdown(f"""
    <style>
    .stApp, [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{bg_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    
    /* Ẩn toolbar mặc định (tùy chọn, giúp giao diện sạch hơn) */
    [data-testid="stToolbar"] {{
        right: 2rem;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.warning(f"Không tìm thấy ảnh nền tại: {bg_path}")

# 4. THÊM FONT TỪ GOOGLE
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Baskervville:ital,wght@0,400..700;1,400..700&family=Courier+Prime:ital,wght@0,400;0,700;1,400;1,700&display=swap');
</style>
""", unsafe_allow_html = True)

# 5. CSS
st.markdown("""
<style>

    /* 1. Headings */
    .headings-font {
        font-family: 'Baskervville', serif;
        font-weight: 500;
        font-size: 40px;
        color: #1A1A1A;
        text-align: center;
    }
    
    /* 2. Subhead */
    .subhead-font {
        font-family: 'Courier Prime', monospace;
        font-weight: 600;
        font-size: 27px;
        color: #1A1A1A;
        text-align: center;
    }
    .pink-highlight { color: #FFD6E0; }
    .blue-highlight { color: #D6EFFF; }

    /* 3. Body */
    .body-text {
        font-family: 'Courier Prime', monospace;
        font-weight: 700; /* Bold */
        font-size: 20px;
        color: #1A1A1A;
        text-align: center;
    }
    
    /* 4. Button */
    a.custom-button {
        background-color: #D8FF84;
        color: #1A1A1A;
        border: 3px solid #1A1A1A;
        border-radius: 16px;
        font-family: 'Courier Prime', monospace;
        font-weight: 400;
        font-size: 20px;
        padding: 16px 30px;
        box-shadow: 5px 5px 10px #FFD6E0;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        transition: transform 0.15s ease;
    }
    .custom-button:hover {
        transform: scale(1.05);
    }        
    
            
    /* 5. Callout/Cards */
    .callout {
        border-radius: 16px;
        padding: 8px 12px;
        text-align: center;
        display: inline-block;
        margin-top: 10px;
        border: 3px solid #1A1A1A;
        font-family: 'Courier Prime', monospace;
        font-weight: 700;
        font-size: 20px;
    }
            
    .callout-pink {
        background-color: #FFD6E0;
        color: #1A1A1A;
    }
            
    .callout-blue {
        background-color: #D6EFFF;
        color: #1A1A1A;
    }
    .stack-wrap { position:relative; width:1400px; height:500px; margin:-30px auto 0 auto; }
        .card { position:absolute; width:300px; height:440px; border-radius:20px; overflow:hidden;
                border:3px solid #1A1A1A; box-shadow:0 25px 30px rgba(0,0,0,0.3); transition:0.2s; }
        .card img{ width:100%; height:100%; object-fit:cover; display:block; }
        .card:hover{ transform:scale(1.06) translateY(-12px); z-index:20; }
        .c1{ left:0px; top:20px; transform:rotate(-14deg); }
        .c2{ left:230px; top:0px; transform:rotate(-6deg); }
        .c3{ left:460px; top:-15px; transform:rotate(0deg); }
        .c4{ left:690px; top:0px; transform:rotate(6deg); }
        .c5{ left:920px; top:20px; transform:rotate(14deg); }
        .stack-callout{ width:1400px; margin:25px auto; text-align:center;}
        .badge{ display:inline-block; margin:0 20px; border:3px solid #1A1A1A;
                padding:10px 20px; border-radius:16px;
                font-family:'Courier Prime', monospace; font-weight:700; }
</style>
            
""", unsafe_allow_html = True)

# 6. WEB LAYOUT

# Navigation Bar
# Hiển thị logo nếu tồn tại
try:
    logo_path = POSTER_DIR / "LOGO.png"
    logo_base64 = get_base64_image(logo_path)
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: -50px; margin-bottom: -60px;">
            <img src="data:image/jpg;base64,{logo_base64}" width="500"/>
        </div>
        """,
        unsafe_allow_html=True
    )
except FileNotFoundError:
    st.error("Lỗi: Không tìm thấy LOGO.PNG")

# Header and subheader
st.markdown("""
<div class="headings-font" style="margin-top: 50px; text-align: center; font-size: 50px; font-weight: 600;">
    When <span style='color: #FFACC0;'>Bag of Words</span> meets <span style='color: #AADEFF;'>Bags of Popcorn</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""<div class = "subhead-font">This is a web for you to analyze your reviews or find your favorite movies!</div>""", unsafe_allow_html=True)

# STICKER DECOR 1
st1_path = POSTER_DIR / "sticker 3.png"
st2_path = POSTER_DIR / "sticker 5.png"
st3_path = POSTER_DIR / "sticker 17.png"
st4_path = POSTER_DIR / "sticker 10.png"

st1_b64 = get_base64_image(st1_path)
st2_b64 = get_base64_image(st2_path)
st3_b64 = get_base64_image(st3_path)
st4_b64 = get_base64_image(st4_path)

# Kiểm tra và hiển thị
if st1_b64 and st2_b64:
    st.markdown(f"""
<div style="display: flex; justify-content: center; align-items: flex-end; margin-top: 20px; margin-bottom: -30px; position: relative; z-index: 100; pointer-events: none; gap: 150px;">
    <div style="transform: translateY(30px);">
        <img src="data:image/png;base64,{st2_b64}" style="width: 100px; height: auto; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));" />
    </div>
    <div style="transform: translateY(-30px) rotate(5deg);">
        <img src="data:image/png;base64,{st1_b64}" style="width: 200px; height: auto; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));" />
    </div>
    <div style="transform: rotate(-15deg);">
        <img src="data:image/png;base64,{st3_b64}" style="width: 100px; height: auto; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));" />
    </div>
    <div>
        <img src="data:image/png;base64,{st4_b64}" style="width: 100px; height: auto; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));" />
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==== helper: đọc ảnh & encode base64 ====
def img_b64(p: Path) -> str:
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
    
posters = [
    POSTER_DIR / "POSTER 1.jpg",
    POSTER_DIR / "POSTER 2.jpg",
    POSTER_DIR / "POSTER 3.jpg",
    POSTER_DIR / "POSTER 4.jpg",
    POSTER_DIR / "POSTER 5.jpg",
]
b64s = [img_b64(p) for p in posters]

# ==== HTML + CSS: xếp chồng & xoay ====
# ==== HTML + CSS: xếp chồng & xoay (BẢN CÓ BADGE ĐÈ LÊN ẢNH) ====
html = f"""
<div class="poster-stack">
  <div class="card card-1"><img src="data:image/jpeg;base64,{b64s[0]}" /></div>
  <div class="card card-2"><img src="data:image/jpeg;base64,{b64s[1]}" /></div>
  <div class="card card-3"><img src="data:image/jpeg;base64,{b64s[2]}" /></div>
  <div class="card card-4"><img src="data:image/jpeg;base64,{b64s[3]}" /></div>
  <div class="card card-5"><img src="data:image/jpeg;base64,{b64s[4]}" /></div>

  <!-- callouts -->
  <div class="badge badge-1">96% Positive 😊</div>
  <div class="badge badge-3">Mind-twisted 🤩</div>
  <div class="badge badge-5">AMAZING 😱!!!!</div>
</div>

<style>
 .poster-stack {{
  position: relative;
  max-width: 1100px;
  height: 600px;       /* trước: 520px */
  margin: 2 auto;
}}

.poster-stack .card {{
  position: absolute;
  top: 40px;
  width: 310px;        /* trước: 220/260px -> TO HƠN */
  aspect-ratio: 2/3;
  border-radius: 16px;
  overflow: hidden;
  border: 3px solid #1A1A1A;
  box-shadow: 0 18px 30px rgba(0,0,0,0.25);
  transition: transform 180ms ease, box-shadow 180ms ease;
}}
  .poster-stack .card img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .poster-stack .card:hover {{ transform: translateY(-6px) scale(1.03) rotate(var(--rot)); z-index: 20; }}

  /* vị trí & góc xoay từng ảnh */
/* vị trí & góc xoay từng ảnh – spacing nới ra */
.poster-stack .card-1 {{ left: 4%;  transform: translateX(0)     rotate(-12deg); --rot:-12deg; z-index:5; }}
.poster-stack .card-2 {{ left: 24%; transform: translateX(-10%)  rotate(-6deg);  --rot:-6deg;  z-index:7; }}
.poster-stack .card-3 {{ left: 44%; transform: translateX(-20%)  rotate(0deg);   --rot:0deg;   z-index:9; }}
.poster-stack .card-4 {{ left: 64%; transform: translateX(-30%)  rotate(6deg);   --rot:6deg;   z-index:7; }}
.poster-stack .card-5 {{ left: 84%; transform: translateX(-40%)  rotate(12deg);  --rot:12deg;  z-index:5; }}


  /* === BADGE ĐÈ LÊN ẢNH === */
  .poster-stack .badge {{
    position: absolute;
    bottom: 200px;                 /* đẩy badge lên giữa poster */
    padding: 8px 14px;
    border-radius: 14px;
    border: 3px solid #1A1A1A;
    font-family: 'Courier Prime', monospace;
    font-weight: 700;
    color: #1A1A1A;
    z-index: 9999;                 /* nằm trên poster */
    box-shadow: 0 8px 16px rgba(0,0,0,0.12);
  }}
.poster-stack .badge-1 {{ 
  left: 10%; 
  bottom: 100px;          /* 215 -> 195 */
  background:#D6EFFF; 
  transform: rotate(-6deg); 
}}

.poster-stack .badge-3 {{
  left: 48%; 
  bottom: 550px;          /* 245 -> 225 */
  background:#FFD6E0; 
  transform: translateX(-20%) rotate(2deg); 
}}

.poster-stack .badge-5 {{ 
  left: 70%; 
  bottom: 100px;          /* 225 -> 205 */
  background:#D6EFFF; 
  transform: rotate(5deg); 
}}


  /* responsive */
  @media (max-width: 1200px) {{
    .poster-stack {{ height: 460px; }}
    .poster-stack .card {{ width: 200px; }}
    .poster-stack .badge {{ bottom: 170px; }}
  }}
  @media (max-width: 992px) {{
    .poster-stack {{ height: 420px; }}
    .poster-stack .card {{ width: 180px; }}
    .poster-stack .badge {{ bottom: 150px; }}
  }}
  @media (max-width: 820px) {{
    .poster-stack {{ height: 360px; }}
    .poster-stack .card {{ width: 140px; }}
    .poster-stack .badge {{ bottom: 120px; }}
  }}
</style>
"""

components.html(html, height=560, scrolling=False)

# STICKER DECOR 2
st5_path = POSTER_DIR / "sticker 11.png"
st6_path = POSTER_DIR / "sticker 19.png"
st7_path = POSTER_DIR / "sticker 20.png"

st5_b64 = get_base64_image(st5_path)
st6_b64 = get_base64_image(st6_path)
st7_b64 = get_base64_image(st7_path)

# Kiểm tra và hiển thị
if st1_b64 and st2_b64:
    st.markdown(f"""
<div style="display: flex; justify-content: center; align-items: flex-end; margin-top: -50px; margin-bottom: 50px; position: relative; z-index: 100; pointer-events: none; gap: 150px;">
    <div style="transform: translateY(-80px);">
        <img src="data:image/png;base64,{st6_b64}" style="width: 200px; height: auto; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));" />
    </div>
    <div style="transform: translateY(50px);">
        <img src="data:image/png;base64,{st5_b64}" style="width: 350px; height: auto; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));" />
    </div>
    <div style="transform: translateY(30px) rotate(5deg);">
        <img src="data:image/png;base64,{st7_b64}" style="width: 200px; height: auto; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));" />
    </div>
</div>
""", unsafe_allow_html=True)

# FONTS + CONTAINER
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baskervvill...amily=Courier+Prime:wght@400;700&display=swap" rel="stylesheet">

<style>
:root{ --bg:#FCFAF5; --ink:#1A1A1A; --lime:#D8FF84; --pink:#FFD6E0; --blue:#D6EFFF; }
[data-testid="stAppViewContainer"]{ background:var(--bg); }
.block-container{ max-width:1400px; padding-top:80px; }

/* ======= NAV & RECOMMEND BUTTON STYLE ======= */
div[data-testid="stVerticalBlock"] button{
    height:65px; 
    border:3px solid var(--ink); 
    border-radius: 20px; 
    background:var(--lime);
    box-shadow:5px 5px 10px 1px var(--pink); 
    transition:transform .15s ease; 
    align-items:center;
}
div[data-testid="stVerticalBlock"] button > * {
    color:var(--ink); 
    font-family:'Courier Prime',monospace; 
    font-weight:700; 
    font-size:20px;
}
div[data-testid="stVerticalBlock"] button:hover{ 
    background:var(--lime); 
    box-shadow:5px 5px 10px 1px var(--pink); 
    transform:scale(1.03); 
}
</style>""", unsafe_allow_html=True)

st.markdown("""
    <div style="margin-top: 50px;"></div>
""", unsafe_allow_html=True)

# CTA Buttons
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Your Next Favourite Movies", use_container_width=True):
        st.switch_page("pages/recommendations.py")            

with col2:
    if st.button("Analyze Your Reviews", use_container_width=True):
        st.switch_page("pages/review.py")

