from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes.farmer_mock import router as farmer_router
from routes.auth import router as auth_router
from utils.logger import logger
from utils.exceptions import CarbonSakthiException

app = FastAPI(
    title=settings.app_name,
    description="Backend API for CarbonSakthi AI platform - Sustainable farming and carbon credit management",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix=f"{settings.api_v1_str}/auth", tags=["Authentication"])
app.include_router(farmer_router, prefix=settings.api_v1_str, tags=["Farmers"])

@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": f"Welcome to {settings.app_name} API",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "api_prefix": settings.api_v1_str,
        "endpoints": {
            "authentication": f"{settings.api_v1_str}/auth",
            "farmers": f"{settings.api_v1_str}/farmer"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version
    }

# Exception handlers
@app.exception_handler(CarbonSakthiException)
async def carbonsakthi_exception_handler(request, exc: CarbonSakthiException):
    logger.error(f"CarbonSakthiException: {exc.message}")
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.message,
            "details": exc.details
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=500,
        content="Internal server error"
    )

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
