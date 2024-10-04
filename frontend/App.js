import React, { useState } from "react";
import "./App.css"; // Import the new CSS file

function App() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [statusMessage, setStatusMessage] = useState("");
  const [webpageUrl, setWebpageUrl] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (response.ok) {
      setStatusMessage(data.message);
    } else {
      setStatusMessage(`Error: ${data.error}`);
    }
  };

  const handleWebpageSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch("http://127.0.0.1:5000/upload_webpage", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: webpageUrl }),
    });

    const data = await response.json();
    if (response.ok) {
      setStatusMessage(data.message);
    } else {
      setStatusMessage(`Error: ${data.error}`);
    }
  };

  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  };

  const handlePromptSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch("http://127.0.0.1:5000/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    const data = await response.json();
    if (response.ok) {
      setResponse(data.response);
    } else {
      setResponse(`Error: ${data.error}`);
    }
  };

  return (
    <div className="container">
      <h1>Upload a PDF or Enter Webpage URL</h1>

      <form onSubmit={handleFileSubmit}>
        <input type="file" accept=".pdf" onChange={handleFileChange} required />
        <button type="submit">Upload and Process PDF</button>
      </form>

      <form onSubmit={handleWebpageSubmit}>
        <input
          type="text"
          placeholder="Enter webpage URL"
          value={webpageUrl}
          onChange={(e) => setWebpageUrl(e.target.value)}
          required
        />
        <button type="submit">Process Webpage</button>
      </form>

      {statusMessage && <p>{statusMessage}</p>}

      <form onSubmit={handlePromptSubmit}>
        <input
          type="text"
          placeholder="Enter your query"
          value={query}
          onChange={handleQueryChange}
          required
        />
        <button type="submit">Ask</button>
      </form>

      {response && <p>Response: {response}</p>}
    </div>
  );
}

export default App;
