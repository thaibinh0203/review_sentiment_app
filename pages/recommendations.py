import streamlit as st
import pandas as pd
import requests
from pathlib import Path



import pandas as pd
import numpy as np
import ast
from collections import Counter
import math

# Đọc dữ liệu
MOVIES_CSV  = "data/tmdb_5000_movies.csv"
CREDITS_CSV = "data/tmdb_5000_credits.csv"

# Merge 2 dataset
movies = movies.merge(credits, left_on='title', right_on='title')

# Chỉ giữ lại các cột cần thiết
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# Hàm convert genres, keywords
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L















# ===================== PATH & KEYS ======================
LOGO_PATH = Path("images/LOGO.jpg")
MOVIES_CSV  = "data/tmdb_5000_movies.csv"
CREDITS_CSV = "data/tmdb_5000_credits.csv"

TMDB_API_KEY = "32be515044e4f084aa5b020364d6e780"

# ===================== PAGE CONFIG ======================
st.set_page_config(page_title="RCM • Movie Recommender", layout="wide")

# ===================== FONTS + THEME CSS =================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baskervville:ital,wght@0,400;0,700;1,400&family=Courier+Prime:wght@400;700&display=swap" rel="stylesheet">

<style>
:root{
  --bg:#FCFAF5; --ink:#1A1A1A; --lime:#D8FF84; --pink:#FFD6E0; --blue:#D6EFFF;
}
.block-container{ max-width:1400px; padding-top:12px; }
[data-testid="stAppViewContainer"]{ background:var(--bg); }

/* Header: chỉ còn logo bên trái */
.header-wrap{ display:flex; align-items:center; justify-content:space-between; gap:24px; }
.brand{ display:flex; align-items:center; gap:18px; }

