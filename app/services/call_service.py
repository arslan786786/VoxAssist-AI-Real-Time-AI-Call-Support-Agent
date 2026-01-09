"""
Call management service
"""
from typing import Optional, Dict, Any
from datetime import datetime
import uuid


class CallService:
    """Service for managing call sessions"""
    
    def __init__(self):
        # In production, this would use a database
        self.active_calls: Dict[str, Dict[str, Any]] = {}
    
    def start_call(
        self,
        caller_number: str,
        call_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Initialize a new call session
        """
        call_id = call_id or f"call_{uuid.uuid4().hex[:12]}"
        
        call_data = {
            "call_id": call_id,
            "caller_number": caller_number,
            "start_time": datetime.now(),
            "status": "active",
            "messages": [],
            "intents": [],
            "sentiment": None
        }
        
        self.active_calls[call_id] = call_data
        return call_data
    
    def end_call(
        self,
        call_id: str,
        duration: Optional[float] = None,
        sentiment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        End a call session
        """
        if call_id not in self.active_calls:
            raise ValueError(f"Call {call_id} not found")
        
        call_data = self.active_calls[call_id]
        call_data["status"] = "ended"
        call_data["end_time"] = datetime.now()
        call_data["sentiment"] = sentiment
        
        if duration:
            call_data["duration"] = duration
        else:
            delta = call_data["end_time"] - call_data["start_time"]
            call_data["duration"] = delta.total_seconds()
        
        # In production, save to database before removing from active calls
        result = call_data.copy()
        del self.active_calls[call_id]
        
        return result
    
    def get_call(self, call_id: str) -> Optional[Dict[str, Any]]:
        """
        Get call information
        """
        return self.active_calls.get(call_id)
    
    def add_message(
        self,
        call_id: str,
        speaker: str,
        message: str,
        intent: Optional[str] = None
    ):
        """
        Add a message to the call conversation
        """
        if call_id not in self.active_calls:
            raise ValueError(f"Call {call_id} not found")
        
        message_data = {
            "speaker": speaker,  # "user" or "assistant"
            "message": message,
            "timestamp": datetime.now(),
            "intent": intent
        }
        
        self.active_calls[call_id]["messages"].append(message_data)
        
        if intent:
            self.active_calls[call_id]["intents"].append(intent)
    
    def update_sentiment(self, call_id: str, sentiment: str):
        """
        Update call sentiment
        """
        if call_id not in self.active_calls:
            raise ValueError(f"Call {call_id} not found")
        
        self.active_calls[call_id]["sentiment"] = sentiment

