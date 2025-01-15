import React from "react";
import { useState } from "react";

const Form = ({ handleFileChange, handleTextChange, handleSubmit, topic }) => {
  return (
    <form onSubmit={handleSubmit}>
      <input
        type="file"
        name="file"
        accept=".pdf"
        onChange={handleFileChange}
      />
      <div>
        <label>Topic:</label>
        <input
          type="text"
          name="topic"
          placeholder="Topic"
          value={topic}
          onChange={handleTextChange}
        />
      </div>
      <button type="submit">Generate Podcast</button>
    </form>
  );
};

export default Form;
