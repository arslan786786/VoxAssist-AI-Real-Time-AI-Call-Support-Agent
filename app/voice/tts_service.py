"""
Text-to-Speech service
"""
import os
from typing import Optional, Dict, Any
import requests
from dotenv import load_dotenv

load_dotenv()


class TTSService:
    """Service for converting text to speech"""
    
    def __init__(self):
        self.provider = os.getenv("TTS_PROVIDER", "elevenlabs")  # elevenlabs, openai, playht
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.elevenlabs_voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    
    def synthesize_speech(
        self,
        text: str,
        voice_id: Optional[str] = None,
        language: Optional[str] = "en"
    ) -> Dict[str, Any]:
        """
        Convert text to speech audio
        
        Args:
            text: Text to convert
            voice_id: Optional voice ID (provider-specific)
            language: Language code
        
        Returns:
            Dict with audio data (base64 or bytes) and metadata
        """
        if self.provider == "elevenlabs":
            return self._elevenlabs_tts(text, voice_id)
        elif self.provider == "openai":
            return self._openai_tts(text, voice_id)
        else:
            return {
                "audio": None,
                "error": f"Unsupported TTS provider: {self.provider}",
                "success": False
            }
    
    def _elevenlabs_tts(self, text: str, voice_id: Optional[str] = None) -> Dict[str, any]:
        """
        Use ElevenLabs for TTS
        """
        if not self.elevenlabs_api_key:
            return {
                "audio": None,
                "error": "ELEVENLABS_API_KEY not configured",
                "success": False
            }
        
        voice_id = voice_id or self.elevenlabs_voice_id
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.elevenlabs_api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                return {
                    "audio": response.content,  # MP3 audio bytes
                    "format": "mp3",
                    "success": True
                }
            else:
                return {
                    "audio": None,
                    "error": f"ElevenLabs API error: {response.status_code}",
                    "success": False
                }
        except Exception as e:
            return {
                "audio": None,
                "error": str(e),
                "success": False
            }
    
    def _openai_tts(self, text: str, voice_id: Optional[str] = None) -> Dict[str, any]:
        """
        Use OpenAI TTS API
        """
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        voice = voice_id or "alloy"  # alloy, echo, fable, onyx, nova, shimmer
        
        try:
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            
            return {
                "audio": response.content,  # MP3 audio bytes
                "format": "mp3",
                "success": True
            }
        except Exception as e:
            return {
                "audio": None,
                "error": str(e),
                "success": False
            }

