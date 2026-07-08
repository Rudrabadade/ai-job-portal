from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Read Job Description
with open("jobs/job1.txt", "r") as file:
    job_description = file.read()

# Get all resume files
resume_files = os.listdir("resumes")

# Read all resumes
resumes = []

for file_name in resume_files:

    with open("resumes/" + file_name, "r") as file:
        resumes.append(file.read())

# Combine job + resumes
documents = [job_description] + resumes

# TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

job_vector = tfidf_matrix[0]

# Calculate scores
for i in range(1, len(documents)):

    score = cosine_similarity(
        job_vector,
        tfidf_matrix[i]
    )[0][0]

    print(
        resume_files[i-1],
        "Score:",
        round(score * 100, 2),
        "%"
    )