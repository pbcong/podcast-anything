import { useState } from "react";
import "./App.css";
import axios from "axios";
import Form from "./components/Form";
import Chat from "./components/Chat";
import { API_URL } from "./config";

function App() {
  const [file, setFile] = useState(null);
  const [topic, setTopic] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [ttsModel, setTtsModel] = useState("tts-1");
  const [filePath, setFilePath] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    if (!file) {
      setError("Please select a PDF file");
      return;
    }

    if (!topic.trim()) {
      setError("Please enter a topic");
      return;
    }

    if (!apiKey.trim()) {
      setError("Please enter your OpenAI API key");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);
    formData.append("topic", topic);
    formData.append("api_key", apiKey);
    formData.append("tts_model", ttsModel);
    try {
      setLoading(true);
      const response = await axios.post(
        `${API_URL}/generate_podcast`,
        formData
      );
      setLoading(false);
      console.log(response);
      setFilePath(response.data.audio_file_path);
    } catch (error) {
      setLoading(false);
      setError(
        error.response?.data?.error ||
          error.response?.data?.message ||
          "An error occurred while generating the podcast"
      );
      console.error(error);
    }
  };
  const handleTextChange = (event) => {
    event.preventDefault();
    setTopic(event.target.value);
  };

  const handleApiKeyChange = (event) => {
    event.preventDefault();
    setApiKey(event.target.value);
  };
  const handleFileChange = (event) => {
    event.preventDefault();
    setFile(event.target.files[0]);
  };

  const handleModelChange = (event) => {
    event.preventDefault();
    setTtsModel(event.target.value);
  };
  return (
    <div className="App">
      <Form
        handleFileChange={handleFileChange}
        handleTextChange={handleTextChange}
        handleApiKeyChange={handleApiKeyChange}
        handleSubmit={handleSubmit}
        topic={topic}
        apiKey={apiKey}
        loading={loading}
        error={error}
        ttsModel={ttsModel}
        handleModelChange={handleModelChange}
      />

      <div className="mt-12 mb-8">
        <h2 className="text-2xl font-semibold text-center mb-4">
          Ask me anything about the document
        </h2>
        <Chat file={file} apiKey={apiKey} apiUrl={API_URL} />
      </div>

      {filePath && (
        <div>
          <h2>Generated Audio</h2>
          <audio controls>
            <source
              src={`${API_URL}/download/combined_audio.mp3`}
              type="audio/mpeg"
            />
            Your browser does not support the audio element.
          </audio>
          <div>
            <a href={`${API_URL}/download/combined_audio.mp3`} download>
              Download Audio
            </a>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
