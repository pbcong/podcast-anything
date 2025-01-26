from src.audio.TTS import TTS_wrapper
from src.text.llm import llm_wrapper
from src.text.doc_input import DocumentParser
from src.config import Config
from src.prompt import get_prompt
import json

def test(**kwargs):
    config = Config()
    parser = DocumentParser()
    doc = parser.parse_document("./src/test/blt.pdf")
    llm = llm_wrapper(config=config)
    TTS = TTS_wrapper()
    script = llm.generate_text(get_prompt(doc, topic = "AI, Deep Learning, and Machine Learning"))
    if script.startswith('```json'):
        script = script[7:-3]
    script = json.loads(script.replace("json\n", ""))
    speech_file_path = TTS.get_audio(script)

if __name__ == '__main__':
    test()