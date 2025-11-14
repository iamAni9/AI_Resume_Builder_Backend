from fastapi import APIRouter, Form, HTTPException
from typing import Optional
import traceback
from app.config.logger import get_logger
from app.services.ats_scorer import ATSScorer

# ==================== ATS SCORING ====================
router = APIRouter()
logger = get_logger("ats_route")
ats_scorer = ATSScorer()

@router.post("/api/calculate-ats-score")
async def calculate_ats_score(
    resume_text: Optional[str] = Form(None),
    job_description: Optional[str] = Form("")
):
    if not resume_text or resume_text.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Resume text cannot be empty"
        )
    logger.info(f"Received request to calculate ATS score, resume text : {resume_text}")
    try:
        logger.info("Calculating ATS score...")
        score_data = ats_scorer.calculate_ats_score(resume_text, job_description or "")
        
        return {
            "status": "success",
            "data": score_data
        }
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error calculating ATS score: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating ATS score: {str(e)}"
        )