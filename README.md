# Audio Transcriber

A Free Python tool for transcribing audio files with timestamps using OpenAI's Whisper model. 
Created to help with the creation of SwiftUI audio maps. Because why pay for services when you can do it yourself?
Created by [https://x.com/Mexican_Whale](https://x.com/Mexican_Whale)

## Features
- Transcribe audio files to text with timestamps.
- Support for multiple audio formats (MP3, WAV, M4A, etc.).
- Local processing using Whisper model.
- Customizable output directory.

## Installation

Clone the repository:
```bash
git clone https://github.com/yourusername/audio-transcriber.git
cd audio-transcriber
```

Create and activate a virtual environment:
- **Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
- **macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

**Basic usage:**
```bash
python audio_map.py
```

**Menu Options:**
1. Add new audio file
2. List existing files
3. Select and transcribe file:
   - Auto mode: Uses Whisper defaults
   - Manual mode: Customize settings:
     - Lines per segment
     - Duration per segment
     - Character limit
     - Segmentation type
4. Exit

**Manual Configuration:**
- Lines per segment defaults to 2
- Target duration defaults to 12.0 seconds
- Character limit defaults to 175 per segment

**Segmentation Modes:**
- **Auto:** Uses Whisper's natural breaks
- **Duration:** Splits by time
- **Lines:** Splits by line count
- **Characters:** Splits by character count

## Output Format
Swift format with segments:
```swift
private let segments = [
    IntroTextSegment(
        text: """
        First part of the segment \
        Second part of the segment
        """,
        timestamp: 0.0
    ),
]
```

## Requirements
- Python 3.8 or higher
- OpenAI Whisper
- FFmpeg for audio processing

---

Created by [https://x.com/Mexican_Whale](https://x.com/Mexican_Whale)
