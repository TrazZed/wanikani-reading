import React, { useState } from "react";
import axios from "axios";

function App() {
  const [apiKey, setApiKey] = useState("");
  const [isValidKey, setIsValidKey] = useState(false);
  const [error, setError] = useState("");
  const [vocabCharacters, setVocabCharacters] = useState([]);

  const validateApiKey = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/validate_key", { api_key: apiKey });

      if (response.data.valid) {
        setIsValidKey(true);
        setError("");
        fetchVocabulary();
      } else {
        setError("Invalid API key. Please try again.");
      }
    } catch (err) {
      setError("Error validating API key.");
    }
  };

  const fetchVocabulary = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/fetch_vocabulary", { api_key: apiKey });
      const vocabList = response.data;
      
      if (!Array.isArray(vocabList)) {
        setError("Invalid response from API.");
        return;
      }

      const characters = vocabList.map(entry => entry.data.characters);
      setVocabCharacters(characters);
      setError(""); // Clear any previous error
    } catch (err) {
      setError("Error fetching vocabulary.");
    }
  };

  return (
    <div>
      {!isValidKey ? (
        <div>
          <h2>Enter your WaniKani API Key</h2>
          <input
            type="text"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Enter API key"
          />
          <button onClick={validateApiKey}>Validate</button>
          {error && <p style={{ color: "red" }}>{error}</p>}
        </div>
      ) : (
        <div>
          <h1>WaniKani Reader</h1>
          {error && <p style={{ color: "red" }}>{error}</p>}
          <h3>Vocabulary Characters:</h3>
          <ul>
            {vocabCharacters.map((char, index) => (
              <li key={index}>{char}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