/* Cặp nút ở giữa */
.top-cta{
  display:flex; justify-content:center; gap:28px;
  margin:10px 0 6px;
}
.btn-pill{
  display:inline-flex; align-items:center; justify-content:center;
  height:56px; min-width:260px; padding:0 22px;
  border:3px solid var(--ink); border-radius:16px; background:var(--lime);
  color:var(--ink); font-family:'Courier Prime',monospace; font-weight:700; font-size:18px;
  box-shadow:8px 8px 12px 2px var(--pink); text-decoration:none; transition:transform .15s ease;
}
.btn-pill:hover{ transform:scale(1.03); background:#E8FF9A; }

/* Title */
h1.hero{
  text-align:center; margin:12px 0 14px;
  font-family:'Baskervville',serif; font-weight:700; font-size:44px; color:var(--ink);
}
.hero .hi{ background:var(--pink); padding:0 8px; border-radius:6px; }

/* Input row */
div[data-baseweb="select"]{ border:3px solid var(--ink); border-radius:16px; }
.stSelectbox > div > div{ height:60px; }
.stSelectbox label{ display:none; }
div[data-testid="stVerticalBlock"] button{
  height:60px; border:3px solid var(--ink); border-radius:16px; background:var(--lime);
  color:var(--ink); font-family:'Courier Prime',monospace; font-weight:700;
  box-shadow:5px 5px 10px 1px var(--pink); transition:transform .15s ease;
}
div[data-testid="stVerticalBlock"] button:hover{ transform:scale(1.03); }

/* Gallery */
.gallery-title{
  text-align:center; font-family:'Courier Prime',monospace; font-weight:700;
  font-size:26px; margin:10px 0 18px; color:var(--ink);
}
.card{ text-align:center; }
.card img{
  height:350px; width:auto; border-radius:16px; box-shadow:0 6px 12px rgba(0,0,0,.25);
  display:block; margin:0 auto;
}
.card .caption{
  margin-top:12px; font-family:'Courier Prime',monospace; font-weight:700; font-size:14px;
  letter-spacing:.3px; color:var(--ink); text-transform:uppercase;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# CUSTOM TF-IDF + COSINE SIM
# ---------------------------

class SimpleTFIDF:
    def __init__(self):
        self.vocab = {}
        self.idf = {}
    
    def fit_transform(self, documents):
        n_docs = len(documents)
        doc_freq = Counter()

        # Tính document frequency
        for doc in documents:
            words = doc.split()
            doc_freq.update(set(words))

        # tạo vocab
        self.vocab = {word: idx for idx, word in enumerate(doc_freq.keys())}

        # tính IDF
        self.idf = {
            word: math.log(n_docs / (freq + 1))
            for word, freq in doc_freq.items()
        }

        # tạo TF-IDF matrix
        tfidf_matrix = []
        for doc in documents:
            words = doc.split()
            word_count = Counter(words)
            length = len(words)

            vector = [0] * len(self.vocab)
            for word, count in word_count.items():
                if word in self.vocab:
                    tf = count / length
                    vector[self.vocab[word]] = tf * self.idf[word]
            tfidf_matrix.append(vector)

        return np.array(tfidf_matrix)

def cosine_similarity_manual(vec1, vec2):
    dot = np.dot(vec1, vec2)
    n1 = np.linalg.norm(vec1)
    n2 = np.linalg.norm(vec2)
    if n1 == 0 or n2 == 0:
        return 0
    return dot / (n1 * n2)

def compute_cosine_similarity_matrix(matrix):
    n = matrix.shape[0]
    sim = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            sim[i][j] = cosine_similarity_manual(matrix[i], matrix[j])
    return sim




# ===================== TMDB POSTER ======================
@st.cache_resource
@st.cache_resource
def load_data():
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

    # build tags
    df["tags"] = df["genres"] + df["keywords"] + df["cast"] + df["crew"]
    df["tags"] = df["tags"].apply(lambda x: " ".join(x))

    df = df[["movie_id", "title", "tags"]]

    # --------- CUSTOM TF-IDF + COSINE SIM -----------
    tfidf = SimpleTFIDF()
    tfidf_matrix = tfidf.fit_transform(df["tags"].tolist())

    similarity = compute_cosine_similarity_matrix(tfidf_matrix)

    return df.reset_index(drop=True), similarity


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    data = requests.get(url).json()
    p = data.get("poster_path")
    return f"https://image.tmdb.org/t/p/w500{p}" if p else None

# ⭐ ADD HERE — FETCH TRAILER FROM TMDB
def fetch_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
    data = requests.get(url).json()

    for v in data.get("results", []):
        if v.get("type") == "Trailer" and v.get("site") == "YouTube":
            key = v.get("key")
            return f"https://www.youtube.com/watch?v={key}"

    return None

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

# ===== HEADER: chỉ logo bên trái =====
st.markdown('<div class="header-wrap">', unsafe_allow_html=True)
st.markdown('<div class="brand">', unsafe_allow_html=True)
if LOGO_PATH.exists():
    st.image(str(LOGO_PATH), width=140)
st.markdown('</div></div>', unsafe_allow_html=True)

# ===== 2 NÚT Ở GIỮA (trang trí) =====
col1, col2 = st.columns([2, 2])
st.markdown("""
<style>
div[data-testid="stButton"] > button {
    background-color:#D8FF84;
    border:3px solid #1A1A1A;
    border-radius:12px;
    padding:12px 20px;
    font-family:'Courier Prime', monospace;
    font-weight:700;
    font-size:24px;
    box-shadow:6px 6px 0px #FFD6E0;
    color:#1A1A1A;
}
div[data-testid="stButton"] > button:hover {
    background-color:#E8FF9A;
}
</style>
""", unsafe_allow_html=True)

with col1:
    if st.button("Homepage", use_container_width=True):
        st.switch_page("homepage.py")            

with col2:
    if st.button("Analyze Movies", use_container_width=True):
        st.switch_page("pages/review.py") 

# ===== TITLE =====
st.markdown('<h1 class="hero">Your <span class="hi">next</span> movie</h1>', unsafe_allow_html=True)

# ===================== INPUT + BUTTON ===================
c1, cbtn, _ = st.columns([6, 2, 1])
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
                    trailer = fetch_trailer(int(mid))

                    if poster:
                        trailer = fetch_trailer(int(mid))

                        if trailer:
                            trailer_html = f"""
                    <a href="{trailer}" target="_blank" style="
                    display:inline-block;
                    margin-top:8px;
                    padding:8px 10px;
                    background:#FF4B4B;
                    color:white;
                    border-radius:8px;
                    font-family:'Courier Prime', monospace;
                    font-size:13px;
                    font-weight:700;
                    text-decoration:none;
                    box-shadow:0 3px 6px rgba(0,0,0,0.25);
                    ">▶ Trailer</a>
                    """
                        else:
                            trailer_html = """
                    <div style="font-size:12px;color:#666;margin-top:8px;">
                    No trailer 🎬
                    </div>
                    """

                        card_html = f"""
                    <div class="card">
                    <img src="{poster}" alt="{title}">
                    <div class="caption">{title}</div>
                    {trailer_html}
                    </div>
                    """

                        st.markdown(card_html, unsafe_allow_html=True)

