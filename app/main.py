from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles # 프론트 화면을 브라우저에 보여주기 위해 필요
from fastapi.responses import FileResponse
from pydantic import BaseModel # DTO 같은거
from pathlib import Path

from app.services.ai_service import tailor_resume # 라우트(main.py)와 로직(ai_service.py)을 분리

app = FastAPI(title="AI Resume Tailoring Assistant") # 앱 객체 생성 / Swagger 문서

# ── Static files ──────────────────────────────────────────────────────────────
STATIC_DIR = Path(__file__).parent / "static" # __file__ = 현재 python 파일 경로
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# app.mount(): FastAPI에서 특정 경로를 외부 파일 폴더와 연결

# ── Schemas ───────────────────────────────────────────────────────────────────
class TailorRequest(BaseModel):
    job_description: str
    resume: str
    instruction: str = "" # 문자열인데, 기본값은 빈 문자열


class KeywordsResult(BaseModel):
    matched: list[str]
    missing: list[str]


class ExperienceItem(BaseModel):
    company: str
    title: str
    bullets: list[str]


class TailorResponse(BaseModel):
    keywords: KeywordsResult
    summary: str
    skills: list[str]
    experience: list[ExperienceItem]


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return FileResponse(str(STATIC_DIR / "index.html"))

# async: 비동기 함수, await를 쓸 수 있는 함수

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/tailor", response_model=TailorResponse)
async def tailor(request: TailorRequest):
    if not request.job_description.strip() or len(request.job_description.strip()) < 50:
        raise HTTPException(status_code=400,
                            detail="Job description is too short. Please paste the full job description.")
    if not request.resume.strip() or len(request.resume.strip()) < 50:
        raise HTTPException(status_code=400, detail="Resume is too short. Please paste your full resume.")

    try:
        result = await tailor_resume(
            job_description=request.job_description,
            resume=request.resume,
            instruction=request.instruction,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
