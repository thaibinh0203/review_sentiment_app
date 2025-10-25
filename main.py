from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from domain.domain import ReviewRequest
from service.review_service import ReviewService
import traceback, logging
review_app = FastAPI()

# health check
@review_app.get("/")
def health():
    return {"ok": True}

# load model 1 lần
svc = ReviewService()

# Trả JSON (mặc định dùng cho API)
@review_app.post("/predict")
def predict_review(request: ReviewRequest):
    df = svc.predict_table(request)
    return df.to_dict("records")

# (Tuỳ chọn) Trả HTML table để xem ngay trên trình duyệt
@review_app.post("/predict_html", response_class=HTMLResponse)
def predict_html(request: ReviewRequest):
    try:
        df = svc.predict_table(request)
        return df.to_html(index=False)
    except Exception:
        logger.exception("predict_html failed")
        return HTMLResponse(
            f"<pre>{traceback.format_exc()}</pre>",
            status_code=500,
        )
