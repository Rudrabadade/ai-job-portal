from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Read job description file
with open("jobs/job1.txt", "r") as file:
    job_description = file.read()

# Read resume1.txt
with open("resumes/resume1.txt", "r") as file:
    resume1 = file.read()

# Read resume2.txt
with open("resumes/resume2.txt", "r") as file:
    resume2 = file.read()

documents = [job_description, resume1, resume2]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

job_vector = tfidf_matrix[0]

score1 = cosine_similarity(job_vector, tfidf_matrix[1])[0][0]
score2 = cosine_similarity(job_vector, tfidf_matrix[2])[0][0]

print("Rudra Score:", score1 * 100)
print("Amit Score:", score2 * 100)