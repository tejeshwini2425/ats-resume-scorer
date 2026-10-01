import re
from sentence_transformers import SentenceTransformer, util

_model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_keywords(text: str) -> set:
    text = text.lower()

    words = re.findall(r"[a-zA-Z][a-zA-Z0-9\+\#\.]*[a-zA-Z0-9\+\#]", text)

    stopwords = {
    "the", "a", "an", "and", "or", "is", "are", "was", "were",
    "to", "of", "in", "on", "for", "with", "as", "by", "at",
    "this", "that", "be", "will", "we", "you", "our", "your",
    "have", "has", "had", "its", "it", "such", "them", "they",
    "through", "under", "very", "while", "within", "both", "from",
    "not", "can", "all", "any", "more", "most", "other", "than",
    "then", "so", "if", "but", "about", "into", "over", "these",
    "those", "their", "there", "here", "who", "which"
}

    return {
        word for word in words
        if word not in stopwords and len(word) > 2
    }


def keyword_match_score(resume_text: str, job_description: str) -> dict:
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_description)

    if not jd_keywords:
        return {
            "score": 0.0,
            "matched": [],
            "missing": []
        }

    matched = jd_keywords & resume_keywords
    missing = jd_keywords - resume_keywords

    score = len(matched) / len(jd_keywords) * 100

    return {
        "score": round(score, 1),
        "matched": sorted(matched),
        "missing": sorted(missing)
    }

def structure_score(resume_text: str) -> dict:
    text_lower = resume_text.lower()

    checks = {
        "has_email": bool(
            re.search(r"[\w\.-]+@[\w\.-]+\.\w+", resume_text)
        ),
        "has_phone": bool(
            re.search(r"(\+?\d[\d\-\s]{8,}\d)", resume_text)
        ),
        "has_education_section": "education" in text_lower,
        "has_experience_section": any(
            word in text_lower
            for word in ["experience", "internship", "work history"]
        ),
        "has_skills_section": "skills" in text_lower,
        "has_projects_section": "project" in text_lower,
        "reasonable_length": 1500 <= len(resume_text) <= 15000,
    }

    passed = sum(checks.values())
    total = len(checks)
    score = round(passed / total * 100, 1)

    return {
        "score": score,
        "checks": checks
    }

def semantic_similarity_score(
    resume_text: str,
    job_description: str
) -> dict:
    resume_embedding = _model.encode(
        resume_text,
        convert_to_tensor=True
    )

    jd_embedding = _model.encode(
        job_description,
        convert_to_tensor=True
    )

    similarity = util.cos_sim(
        resume_embedding,
        jd_embedding
    )

    score = float(similarity[0][0]) * 100

    return {
        "score": round(score, 1)
    }

def compute_hybrid_score(
    keyword_result: dict,
    structure_result: dict,
    semantic_result: dict
) -> dict:
    KEYWORD_WEIGHT = 0.30
    STRUCTURE_WEIGHT = 0.20
    SEMANTIC_WEIGHT = 0.50

    final_score = (
        keyword_result["score"] * KEYWORD_WEIGHT
        + structure_result["score"] * STRUCTURE_WEIGHT
        + semantic_result["score"] * SEMANTIC_WEIGHT
    )

    return {
        "final_score": round(final_score, 1),
        "breakdown": {
            "keyword_match": {
                "score": keyword_result["score"],
                "weight": KEYWORD_WEIGHT
            },
            "structure": {
                "score": structure_result["score"],
                "weight": STRUCTURE_WEIGHT
            },
            "semantic_similarity": {
                "score": semantic_result["score"],
                "weight": SEMANTIC_WEIGHT
            }
        }
    }