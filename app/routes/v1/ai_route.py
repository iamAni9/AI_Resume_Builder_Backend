from fastapi import APIRouter, HTTPException, Form
from app.config.logger import get_logger
from app.services.ai_enhancer import AIEnhancer

# ==================== AI FEATURES ====================

router = APIRouter()
logger = get_logger("ai_route")
ai_enhancer = AIEnhancer()

@router.post("/api/generate-summary")
async def generate_summary(resume_data: dict):
    """
    Generate professional summary using AI
    
    Args:
        resume_data: Resume data for generating summary
    
    Returns:
        Generated professional summary
    """
    
    if not resume_data:
        raise HTTPException(
            status_code=400,
            detail="Resume data is required"
        )
    
    try:
        logger.info("Generating professional summary...")
        summary = ai_enhancer.generate_summary(resume_data)
        
        return {
            "status": "success",
            "summary": summary
        }
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/api/enhance-bullet-points")
async def enhance_bullet_points(bullet_points: list):
    """
    Enhance bullet points for better impact
    
    Args:
        bullet_points: List of bullet points to enhance
    
    Returns:
        Enhanced bullet points
    """
    
    if not bullet_points or not isinstance(bullet_points, list):
        raise HTTPException(
            status_code=400,
            detail="bullet_points must be a non-empty list"
        )
    
    try:
        logger.info("Enhancing bullet points...")
        enhanced = ai_enhancer.enhance_bullet_points(bullet_points)
        
        return {
            "status": "success",
            "enhanced_points": enhanced
        }
        
    except Exception as e:
        logger.error(f"Error enhancing bullet points: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/api/suggest-improvements")
async def suggest_improvements(resume_text: str = Form(...)):
    """
    Get improvement suggestions for resume
    
    Args:
        resume_text: Resume text to analyze
    
    Returns:
        List of improvement suggestions
    """
    
    if not resume_text or resume_text.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Resume text cannot be empty"
        )
    
    try:
        logger.info("Generating improvement suggestions...")
        suggestions = ai_enhancer.suggest_improvements(resume_text)
        
        return {
            "status": "success",
            "suggestions": suggestions
        }
        
    except Exception as e:
        logger.error(f"Error generating suggestions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )