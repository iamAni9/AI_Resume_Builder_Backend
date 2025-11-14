from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from app.config.logger import get_logger
from app.services.pdf_parser import PDFParser
import tempfile
import traceback

# ==================== RESUME UPLOAD & PARSING ====================

router = APIRouter()
logger = get_logger("resume_route")
pdf_parser = PDFParser()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and parse an existing resume PDF
    
    Returns:
        Parsed resume data with extracted sections
    """
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', dir=UPLOAD_DIR) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        logger.info(f"File uploaded: {file.filename}")
        
        # Parse resume
        parsed_data = pdf_parser.parse_resume(tmp_path)
        
        # Clean up
        os.unlink(tmp_path)
        
        return {
            "status": "success",
            "message": "Resume parsed successfully",
            "data": parsed_data
        }
        
    except Exception as e:
        logger.error(f"Error uploading resume: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing resume: {str(e)}"
        )