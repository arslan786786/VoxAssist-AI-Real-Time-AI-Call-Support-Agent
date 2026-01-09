"""
Database connection and operations
"""
import os
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# In production, use actual database connections
# For now, using in-memory storage as placeholder


class Database:
    """Database service (placeholder - implement with PostgreSQL/MongoDB)"""
    
    def __init__(self):
        self.db_type = os.getenv("DATABASE_TYPE", "memory")  # memory, postgresql, mongodb
        # In-memory storage for development
        self.calls: Dict[str, Dict] = {}
        self.conversations: List[Dict] = []
        self.faqs: List[Dict] = []
        self.agents: Dict[str, Dict] = {}
    
    def save_call(self, call_data: Dict[str, Any]) -> str:
        """Save call to database"""
        call_id = call_data.get("call_id")
        if call_id:
            self.calls[call_id] = call_data
        return call_id
    
    def get_call(self, call_id: str) -> Optional[Dict[str, Any]]:
        """Get call by ID"""
        return self.calls.get(call_id)
    
    def update_call(self, call_id: str, updates: Dict[str, Any]):
        """Update call data"""
        if call_id in self.calls:
            self.calls[call_id].update(updates)
    
    def save_conversation(self, conversation_data: Dict[str, Any]) -> str:
        """Save conversation message"""
        self.conversations.append(conversation_data)
        return conversation_data.get("id", "conv_1")
    
    def get_conversations(self, call_id: str) -> List[Dict[str, Any]]:
        """Get all conversations for a call"""
        return [c for c in self.conversations if c.get("call_id") == call_id]
    
    def save_faq(self, faq_data: Dict[str, Any]) -> str:
        """Save FAQ"""
        self.faqs.append(faq_data)
        return faq_data.get("id", "faq_1")
    
    def search_faqs(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search FAQs (simple keyword search - use vector search in production)"""
        results = []
        query_lower = query.lower()
        
        for faq in self.faqs:
            if query_lower in faq.get("question", "").lower() or query_lower in faq.get("answer", "").lower():
                results.append(faq)
                if len(results) >= limit:
                    break
        
        return results
    
    def get_available_agents(self) -> List[Dict[str, Any]]:
        """Get available agents"""
        return [
            agent for agent in self.agents.values()
            if agent.get("status") == "available"
        ]


# Global database instance
db = Database()

