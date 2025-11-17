import streamlit as st
import pandas as pd
import requests
from pathlib import Path

# ===================== PATH & KEYS ======================
LOGO_PATH = Path("images/LOGO.jpg")
MOVIES_CSV  = "data/tmdb_5000_movies.csv"
CREDITS_CSV = "data/tmdb_5000_credits.csv"

TMDB_API_KEY = "32be515044e4f084aa5b020364d6e780"

# ===================== PAGE CONFIG ======================
st.set_page_config(page_title="RCM • Movie Recommender", layout="wide")

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
            
# ===================== LOGO + NAVIGATION ==========================
col_img, col1, col2 = st.columns([3, 3, 3])

with col_img:    
    logo_path = Path.cwd() / "images" / "LOGO.jpg"
    if logo_path.exists():
        st.image(str(logo_path), width=300)
    else:
        st.error(f"Không tìm thấy logo: {logo_path}")

with col1:
    st.markdown("""
    <div style="text-align:center;">
        <a href="/homepage" target="_self">
            <button style="
                background-color:var(--lime);
                border:2px solid var(--ink);
                border-radius:16px;
                height:60px;
                padding:10px 65px;  
                font-family:'Courier Prime', monospace;
                font-weight:700;
                font-size:20px;
                line-height:20px;
                box-shadow:5px 5px 10px 1px var(--pink);">
                Homepage
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)
 
with col2:
    st.markdown("""
    <div style="text-align:center;">
        <a href="/pages/review" target="_self">
            <button style="
                background-color:var(--lime);
                border:2px solid var(--ink);
                border-radius:16px;
                height:60px;
                padding:10px 30px;
                font-family:'Courier Prime', monospace;
                font-weight:700;
                font-size:20px;
                line-height:20px;
                box-shadow:5px 5px 10px 1px var(--pink);">
                Analyze Movies
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

# ======= TITLE =======
st.markdown("""<style>
h1.hero{
    text-align:center; margin-top:10px; color:var(--ink);
    font-family:'Baskervville',serif; font-weight:500; font-size:50px; 
} 
.hero .hi{ background:var(--pink); padding:0 8px; border-radius:6px; } 
</style>

<h1 class="hero">Your <span class="hi">next</span> movie</h1>
""", unsafe_allow_html=True)

st.markdown("---")  

# ============== INPUT BOX + RECOMMEND BUTTON + GALLERY ================           
st.markdown("""<style>
/* ======= INPUT BOX ======= */
.stSelectbox label { display:none; }
.stSelectbox > div > div { height:60px; }

/* Style box */
div[data-baseweb="select"] {
    background-color: var(--bg) !important;  /* Keep your preferred blue */
    border: 3px solid var(--ink) !important;
    border-radius: 11px !important;
}
/* Text inside */
div[data-baseweb="select"] * {
    background-color: transparent !important;
    font-family: 'Courier Prime', monospace !important;
    font-size: 17px !important;
    align-items: center;
}

/* ======= RECOMMEND BUTTON ======= */
div[data-testid="stVerticalBlock"] button{
    height:65px; border:3px solid var(--ink); border-radius:11px; background:var(--lime);
    box-shadow:5px 5px 10px 1px var(--pink); transition:transform .15s ease; align-items:center;
}
div[data-testid="stVerticalBlock"] button > * {
    color:var(--ink); font-family:'Courier Prime',monospace; font-weight:700; font-size:20px;
}
div[data-testid="stVerticalBlock"] button:hover{ 
    background:var(--lime); box-shadow:5px 5px 10px 1px var(--pink); transform:scale(1.03); 
}

/* ======= GALLERY ======= */
.gallery-title{
    text-align:center; font-family:'Courier Prime',monospace; font-weight:700;
    font-size:26px; margin:10px 0 20px; color:var(--ink);
} 
.card{ text-align:center; margin-bottom:30px; }
.card img{
    aspect-ratio: 2 / 3; width:auto; border-radius:16px; box-shadow:0 6px 12px rgba(0,0,0,.25);
    display:block; margin:0 auto; object-fit:cover;
}
.card:hover img { transform: scale(1.05); }
.card .caption{
    margin-top:12px; font-family:'Courier Prime',monospace; font-weight:700; font-size:14px;
    letter-spacing:1.3px; color:var(--ink); text-transform:uppercase;
}
</style> """, unsafe_allow_html=True)

# ===================== TMDB POSTER ======================
@st.cache_resource
def load_data():
    import ast
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    movies = pd.read_csv(MOVIES_CSV)
    credits = pd.read_csv(CREDITS_CSV)

    df = movies.merge(credits, on="title")

    def convert(obj):
        L = []
        for i in ast.literal_eval(obj):
            L.append(i["name"])
        return L

    df["genres"] = df["genres"].apply(convert)
    df["keywords"] = df["keywords"].apply(convert)

    def convert_cast(obj):
        L = []
        counter = 0
        for i in ast.literal_eval(obj):
            if counter < 3:
                L.append(i["name"])
                counter += 1
        return L

    df["cast"] = df["cast"].apply(convert_cast)

    def get_director(obj):
        for i in ast.literal_eval(obj):
            if i["job"] == "Director":
                return i["name"]
        return ""
        
    df["crew"] = df["crew"].apply(lambda x: [get_director(x)])

    df["tags"] = df["genres"] + df["keywords"] + df["cast"] + df["crew"]
    df["tags"] = df["tags"].apply(lambda x: " ".join(x))
    df = df[["movie_id","title","tags"]]

    tfidf = TfidfVectorizer(stop_words="english")
    vectors = tfidf.fit_transform(df["tags"])
    similarity = cosine_similarity(vectors)

    return df.reset_index(drop=True), similarity

movies, similarity = load_data()
all_titles = movies["title"].tolist()

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    data = requests.get(url).json()
    p = data.get("poster_path")
    return f"https://image.tmdb.org/t/p/w500{p}" if p else None

# ===================== RECOMMEND CORE ===================
def recommend(title, top_k=10):
    # vị trí phim được chọn
    index = movies[movies["title"] == title].index[0]
    # sắp xếp theo độ tương tự giảm dần
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )
    # bỏ phần tử đầu tiên (chính nó), lấy top_k tiếp theo
    picks = []
    for i, _score in distances[1: top_k + 1]:
        row = movies.iloc[i]
        picks.append((row["title"], row["movie_id"]))
    return picks

