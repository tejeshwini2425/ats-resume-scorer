import { useState, useEffect } from "react";
import { getHistory, getScoreById } from "./api";
import ProgressBar from "./ProgressBar";
import "./App.css";

function History() {
  const [records, setRecords] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getHistory()
      .then(setRecords)
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  async function handleSelect(id) {
    const fullRecord = await getScoreById(id);
    setSelected(fullRecord);
  }

  if (loading) {
    return <p>Loading history...</p>;
  }

  if (records.length === 0) {
    return <p>No scores yet. Score a resume to see history here.</p>;
  }

  return (
    <div style={{ marginTop: 40 }}>
      <h2>History</h2>

      <ul className="history-list">
  {records.map((r) => (
    <li
      key={r.id}
      className="history-item"
      onClick={() => handleSelect(r.id)}
    >
      <span>{r.filename}</span>
      <span>{r.final_score}/100</span>
    </li>
  ))}
</ul>

      {selected && (
        <div className="card">
          <h3>{selected.filename}</h3>

          <div className="final-score">
            {selected.final_score} / 100
          </div>

          <ProgressBar
            label="Keyword Match"
            value={selected.breakdown.keyword_match.score}
          />

          <ProgressBar
            label="Structure"
            value={selected.breakdown.structure.score}
          />

          <ProgressBar
            label="Semantic Similarity"
            value={selected.breakdown.semantic_similarity.score}
          />
        </div>
      )}
    </div>
  );
}

export default History;