# 🎯 ATS Resume Scorer

AI-powered resume scoring tool that analyzes how well a resume matches a job description — combining keyword matching, structural analysis, and semantic similarity into a single explainable score.

---

## 📖 About the Project

Most ATS (Applicant Tracking System) checkers give you a single opaque score with no explanation. This project takes a different approach: it breaks the score down into three transparent, independently-computed signals — so instead of just knowing *that* a resume scored 52%, you know *why*.

Built as a full-stack application with a Python/FastAPI backend, a React frontend, PostgreSQL for persistence, and a Hugging Face sentence-embedding model for semantic analysis.

---

## ✨ Features

- 🤖 AI-powered ATS scoring
- 📄 Resume + Job Description analysis
- 🔑 Keyword matching
- 📐 Resume structure analysis
- 🧠 Semantic similarity using Sentence Transformers
- ⚡ FastAPI backend
- ⚛️ React frontend
- 🐘 PostgreSQL database
- 📊 Score history

---

## 🧮 How the ATS Score is Calculated

The final score is a **weighted hybrid** of three independent signals:

| Signal | Weight | What it measures |
|---|---|---|
| **Keyword Match** | 30% | Exact overlap between resume and job description keywords |
| **Structure Score** | 20% | Presence of key resume sections (contact info, education, experience, skills, projects) and reasonable length |
| **Semantic Similarity** | 50% | Conceptual similarity between resume and job-description text using sentence embeddings (`all-MiniLM-L6-v2`) |



Each sub-score, along with matched/missing keywords, is returned in the API response for full transparency.

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

### Frontend
- React
- Vite
- JavaScript
- CSS

### AI / NLP
- Hugging Face Sentence Transformers
- `all-MiniLM-L6-v2`
- Text embeddings for semantic similarity
- pypdf / python-docx for resume text extraction

---

## 🏗️ Project Architecture

```text
ats-resume-scorer/
│
├── backend/
│   ├── main.py            # FastAPI app & routes
│   ├── database.py        # DB connection setup
│   ├── models.py          # SQLAlchemy models
│   ├── resume_parser.py   # PDF/DOCX text extraction
│   └── scoring.py         # Keyword, structure, semantic & hybrid scoring logic
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── UploadForm.jsx
│   │   ├── History.jsx
│   │   ├── ProgressBar.jsx
│   │   ├── api.js
│   │   └── App.css
│   └── ...
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔄 How It Works

1. The user uploads a resume in PDF or DOCX format.
2. The user enters a target job description.
3. The backend extracts the resume text.
4. The system calculates:
   - Keyword Match Score
   - Resume Structure Score
   - Semantic Similarity Score
5. The three scores are combined using the weighted scoring formula.
6. The result is displayed through the React frontend.
7. The score is stored in PostgreSQL and can be viewed later through the History section.

---

## 📊 Example Score Breakdown

```text
Final Score
50.7 / 100

Keyword Match
17.8%

Structure
100%

Semantic Similarity
50.7%
```

The individual scores help explain which parts of the resume contributed to the overall result.

---

## 🚀 Running the Project Locally

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL

### 1. Clone the repository

```bash
git clone https://github.com/tejeshwini2425/ats-resume-scorer.git
cd ats-resume-scorer
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install backend dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ats_scorer
```

> Do not commit `.env` to GitHub. It is included in `.gitignore`.

### 5. Create the database

```powershell
psql -U postgres -c "CREATE DATABASE ats_scorer;"
```

### 6. Start the backend

```powershell
uvicorn backend.main:app --reload
```

Backend: `http://127.0.0.1:8000`
API docs: `http://127.0.0.1:8000/docs`

### 7. Start the frontend

Open another terminal:

```powershell
cd frontend
npm install
npm.cmd run dev
```

Frontend: `http://localhost:5173/`

---

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check that the API is running |
| GET | `/health` | Health check |
| POST | `/upload-resume` | Upload and parse a resume |
| POST | `/score-resume` | Score a resume against a job description |
| GET | `/history` | Retrieve previous scores |
| GET | `/score/{score_id}` | Retrieve a specific score |

Interactive API documentation is available through FastAPI Swagger UI at `http://127.0.0.1:8000/docs`

---

## 🔐 Security

Sensitive configuration is stored using environment variables. The repository ignores:

```text
.env
venv/
node_modules/
__pycache__/
*.pyc
frontend/dist/
```

Database credentials are kept outside the source code and are never committed to the repository.

---

## 📸 Screenshots
### Resume Scoring

![Resume Scoring](screenshots/Screenshot1.png)

### Score Result

![Score Result](screenshots/screenshot2%20.png)



## 🔮 Future Improvements

- Better keyword extraction and normalization
- Missing-skill recommendations
- Resume section-specific scoring
- User authentication
- Deployment to a cloud platform
- More detailed score history and analytics

---

## 🎓 What I Learned

Through this project, I worked with:

- REST API development using FastAPI
- React frontend development
- PostgreSQL database integration
- SQLAlchemy ORM
- NLP and sentence embeddings
- Resume text extraction
- Hybrid scoring systems
- API integration between frontend and backend
- Environment variable management
- Git and GitHub version control

---

## 👩‍💻 Author

**Tejeshwini Rajendran**
B.Tech — Computer Science (Data Science)

[LinkedIn](https://linkedin.com/in/tejeshwini2425) · [GitHub](https://github.com/tejeshwini2425)

---

## ⭐ Project

If you find this project useful, feel free to star the repository.



