# 🎯 Receptro.AI - Modular Media & Data Processing Pipeline

A comprehensive end-to-end AI pipeline for processing audio and image files with intelligent intent analysis and natural language responses.

## 📋 Requirements

Create a `requirements.txt` file with these dependencies:

```txt
openai>=1.0.0
streamlit>=1.28.0
pyttsx3>=2.90
python-dotenv>=1.0.0
```

## 🚀 Features

- **🎵 Complete Audio Pipeline**: Speech → Text → Intent Analysis → AI Response → Audio Reply
- **🖼️ Document Extraction**: Images → Text → Structured Data Extraction  
- **🧠 Smart Intent Analysis**: Natural language understanding with context awareness
- **🔊 Natural TTS**: Human-like speech synthesis for responses
- **🌐 Web Interface**: Easy-to-use Streamlit interface
- **📊 Performance Monitoring**: Processing time tracking and quality metrics

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Receptro.AI Pipeline                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐                   │
│  │   AUDIO PIPELINE │    │  IMAGE PIPELINE │                   │
│  └─────────────────┘    └─────────────────┘                   │
│                                                                 │
│  Audio File                    Image File                       │
│      ↓                             ↓                           │
│  ┌─────────────┐               ┌─────────────┐                 │
│  │   Whisper   │               │   GPT-4o    │                 │
│  │ Transcriber │               │  Vision     │                 │
│  └─────────────┘               └─────────────┘                 │
│      ↓                             ↓                           │
│  ┌─────────────┐               ┌─────────────┐                 │
│  │   Intent    │               │ Structured  │                 │
│  │  Analyzer   │               │    Data     │                 │
│  │  (GPT-4o)   │               │ Extraction  │                 │
│  └─────────────┘               └─────────────┘                 │
│      ↓                             ↓                           │
│  ┌─────────────┐               ┌─────────────┐                 │
│  │  Response   │               │   Entity    │                 │
│  │ Generation  │               │ Recognition │                 │
│  └─────────────┘               └─────────────┘                 │
│      ↓                                                         │
│  ┌─────────────┐                                               │
│  │    TTS      │                                               │
│  │ Synthesizer │                                               │
│  └─────────────┘                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🧩 Core Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| **WhisperTranscriber** | Audio → Text conversion | OpenAI Whisper API |
| **IntentAnalyzer** | Text → Intent + Entities | GPT-4o |
| **TTSSynthesizer** | Text → Natural Speech | pyttsx3 |
| **DocumentExtractor** | Image → Structured Data | GPT-4o Vision |
| **PipelineOrchestrator** | Workflow Management | Python |
| **Streamlit Interface** | Web UI | Streamlit |

## 📁 Project Structure

```
receptro-ai/
├── transcribe/
│   └── whisper_transcriber.py    # Audio to text
├── interpret/
│   └── intent_analyzer.py        # Text to intent analysis
├── synthesize/
│   └── tts_synthesizer.py        # Text to speech
├── extract/
│   └── document_extractor.py     # Image to structured data
├── orchestrator/
│   └── pipeline_orchestrator.py  # Main workflow coordinator
├── config.py                     # Configuration settings
├── app.py                        # Streamlit web interface
├── outputs/
│   ├── audio/                    # Generated audio files
│   └── json/                     # Processing results
└── temp/                         # Temporary file storage
```

## ⚡ Quick Start

### 1. Prerequisites

- Python 3.8+ installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Git installed

### 2. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/receptro-ai.git
cd receptro-ai

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Or install manually:
pip install openai streamlit pyttsx3 python-dotenv
```

### 4. Environment Configuration

Create `.env` file in the root directory:
```bash
# Copy example file
cp .env.example .env

# Or create manually
touch .env
```

Add your OpenAI API key to `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Create Required Directories

```bash
# Create output directories
mkdir -p outputs/audio
mkdir -p outputs/json
mkdir -p temp
```

## 🚀 How to Run

### 🌐 Running the Streamlit Web Interface

The easiest way to use Receptro.AI is through the web interface:

```bash
# Navigate to project directory
cd receptro-ai

# Activate virtual environment (if using one)
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Start Streamlit application
streamlit run app.py
```

**The application will start and show:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

**Access the app:**
- Open your browser
- Go to: `http://localhost:8501`
- Upload audio (.wav, .mp3) or image (.png, .jpg) files
- Click "🚀 Process Through Pipeline"
- View results and download JSON output

