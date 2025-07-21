import json
import os
from typing import Dict, Any
from openai import OpenAI
from config import Config

class WhisperTranscriber:
    """
    REQUIREMENT: Turn speech in an audio file into text
    Uses OpenAI Whisper API for speech-to-text conversion
    """
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        print("✅ Speech-to-Text: WhisperTranscriber initialized")
    
    def transcribe_audio(self, audio_path: str) -> Dict[str, Any]:
        """Convert audio file to text"""
        try:
            print(f"🎤 Transcribing audio: {os.path.basename(audio_path)}")
            
            with open(audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json"
                )
            
            result = {
                "status": "success",
                "text": transcript.text.strip(),
                "language": getattr(transcript, 'language', 'unknown'),
                "duration": getattr(transcript, 'duration', 0),
                "segments": [
                    {
                        "start": 0.0,
                        "end": getattr(transcript, 'duration', 5.0),
                        "text": transcript.text.strip()
                    }
                ],
                "metadata": {
                    "audio_file": os.path.basename(audio_path),
                    "model": "openai-whisper-1",
                    "confidence": "high",
                    "step": "1_speech_to_text"
                }
            }
            
            print(f"✅ Transcribed: '{result['text'][:50]}...'")
            return result
            
        except Exception as e:
            print(f"❌ Transcription failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "text": "",
                "metadata": {"audio_file": os.path.basename(audio_path), "step": "1_speech_to_text"}
            }