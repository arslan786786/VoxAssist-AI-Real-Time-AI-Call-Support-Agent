"""
LLM service for AI responses and intent understanding
"""
import os
from typing import Dict, List, Optional, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMService:
    """Service for interacting with LLM (OpenAI GPT)"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.system_prompt = self._load_system_prompt()
    
    def _load_system_prompt(self) -> str:
        """
        Load the system prompt for the AI agent
        """
        try:
            with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            # Default prompt if file doesn't exist
            return """You are VoxAssist AI, a polite and professional call support agent.
Your goals:
- Answer clearly and concisely
- Be helpful and empathetic
- Ask follow-up questions if needed
- Escalate to a human if unsure or if the user is upset
- Never hallucinate or make up information
- Use tools when required to fetch real data

Keep responses brief and natural for voice conversation."""
    
    def generate_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        context: Optional[Dict[str, Any]] = None,
        tools: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Generate AI response using LLM
        
        Args:
            user_message: Current user message
            conversation_history: Previous messages in format [{"role": "user/assistant", "content": "..."}]
            context: Additional context (call_id, caller_info, etc.)
            tools: Available tools/functions for the LLM to call
        
        Returns:
            Dict with response text, intent, and other metadata
        """
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add context if provided
        if context:
            context_str = f"Call context: {context}"
            messages.append({"role": "system", "content": context_str})
        
        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=200,  # Keep responses brief for voice
                tools=tools if tools else None
            )
            
            assistant_message = response.choices[0].message
            
            return {
                "text": assistant_message.content,
                "intent": None,  # Would be extracted from response
                "requires_tool": assistant_message.tool_calls is not None,
                "tool_calls": assistant_message.tool_calls if assistant_message.tool_calls else []
            }
        
        except Exception as e:
            # Fallback response on error
            return {
                "text": "I apologize, but I'm having trouble processing that. Let me transfer you to a human agent.",
                "intent": "transfer",
                "error": str(e),
                "requires_tool": False
            }
    
    def detect_intent_advanced(self, text: str) -> Dict[str, Any]:
        """
        Use LLM to detect intent with better accuracy
        """
        prompt = f"""Analyze this user message and determine the intent.

Message: "{text}"

Respond with JSON:
{{
    "intent": "business_hours|appointment_booking|job_inquiry|complaint|faq|transfer|unknown",
    "confidence": 0.0-1.0,
    "entities": {{}},
    "sentiment": "positive|neutral|negative"
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an intent classification system. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
        
        except Exception as e:
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "entities": {},
                "sentiment": "neutral",
                "error": str(e)
            }