### 🔧 Streamlit Run Options

```bash
# Run on specific port
streamlit run app.py --server.port 8502

# Run on all network interfaces (accessible from other devices)
streamlit run app.py --server.address 0.0.0.0

# Run with custom configuration
streamlit run app.py --server.maxUploadSize 50

# Run in development mode with auto-reload
streamlit run app.py --server.runOnSave true
```


## 🔧 Configuration Options

### Environment Variables (.env)

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (with defaults)
AUDIO_OUTPUT_DIR=outputs/audio
JSON_OUTPUT_DIR=outputs/json  
TEMP_DIR=temp
```

### Streamlit Configuration

Create `.streamlit/config.toml` for custom settings:

```toml
[server]
port = 8501
maxUploadSize = 25

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
```

## 🧪 Testing Your Setup

### 1. Quick Health Check

```bash
python -c "
from orchestrator.pipeline_orchestrator import PipelineOrchestrator
orchestrator = PipelineOrchestrator()
print('✅ Pipeline initialized successfully!')
"
```

### 2. Test with Sample Files

```bash
# Test audio processing
python -c "
from orchestrator.pipeline_orchestrator import PipelineOrchestrator
import os

orchestrator = PipelineOrchestrator()

# Create a test (requires actual audio file)
if os.path.exists('test_audio.wav'):
    result = orchestrator.process_audio_pipeline('test_audio.wav')
    print('Audio test passed!')
else:
    print('Upload an audio file via web interface to test')
"
```

### 3. Verify Dependencies

```bash
python -c "
import openai
import streamlit
import pyttsx3
print('✅ All dependencies installed correctly!')
"
```

## 🐛 Troubleshooting

### Common Issues:

**1. OpenAI API Key Error:**
```bash
# Verify your API key is set
python -c "import os; print('API Key:', os.getenv('OPENAI_API_KEY')[:10] + '...')"
```

**2. TTS Not Working:**
```bash
# Install system TTS dependencies
# Ubuntu/Debian:
sudo apt-get install espeak espeak-data libespeak1 libespeak-dev

# macOS:
brew install espeak
```

**3. Port Already in Use:**
```bash
# Run on different port
streamlit run app.py --server.port 8502
```

**4. File Upload Issues:**
```bash
# Check permissions
chmod 755 temp/
chmod 755 outputs/
```

## 🎯 Usage Examples

### Audio Processing
```python
from orchestrator.pipeline_orchestrator import PipelineOrchestrator

orchestrator = PipelineOrchestrator()

# Process audio file
result = orchestrator.process_audio_pipeline("input.wav")
print(f"Intent: {result['final_output']['detected_intent']}")
print(f"Response: {result['final_output']['response_text']}")
```

### Image Processing
```python
# Process document image
result = orchestrator.process_image_pipeline("document.jpg")
print(f"Document Type: {result['final_output']['document_type']}")
print(f"Extracted Text: {result['final_output']['extracted_text']}")
```

### Auto-Detection
```python
# Automatically detect file type and process
result = orchestrator.process_file("unknown_file.mp3")
```

## 📊 API Response Format

### Audio Pipeline Output
```json
{
  "pipeline_type": "audio",
  "final_output": {
    "transcribed_text": "Book me a flight to Paris",
    "detected_intent": "transaction",
    "sentiment": "neutral",
    "response_text": "I'd love to help you book a flight to Paris!",
    "response_audio": "path/to/response.wav",
    "confidence": "high"
  },
  "performance": {
    "total_time": 3.45,
    "transcription_time": 1.2,
    "intent_analysis_time": 0.8,
    "tts_time": 1.45
  }
}
```

### Image Pipeline Output
```json
{
  "pipeline_type": "image", 
  "final_output": {
    "document_type": "business_card",
    "extracted_text": "John Smith\nSoftware Engineer\njohn@company.com",
    "structured_fields": {
      "name": "John Smith",
      "email": "john@company.com",
      "phone": "(555) 123-4567"
    },
    "extraction_confidence": "high"
  }
}
```

## 🚀 Performance

- **Audio Processing**: ~3-5 seconds per file
- **Image Processing**: ~2-3 seconds per file  
- **Supported Formats**: WAV, MP3, PNG, JPG, JPEG
- **File Size Limit**: 25MB per file

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/receptro-ai/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/receptro-ai/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/receptro-ai/discussions)

---

**Built with ❤️ using OpenAI GPT-4o, Whisper, and Python**
