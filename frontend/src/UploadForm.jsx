import { useState } from "react";
import { scoreResume } from "./api";

function UploadForm({ onScoreComplete }) {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    if (!file) {
      setError("Please select a resume file.");
      return;
    }

    if (!jobDescription.trim()) {
      setError("Please enter a job description.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const data = await scoreResume(file, jobDescription);
      onScoreComplete(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="upload-form"> 
      <div style={{ marginBottom: 20 }}>
        <label>Resume:</label>
        <br />
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={(event) => setFile(event.target.files[0])}
        />
      </div>

      <div style={{ marginBottom: 20 }}>
        <label>Job Description:</label>
        <br />
        <textarea
          rows="10"
          style={{ width: "100%", marginTop: 8 }}
          value={jobDescription}
          onChange={(event) => setJobDescription(event.target.value)}
        />
      </div>

      <button type="submit" disabled={loading}>
        {loading ? "Scoring..." : "Score Resume"}
      </button>

      {error && (
        <p style={{ marginTop: 15 }}>
          {error}
        </p>
      )}
    </form>
  );
}

export default UploadForm;