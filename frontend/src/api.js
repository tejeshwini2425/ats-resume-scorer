const API_BASE_URL = "http://127.0.0.1:8000";

export async function scoreResume(file, jobDescription) {
  const formData = new FormData();

  formData.append("file", file);
  formData.append("job_description", jobDescription);

  const response = await fetch(`${API_BASE_URL}/score-resume`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Failed to score resume");
  }

  return response.json();
}

export async function getHistory() {
  const response = await fetch(`${API_BASE_URL}/history`);

  if (!response.ok) {
    throw new Error("Failed to fetch history");
  }

  return response.json();
}

export async function getScoreById(id) {
  const response = await fetch(`${API_BASE_URL}/score/${id}`);

  if (!response.ok) {
    throw new Error("Failed to fetch score");
  }

  return response.json();
}