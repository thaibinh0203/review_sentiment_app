import streamlit as st
import pandas as pd
import requests
import os

#Title
st.set_page_config(page_title="Movie Analytic & Recommendation", page_icon="🎬", layout="wide") #chỉnh thành wide nếu muốn nó rộng hơn

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
col_img, col1, col2 = st.columns([2, 2, 2])
from pathlib import Path
with col_img:
    logo_path = Path.cwd() / "images" / "LOGO.jpg"
    if logo_path.exists():
        st.image(str(logo_path), width=300)
    else:
        st.error(f"Không tìm thấy logo: {logo_path}")

with col1:
    if st.button("Homepage", use_container_width=True):
        st.switch_page("homepage.py")            

with col2:
    if st.button("Recommendations", use_container_width=True):
        st.switch_page("pages/recommendations.py") 

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

st.markdown("---")

#Add styles
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Baskervville:ital,wght@0,400;0,700;1,400&family=Courier+Prime:wght@400;700&display=swap');
            
        /* Background */
        body, .stApp {
            background-color: #FCFAF5;
            color: #1A1A1A;
            font-family: 'Georgia', serif;
        }

        /* Title */
        .main-title {
            font-family: 'Caveat', cursive;
            font-size: 56px;
            color: #1A1A1A;
            text-align: left;
            margin-bottom: -10px;
        }
        /* Headings */
        h1, h2, h3 {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            font-weight: bold;
        }
        
        /* Style the input box */
        [data-testid="stFileUploader"] {
            background-color: #D6EFFF !important;  /* Keep your preferred blue */
            border: 2px solid #1A1A1A !important;
            border-radius: 12px !important;
            padding: 16px !important;
            box-shadow: none !important;
        }

        /* Remove inner white layers if any */
        [data-testid="stFileUploader"] * {
            background-color: transparent !important;
        }

        /* Style the textarea input */
        textarea {
            font-family: 'Caveat', cursive !important;
            font-size: 20px !important;
            color: #1A1A1A !important;
            background-color: #FFFBEA !important;
            border: 2px solid #1A1A1A !important;
            border-radius: 10px !important;
            padding: 10px !important;
            box-shadow: none !important;
        }
            
        /* Subtitle */
        .subtitle {
            font-family: 'Baskervville', serif;
            font-size: 26px;
            text-align: center;
            color: #1A1A1A;
            margin-top: -10px;
        }
        .highlight {
            background-color: #FFD6E0;
            padding: 2px 8px;
            border-radius: 4px;
        }

        /* Buttons */
        div[data-testid="stButton"] > button {
            background-color: #D8FF84;
            color: #1A1A1A;
            border: 2px solid #1A1A1A;
            border-radius: 12px;
            font-family: 'Courier Prime', monospace;
            font-weight: 700;
            font-size: 18px;
            padding: 8px 20px;
            box-shadow: 3px 3px 0px #FFD6E0;
        }
        div[data-testid="stButton"] > button:hover {
            background-color: #FFD6E0;
            box-shadow: 3px 3px 0px #D8FF84;
        }

        /* File uploader */
        [data-testid="stFileUploader"] {
            background-color: #D6EFFF;
            border-radius: 10px;
            border: 2px solid #1A1A1A;
            padding: 8px;
            font-family: 'Courier Prime', monospace;
        }

        /* DataFrame styling */
        .stDataFrame {
            background-color: white;
            border: 2px solid #1A1A1A;
            border-radius: 6px;
            font-family: 'Courier Prime', monospace;
        }

        /* Result box */
        .result-box {
            background-color: #FFFFFF;
            border: 2px solid #1A1A1A;
            border-radius: 10px;
            padding: 20px;
            font-family: 'Courier Prime', monospace !important;
            font-weight: bold;
            font-size: 20px;
            text-align: center;
        }

        /* Table header style */
        th {
            background-color: #D8FF84 !important;
            color: #1A1A1A !important;
            font-family: 'Courier Prime', monospace !important;
            border: 1px solid #1A1A1A !important;
        }
            
        /* Remove outer container styling */
        .stTextArea {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
    </style>
""", unsafe_allow_html=True)

#API
API_URL = "https://review-sentiment-app.onrender.com/predict"

#Input raw text & upload file
left, center, right = st.columns([1, 6, 1])
with center:
    col3, col4 = st.columns([2, 1])
    with col3:
        st.markdown("<div style='font-family:Caveat, cursive; font-size:30px;'>Write your movie review here</div>", unsafe_allow_html=True)
        raw_text = st.text_area("", placeholder="Text area...", height=200)
    with col4:
        st.markdown("<div style='font-family:Caveat, cursive; font-size:30px;'>Upload your review file here</div>", unsafe_allow_html=True)
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=["csv"])

#Data process, Data display
df = pd.DataFrame()

left, center, right = st.columns([1, 6, 1])
with center:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("#### Data preview")
        st.dataframe(df.head())

    elif raw_text:
        df = pd.DataFrame({"Review": [raw_text]})
        st.write("#### Your review:")
        st.dataframe(df)
    analyse = st.button(label = "Analyse")

#Send Data to API
if analyse:
    #If user import text
    if raw_text and uploaded_file is None:
        input_data = {"text": [raw_text]}
        try:
            result = requests.post(API_URL, json=input_data)
            response_json = result.json()

            if isinstance(response_json, list) and len(response_json) > 0:
                first_result = response_json[0]
                st.success(f"🎬 Review: **{first_result.get('review','')}**")
                st.write(f"Prediction: **{first_result.get('pred','unknown').upper()}** "
                         f"({round(first_result.get('score',0.0),3)})")
            else:
                left, center, right = st.columns([1, 6, 1])
                with center:
                    st.error("⚠️ API returned invalid format.")
        except Exception as e:
            left, center, right = st.columns([1, 6, 1])
            with center:
                st.error(f"🚫 API connection error: {e}")

    #If user import file
    elif uploaded_file is not None:
        try:
            #Assume the first column contains reviews
            text_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
            texts = df[text_col].astype(str).tolist()

            input_data = {"text": texts}
            left, center, right = st.columns([1, 6, 1])
            with center:
                st.info("⏳ Sending data to API... please wait a moment.")
            result = requests.post(API_URL, json=input_data, timeout=60)

            response_json = result.json()

            if isinstance(response_json, list):
                #Convert list dict to DataFrame
                df_result = pd.DataFrame(response_json)
                df_result.reset_index(inplace=True)
                df_result.rename(columns={"index": "stt"}, inplace=True)
                df_result["stt"] = df_result["stt"] + 1

                #Results Display
                left, center, right = st.columns([1, 6, 1])
                with center:
                    st.success("✅ Analysis successful!")
                if "pred" in df_result.columns:
                    counts = df_result["pred"].str.lower().value_counts(dropna=False)
                    pos = int(counts.get("positive", 0))
                    neg = int(counts.get("negative", 0))
            
                    total = len(df_result)
                    pos_rate = pos / total if total else 0.0
                    neg_rate = neg / total if total else 0.0
        

                left, center, right = st.columns([1, 6, 1])
                with center:
                    st.markdown("### 📊 Results Table")
                left, center, right = st.columns([1, 6, 1])
                with center:
                    col5, col6 = st.columns([2, 1])
                    with col5:
                        st.dataframe(df_result[["stt", "review", "pred", "score"]])

                    with col6:
                        st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
                        st.markdown(
                            f"""
                            <div style="
                                background-color:#FFFFFF;
                                border:2px solid #1A1A1A;
                                border-radius:10px;
                                padding:25px 10px;
                                text-align:center;
                                font-family:'Courier Prime', monospace;
                                font-weight:800;
                                font-size:18px;
                                line-height:1.8;
                                box-shadow:4px 4px 0px #D8FF84;
                                width:250px;
                                margin: 0 auto;
                                position: relative;
                                top: 40px;">
                                POSITIVE: {pos} ({pos_rate:.1%})<br>
                                NEGATIVE: {neg} ({neg_rate:.1%})
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
            else:
                st.error("⚠️ API returned invalid format.")
        except Exception as e:
            st.error(f"🚫 API connection error: {e}")
