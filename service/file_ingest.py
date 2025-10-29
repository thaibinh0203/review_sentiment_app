
import io, re
import pandas as pd

TEXT_ALIASES = ("text", "review", "content", "comment", "message")

def _choose_text_col(df: pd.DataFrame, stt_key: str | None) -> str | None:
    # Ưu tiên theo alias
    lower_map = {c.replace("\ufeff", "").strip().lower(): c for c in df.columns}
    for k in TEXT_ALIASES:
        if k in lower_map:
            return lower_map[k]
    # Nếu có 'stt', lấy cột đầu khác 'stt'
    if stt_key:
        for c in df.columns:
            if c != stt_key:
                return c
    # Fallback: cột đầu
    return df.columns[0] if len(df.columns) else None

def _looks_invalid_text(series: pd.Series) -> bool:
    """'Xấu' nếu đa số là số/rỗng (không phải câu chữ)."""
    s = series.astype(str).str.strip()
    if s.empty:
        return True
    frac_bad = ((s == "") | s.str.fullmatch(r"\d+")).mean()
    return frac_bad >= 0.6

# ---------- TXT ----------
def parse_txt_bytes(b: bytes, encoding: str = "utf-8") -> list[tuple[str, str]]:
    s = b.decode(encoding, errors="ignore")
    lines = [ln.strip() for ln in s.splitlines() if ln.strip()]
    if not lines:
        return []
    # Header kiểu: "stt text" hoặc "stt review"
    if re.match(r"^stt(\s+|\t+)(text|review)\b", lines[0], flags=re.I):
        rows: list[tuple[str, str]] = []
        for ln in lines[1:]:
            m = re.match(r"^(\d+)\s+(.+)$", ln)
            if m:
                rows.append((m.group(1), m.group(2).strip().strip('"')))
        return rows
    # Mặc định: mỗi dòng là 1 review → tự gán stt
    return [(str(i + 1), ln) for i, ln in enumerate(lines)]

# ---------- CSV ----------
def parse_csv_bytes(b: bytes) -> list[tuple[str, str]]:
    # Sniff sep: auto -> ',' -> ';' -> whitespace
    for sep_try in [None, ",", ";", r"\s+"]:
        try:
            df = pd.read_csv(io.BytesIO(b), sep=sep_try, engine="python")
            if df.shape[1] >= 1:
                break
        except Exception:
            continue

    # Chuẩn hoá header (strip + remove BOM)
    df.columns = [c.replace("\ufeff", "").strip() for c in df.columns]
    lower_map = {c.lower(): c for c in df.columns}

    stt_key = lower_map.get("stt")
    txt_key = _choose_text_col(df, stt_key)

    if stt_key and txt_key:
        s_stt = df[stt_key]
        s_txt = df[txt_key]
        if _looks_invalid_text(s_txt):
            for c in df.columns:
                if c != stt_key and not _looks_invalid_text(df[c]):
                    txt_key = c
                    s_txt = df[c]
                    break
        sub = pd.DataFrame({"stt": s_stt, "text": s_txt}).dropna()
        return [(str(r["stt"]).strip(), str(r["text"]).strip()) for _, r in sub.iterrows()]

    # Không có 'stt' → coi cột văn bản là txt_key, tự gán stt
    if txt_key:
        texts = df[txt_key].dropna().astype(str).str.strip().tolist()
        return [(str(i + 1), t) for i, t in enumerate(texts)]

    return []

# ---------- XLSX ----------
def parse_xlsx_bytes(b: bytes) -> list[tuple[str, str]]:
    df = pd.read_excel(io.BytesIO(b))
    df.columns = [c.replace("\ufeff", "").strip() for c in df.columns]
    lower_map = {c.lower(): c for c in df.columns}

    stt_key = lower_map.get("stt")
    txt_key = _choose_text_col(df, stt_key)

    if stt_key and txt_key:
        s_stt = df[stt_key]
        s_txt = df[txt_key]
        if _looks_invalid_text(s_txt):
            for c in df.columns:
                if c != stt_key and not _looks_invalid_text(df[c]):
                    txt_key = c
                    s_txt = df[c]
                    break
        sub = pd.DataFrame({"stt": s_stt, "text": s_txt}).dropna()
        return [(str(r["stt"]).strip(), str(r["text"]).strip()) for _, r in sub.iterrows()]

    if txt_key:
        texts = df[txt_key].dropna().astype(str).str.strip().tolist()
        return [(str(i + 1), t) for i, t in enumerate(texts)]

    return []