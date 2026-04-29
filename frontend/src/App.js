import React, { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Upload resume");

    const formData = new FormData();
    formData.append("resume", file);

    setLoading(true);

    const res = await fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      body: formData
    });

    const result = await res.json();
    setData(result);
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>🚀 AI Resume Analyzer</h1>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <br /><br />
      <button onClick={handleUpload}>Analyze</button>

      {loading && <p>Analyzing... ⏳</p>}

      {data && (
        <div className="result">

          <h2>ATS Score: {data.ats_score}%</h2>

          {/* Progress Bar */}
          <div className="progress">
            <div
              className="progress-bar"
              style={{ width: `${data.ats_score}%` }}
            ></div>
          </div>

          <h3>✅ Skills Found</h3>
          <p>{data.found_skills.join(", ")}</p>

          <h3>❌ Missing Skills</h3>
          <p>{data.missing_skills.join(", ")}</p>

          <h3>📊 Section Scores</h3>
          <ul>
            {Object.entries(data.section_scores).map(([k, v]) => (
              <li key={k}>{k}: {v}%</li>
            ))}
          </ul>

          <h3>💡 Suggestions</h3>
          <ul>
            {data.suggestions.map((s, i) => <li key={i}>{s}</li>)}
          </ul>

          <h3>📝 Grammar Issues</h3>
          <ul>
            {data.grammar_issues.length > 0
              ? data.grammar_issues.map((g, i) => <li key={i}>{g}</li>)
              : <li>No major issues</li>}
          </ul>

          <h3>⚡ Action Verb Feedback</h3>
          <ul>
            {data.verb_feedback.length > 0
              ? data.verb_feedback.map((v, i) => <li key={i}>{v}</li>)
              : <li>Good usage of action verbs</li>}
          </ul>

        </div>
      )}
    </div>
  );
}

export default App;