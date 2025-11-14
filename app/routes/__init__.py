from fastapi import FastAPI
from .v1.ats_route import router as ats_router
from .v1.resume_route import router as resume_router
from .v1.template_route import router as template_router
from .v1.enhancement_route import router as enhancement_router
from .v1.generation_route import router as generation_router
from .v1.ai_route import router as ai_router

def register_routers(app: FastAPI):
    app.include_router(ats_router, prefix="/v1")
    app.include_router(resume_router, prefix="/v1")
    app.include_router(template_router, prefix="/v1")
    app.include_router(enhancement_router, prefix="/v1")
    app.include_router(generation_router, prefix="/v1")
    app.include_router(ai_router, prefix="/v1")
    
