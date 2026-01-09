"""
Speech-to-Text service
"""
import os
from typing import Optional, BinaryIO, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class STTService:
    """Service for converting speech to text"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "whisper-1"
    
    def transcribe_audio(
        self,
        audio_file: BinaryIO,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transcribe audio to text using Whisper API
        
        Args:
            audio_file: Audio file (mp3, wav, etc.)
            language: Optional language code (e.g., 'en', 'es')
        
        Returns:
            Dict with transcribed text and metadata
        """
        try:
            transcript = self.client.audio.transcriptions.create(
                model=self.model,
                file=audio_file,
                language=language
            )
            
            return {
                "text": transcript.text,
                "language": transcript.language if hasattr(transcript, 'language') else language,
                "success": True
            }
        
        except Exception as e:
            return {
                "text": "",
                "error": str(e),
                "success": False
            }
    
    def transcribe_audio_url(self, audio_url: str) -> Dict[str, Any]:
        """
        Transcribe audio from URL
        """
        # In production, download audio and process
        # For now, placeholder
        return {
            "text": "",
            "error": "URL transcription not implemented",
            "success": False
        }

