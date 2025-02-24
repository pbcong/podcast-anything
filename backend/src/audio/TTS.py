from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os
import warnings
import numpy as np
from moviepy.editor import concatenate_audioclips, AudioFileClip
import soundfile as sf
from kokoro import KPipeline
warnings.filterwarnings("ignore")

load_dotenv()

class TTS_wrapper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.openai_client = OpenAI(api_key=api_key)
        # Initialize Kokoro model only when needed
        self.kokoro_initialized = False
        self.kokoro_pipeline = None
        self.sample_rate = 24000  # Kokoro model's output sample rate

    def _init_kokoro(self):
        if not self.kokoro_initialized:
            self.kokoro_pipeline = KPipeline(lang_code='a')  # American English
            self.kokoro_initialized = True

    def get_audio(self, script: object, output_path: str, model: str = "tts-1") -> Path:
        files = []
        for i, line in enumerate(script):
            speech_file_path = Path(__file__).parent / f"speech_{i}.{'mp3' if 'tts' in model else 'wav'}"
            if 'kokoro' in model.lower():
                self._generate_audio_kokoro(line["role"], line["line"], speech_file_path)
            else:
                self._generate_audio_openai(line["role"], line["line"], speech_file_path)
            files.append(speech_file_path)
        
        concatenated_audio_path = self._concate_audio(files, output_path=output_path)
        for f in files:
            os.remove(f)
        return concatenated_audio_path

    def _concate_audio(self, files, output_path: str = "tmp/combined_speech.mp3"):
        if any('wav' in str(f) for f in files):  # If any WAV files (kokoro)
            print("Concatenating WAV files using soundfile")
            # Read all audio files
            audio_segments = []
            for f in files:
                data, _ = sf.read(str(f))
                audio_segments.append(data)
            
            # Concatenate audio data
            final_audio = np.concatenate(audio_segments)
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            # Write concatenated audio
            print(f"Writing concatenated audio to: {output_path}")
            sf.write(output_path, final_audio, self.sample_rate)
        else:  # MP3 files (OpenAI)
            clips = [AudioFileClip(str(c)) for c in files]
            final_clip = concatenate_audioclips(clips)
            final_clip.write_audiofile(output_path)
        
        return output_path

    def _generate_audio_openai(self, role, text, speech_file_path):
        response = self.openai_client.audio.speech.create(
            model='tts-1',
            voice='echo' if role == 'Host' else 'nova',
            input=text,
        )
        response.stream_to_file(speech_file_path)
        return response

    def _generate_audio_kokoro(self, role, text, speech_file_path):
        try:
            print(f"Generating audio for text: {text}")
            self._init_kokoro()  # Initialize Kokoro pipeline if not already done
            print("Kokoro pipeline initialized")
            
            # Use different voices for host and guest
            voice = 'am_fenrir' if role == 'Host' else 'af_heart'
            print(f"Using voice: {voice}")
            
            # Generate speech using Kokoro pipeline
            generator = self.kokoro_pipeline(
                text,
                voice=voice,
                speed=1.0,
                split_pattern=None  # Don't split the text
            )
            print("Generator created")
            
            # Collect all audio segments
            audio_segments = []
            for _, _, audio in generator:
                print(f"Received audio segment of shape: {audio.shape}")
                audio_segments.append(audio)
            
            if not audio_segments:
                raise Exception("No audio segments were generated")
            
            # Combine audio segments if there are multiple
            final_audio = audio_segments[0]  # For now just take first segment
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(speech_file_path) if os.path.dirname(speech_file_path) else '.', exist_ok=True)
            
            print(f"Writing audio to: {speech_file_path}")
            sf.write(str(speech_file_path), final_audio, self.sample_rate)
            print(f"Audio file written successfully: {os.path.exists(speech_file_path)}")
            
            return speech_file_path
        except Exception as e:
            print(f"Error in _generate_audio_kokoro: {str(e)}")
            raise