# ===================== INPUT + BUTTON ===================
c1, cbtn, _ = st.columns([7, 2, 0.25])
with c1:
    # was: selected = st.selectbox("", movie_titles, index=0)
    selected = st.selectbox("", all_titles, index=0)
with cbtn:
    run = st.button("Recommend", use_container_width=True)

# ===================== RESULTS ==========================
if run:
    recs = recommend(selected, top_k=10)
    if not recs:
        st.warning("No recommendation found for this title.")
    else:
        st.markdown('<div class="gallery-title">Recommended movies:</div>', unsafe_allow_html=True)
        rows = [recs[:5], recs[5:10]]
        for row in rows:
            cols = st.columns(5, gap="large")
            for col, (title, mid) in zip(cols, row):
                with col:
                    poster = fetch_poster(int(mid))
                    if poster:
                        st.markdown(f"""
                            <div class="card">
                                <img src="{poster}" alt="{title}">
                                <div class="caption">{title}</div>
                            </div>""", unsafe_allow_html=True)                    
                    else:
                        st.markdown(f"""
                            <div class="card">
                                <div style="height:350px;width:230px;border-radius:16px;
                                background:#eee;display:flex;align-items:center;justify-content:center;
                                color:#666;box-shadow:0 6px 12px rgba(0,0,0,.25);margin:0 auto;">No poster🎬</div>
                            <div class="caption">{title}</div>
                            </div>""", unsafe_allow_html=True)
