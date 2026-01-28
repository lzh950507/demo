import urllib.request
import urllib.parse
import json
import wave
import struct
import math
import os

# 1. Create a dummy WAV file (1 sec silence)
filename = "test.wav"
sample_rate = 16000
duration = 1.0
frequency = 440.0

print(f"Generating {filename}...")
with wave.open(filename, 'w') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    for i in range(int(duration * sample_rate)):
        value = int(32767.0 * math.cos(frequency * math.pi * float(i) / float(sample_rate)))
        data = struct.pack('<h', value)
        wav_file.writeframes(data)

# 2. Upload file
url = 'http://127.0.0.1:8000/asr/audio/transcriptions'
print(f"Sending request to {url}...")

# Simple multipart upload using standard library is painful.
# Let's try to use requests if available, otherwise just use a simple manual construction or try to use a tool that might be installed?
# 'python-multipart' is in pyproject.toml, so maybe I can rely on a simpler client?
# Let's just try to import requests, if it fails, I'll fallback to a simpler test or just check server logs.
# Actually, I can use `curl` via run_command if available. That's way easier.

import sys
try:
    import requests
    with open(filename, 'rb') as f:
        files = {'file': (filename, f, 'audio/wav')}
        response = requests.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
except ImportError:
    print("requests not found, skipping python client test. Use curl.")

