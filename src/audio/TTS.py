from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os
import warnings
from pydub import AudioSegment
from moviepy import concatenate_audioclips, AudioFileClip
warnings.filterwarnings("ignore")

load_dotenv()

class TTS_wrapper:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def get_audio(self, script: object, output_path: str, model: str = "tts-1") -> Path:
        
        files=[]
        for i, line in enumerate(script):
            speech_file_path = Path(__file__).parent / f"speech_{i}.mp3"
            response = self._generate_audio(line["role"], line["line"], speech_file_path)
            files.append(speech_file_path)
        concatenated_audio_path = self._concate_audio(files, output_path=output_path)
        for f in files:
            os.remove(f)
        return concatenated_audio_path
        
    def _concate_audio(self, files, output_path: str = "tmp/combined_speech.mp3"):
        clips = [AudioFileClip(c) for c in files]
        final_clip = concatenate_audioclips(clips)
        final_clip.write_audiofile(output_path)
        return output_path

    def _generate_audio(self, role, text, speech_file_path):
        response = self.client.audio.speech.create(
            model='tts-1',
            voice='echo' if role == 'Host' else 'nova',
            input=text,
        )
        response.stream_to_file(speech_file_path)
        return response