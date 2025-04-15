# Simple Video Recorder

A minimal web-based video and audio recording application.

## Features

- Record video and audio from your webcam and microphone
- Simple one-page interface
- Download recordings in WebM format
- No server-side storage (all processing happens in the browser)

## Setup

1. Activate the virtual environment:
   ```bash
   # On Windows
   .\venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   python server.py
   ```

4. Open your browser to `http://localhost:8000`

## Usage

1. Click "Start Recording" to begin recording
2. Click "Stop Recording" when finished
3. Click "Download Recording" to save the video to your computer

## Notes

- The application requires a modern browser with support for the MediaRecorder API
- You'll need to grant camera and microphone permissions when prompted
- Recordings are saved in WebM format
- All processing happens in the browser - no data is sent to any server