from fastapi import APIRouter, HTTPException
from app.config.logger import get_logger
from app.services.template_manager import TemplateManager

# ==================== TEMPLATES ====================

router = APIRouter()
logger = get_logger("template_route")
template_manager = TemplateManager()

@router.get("/api/templates")
async def get_templates():
    """
    Get list of available resume templates
    
    Returns:
        List of template names
    """
    try:
        templates = template_manager.list_available_templates()
        
        template_info = {
            "template1": {
                "name": "Professional",
                "description": "Clean and modern design for corporate roles"
            },
            "template2": {
                "name": "Creative",
                "description": "Eye-catching layout for creative industries"
            },
            "template3": {
                "name": "Academic",
                "description": "Structured format for research positions"
            }
        }
        
        return {
            "status": "success",
            "templates": templates,
            "details": template_info
        }
        
    except Exception as e:
        logger.error(f"Error getting templates: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
