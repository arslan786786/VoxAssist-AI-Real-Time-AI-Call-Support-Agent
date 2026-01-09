"""
Database models for VoxAssist AI
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Call(BaseModel):
    """Call model"""
    id: Optional[str] = None
    call_id: str
    caller_number: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    status: str = "active"  # active, ended, transferred
    sentiment: Optional[str] = None  # positive, neutral, negative, angry
    created_at: datetime = Field(default_factory=datetime.now)


class Conversation(BaseModel):
    """Conversation message model"""
    id: Optional[str] = None
    call_id: str
    speaker: str  # "user" or "assistant"
    message: str
    intent: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class FAQ(BaseModel):
    """FAQ model"""
    id: Optional[str] = None
    question: str
    answer: str
    category: Optional[str] = None
    frequency: int = 0
    embedding: Optional[list] = None  # Vector embedding for semantic search
    created_at: datetime = Field(default_factory=datetime.now)


class Agent(BaseModel):
    """Human agent model"""
    id: Optional[str] = None
    agent_id: str
    name: str
    status: str = "available"  # available, busy, offline
    specialization: Optional[str] = None
    current_calls: int = 0
    max_concurrent_calls: int = 3

