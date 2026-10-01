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