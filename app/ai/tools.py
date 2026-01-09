"""
Tool definitions for LLM function calling
"""
from typing import Dict, Any, List


def get_tool_definitions() -> List[Dict[str, Any]]:
    """
    Define available tools for LLM function calling
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "get_business_hours",
                "description": "Get the business operating hours",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_job_openings",
                "description": "Fetch current job openings and positions available",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "department": {
                            "type": "string",
                            "description": "Filter by department (optional)"
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "book_appointment",
                "description": "Schedule an appointment for the caller",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "Preferred date (YYYY-MM-DD)"
                        },
                        "time": {
                            "type": "string",
                            "description": "Preferred time (HH:MM)"
                        },
                        "service": {
                            "type": "string",
                            "description": "Type of service needed"
                        }
                    },
                    "required": ["date", "time"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_faqs",
                "description": "Search frequently asked questions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "transfer_to_human",
                "description": "Transfer the call to a human agent",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reason": {
                            "type": "string",
                            "description": "Reason for transfer"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "normal", "high", "urgent"],
                            "description": "Transfer priority"
                        }
                    },
                    "required": []
                }
            }
        }
    ]


async def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a tool/function call
    """
    if tool_name == "get_business_hours":
        return {
            "hours": "Monday to Friday: 9 AM - 5 PM EST",
            "timezone": "EST"
        }
    
    elif tool_name == "get_job_openings":
        department = arguments.get("department")
        # In production, query database
        return {
            "openings": [
                {
                    "title": "Software Engineer",
                    "department": "Engineering",
                    "location": "Remote"
                }
            ],
            "department": department
        }
    
    elif tool_name == "book_appointment":
        # In production, call scheduling API
        return {
            "status": "success",
            "appointment_id": "apt_123",
            "date": arguments.get("date"),
            "time": arguments.get("time"),
            "message": "Appointment scheduled successfully"
        }
    
    elif tool_name == "search_faqs":
        query = arguments.get("query", "")
        # In production, use vector search
        return {
            "results": [
                {
                    "question": "Sample FAQ",
                    "answer": "Sample answer"
                }
            ]
        }
    
    elif tool_name == "transfer_to_human":
        return {
            "status": "transferring",
            "reason": arguments.get("reason", "User request"),
            "estimated_wait": 30
        }
    
    else:
        return {
            "error": f"Unknown tool: {tool_name}"
        }

