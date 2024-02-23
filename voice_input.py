import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import requests
import json
from config import *

api_key = API_KEY

# Function to record audio
def record_audio(duration=5, samplerate=44100):
    print("Recording...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype='int16')
    sd.wait()
    print("Recording stopped")
    return recording, samplerate

# Save the recording to a WAV file
def save_recording(recording, samplerate, filename='output.wav'):
    wav.write(filename, samplerate, recording)

# Send audio file to OpenAI's API
def transcribe_audio(file_path, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "whisper-1"
    }
    files = {
        "file": open(file_path, "rb")
    }
    response = requests.post("https://api.openai.com/v1/audio/transcriptions", headers=headers, data=data, files=files)
    return response.json()

def process_audio_to_text(duration=5, api_key= api_key):
    # Record audio 
    recording, samplerate = record_audio(duration)  # Duration in seconds
    save_recording(recording, samplerate)
    
    # Transcribe the recorded audio
    transcription_result = transcribe_audio('output.wav', api_key)
    transcription_text = transcription_result.get('text', '')
    
    print(transcription_text)
    return transcription_text