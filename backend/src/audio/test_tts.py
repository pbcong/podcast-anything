import unittest
from pathlib import Path
import os
from unittest.mock import MagicMock, patch
from TTS import TTS_wrapper

def test():
    # Initialize with dummy API key since kokoro doesn't need it
    tts = TTS_wrapper(api_key="dummy")
    data = [
  {
    "role": "Host",
    "line": "Welcome to our podcast!"
  },
  {
    "role": "Expert",
    "line": "Thank you for having me."
  },
  {
    "role": "Host",
    "line": "Can you tell us about your latest research?"
  },
  {
    "role": "Expert",
    "line": "Sure, I'd be happy to."
  },
  {
    "role": "Host",
    "line": "That's fascinating. How did you come up with the idea?"
  },
  {
    "role": "Expert",
    "line": "It all started when I noticed a gap in the existing literature."
  }
]
    # Test individual file generation first
    files = []
    try:
        print("\nTesting individual file generation:")
        for i, line in enumerate(data):
            speech_file_path = Path(__file__).parent / f"speech_{i}.wav"
            print(f"\nGenerating file {i}: {speech_file_path}")
            tts._generate_audio_kokoro(line["role"], line["line"], speech_file_path)
            assert os.path.exists(speech_file_path), f"File {speech_file_path} was not created"
            print(f"File {i} created successfully")
            files.append(speech_file_path)

        print("\nAll individual files generated successfully")
        print("Files to concatenate:", files)
        
        # Now test concatenation
        output_path = "./result.wav"
        print(f"\nAttempting to concatenate files to: {output_path}")
        tts._concate_audio(files, output_path=output_path)
        
        assert os.path.exists(output_path), "Final concatenated file was not created"
        print("Concatenation successful")
        
        # Clean up
        for f in files:
            os.remove(f)
        # os.remove(output_path)
        
    except Exception as e:
        print(f"\nError during test: {str(e)}")
        # Clean up in case of error
        for f in files:
            if os.path.exists(f):
                os.remove(f)
        if os.path.exists(output_path):
            os.remove(output_path)
        raise

if __name__ == "__main__":
    test()
