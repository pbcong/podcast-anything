from flask import Flask, request, jsonify, send_from_directory
from src.audio.TTS import TTS_wrapper
from src.text.llm import llm_wrapper
from src.text.doc_input import DocumentParser
from src.config import Config
from src.prompt import get_prompt
import json
import os
import tempfile
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route("/generate_podcast", methods=['POST'])
def generate_podcast():
    file = request.files['file']
    topic = request.form['topic']

    # Create a temporary directory
    file_path = os.path.join('./tmp', file.filename)
    file.save(file_path)
        
    config = Config()
    parser = DocumentParser()
    doc = parser.parse_document(file_path)
    llm = llm_wrapper(config=config)
    TTS = TTS_wrapper()
    script = llm.generate_text(get_prompt(doc, topic=topic))
    if script.startswith('```json'):
        script = script[7:-3]
    script = json.loads(script.replace("json\n", ""))
    speech_file_path = TTS.get_audio(script, output_path=os.path.join('./tmp', 'combined_audio.mp3'))
    os.remove(file_path)
        
    # Return the path to the generated audio file
    return jsonify({'audio_file_path': speech_file_path})

@app.route('/download/<path:filename>', methods=['GET'])
def download_audio(filename):
    return send_from_directory('./tmp', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)