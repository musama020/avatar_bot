"""Every setting for the project. Secrets and deploy-specific values come from .env; nothing else reads it."""
import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

MODEL_CACHE_DIRECTORY = PROJECT_ROOT / "models"

# LiveKit
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "")
TOKEN_SERVER_HOST = os.getenv("TOKEN_SERVER_HOST", "0.0.0.0")
TOKEN_SERVER_PORT = int(os.getenv("TOKEN_SERVER_PORT", "8100"))

# Listening: Silero VAD + self-hosted Nemotron + LiveKit turn detector
SPEECH_SERVER_HOST = os.getenv("SPEECH_SERVER_HOST", "127.0.0.1")
SPEECH_SERVER_PORT = int(os.getenv("SPEECH_SERVER_PORT", "8101"))
SPEECH_MODEL_ID = "nvidia/nemotron-speech-streaming-en-0.6b"
SPEECH_CHUNK_MILLISECONDS = 160
SPEECH_SAMPLE_RATE = 16000
MIN_INTERRUPTION_SECONDS = 0.3
MIN_END_OF_TURN_DELAY_SECONDS = 0.2
MAX_END_OF_TURN_DELAY_SECONDS = 3.0

# Reasoning: Groq first, OpenAI when Groq limits are hit
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-20b")
LLM_REASONING_EFFORT = os.getenv("LLM_REASONING_EFFORT", "low")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_TEMPERATURE = 0.4
LLM_MAX_COMPLETION_TOKENS = 600
CONVERSATION_LANGUAGE = os.getenv("CONVERSATION_LANGUAGE", "English")
CONVERSATION_GREETING = "Hi! How can I help you?"
REASONING_STAGE_DIRECTORY = PROJECT_ROOT / "worker" / "stages" / "reasoning"
SYSTEM_PROMPT_PATH = REASONING_STAGE_DIRECTORY / "system_prompt.txt"

# Knowledge base (RAG): BGE-M3 dense + sparse vectors in embedded Qdrant, merged with RRF
KNOWLEDGE_BASE_PATH = REASONING_STAGE_DIRECTORY / "knowledge_base" / "smart4u_en.md"
QDRANT_STORAGE_PATH = PROJECT_ROOT / "qdrant_data"
KNOWLEDGE_COLLECTION_NAME = "smart4u_en"
EMBEDDING_MODEL_ID = "BAAI/bge-m3"
EMBEDDING_DIMENSIONS = 1024
RETRIEVAL_TOP_K = 3
RETRIEVAL_CANDIDATES_PER_SEARCH = 10
RETRIEVAL_MIN_DENSE_SCORE = 0.45

# Speaking: ElevenLabs
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")
ELEVENLABS_MODEL = os.getenv("ELEVENLABS_MODEL", "eleven_flash_v2_5")

# Avatar: self-hosted FlashHead Lite
AVATAR_SERVER_HOST = os.getenv("AVATAR_SERVER_HOST", "127.0.0.1")
AVATAR_SERVER_PORT = int(os.getenv("AVATAR_SERVER_PORT", "8102"))
AVATAR_MODEL_VARIANT = os.getenv("AVATAR_MODEL_VARIANT", "lite")
AVATAR_REFERENCE_IMAGE_PATH = Path(os.getenv("AVATAR_REFERENCE_IMAGE_PATH", str(PROJECT_ROOT / "assets" / "avatar_face.png")))
AVATAR_FRAME_RATE = 25

# MVP targets, used by evaluation
TARGET_REPLY_START_SECONDS = 1.2
TARGET_INTERRUPT_STOP_SECONDS = 0.3
TARGET_AVATAR_FIRST_FRAME_SECONDS = 0.3
TARGET_LIP_OFFSET_SECONDS = 0.045
