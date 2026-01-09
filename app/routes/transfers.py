"""
Human agent transfer routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/human", tags=["transfers"])


class TransferRequest(BaseModel):
    call_id: str
    reason: Optional[str] = None
    priority: Optional[str] = "normal"  # low, normal, high, urgent
    agent_id: Optional[str] = None


class TransferResponse(BaseModel):
    status: str
    call_id: str
    transfer_id: str
    agent_id: Optional[str] = None
    estimated_wait_time: Optional[int] = None
    message: str


@router.post("/transfer")
async def transfer_to_human(request: TransferRequest):
    """
    Transfer a call to a human agent
    """
    try:
        # In production, this would:
        # 1. Find an available agent
        # 2. Create a transfer record
        # 3. Route the call to the agent's phone/extension
        # 4. Update call status
        
        transfer_id = f"transfer_{datetime.now().timestamp()}"
        
        return TransferResponse(
            status="success",
            call_id=request.call_id,
            transfer_id=transfer_id,
            agent_id=request.agent_id or "agent_001",
            estimated_wait_time=30,  # seconds
            message=f"Call {request.call_id} transferred to human agent. Reason: {request.reason or 'User request'}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/available")
async def get_available_agents():
    """
    Get list of available human agents
    """
    # Placeholder - would query agent availability from database
    return {
        "agents": [
            {
                "agent_id": "agent_001",
                "name": "Sarah Johnson",
                "status": "available",
                "specialization": "technical_support"
            },
            {
                "agent_id": "agent_002",
                "name": "Mike Chen",
                "status": "available",
                "specialization": "sales"
            }
        ],
        "count": 2
    }


@router.post("/escalate")
async def escalate_call(request: TransferRequest):
    """
    Escalate a call (high priority transfer)
    """
    request.priority = "urgent"
    return await transfer_to_human(request)

