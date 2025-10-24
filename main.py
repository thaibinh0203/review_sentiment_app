from fastapi import FastAPI
from domain.domain import ReviewRequest
from service.review_service import ReviewService

review_app = FastAPI()

# tạo 1 instance, load model 1 lần
svc = ReviewService()

@review_app.post("/predict")
def predict_review(request: ReviewRequest):
    df = svc.predict_table(request)          # luôn trả DataFrame
    return df.to_dict("records")             # trả JSON cho FastAPI
