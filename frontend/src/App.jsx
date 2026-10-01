import { useState } from "react";
import UploadForm from "./UploadForm";
import History from "./History";
import ProgressBar from "./ProgressBar";
import "./App.css";

function App() {
  const [scoreData, setScoreData] = useState(null);
  const [view, setView] = useState("score");

  return (
    <div className="app-container">
      <h1>ATS Resume Scorer</h1>
      <p className="subtitle">
  Analyze your resume against a job description using AI-powered scoring.
</p>
<br>
</br>
      <div className="tabs">
        <button
          className="tab-button"
          onClick={() => setView("score")}
          disabled={view === "score"}
        >
          Score a Resume
        </button>

        <button
          className="tab-button"
          onClick={() => setView("history")}
          disabled={view === "history"}
        >
          View History
        </button>
      </div>

      {view === "score" && (
        <>
          <UploadForm onScoreComplete={setScoreData} />

          {scoreData && (
            <div className="card">
              <div className="final-score">
                {scoreData.final_score} / 100
              </div>

              <ProgressBar
                label="Keyword Match"
                value={scoreData.breakdown.keyword_match.score}
              />

              <ProgressBar
                label="Structure"
                value={scoreData.breakdown.structure.score}
              />

              <ProgressBar
                label="Semantic Similarity"
                value={
                  scoreData.breakdown.semantic_similarity.score
                }
              />
            </div>
          )}
        </>
      )}

      {view === "history" && <History />}
    </div>
  );
}

export default App;