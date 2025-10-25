import os, nltk
nltk.data.path.append(os.environ.get("NLTK_DATA", "/opt/render/nltk_data"))
from nltk.corpus import stopwords
import numpy as np
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
def clean_text(text):
    # 2.1 Xóa HTML bằng BeautifulSoup (chính xác hơn Regex)
    text = BeautifulSoup(text, "html.parser").get_text()

    # 2.2 Xóa HTML còn sót lại bằng Regex (dự phòng)
    text = re.sub(r'<.*?>', '', text)

    # 2.3 Chuyển toàn bộ về chữ thường (lowercase) để tránh phân biệt "Học" vs "học"
    text = text.lower()

    # 2.4 Xóa ký tự đặc biệt, số, dấu câu — chỉ giữ lại chữ cái (có hỗ trợ tiếng Việt)
    text = re.sub(r'[^a-zA-Zà-ỹÀ-Ỹ\s]', '', text)

    # 2.5 Xóa khoảng trắng dư thừa
    text = re.sub(r'\s+', ' ', text).strip()

    # 2.6 Xóa stopwords (bao gồm cả tiếng Anh + tiếng Việt tự thêm vào)
   # stopwords tiếng Anh gốc
    stop_words = set(stopwords.words('english'))

    # *** GIỮ LẠI CÁC TỪ PHỦ ĐỊNH ***
    neg_keep = {
        "not", "no", "nor", "never", "without",
        "n't",  # để giữ dạng don't/doesn't... nếu bạn giữ dấu '
        "cannot", "cant", "can't", "dont", "don't", "wont", "won't",
        "isnt", "isn't", "arent", "aren't", "wasnt", "wasn't",
        "werent", "weren't", "shouldnt", "shouldn't", "wouldnt", "wouldn't",
        "couldnt", "couldn't", "mustnt", "mustn't"
    }
    stop_words = stop_words.difference(neg_keep)

    # Lọc stopwords
    text = ' '.join([word for word in text.split() if word not in stop_words])
    # 2.7 Stemming (ví dụ running -> run, learners -> learn)
    stemmer = nltk.stem.SnowballStemmer('english')
    words = text.split()                     # <-- lấy token sau 2.6
    words = [stemmer.stem(w) for w in words] # <-- stem từng từ tiếng Anh
    text = ' '.join(words)                   # <-- ghép lại thành chuỗi
    return text
def _clean_batch(X):
    return np.array([clean_text(t) for t in X], dtype=object)