import { useState } from "react";
import "./App.css";
import axios from "axios";
import Form from "./components/Form";

function App() {
  const API_URL = "http://127.0.0.1:5000";
  const [file, setFile] = useState(null);
  const [topic, setTopic] = useState("");
  const [filePath, setFilePath] = useState("");
  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log("running");
    const formData = new FormData();
    formData.append("file", file);
    formData.append("topic", topic);
    try {
      const response = await axios.post(
        `${API_URL}/generate_podcast`,
        formData
      );
      console.log(response);
      setFilePath(response.data.audio_file_path);
    } catch (error) {
      console.error(error);
    }
  };
  const handleTextChange = (event) => {
    event.preventDefault();
    setTopic(event.target.value);
    console.log(topic);
  };
  const handleFileChange = (event) => {
    event.preventDefault();
    setFile(event.target.files[0]);
    console.log(file);
  };
  return (
    <div className="App">
      <Form
        handleFileChange={handleFileChange}
        handleTextChange={handleTextChange}
        handleSubmit={handleSubmit}
      />

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
