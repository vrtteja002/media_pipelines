import os
import json
import time
from typing import Dict, Any
from transcribe.whisper_transcriber import WhisperTranscriber
from interpret.intent_analyzer import IntentAnalyzer
from synthesize.tts_synthesizer import TTSSynthesizer
from extract.document_extractor import DocumentExtractor
from config import Config

class PipelineOrchestrator:
    """
    REQUIREMENT: Tie all steps together behind a single, easy-to-use interface
    Enhanced with performance monitoring and error recovery
    """
    def __init__(self):
        print("🚀 Initializing Enhanced Media & Data Processing Pipeline")
        
        # Initialize all components
        self.transcriber = WhisperTranscriber()
        self.intent_analyzer = IntentAnalyzer() 
        self.tts_synthesizer = TTSSynthesizer()
        self.document_extractor = DocumentExtractor()
        
        # Supported file types for auto-routing
        self.audio_extensions = {'.wav', '.mp3'}
        self.image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif'}
        
        print("✅ Pipeline orchestrator ready")
    
    def get_file_type(self, file_path: str) -> str:
        """Auto-detect file type based on extension"""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in self.audio_extensions:
            return "audio"
        elif ext in self.image_extensions:
            return "image"
        else:
            return "unknown"
    
    def process_audio_pipeline(self, audio_path: str) -> Dict[str, Any]:
        """
        COMPLETE AUDIO PIPELINE with performance tracking
        """
        print(f"\n🎵 Starting AUDIO pipeline for: {os.path.basename(audio_path)}")
        start_time = time.time()
        
        pipeline_result = {
            "pipeline_type": "audio",
            "input_file": audio_path,
            "steps": {},
            "final_output": {},
            "performance": {}
        }
        
        # Step 1: Speech to Text
        print("Step 1/4: Speech → Text")
        step_start = time.time()
        transcription = self.transcriber.transcribe_audio(audio_path)
        pipeline_result["steps"]["1_transcription"] = transcription
        pipeline_result["performance"]["transcription_time"] = time.time() - step_start
        
        if transcription["status"] != "success":
            pipeline_result["final_output"] = {"error": "Speech-to-text failed"}
            return pipeline_result
        
        # Step 2: Intent Analysis
        print("Step 2/4: Text → Intent Analysis")
        step_start = time.time()
        intent_analysis = self.intent_analyzer.analyze_intent(transcription["text"])
        pipeline_result["steps"]["2_intent_analysis"] = intent_analysis
        pipeline_result["performance"]["intent_analysis_time"] = time.time() - step_start
        
        if intent_analysis["status"] != "success":
            pipeline_result["final_output"] = {"error": "Intent analysis failed"}
            return pipeline_result
        
        # Step 3: Generate Response Text
        print("Step 3/4: Intent → Response Generation")
        suggested_response = intent_analysis["analysis"].get("suggested_response", 
                                                           "Thank you for your message. I understand your request.")
        
        # Step 4: Text to Speech
        print("Step 4/4: Response → Audio")
        step_start = time.time()
        tts_filename = f"response_{os.path.splitext(os.path.basename(audio_path))[0]}.wav"
        tts_result = self.tts_synthesizer.text_to_speech(suggested_response, tts_filename)
        pipeline_result["steps"]["3_text_to_speech"] = tts_result
        pipeline_result["performance"]["tts_time"] = time.time() - step_start
        
        # Total processing time
        total_time = time.time() - start_time
        pipeline_result["performance"]["total_time"] = total_time
        
        # Final comprehensive output
        pipeline_result["final_output"] = {
            "original_audio": audio_path,
            "transcribed_text": transcription["text"],
            "detected_intent": intent_analysis["analysis"].get("intent", "unknown"),
            "extracted_entities": intent_analysis["analysis"].get("entities", []),
            "sentiment": intent_analysis["analysis"].get("sentiment", "neutral"),
            "response_text": suggested_response,
            "response_audio": tts_result.get("audio_file"),
            "confidence": intent_analysis["analysis"].get("confidence", "medium"),
            "processing_steps": ["speech_to_text", "intent_analysis", "response_generation", "text_to_speech"],
            "metadata": {
                "total_steps": 4,
                "pipeline_type": "complete_audio_processing",
                "success": True,
                "processing_time_seconds": round(total_time, 2)
            }
        }
        
        print(f"✅ Audio pipeline completed in {total_time:.2f} seconds!")
        return pipeline_result
    
    def process_image_pipeline(self, image_path: str) -> Dict[str, Any]:
        """
        COMPLETE IMAGE PIPELINE with enhanced extraction
        """
        print(f"\n🖼️ Starting IMAGE pipeline for: {os.path.basename(image_path)}")
        start_time = time.time()
        
        pipeline_result = {
            "pipeline_type": "image",
            "input_file": image_path,
            "steps": {},
            "final_output": {},
            "performance": {}
        }
        
        # Step 1: Document Extraction
        print("Step 1/1: Image → Structured Data Extraction")
        step_start = time.time()
        extraction = self.document_extractor.extract_document_data(image_path)
        pipeline_result["steps"]["1_document_extraction"] = extraction
        pipeline_result["performance"]["extraction_time"] = time.time() - step_start
        
        if extraction["status"] == "error":
            pipeline_result["final_output"] = {"error": "Document extraction failed"}
            return pipeline_result
        
        # Total processing time
        total_time = time.time() - start_time
        pipeline_result["performance"]["total_time"] = total_time
        
        # Final comprehensive output
        pipeline_result["final_output"] = {
            "input_image": image_path,
            "document_type": extraction["extraction"].get("document_type", "unknown"),
            "extracted_text": extraction["extraction"].get("extracted_text", ""),
            "structured_fields": extraction["extraction"].get("structured_fields", {}),
            "extracted_entities": extraction["extraction"].get("entities", []),
            "extraction_confidence": extraction["extraction"].get("confidence", "unknown"),
            "processing_methods": extraction["extraction"].get("metadata", {}).get("processing_methods", []),
            "processing_steps": ["document_extraction", "text_structuring", "entity_extraction"],
            "metadata": {
                "total_steps": 1,
                "pipeline_type": "complete_image_processing", 
                "success": extraction["status"] in ["success", "partial_success"],
                "processing_time_seconds": round(total_time, 2)
            }
        }
        
        print(f"✅ Image pipeline completed in {total_time:.2f} seconds!")
        return pipeline_result
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        MAIN ENTRY POINT - Auto-routes file to appropriate pipeline
        """
        print(f"\n🎯 Processing file: {file_path}")
        
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}
        
        # Check file size
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        if file_size > 25:
            return {"error": f"File too large: {file_size:.1f}MB (max 25MB)"}
        
        # Auto-detect file type and route
        file_type = self.get_file_type(file_path)
        print(f"🔍 Detected file type: {file_type}")
        
        if file_type == "audio":
            result = self.process_audio_pipeline(file_path)
        elif file_type == "image":
            result = self.process_image_pipeline(file_path)
        else:
            return {"error": f"Unsupported file type: {os.path.splitext(file_path)[1]}"}
        
        # Save comprehensive JSON result
        output_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_result.json"
        output_path = os.path.join(Config.JSON_OUTPUT_DIR, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        result["output_json"] = output_path
        print(f"💾 Results saved to: {output_path}")
        
        return result