from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
import pickle
from sklearn.preprocessing import FunctionTransformer
import numpy as np # Xử lí data 
import re # Xóa HTML
import os # Xử lí file
import pandas as pd # thư viện đọc file
from bs4 import BeautifulSoup               # Dùng để xóa HTML
import nltk
from nltk.corpus import stopwords     # Danh sách stopwords có sẵn
from typing import List, Union
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV, StratifiedKFold, learning_curve
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint
from sklearn.model_selection import cross_validate
from domain.domain import ReviewRequest, ReviewResponse
import numpy as np
from scipy import sparse
from service.text_preproc import _clean_batch  # hàm đúng như khi train
import __main__      
# gắn tên hàm vào __main__ để pickle tìm thấy
__main__._clean_batch = _clean_batch
LABEL_TEXT = {0: "negative", 1: "positive"}  # đổi nếu mapping khác

class ReviewService():
    def __init__(self):
        self.path_model = "artifacts/textclf.pkl"
        self.model = self.load_artifact(self.path_model)
    def load_artifact(self, path_to_artifact):
        '''Load a prediction artifact from a pickle file'''
        with open(path_to_artifact, "rb") as f:
            artifact = pickle.load(f)
        return artifact 
    def preprocess_input(self, request: ReviewRequest):
        return request.as_list()
    def _positive_col(self, positive_label=1) -> int:
        clf = getattr(self.model, "named_steps", {}).get("model", None) or self.model.steps[-1][1]
        classes_ = getattr(clf, "classes_", None)
        if classes_ is None: return 1
        if positive_label in classes_: return int(np.where(classes_ == positive_label)[0][0])
        if "positive" in classes_:    return int(np.where(classes_ == "positive")[0][0])
        return 1

    def predict_table(self, data):
    # chuẩn hoá X như trước...
        X = [data] if isinstance(data, str) else (data.as_list() if isinstance(data, ReviewRequest) else list(data))

        y = self.model.predict(X)
        # map về nhãn chữ, bỏ hẳn pred_id
        if np.issubdtype(np.array(y).dtype, np.number):
            labels = [LABEL_TEXT.get(int(i), str(i)) for i in y]
        else:
            labels = [str(i) for i in y]

        scores = None
        if hasattr(self.model, "predict_proba"):
            idx = self._positive_col(1)
            scores = self.model.predict_proba(X)[:, idx].astype(float)
        elif hasattr(self.model, "decision_function"):
            scores = np.ravel(self.model.decision_function(X)).astype(float)

        return pd.DataFrame({"review": X, "pred": labels, "score": scores})
