import axios from "axios";
import { useState } from "react";
import ReactMarkdown from "react-markdown";
const API_URL = "http://127.0.0.1:5000";
function Chat({ file }) {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [error, setError] = useState("");

  const handleSend = (e) => {
    setError("");
    e.preventDefault();
    if (!file) {
      setError("Please upload a document first");
      return;
    }

    if (newMessage.trim()) {
      setMessages([...messages, { text: newMessage, sender: "user" }]);
      setNewMessage("");
      const formData = new FormData();
      formData.append("file", file);
      formData.append("question", newMessage);

      axios
        .post(`${API_URL}/answer_question`, formData)
        .then((response) => {
          setMessages([
            ...messages,
            { text: response.data.answer, sender: "bot" },
          ]);
        })
        .catch((error) => {
          setError("Failed to get answer. Please try again.");
          console.error("Error sending message:", error);
        });
    }
  };

  if (!file) {
    return (
      <div className="flex flex-col h-[500px] w-full max-w-2xl mx-auto border border-gray-300 rounded-lg bg-white shadow-xl items-center justify-center">
        <p className="text-gray-500">
          Please upload a document to start chatting
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-[500px] w-full max-w-2xl mx-auto border border-gray-300 rounded-lg bg-white shadow-xl">
      {error && (
        <div
          className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded relative"
          role="alert"
        >
          <span className="block sm:inline">{error}</span>
        </div>
      )}
      <div className="flex-1 p-4 overflow-y-auto bg-gray-100">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`mb-4 ${
              message.sender === "user" ? "text-right" : "text-left"
            }`}
          >
            <div
              className={`inline-block p-3 rounded-lg ${
                message.sender === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-200 text-gray-800"
              }`}
            >
              {message.sender === "user" ? (
                message.text
              ) : (
                <ReactMarkdown className="prose prose-sm max-w-none prose-pre:bg-gray-800 prose-pre:text-white prose-pre:p-2 prose-pre:rounded prose-code:text-gray-800 prose-headings:text-gray-800">
                  {message.text}
                </ReactMarkdown>
              )}
            </div>
          </div>
        ))}
      </div>
      <form onSubmit={handleSend} className="border-t p-4 bg-white">
        <div className="flex gap-2">
          <input
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Type a message..."
            className="flex-1 p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
}

export default Chat;
