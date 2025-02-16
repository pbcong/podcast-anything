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
CORS(app, resources={r"/*": {"origins": "*"}})
@app.route("/generate_podcast", methods=['POST'])
def generate_podcast():
    file = request.files['file']
    topic = request.form['topic']
    api_key = request.form['api_key']
    
    if not api_key:
        return jsonify({'error': 'OpenAI API key is required'}), 400

    # Create a temporary directory
    file_path = os.path.join('./tmp', file.filename)
    os.makedirs('./tmp', exist_ok=True)
    file.save(file_path)
        
    config = Config()
    parser = DocumentParser()
    doc = parser.parse_document(file_path)
    llm = llm_wrapper(config=config, api_key=api_key)
    TTS = TTS_wrapper(api_key)
    script = llm.generate_text(get_prompt(doc, topic=topic))
    if script.startswith('```json'):
        script = script[7:-3]
    script = json.loads(script.replace("json\n", ""))
    speech_file_path = TTS.get_audio(script, output_path=os.path.join('./tmp/', 'combined_audio.mp3'))
    if os.path.exists(file_path):
        os.remove(file_path)
        
    # Return the path to the generated audio file
    return jsonify({'audio_file_path': speech_file_path})

@app.route("/status", methods=['GET'])
def get_status():
    return jsonify({'status': 'OK'})

@app.route('/download/<path:filename>', methods=['GET'])
def download_audio(filename):
    return send_from_directory('./tmp', filename)

@app.route('/answer_question', methods=['POST'])
def answer_question():
    try:
        file = request.files['file']
        question = request.form['question']
        api_key = request.form['api_key']
        
        if not api_key:
            return jsonify({'error': 'OpenAI API key is required'}), 400

        # Create a temporary directory
        file_path = os.path.join('./tmp', file.filename)
        os.makedirs('./tmp', exist_ok=True)
        if not os.path.exists(file_path):
            file.save(file_path)
            
        config = Config()
        parser = DocumentParser()
        doc = parser.parse_document(file_path)
        llm = llm_wrapper(config=config, api_key=api_key)
        
        # Generate response using LLM
        response = llm.generate_text(f"""
        Please provide a clear and concise answer to the question based on the context provided.
        Context: {doc}
        Question: {question}
        """)
        
        return jsonify({
            'status': 'success',
            'answer': response
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
