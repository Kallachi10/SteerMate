from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import create_tables
from routers import auth_router, user_router, trips_router, detection_router

# Import models to ensure they are registered with SQLAlchemy
import models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup: Create database tables
    await create_tables()
    yield
    # Shutdown: Cleanup if needed


app = FastAPI(
    title="SteerMate Backend",
    description="Backend API for SteerMate - Smartphone-based Driver Assistance System",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(trips_router)
app.include_router(detection_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "SteerMate Backend",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}