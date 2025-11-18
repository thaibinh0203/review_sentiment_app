# 🎬 Movie Review Sentiment Analysis & Recommendation System

NLP-based web application for:
- **Sentiment analysis** on user reviews/comments  
- **Content-based movie recommendations** based on user input

Deployed using:
- **Streamlit** for the web UI  
- **Render** for hosting the ML API  
- **Streamlit Cloud** (`share.streamlit.io`) for deploying the final app  

👉 **Live demo:**  
https://reviewsentimentapp-xntsyzheg3id5vbngkiq6j.streamlit.app/  

> 💡 **Note:**  
> If the review analysis feature throws a `RuntimeError` or returns no result, **try running it again**.  
> On Render free tier, the first request may be slow while the server is “waking up”; from the second request onwards it is much faster.

---

## 📌 1. Project Introduction

This project explores the application of **Natural Language Processing (NLP)** in two related tasks:

1. **Sentiment Analysis of User Comments**
   - Input: raw text from user or a `.csv` file with 2 columns:
     - `stt`: index from 1 to number of reviews  
     - `reviews`: the review text  
   - Main NLP steps:
     - Tokenization  
     - Stopword removal  
     - Stemming / Lemmatization  
     - Vectorization using **Bag of Words (BoW)** / **TF-IDF**  
   - Output: predicted **sentiment** (positive / negative).

2. **Movie Recommendation System**
   - Uses **content-based filtering** with textual features such as:
     - Genres  
     - Keywords  
     - Plot summaries  
     - Cast & crew  
   - Techniques:
     - **TF-IDF vectorization**  
     - **Cosine similarity**  
   - User can:
     - Type a movie name, or  
     - Select a movie from the **Streamlit selectbox**  
   - Output: a list of **recommended movies** most similar to the selected/input movie.

Together, these two tasks show how NLP can:
- Understand human language (by classifying sentiment), and  
- Drive intelligent recommendations (by computing similarity between movies and user input).

---

## 🏗️ 2. Project Structure & Git Branches

The repository is organized into multiple branches, each responsible for a specific part of the system:

### 🔹 `Review_Sentiment_Machine_Learning`
- Implements the **Bag of Words meets Bag of Popcorns** assignment.
- Tasks:
  - Data cleaning & preprocessing  
  - TF-IDF & BoW feature extraction  
  - Train & compare ML models:
    - Logistic Regression  
    - Linear SVC  
    - Random Forest  
  - Evaluate metrics and select the **best model**
  - Save the trained model to `.pkl` for later use.

### 🔹 `Review_Sentiment_Backend_Render`
- Backend for **API deployment on Render**.
- Main components:
  - `artifacts/`: stores `.pkl` model file(s)  
  - `domain/`: Pydantic models & schema for requests/responses  
  - `services/`: file processing, input handling, and prediction logic  
  - `main.py`: FastAPI / Uvicorn entrypoint for Render

### 🔹 `Movie_Recommendations_Machine_Learning`
- Prototyping & testing **movie recommendation algorithms** on localhost.
- Uses:
  - TF-IDF on movie metadata  
  - Cosine similarity to recommend top similar movies.
- Prepares logic for integration into the Streamlit app.

### 🔹 `Homepage_Combine`
- Final **integrated Streamlit app**, combining all previous parts:
  - `homepage.py`: main homepage UI + navigation  
  - `review.py`: connects to the **sentiment analysis** backend/API  
  - `recommendations.py`: runs the **movie recommendation** logic  
- Deployed to **Streamlit Cloud** for users.

---

## 👨‍💻 3. Team Members & Contributions

| No. | Member                | Role          | Contribution | Main Responsibilities |
|-----|-----------------------|---------------|--------------|------------------------|
| 1   | **Thái Thanh Bình**   | Leader        | 17.5%        | Idea, ML workflow (BoW meets BoP), Streamlit structure, ML (Logistic Regression + Linear SVC), Review_Sentiment_Backend_Render, core part of `ReviewSentiment.ipynb`, bug fixing & integration, `review.py` logic |
| 2   | **Nguyễn Ngọc Linh**  | Vice Leader   | 14.5%        | ML with Random Forest, metrics/compare in `ReviewSentiment.ipynb`, idea for movie recommendations, `Movie_Recommendations_Testing` branch, logic in `recommendations.py` |
| 3   | **Phùng Nhật Minh**   | Member        | 14.5%        | Data cleaning in `ReviewSentiment.ipynb`, learn & implement TF-IDF, design + function in `homepage.py` |
| 4   | **Ngô Mạnh Duy**      | Member        | 10%          | Data cleaning, TF-IDF, writing report, making presentation slides |
| 5   | **Hoàng Linh Phương** | Member        | 14.5%        | Homepage design, drawing and UI for Homepage/Review/Recommendation, `homepage.py` (design + function), learning Streamlit |
| 6   | **Nguyễn Lâm Huy**    | Member        | 14.5%        | UI design & implementation for `review.py` in `Homepage_Combine`, learning Streamlit |
| 7   | **Lê Thị Như Ý**      | Member        | 14.5%        | UI design & implementation for recommendations page, learning Streamlit |

---

## ⚙️ 4. Installation & Setup

### 🐍 Python Version

- Recommended: **Python 3.12**

### 📦 Dependencies

Each branch includes its own `requirements.txt`.  
You can install dependencies with:

```bash
pip install -r requirements.txt
