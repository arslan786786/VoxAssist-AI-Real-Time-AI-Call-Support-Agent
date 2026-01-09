# VoxAssist AI - Setup Guide

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file** (copy from template below)
   ```bash
   # Create .env file with your API keys
   ```

3. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## Environment Variables (.env)

Create a `.env` file in the root directory with:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o

# Vapi Configuration (for voice calls)
VAPI_API_KEY=your_vapi_api_key_here

# Twilio Configuration (alternative to Vapi)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# ElevenLabs Configuration (TTS)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM

# TTS Provider (elevenlabs, openai, playht)
TTS_PROVIDER=elevenlabs

# Database Configuration
DATABASE_TYPE=memory
# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/voxassist
# For MongoDB:
# MONGODB_URL=mongodb://localhost:27017/voxassist

# Application Settings
DEBUG=True
LOG_LEVEL=INFO

# Security
SECRET_KEY=your_secret_key_here
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## Project Structure

```
VoxAssist-AI/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── routes/              # API endpoints
│   ├── services/            # Business logic
│   ├── ai/                  # LLM integration
│   ├── voice/               # STT/TTS services
│   └── db/                  # Database models
├── prompts/                 # LLM prompt templates
├── workflows/               # Call flow definitions
├── docker/                  # Docker configuration
└── requirements.txt         # Python dependencies
```

## Next Steps

1. Get API keys from:
   - OpenAI: https://platform.openai.com/api-keys
   - ElevenLabs: https://elevenlabs.io/
   - Vapi: https://www.vapi.ai/
   - Twilio: https://www.twilio.com/

2. Test the API:
   - Visit http://localhost:8000/docs for interactive API documentation
   - Test endpoints using the Swagger UI

3. Integrate with telephony:
   - Set up Vapi or Twilio webhooks
   - Configure call routing

4. Customize prompts:
   - Edit `prompts/system_prompt.txt` for your use case
   - Modify `workflows/call_flow.json` for custom flows

