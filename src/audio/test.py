from TTS import TTS_wrapper
import json

tts = TTS_wrapper()

with open("test.json", "r") as f:
    data = json.load(f)

tts.get_audio(data)