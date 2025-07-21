import pyttsx3
import os
from typing import Dict, Any
from config import Config

class TTSSynthesizer:
    """
    REQUIREMENT: Convert text back into an audio reply
    Uses pyttsx3 for text-to-speech conversion
    """
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            # Configure voice settings
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[0].id)
            self.engine.setProperty('rate', 150)    # Speed
            self.engine.setProperty('volume', 0.9)  # Volume
            print("✅ Text-to-Speech: TTSSynthesizer initialized")
        except Exception as e:
            print(f"⚠️ TTS initialization issue: {e}")
            self.engine = None
    
    def text_to_speech(self, text: str, output_filename: str = None) -> Dict[str, Any]:
        """Convert text to speech and save as audio file"""
        try:
            print(f"🔊 Converting to speech: '{text[:30]}...'")
            
            if not output_filename:
                output_filename = "response.wav"
            
            output_path = os.path.join(Config.AUDIO_OUTPUT_DIR, output_filename)
            
            if self.engine:
                # Save speech to file
                self.engine.save_to_file(text, output_path)
                self.engine.runAndWait()
                
                result = {
                    "status": "success",
                    "text": text,
                    "audio_file": output_path,
                    "filename": output_filename,
                    "metadata": {
                        "engine": "pyttsx3",
                        "processor": "tts_synthesizer",
                        "text_length": len(text),
                        "step": "3_text_to_speech"
                    }
                }
                
                print(f"✅ Audio saved: {output_path}")
                return result
            else:
                # TTS not available, return text response
                result = {
                    "status": "success",
                    "text": text,
                    "audio_file": None,
                    "filename": output_filename,
                    "metadata": {
                        "engine": "text_only",
                        "processor": "tts_synthesizer",
                        "text_length": len(text),
                        "step": "3_text_to_speech",
                        "note": "TTS engine not available, text response only"
                    }
                }
                print("⚠️ TTS not available, returning text only")
                return result
                
        except Exception as e:
            print(f"❌ TTS failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "text": text,
                "audio_file": None,
                "metadata": {"engine": "pyttsx3", "processor": "tts_synthesizer", "step": "3_text_to_speech"}
            }
