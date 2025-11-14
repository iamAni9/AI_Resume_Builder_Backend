from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
import traceback
from app.config.logger import get_logger
from app.services.document_generator import DocumentGenerator


# ==================== DOCUMENT GENERATION ====================

router = APIRouter()
logger = get_logger("generation_route")
doc_generator = DocumentGenerator()

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/api/generate-resume")
async def generate_resume(
    resume_data: dict,
    template: str = "template1",
    format: str = "docx"
):
    """
    Generate final resume document in DOCX or PDF format
    
    Args:
        resume_data: Complete resume data
        template: Template name (template1, template2, template3)
        format: Output format ('docx' or 'pdf')
    
    Returns:
        Generated resume file for download
    """
    
    if format not in ["docx", "pdf"]:
        raise HTTPException(
            status_code=400,
            detail="Format must be 'docx' or 'pdf'"
        )
    
    if not resume_data:
        raise HTTPException(
            status_code=400,
            detail="Resume data is required"
        )
    
    try:
        logger.info(f"Generating resume in {format.upper()} format...")
        
        output_filename = f"resume_{template}.{format}"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # Generate DOCX (always generated first)
        docx_path = output_path.replace('.pdf', '.docx') if format == 'pdf' else output_path
        doc_generator.generate_docx(resume_data, docx_path)
        logger.info(f"DOCX generated: {docx_path}")
        
        if format == "pdf":
            # Try to convert to PDF
            pdf_result = doc_generator.generate_pdf_from_docx(docx_path, output_path)
            if pdf_result is None:
                logger.warning("PDF conversion failed, returning DOCX instead")
                output_path = docx_path
                output_filename = output_filename.replace('.pdf', '.docx')
        
        # Return file
        return FileResponse(
            output_path,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document' if format == 'docx' else 'application/pdf',
            filename=output_filename,
            headers={"Content-Disposition": f"attachment; filename={output_filename}"}
        )
        
    except Exception as e:
        logger.error(f"Error generating resume: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error generating resume: {str(e)}"
        )

