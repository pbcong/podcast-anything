from src.audio.TTS import TTS_wrapper
import os
from moviepy import concatenate_audioclips, AudioFileClip

files = [f"./src/audio/speech_{i}.mp3" for i in range(19)]

def concatenate_audio_moviepy(audio_clip_paths, output_path):
    clips = [AudioFileClip(c) for c in audio_clip_paths]
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_path)

concatenate_audio_moviepy(files, "./src/audio/combined_speech.mp3")