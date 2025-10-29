from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from domain.domain import ReviewRequest
from service.review_service import ReviewService
from service.file_ingest import parse_txt_bytes, parse_csv_bytes, parse_xlsx_bytes
import traceback
import logging

review_app = FastAPI(title="Review Sentiment API")

# Logger của Uvicorn (in chắc chắn ra console khi có lỗi)
logger = logging.getLogger("uvicorn.error")

# CORS (để Swagger/FE gọi OK)
review_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # đổi thành domain FE của bạn nếu cần
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Health check ----
@review_app.get("/")
def health():
    return {"ok": True}

# ---- Load model 1 lần ----
svc = ReviewService()  # mặc định artifacts/textclf.pkl

# ---- API: JSON (body theo ReviewRequest) ----
@review_app.post("/predict")
def predict_review(request: ReviewRequest):
    df = svc.predict_table(request)  # trả review, pred, score (tùy bạn giữ hay tối giản)
    return df.to_dict("records")

# ---- Upload file TXT/CSV/XLSX → trả stt, pred, score ----
ALLOWED_TYPES = {
    "text/plain": "txt",
    "text/csv": "csv",
    "application/vnd.ms-excel": "csv",  # đôi khi .csv gửi kiểu này
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
}
MAX_BYTES = 10 * 1024 * 1024  # 10MB

@review_app.post("/predict_file")
async def predict_file(file: UploadFile = File(...)):
    ctype = (file.content_type or "").lower()
    kind = ALLOWED_TYPES.get(ctype)
    if not kind:
        raise HTTPException(status_code=415, detail=f"Unsupported file type: {ctype}")

    blob = await file.read()
    if len(blob) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="File too large (>10MB)")

    try:
        if kind == "txt":
            rows = parse_txt_bytes(blob)       # list[(stt, text)] – auto stt 1..n nếu không có
        elif kind == "csv":
            rows = parse_csv_bytes(blob)       # chấp nhận header: stt + text/review/...
        else:  # xlsx
            rows = parse_xlsx_bytes(blob)      # chấp nhận header: stt + text/review/...
    except Exception as e:
        logger.exception("parse file failed")
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {e}")

    if not rows:
        raise HTTPException(status_code=400, detail="No text found")

    # “Cầu chì”: nếu lỡ parser trả list[str], chuyển thành (stt, text)
    if rows and isinstance(rows[0], str):
        rows = [(str(i + 1), t) for i, t in enumerate(rows)]

    # CHỈ trả về pred + score (xác suất positive)
    df = svc.predict_stt_pred_score(rows)

    return {"ok": True, "n": len(df), "items": df.to_dict(orient="records")}
