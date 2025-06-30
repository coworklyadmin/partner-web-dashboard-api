"""Main FastAPI application."""

import logging
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .services.auth import initialize_firebase
from .api import spaces_router, posts_router, features_router, health_router, dashboard_metrics_router
from .utils.config import settings

# Initialize Firebase
initialize_firebase()

# Create FastAPI app
app = FastAPI(
    title="CoWorkly Partner Dashboard API",
    version="1.0.0",
    description="API for CoWorkly Partner Dashboard",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f"Request validation error: {exc.errors()}")
    logging.error(f"Request body: {exc.body}")
    logging.error(f"Request method: {request.method}")
    logging.error(f"Request URL: {request.url}")
    logging.error(f"Request headers: {dict(request.headers)}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.error(f"General exception: {str(exc)}")
    logging.error(f"Exception type: {type(exc)}")
    logging.error(f"Request method: {request.method}")
    logging.error(f"Request URL: {request.url}")
    import traceback
    logging.error(f"Traceback: {traceback.format_exc()}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": f"Internal server error: {str(exc)}"}),
    )

# Include routers
app.include_router(spaces_router)
app.include_router(posts_router)
app.include_router(features_router)
app.include_router(health_router)
app.include_router(dashboard_metrics_router) 