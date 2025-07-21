import streamlit as st
import os
import json
from orchestrator.pipeline_orchestrator import PipelineOrchestrator
from config import Config

def main():
    """
    REQUIREMENT: Single, easy-to-use interface
    Streamlit web interface for the complete pipeline
    """
    st.set_page_config(
        page_title="Receptro.AI Media Pipeline", 
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("🎯 Receptro.AI Modular Media & Data Processing Pipeline")
    st.markdown("""
    **Complete End-to-End Solution:**
    - 🎤 **Audio**: Speech → Text → Intent Analysis → Response → Audio Reply
    - 🖼️ **Images**: Document → Text Extraction → Structured Fields
    """)
    
    # Initialize pipeline
    if 'orchestrator' not in st.session_state:
        with st.spinner("Initializing pipeline components..."):
            st.session_state.orchestrator = PipelineOrchestrator()
    
    # File upload with auto-routing
    uploaded_file = st.file_uploader(
        "Upload Audio or Image File",
        type=['wav', 'mp3', 'm4a', 'mp4', 'mpeg', 'mpga', 'webm', 'png', 'jpg', 'jpeg', 'bmp'],
        help="Audio files: WAV, MP3, M4A, MP4, WebM | Image files: PNG, JPG, JPEG, BMP"
    )
    
    if uploaded_file is not None:
        # Save file temporarily
        temp_path = os.path.join(Config.TEMP_DIR, uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Auto-detect file type
        file_type = st.session_state.orchestrator.get_file_type(temp_path)
        
        if file_type == "audio":
            st.info("🎵 **Audio File Detected** - Will process through complete audio pipeline")
        elif file_type == "image":
            st.info("🖼️ **Image File Detected** - Will extract structured document data")
        else:
            st.error("❌ Unsupported file type")
            return
        
        # Process button
        if st.button("🚀 Process Through Pipeline", type="primary", use_container_width=True):
            with st.spinner("Running complete end-to-end pipeline..."):
                result = st.session_state.orchestrator.process_file(temp_path)
            
            if "error" in result:
                st.error(f"❌ Pipeline Error: {result['error']}")
            else:
                st.success("✅ Pipeline completed successfully!")
                
                # Display results based on file type
                final_output = result.get("final_output", {})
                
                if file_type == "audio":
                    st.subheader("🎵 Complete Audio Processing Results")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**1. Speech → Text (Transcription)**")
                        st.text_area("Transcribed Text", 
                                   final_output.get("transcribed_text", "N/A"), 
                                   height=80)
                        
                        st.markdown("**2. Intent Analysis**")
                        st.write(f"**Intent:** {final_output.get('detected_intent', 'N/A')}")
                        st.write(f"**Sentiment:** {final_output.get('sentiment', 'N/A')}")
                        
                        entities = final_output.get("extracted_entities", [])
                        if entities:
                            st.write("**Entities:** " + ", ".join(entities))
                    
                    with col2:
                        st.markdown("**3. Generated Response**")
                        st.text_area("AI Response", 
                                   final_output.get("response_text", "N/A"), 
                                   height=80)
                        
                        st.markdown("**4. Text → Speech (Audio Reply)**")
                        audio_file = final_output.get("response_audio")
                        if audio_file and os.path.exists(audio_file):
                            st.audio(audio_file)
                            st.success("🔊 Audio reply generated successfully!")
                        else:
                            st.info("Audio generation not available")
                
                elif file_type == "image":
                    st.subheader("🖼️ Document Extraction Results")
                    
                    st.markdown("**Document Type**")
                    st.write(final_output.get("document_type", "N/A"))
                    
                    st.markdown("**Extracted Text**")
                    st.text_area("All Text Found", 
                               final_output.get("extracted_text", ""), 
                               height=150)
                    
                    st.markdown("**Structured Fields**")
                    structured_fields = final_output.get("structured_fields", {})
                    if structured_fields:
                        for key, value in structured_fields.items():
                            st.write(f"**{key.title()}:** {value}")
                    else:
                        st.write("No structured fields extracted")
                    
                    entities = final_output.get("extracted_entities", [])
                    if entities:
                        st.markdown("**Extracted Entities**")
                        for entity in entities:
                            st.write(f"• {entity}")
                
                # Show processing steps
                with st.expander("📋 View Processing Steps"):
                    steps = final_output.get("processing_steps", [])
                    for i, step in enumerate(steps, 1):
                        st.write(f"{i}. {step.replace('_', ' ').title()}")
                
                # JSON download
                with st.expander("📥 Download Complete Results"):
                    json_str = json.dumps(result, indent=2)
                    st.download_button(
                        "Download JSON Results",
                        json_str,
                        f"{uploaded_file.name}_results.json",
                        "application/json"
                    )
                    st.json(result)
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    main()