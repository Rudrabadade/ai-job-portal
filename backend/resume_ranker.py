import os
from backend.resume_matcher import calculate_match

def rank_resumes(job_description):
    
    results = []

    resumes_folder = "resumes"

    for filename in os.listdir(resumes_folder): #os.listdir() return all files inside folder

        if filename.endswith(".txt"):

            filepath = os.path.join(resumes_folder, filename)

            with open(filepath, "r", encoding="utf-8") as file:
                resume_text = file.read()

            result = calculate_match(
                resume_text,
                job_description
            )

            results.append({
                "filename": filename,
                "match_score": float(result["score"])
            })

    results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return results