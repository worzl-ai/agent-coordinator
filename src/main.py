"""
Enterprise Agent Coordinator - Main Application
A sophisticated orchestration system for managing distributed AI agents
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import logging
import time
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import asyncio
import uuid

from .coordinator import AgentCoordinator
from .auth import get_current_user, User
from .models import (
    CoordinationRequest, 
    CoordinationResponse, 
    AgentStatus, 
    SystemHealth,
    QualityMetrics,
    CoordinationRequestWithClient,
    CoordinationResponseWithClient
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Enterprise Agent Coordinator",
    description="Sophisticated orchestration system for distributed AI agents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the coordinator
coordinator = AgentCoordinator()

@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    logger.info("Starting Enterprise Agent Coordinator...")
    await coordinator.initialize()
    logger.info("Agent Coordinator initialized successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Agent Coordinator...")
    await coordinator.shutdown()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Health check endpoints
@app.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/health/detailed", response_model=SystemHealth)
async def detailed_health_check():
    """Detailed system health check"""
    return await coordinator.get_system_health()

# Main coordination endpoints
@app.post("/coordinate", response_model=CoordinationResponse)
async def coordinate_request(
    request: CoordinationRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Main coordination endpoint - routes requests to appropriate agents
    Implements 2-second routing decision SLA
    """
    try:
        start_time = time.time()
        
        # Log the request
        logger.info(f"Coordination request from user {current_user.email}: {request.query[:100]}...")
        
        # Process the request through the coordinator
        response = await coordinator.process_request(request, current_user)
        
        # Check SLA compliance
        processing_time = time.time() - start_time
        if processing_time > 2.0:
            logger.warning(f"SLA violation: Request took {processing_time:.2f}s (>2s)")
        
        return response
        
    except Exception as e:
        logger.error(f"Coordination error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Coordination failed: {str(e)}")

# CLIENT-AWARE COORDINATION ENDPOINTS

@app.post("/coordinate/client", response_model=CoordinationResponseWithClient)
async def coordinate_request_with_client(
    request: CoordinationRequestWithClient,
    current_user: User = Depends(get_current_user)
):
    """
    Client-aware coordination endpoint
    Processes requests with optional client context integration
    """
    try:
        start_time = time.time()
        
        logger.info(f"Client-aware coordination request from {current_user.email} for client {request.client_id}")
        
        # Process with client context
        response = await coordinator.process_request_with_client(request, current_user)
        
        # Check SLA compliance
        processing_time = time.time() - start_time
        if processing_time > 2.0:
            logger.warning(f"SLA violation: Client request took {processing_time:.2f}s")
        
        return response
        
    except Exception as e:
        logger.error(f"Client coordination error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Client coordination failed: {str(e)}")

@app.get("/clients/{client_id}/context")
async def get_client_context_preview(
    client_id: str,
    current_user: User = Depends(get_current_user)
):
    """Preview what client context would be available"""
    try:
        context = await coordinator._get_client_context(client_id, current_user)
        if not context:
            raise HTTPException(status_code=404, detail="Client not found or access denied")
        
        return {
            "client_id": context.client_id,
            "has_brand_voice": context.brand_voice is not None,
            "has_target_audience": context.target_audience is not None,
            "compliance_requirements_count": len(context.compliance_notes or []),
            "preview": {
                "brand_tone": context.brand_voice.get("tone") if context.brand_voice else None,
                "primary_audience": context.target_audience.get("primary_audience") if context.target_audience else None,
                "compliance_summary": context.compliance_notes[:3] if context.compliance_notes else []
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving client context: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve client context")

@app.get("/clients")
async def list_accessible_clients(
    current_user: User = Depends(get_current_user)
):
    """List client IDs accessible to the current user"""
    try:
        from .client_storage import client_storage_service
        client_ids = await client_storage_service.list_client_ids(current_user.user_id)
        return {
            "client_ids": client_ids,
            "count": len(client_ids),
            "user_id": current_user.user_id
        }
    except Exception as e:
        logger.error(f"Error listing clients: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list accessible clients")

@app.get("/agents/status", response_model=List[AgentStatus])
async def get_agent_status(current_user: User = Depends(get_current_user)):
    """Get status of all agents in the system"""
    return await coordinator.get_agent_status()

@app.get("/agents/{agent_id}/status", response_model=AgentStatus)
async def get_specific_agent_status(
    agent_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get status of a specific agent"""
    status = await coordinator.get_agent_status(agent_id)
    if not status:
        raise HTTPException(status_code=404, detail="Agent not found")
    return status

# Quality and performance endpoints
@app.get("/metrics/quality", response_model=QualityMetrics)
async def get_quality_metrics(current_user: User = Depends(get_current_user)):
    """Get system quality metrics"""
    return await coordinator.get_quality_metrics()

@app.get("/metrics/performance")
async def get_performance_metrics(current_user: User = Depends(get_current_user)):
    """Get detailed performance metrics"""
    return await coordinator.get_performance_metrics()

# Admin endpoints
@app.post("/admin/agents/{agent_id}/restart")
async def restart_agent(
    agent_id: str,
    current_user: User = Depends(get_current_user)
):
    """Restart a specific agent (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    result = await coordinator.restart_agent(agent_id)
    return {"message": f"Agent {agent_id} restart initiated", "success": result}

@app.post("/admin/system/maintenance")
async def enter_maintenance_mode(
    current_user: User = Depends(get_current_user)
):
    """Enter system maintenance mode (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    await coordinator.enter_maintenance_mode()
    return {"message": "System entering maintenance mode"}

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with proper logging"""
    logger.error(f"HTTP error {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "timestamp": datetime.utcnow().isoformat()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
