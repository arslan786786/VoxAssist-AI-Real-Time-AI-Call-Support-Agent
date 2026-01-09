"""
VoxAssist AI - Real-Time Call Support Agent
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import calls, faqs, transfers

app = FastAPI(
    title="VoxAssist AI - Real-Time Call Support Agent",
    description="AI-powered voice assistant for handling customer calls in real-time",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(calls.router)
app.include_router(faqs.router)
app.include_router(transfers.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "VoxAssist AI - Real-Time Call Support Agent",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "VoxAssist AI"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
