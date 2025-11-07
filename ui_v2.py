import streamlit as st
import pandas as pd
import requests
import json

#Title
st.set_page_config(page_title="Movie Analytic & Recommendation", page_icon="🎬", layout="centered") #chỉnh thành wide nếu muốn nó rộng hơn

#Navigation
st.markdown('<p class="main-title">Movie Analytic & Recommendation</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div style="text-align:center;"><button style="background-color:#D8FF84;border:2px solid #1A1A1A;border-radius:10px;padding:10px 20px;font-family:\'Courier Prime\', monospace;font-weight:700;font-size:18px;box-shadow:3px 3px 0px #FFD6E0;">Analyze Movies</button></div>', unsafe_allow_html=True)
with col2:  
    st.markdown('<div style="text-align:center;"><button style="background-color:#D8FF84;border:2px solid #1A1A1A;border-radius:10px;padding:10px 20px;font-family:\'Courier Prime\', monospace;font-weight:700;font-size:18px;box-shadow:3px 3px 0px #FFD6E0;">Movie Recommendations</button></div>', unsafe_allow_html=True)

st.markdown('<p class="subtitle">Help you <span class="highlight">analyze</span> your movies</p>', unsafe_allow_html=True)
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
            font-family: 'Courier Prime', monospace;
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
    </style>
""", unsafe_allow_html=True)

#API
API_URL = "https://review-sentiment-app.onrender.com/predict"

#Nhập raw text & upload file
movie_name = st.text_input("Enter your movie name...")
col3, col4 = st.columns([2, 1])
with col3:
    raw_text = st.text_area("Enter your comment...", placeholder="Write your movie review here...")
with col4:
    uploaded_file = st.file_uploader("Upload your file (.csv)", type=["csv"])

#Xử lý dữ liệu, hiển thị preview
df = pd.DataFrame()

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("#### Data preview")
    st.dataframe(df.head())

elif raw_text:
    df = pd.DataFrame({"Review": [raw_text]})
    st.write("#### Your review:")
    st.dataframe(df)
analyse = st.button(label = "Analyse")

#Gửi dữ liệu đến API
if analyse:
    # 1️⃣ Nếu người dùng nhập text
    if raw_text and uploaded_file is None:
        input_data = {"text": [raw_text]}  # API yêu cầu list
        try:
            result = requests.post(API_URL, json=input_data)
            response_json = result.json()

            if isinstance(response_json, list) and len(response_json) > 0:
                first_result = response_json[0]
                st.success(f"🎬 Review: **{first_result.get('review','')}**")
                st.write(f"Prediction: **{first_result.get('pred','unknown').upper()}** "
                         f"({round(first_result.get('score',0.0),3)})")
            else:
                st.error("⚠️ API trả về định dạng không hợp lệ.")
        except Exception as e:
            st.error(f"🚫 Lỗi kết nối API: {e}")

    # 2️⃣ Nếu người dùng upload file CSV
    elif uploaded_file is not None:
        try:
            # Giả định cột đầu tiên chứa review
            text_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
            texts = df[text_col].astype(str).tolist()

            input_data = {"text": texts}
            st.info("⏳ Sending data to API... please wait a moment.")
            result = requests.post(API_URL, json=input_data, timeout=60)

            response_json = result.json()

            if isinstance(response_json, list):
                # Chuyển list dict thành DataFrame
                df_result = pd.DataFrame(response_json)
                df_result.reset_index(inplace=True)
                df_result.rename(columns={"index": "stt"}, inplace=True)
                df_result["stt"] = df_result["stt"] + 1

                # Hiển thị kết quả
                st.success("✅ Phân tích thành công!")
                if "pred" in df_result.columns:
                    counts = df_result["pred"].str.lower().value_counts(dropna=False)
                    pos = int(counts.get("positive", 0))
                    neg = int(counts.get("negative", 0))
            
                    total = len(df_result)
                    pos_rate = pos / total if total else 0.0
                    neg_rate = neg / total if total else 0.0
        

                st.markdown("### 📊 Results Table")
                col5, col6 = st.columns([2, 1])
                
                with col5:
                    st.dataframe(df_result[["stt", "review", "pred", "score"]])


                with col6:
                    # POS/NEG box
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
                st.error("⚠️ API trả về định dạng không hợp lệ.")
        except Exception as e:
            st.error(f"🚫 Lỗi kết nối API: {e}")

#Find similar movies
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
st.button("Find similar movies?", key="find_btn")
st.markdown('</div>', unsafe_allow_html=True)