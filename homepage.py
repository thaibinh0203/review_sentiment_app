import streamlit as st

# 1. CẤU HÌNH
st.set_page_config(page_title = "Movie Homepage", layout = "wide")

# ===================== FONTS + CONTAINER =================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baskervville:ital,wght@0,400;0,700;1,400&family=Courier+Prime:wght@400;700&display=swap" rel="stylesheet">

<style>
:root{ --bg:#FCFAF5; --ink:#1A1A1A; --lime:#D8FF84; --pink:#FFD6E0; --blue:#D6EFFF; }
[data-testid="stAppViewContainer"]{ background:var(--bg); }
.block-container{ max-width:1400px; padding-top:80px; }

</style>""", unsafe_allow_html=True)

#Navigation
col1, col2 = st.columns([1,1])

with col1:
    if st.button("Homepage", use_container_width=True):
        st.switch_page("homepage.py")            

with col2:
    if st.button("Analyze Reviews", use_container_width=True):
        st.switch_page("pages/review.py") 

st.markdown("""
    <style>
        .subtitle-box {
            font-family: 'Caveat', cursive;
            font-size: 40px;
            text-align: center;
            color: #1A1A1A;
            margin-top: 20px;
        }

        .highlight {
            background-color: #FFD6E0;
            padding: 4px 10px;
            border-radius: 6px;
        }
   
    </style>

    <div class="subtitle-box">
        
    </div>
""", unsafe_allow_html=True)
# 3. CSS
st.markdown("""
<style>
    /* 1. Background */
    [data-testid="stAppViewContainer"] {
        background-color: #FCFAF5;
    }

    /* 2. Headings */
    .headings-font {
        font-family: 'Baskervville', serif;
        font-weight: 500;
        font-size: 40px;
        color: #1A1A1A;
        text-align: center;
    }
    
    /* 3. Subhead */
    .subhead-font {
        font-family: 'Courier Prime', monospace;
        font-weight: 400;
        font-size: 25px;
        color: #1A1A1A;
        text-align: center;
    }
    .pink-highlight { color: #FFD6E0; }
    .blue-highlight { color: #D6EFFF; }

    /* 4. Body */
    .body-text {
        font-family: 'Courier Prime', monospace;
        font-weight: 700; /* Bold */
        font-size: 20px;
        color: #1A1A1A;
        text-align: center;
    }
    
    /* 5. Button */
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
    
            
    /* 6. Callout/Cards */
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

# 3. WEB LAYOUT

# Navigation Bar
header_cols = st.columns([2, 1, 1]) # Chia layout thành 3 cột
import os
from pathlib import Path

BASE_DIR = Path(os.getcwd()) # Lấy đường dẫn thư mục hiện tại
poster_dir = BASE_DIR / "images" # Thư mục chứa ảnh

# Hiển thị logo nếu tồn tại
with header_cols[0]:
    try:
        st.image(str((poster_dir / "LOGO.jpg")), width=300)
    except FileNotFoundError:
        st.error("Lỗi: Không tìm thấy LOGO.jpg")

# Header and subheader
st.markdown("""
<div class="headings-font">
    When <span style='color: #FFACC0;'>Bag of Words</span> meets <span style='color: #AADEFF;'>Bags of Popcorn</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""<div class = "subhead-font">This is a web for you to analyze your reviews or find your favorite movie !</div>""", unsafe_allow_html=True)


st.divider()

import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# ==== helper: đọc ảnh & encode base64 ====
def img_b64(p: Path) -> str:
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")



posters = [
    poster_dir / "POSTER 1.jpg",
    poster_dir / "POSTER 2.jpg",
    poster_dir / "POSTER 3.jpg",
    poster_dir / "POSTER 4.jpg",
    poster_dir / "POSTER 5.jpg",
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
  max-width: 1500px;   /* trước: 1100px */
  height: 630px;       /* trước: 520px */
  margin: 0 auto;
}}

.poster-stack .card {{
  position: absolute;
  top: 40px;
  width: 320px;        /* trước: 220/260px -> TO HƠN */
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

# ===================== FONTS + CONTAINER =================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baskervville:ital,wght@0,400;0,700;1,400&family=Courier+Prime:wght@400;700&display=swap" rel="stylesheet">

<style>
:root{ --bg:#FCFAF5; --ink:#1A1A1A; --lime:#D8FF84; --pink:#FFD6E0; --blue:#D6EFFF; }
[data-testid="stAppViewContainer"]{ background:var(--bg); }
.block-container{ max-width:1400px; padding-top:80px; }

</style>""", unsafe_allow_html=True)

#Navigation
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Recommendations", use_container_width=True):
        st.switch_page("pages/recommendations.py")            

with col2:
    if st.button("Analyze Reviews", use_container_width=True):
        st.switch_page("pages/review.py") 












