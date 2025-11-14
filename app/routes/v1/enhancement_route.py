from fastapi import APIRouter, HTTPException
from typing import Optional
import json
import traceback
from app.config.logger import get_logger
from app.services.ai_enhancer import AIEnhancer
from app.services.ats_scorer import ATSScorer

# ==================== RESUME ENHANCEMENT ====================
router = APIRouter()
logger = get_logger("enhancement_route")
ai_enhancer = AIEnhancer()
ats_scorer = ATSScorer()

@router.post("/api/enhance-resume")
async def enhance_resume(
    resume_data: dict,
    job_description: Optional[str] = ""
):
    """
    Enhance resume content using AI
    
    Args:
        resume_data: Complete resume data dictionary
        job_description: Optional job description
    
    Returns:
        Enhanced resume data with ATS score comparison
    """
    
    if not resume_data:
        raise HTTPException(
            status_code=400,
            detail="Resume data is required"
        )
    
    try:
        logger.info("Enhancing resume with AI...")
        
        # Calculate original ATS score
        resume_text = json.dumps(resume_data)
        original_score_data = ats_scorer.calculate_ats_score(
            resume_text,
            job_description or ""
        )
        
        # Enhance resume
        enhanced_data = ai_enhancer.enhance_resume_content(
            resume_data,
            job_description or ""
        )
        
        # Calculate enhanced ATS score
        enhanced_text = json.dumps(enhanced_data)
        enhanced_score_data = ats_scorer.calculate_ats_score(
            enhanced_text,
            job_description or ""
        )
        
        # Compare scores
        improvements = ats_scorer.compare_scores(
            original_score_data['score'],
            enhanced_score_data['score']
        )
        
        logger.info(f"Resume enhanced. Original: {original_score_data['score']}, Enhanced: {enhanced_score_data['score']}")
        
        return {
            "status": "success",
            "data": {
                "enhanced_data": enhanced_data,
                "original_score": original_score_data['score'],
                "enhanced_score": enhanced_score_data['score'],
                "improvements": improvements,
                "suggestions": enhanced_score_data.get('suggestions', [])
            }
        }
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error enhancing resume: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error enhancing resume: {str(e)}"
        )
