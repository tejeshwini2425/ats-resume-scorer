import os

os.environ["HF_HUB_OFFLINE"] = "1"

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session



from .resume_parser import extract_resume_text
from .scoring import keyword_match_score, structure_score, semantic_similarity_score, compute_hybrid_score
from .database import engine, get_db, Base
from .models import ScoreResult

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "ATS Resume Scorer API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

async def process_uploaded_resume(file: UploadFile) -> str:
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported"
        )

    file_bytes = await file.read()

    try:
        return extract_resume_text(file.filename, file_bytes)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    extracted_text = await process_uploaded_resume(file)

    return {
        "filename": file.filename,
        "character_count": len(extracted_text),
        "preview": extracted_text[:300]
    }


@app.post("/score-resume")
async def score_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db)
):


    resume_text = await process_uploaded_resume(file)

    keyword_result = keyword_match_score(resume_text, job_description)
    structure_result = structure_score(resume_text)
    semantic_result = semantic_similarity_score(
        resume_text,
        job_description
    )

    hybrid_result = compute_hybrid_score(
        keyword_result,
        structure_result,
        semantic_result
    )

    score_record = ScoreResult(
    filename=file.filename,
    final_score=hybrid_result["final_score"],
    breakdown=hybrid_result["breakdown"],
    job_description=job_description
)

    db.add(score_record)
    db.commit()
    db.refresh(score_record)

    return {
        "filename": file.filename,
        "final_score": hybrid_result["final_score"],
        "breakdown": hybrid_result["breakdown"],
        "details": {
            "keyword_match": keyword_result,
            "structure": structure_result,
            "semantic_similarity": semantic_result
        }
    }

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    records = (
        db.query(ScoreResult)
        .order_by(ScoreResult.created_at.desc())
        .all()
    )

    return [
        {
            "id": r.id,
            "filename": r.filename,
            "final_score": r.final_score,
            "created_at": r.created_at
        }
        for r in records
    ]


@app.get("/score/{score_id}")
def get_score(score_id: int, db: Session = Depends(get_db)):
    record = (
        db.query(ScoreResult)
        .filter(ScoreResult.id == score_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Score not found"
        )

    return {
        "id": record.id,
        "filename": record.filename,
        "final_score": record.final_score,
        "breakdown": record.breakdown,
        "job_description": record.job_description,
        "created_at": record.created_at
    }