from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import os

app = FastAPI(title="Interactive App", description="Simple interactive application for DevOps deployment")

class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str
    status: str = "success"

# Health check endpoint
@app.get("/healthz")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for Kubernetes liveness and readiness probes"""
    return {"status": "healthy", "service": "interactive-app"}

# Submit message endpoint
@app.post("/api/submit", response_model=MessageResponse)
async def submit_message(request: MessageRequest) -> MessageResponse:
    """Accept a message and return a formatted response"""
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    response_text = f"Received: {request.message}"
    return MessageResponse(response=response_text)

# Get app info
@app.get("/api/info")
async def get_app_info() -> Dict[str, Any]:
    """Return application information"""
    return {
        "app": "Interactive DevOps Application",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "endpoints": ["/healthz", "/api/submit", "/api/info"]
    }

# Mount static files (frontend)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve the main HTML file at root
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    with open("frontend/index.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)