from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import traceback
from app.routes import register_routers
from app.config.logger import get_logger
from app.config.settings import settings

load_dotenv()
logger = get_logger("main")

# Initialize FastAPI app
app = FastAPI(
    title="AI Resume Builder API",
    description="API for building and optimizing ATS-friendly resumes with AI",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# CORS configuration
allowed_origins = [origin.strip() for origin in settings.FRONTEND_ORIGIN.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Register API routers
register_routers(app)

# ==================== ROOT ENDPOINTS ====================

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Resume Builder API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "gemini_ai": "ready",
            "pdf_parser": "ready",
            "document_generator": "ready"
        }
    }

# ==================== ERROR HANDLERS ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    logger.info(f"HTTP exception: {str(exc.detail)}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# if __name__ == "__main__":
#     import uvicorn
    
#     host = os.getenv("HOST", "0.0.0.0")
#     port = int(os.getenv("PORT", 8000))
#     debug = os.getenv("DEBUG", "False").lower() == "true"
    
#     logger.info(f"Starting server at {host}:{port}")
    
#     uvicorn.run(
#         "app.main:app",
#         host=host,
#         port=port,
#         reload=debug,
#         log_level="info"
#     )
