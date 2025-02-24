import React from "react";
import { useState } from "react";

const Form = ({
  handleFileChange,
  handleTextChange,
  handleApiKeyChange,
  handleModelChange,
  handleSubmit,
  topic,
  apiKey,
  ttsModel,
  loading,
  error,
}) => {
  return (
    <form
      onSubmit={handleSubmit}
      className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md"
    >
      {error && (
        <div
          className="mb-6 p-4 text-red-700 bg-red-100 border-l-4 border-red-500 rounded"
          role="alert"
        >
          <p>{error}</p>
        </div>
      )}
      <div className="mb-6">
        <label
          className="block text-gray-700 text-sm font-bold mb-2"
          htmlFor="file"
        >
          Upload PDF
        </label>
        <div className="relative">
          <input
            type="file"
            id="file"
            name="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-md file:border-0
              file:text-sm file:font-semibold
              file:bg-blue-50 file:text-blue-700
              hover:file:bg-blue-100
              cursor-pointer border rounded-lg
              focus:outline-none focus:border-blue-500
              transition-colors duration-200"
          />
        </div>
      </div>
      <div className="mb-6">
        <label
          className="block text-gray-700 text-sm font-bold mb-2"
          htmlFor="apiKey"
        >
          OpenAI API Key
        </label>
        <input
          type="password"
          id="apiKey"
          name="apiKey"
          placeholder="Enter your OpenAI API key"
          value={apiKey}
          onChange={handleApiKeyChange}
          className="w-full px-3 py-2 border rounded-lg
            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
            placeholder-gray-400 transition-colors duration-200"
        />
      </div>
      <div className="mb-6">
        <label
          className="block text-gray-700 text-sm font-bold mb-2"
          htmlFor="ttsModel"
        >
          TTS Model
        </label>
        <select
          id="ttsModel"
          name="ttsModel"
          value={ttsModel}
          onChange={handleModelChange}
          className="w-full px-3 py-2 border rounded-lg
            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
            bg-white transition-colors duration-200"
        >
          <option value="tts-1">OpenAI TTS-1</option>
          <option value="kokoro">Kokoro 82M</option>
        </select>
      </div>

      <div className="mb-6">
        <label
          className="block text-gray-700 text-sm font-bold mb-2"
          htmlFor="topic"
        >
          Topic
        </label>
        <input
          type="text"
          id="topic"
          name="topic"
          placeholder="Enter your topic"
          value={topic}
          onChange={handleTextChange}
          className="w-full px-3 py-2 border rounded-lg
            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
            placeholder-gray-400 transition-colors duration-200"
        />
      </div>
      <button
        type="submit"
        disabled={loading}
        className={`w-full mt-4 px-4 py-2 text-white font-semibold rounded-lg shadow-md transition-colors duration-200 
          ${
            loading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 focus:outline-none active:bg-blue-800"
          }`}
      >
        {loading ? (
          <div className="flex items-center justify-center">
            <svg
              className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            Generating...
          </div>
        ) : (
          "Generate Podcast"
        )}
      </button>
    </form>
  );
};

export default Form;
