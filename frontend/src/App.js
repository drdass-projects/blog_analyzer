import React, { useState, useEffect } from "react";
import axios from "axios";
import { Loader2, Download, Search, Moon, Sun } from "lucide-react";
import "./App.css";

export default function App() {
  const [keyword, setKeyword] = useState("");
  const [fileNameInput, setFileNameInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [fileName, setFileName] = useState(null);
  const [error, setError] = useState(null);
  const [darkMode, setDarkMode] = useState(true);
  const [blogCount, setBlogCount] = useState(0);

  useEffect(() => {
    document.body.className = darkMode ? "dark" : "light";
  }, [darkMode]);

  const handleFetch = async () => {
    setLoading(true);
    setError(null);
    setFileName(null);
    setBlogCount(0);

    try {
      const res = await axios.get("http://localhost:8000/fetch-and-analyze", {
        params: {
          keyword: keyword,
          filename: fileNameInput.trim(),
        },
      });

      if (res.data.error) {
        setError(res.data.error);
      } else {
        setFileName(res.data.file_name);
        setBlogCount(res.data.total_blogs);
      }
    } catch (err) {
      console.error(err);
      setError("Failed to fetch blogs. Try again.");
    }

    setLoading(false);
  };

  const toggleTheme = () => setDarkMode(!darkMode);

  return (
    <div className="app-container">
      <div className="theme-toggle" onClick={toggleTheme}>
        {darkMode ? <Sun size={20} /> : <Moon size={20} />}
      </div>

      <div className="card">
        <h1 className="title">Blog Analyzer</h1>
        <p className="subtitle">Enter a keyword and optional filename to analyze blogs and export results.</p>

        <div className="input-group">
          <input
            type="text"
            placeholder="Enter keyword e.g. machine learning"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            className="keyword-input"
          />
          <input
            type="text"
            placeholder="Custom Excel file name (optional)"
            value={fileNameInput}
            onChange={(e) => setFileNameInput(e.target.value)}
            className="keyword-input"
          />
          <button
            onClick={handleFetch}
            disabled={loading || !keyword.trim()}
            className="analyze-btn"
          >
            {loading ? <Loader2 className="spinner" size={18} /> : <Search size={18} />} Analyze
          </button>
        </div>

        {!loading && !fileName && !error && (
          <div style={{ color: "#999", marginTop: "1rem" }}>
            Enter a keyword and press Analyze to begin.
          </div>
        )}

        {fileName && (
          <div className="output success">
            ✅ Found {blogCount} blogs.
            <a
              href={`http://localhost:8000/${fileName}`}
              download={fileName}
              style={{ marginLeft: "10px", textDecoration: "underline", color: "#93c5fd" }}
            >
              <Download size={18} /> Download Excel
            </a>
          </div>
        )}

        {error && (
          <div className="output error">{error}</div>
        )}
      </div>
    </div>
  );
}
