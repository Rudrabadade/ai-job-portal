from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def calculate_match(resume, job_description):

    resume = resume.lower()
    job_description = job_description.lower()

    common_skills = [

        "python",
        "java",
        "c++",
        "javascript",
        "html",
        "css",
        "react",
        "react.js",
        "node",
        "node.js",
        "sql",
        "postgresql",
        "postgres",
        "postgres sql",
        "mysql",
        "mongodb",
        "fastapi",
        "django",
        "flask",
        "machine learning",
        "deep learning",
        "pandas",
        "numpy",
        "git",
        "github",
        "docker",
        "aws",
        "rest api",
        "api",
        "bootstrap"

    ]

    required_skills = []
    matched_skills = []

    # Required skills from job description
    for skill in common_skills:

        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, job_description):
            required_skills.append(skill)

    # Skills matched in resume
    for skill in required_skills:

        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, resume):
            matched_skills.append(skill)

    # Skill score = 70%
    if required_skills:
        skill_score = (
            len(matched_skills)
            /
            len(required_skills)
        ) * 70

    else:
        skill_score = 0


    # Similarity score = 30%
    documents = [
        resume,
        job_description
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1,2)
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0],
        tfidf_matrix[1]
    )[0][0]

    similarity_score = similarity * 30

    final_score = skill_score + similarity_score

    return {

        "score": round(
            min(final_score,100),
            2
        ),

        "matched_skills": matched_skills

    }