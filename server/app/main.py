"""
APA Formatter API
FastAPI backend for the APA 7th Edition document formatter
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .routers import format

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="APA Formatter API",
    description="Transform messy documents into properly formatted APA 7th edition documents",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(format.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "APA Formatter API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
