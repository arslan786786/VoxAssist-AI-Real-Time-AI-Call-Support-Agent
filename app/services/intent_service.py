"""
Intent detection and classification service
"""
from typing import Dict, List, Optional
from enum import Enum


class IntentType(str, Enum):
    """Common intent types"""
    BUSINESS_HOURS = "business_hours"
    APPOINTMENT_BOOKING = "appointment_booking"
    JOB_INQUIRY = "job_inquiry"
    COMPLAINT = "complaint"
    FAQ = "faq"
    TRANSFER = "transfer"
    UNKNOWN = "unknown"
    GREETING = "greeting"
    GOODBYE = "goodbye"


class IntentService:
    """Service for detecting and classifying user intents"""
    
    def __init__(self):
        # Intent keywords mapping (in production, use ML model)
        self.intent_keywords: Dict[IntentType, List[str]] = {
            IntentType.BUSINESS_HOURS: [
                "hours", "open", "close", "when", "time", "available"
            ],
            IntentType.APPOINTMENT_BOOKING: [
                "appointment", "schedule", "book", "reserve", "meeting"
            ],
            IntentType.JOB_INQUIRY: [
                "job", "career", "position", "hiring", "apply", "employment"
            ],
            IntentType.COMPLAINT: [
                "complaint", "problem", "issue", "wrong", "bad", "angry", "upset"
            ],
            IntentType.FAQ: [
                "what", "how", "why", "where", "question", "tell me"
            ],
            IntentType.TRANSFER: [
                "human", "agent", "person", "speak to", "transfer"
            ],
            IntentType.GREETING: [
                "hello", "hi", "hey", "good morning", "good afternoon"
            ],
            IntentType.GOODBYE: [
                "bye", "goodbye", "thanks", "thank you", "see you"
            ]
        }
    
    def detect_intent(self, text: str) -> Dict[str, any]:
        """
        Detect intent from user text
        Returns intent type and confidence score
        """
        text_lower = text.lower()
        
        # Simple keyword matching (in production, use LLM or ML model)
        intent_scores: Dict[IntentType, int] = {}
        
        for intent_type, keywords in self.intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                intent_scores[intent_type] = score
        
        if not intent_scores:
            return {
                "intent": IntentType.UNKNOWN,
                "confidence": 0.0,
                "requires_clarification": True
            }
        
        # Get intent with highest score
        detected_intent = max(intent_scores.items(), key=lambda x: x[1])
        confidence = min(detected_intent[1] / 3.0, 1.0)  # Normalize to 0-1
        
        return {
            "intent": detected_intent[0].value,
            "confidence": confidence,
            "requires_clarification": confidence < 0.5
        }
    
    def should_escalate(self, intent: str, sentiment: Optional[str] = None) -> bool:
        """
        Determine if call should be escalated to human
        """
        escalation_intents = [
            IntentType.COMPLAINT,
            IntentType.TRANSFER
        ]
        
        if intent in [e.value for e in escalation_intents]:
            return True
        
        if sentiment in ["angry", "frustrated", "upset"]:
            return True
        
        return False

