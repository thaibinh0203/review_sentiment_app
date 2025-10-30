import streamlit as st
import pandas as pd
import requests
import json
st.set_page_config(page_title="Movie Review & Suggestion", page_icon="🎬", layout="centered")

st.title("🎬 Movie Review & Suggestion")
st.markdown("---")
menu = ["Home", "Movie suggestions"]
choice = st.sidebar.selectbox("Navigation", menu)
API_URL = "https://review-sentiment-app.onrender.com/predict"
#Nhập raw text & upload file
st.subheader("Movie Review & Suggestion")
st.write("### Nhập review trực tiếp")
raw_text = st.text_area("Nhập bình luận phim của bạn tại đây:", placeholder="Nhập review...")
st.write("### Hoặc tải lên file CSV")
uploaded_file = st.file_uploader("Drag and drop file here", type=["csv"])

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
# --- Gửi dữ liệu đến API ---
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
            result = requests.post(API_URL, json=input_data)
            response_json = result.json()

            if isinstance(response_json, list):
                # Chuyển list dict thành DataFrame
                df_result = pd.DataFrame(response_json)
                df_result.reset_index(inplace=True)
                df_result.rename(columns={"index": "stt"}, inplace=True)
                df_result["stt"] = df_result["stt"] + 1

                # Hiển thị kết quả
                st.success("✅ Phân tích thành công!")
                st.dataframe(df_result[["stt", "review", "pred", "score"]])
                if "pred" in df_result.columns:
                    counts = df_result["pred"].str.lower().value_counts(dropna=False)
                    pos = int(counts.get("positive", 0))
                    neg = int(counts.get("negative", 0))
            
                    total = len(df_result)
                    pos_rate = pos / total if total else 0.0
                    neg_rate = neg / total if total else 0.0
        

                    st.markdown("### 📊 Tổng kết")
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Tổng review", f"{total}")
                    c2.metric("Positive", f"{pos}", f"{pos_rate:.1%}")
                    c3.metric("Negative", f"{neg}", f"{neg_rate:.1%}")
                    st.write(
                        pd.DataFrame(
                            {
                                "label": ["positive", "negative", "neutral"],
                                "count": [pos, neg],
                                "ratio": [f"{pos_rate:.2%}", f"{neg_rate:.2%}"],
                            }
                        )
                    )
                # Tải xuống kết quả
                csv = df_result.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Tải kết quả CSV",
                    data=csv,
                    file_name="sentiment_results.csv",
                    mime="text/csv"
                )

            else:
                st.error("⚠️ API trả về định dạng không hợp lệ.")
        except Exception as e:
            st.error(f"🚫 Lỗi kết nối API: {e}")
    