from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
from pydantic import BaseModel
import shutil
import os
from pathlib import Path

# Resolve project root (parent of backend/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Ensure resumes directory exists
os.makedirs(BASE_DIR / "resumes", exist_ok=True)

app = FastAPI()
app.mount(
    "/resumes",
    StaticFiles(directory=str(BASE_DIR / "resumes")),
    name="resumes"
)

from backend.resume_matcher import calculate_match
from backend.resume_ranker import rank_resumes
from backend.text_extractor import extract_text
from backend.database import (
    get_job_by_id,
    get_connection,
    save_ranking,
    save_job,
    get_all_jobs,
    register_user,
    login_user,
    apply_job,
    get_user_applications,
    save_candidate,
    update_match_score,
    get_candidates_by_job,
    update_candidate_status
)




# Job Model
class JobCreate(BaseModel):
    title: str
    description: str
    skills: str
    recruiter_name: str


# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home Route — serve login page
@app.get("/")
def home():
    return FileResponse(str(BASE_DIR / "login.html"))


# Resume Match API
@app.post("/match")
def match_resume(
    resume: str,
    job_description: str
):

    result = calculate_match(
        resume,
        job_description
    )
    score = float(result["score"])

    return {
        "match_score": score
    }


# Upload Single Resume
@app.post("/upload_resume")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    try:

        resume_text = extract_text(file)

        result = calculate_match(
            resume_text,
            job_description
        )
        score = float(result["score"])

        save_ranking(
            file.filename,
            score,
            job_description
        )

        return {
            "filename": file.filename,
            "match_score": score
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# Rank Resumes From Folder
@app.post("/rank_resumes")
def rank_all_resumes(
    job_description: str
):

    results = rank_resumes(job_description)

    return {
        "rankings": results
    }


# Upload Multiple Resumes And Rank Them
@app.post("/rank_uploaded_resumes")
async def rank_uploaded_resumes(
    job_description: str = Form(...),
    files: List[UploadFile] = File(...)
):

    print("\n===== DEBUG INFO =====")
    print("Number of files received:", len(files))

    results = []

    for file in files:

        print("\nProcessing file:", file.filename)

        try:

            resume_text = extract_text(file)

            print("Text extracted successfully")

            result = calculate_match(
                resume_text,
                job_description
            )
            score = float(result["score"])

            save_ranking(
                file.filename,
                score,
                job_description
            )

            print("Match score:", score)

            results.append({
                "filename": file.filename,
                "match_score": score
            })

        except Exception as e:

            print("ERROR:", e)

            results.append({
                "filename": file.filename,
                "error": str(e)
            })

    results.sort(
        key=lambda x: x.get("match_score", 0),
        reverse=True
    )

    return {
        "rankings": results
    }


# Create New Job
@app.post("/jobs")
def create_job(job: JobCreate):

    try:

        save_job(
            job.title,
            job.description,
            job.skills,
            job.recruiter_name
        )

        return {
            "message": "Job Posted Successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# View All Jobs
@app.get("/jobs")
def view_jobs():

    try:

        jobs = get_all_jobs()

        results = []

        for job in jobs:

            results.append({
                "id": job[0],
                "title": job[1],
                "description": job[2],
                "skills": job[3],
                "recruiter_name": job[4],
                "status": job[5],
                "created_at": str(job[6])
            })

        return {
            "jobs": results
        }

    except Exception as e:

        return {
            "error": str(e)
        }
# Database Connection Test
@app.get("/test_db")
def test_db():

    try:

        conn = get_connection()

        conn.close()

        return {
            "message": "Database Connected Successfully"
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# View All Rankings
@app.get("/rankings")
def get_rankings():

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                filename,
                match_score,
                job_description,
                created_at
            FROM rankings
            ORDER BY match_score DESC
            """
        )

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        rankings = []

        for row in rows:

            rankings.append({
                "id": row[0],
                "filename": row[1],
                "match_score": float(row[2]),
                "job_description": row[3],
                "created_at": str(row[4])
            })

        return {
            "rankings": rankings
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# Test Upload Endpoint
@app.post("/register")
async def register(

    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)
):

    try:

        register_user(
            full_name,
            email,
            password,
            role
        )

        return {
            "message":"User registered successfully"
        }

    except Exception as e:

        print("REGISTER ERROR:", e)

        return {
            "message": f"Registration failed: {str(e)}"
        }


@app.post("/login")
async def login(

    email: str = Form(...),
    password: str = Form(...)
):

    user = login_user(
        email,
        password
    )

    if user:

        return {

            "message":"Login successful",
            "user_id":user[0],
            "full_name":user[1],
            "role":user[4]

        }

    return {

        "message":"Invalid email or password"

    }

@app.post("/job_apply")
async def apply(

    user_id: int = Form(...),
    job_id: int = Form(...)
):

    apply_job(
        user_id,
        job_id
    )

    return {
        "message": "Job applied successfully"
    }

@app.get("/my_applications")
async def my_applications(user_id: int):

    jobs = get_user_applications(user_id)

    results = []

    for job in jobs:

        results.append({
            "job_id": job[0],
            "title": job[1],
            "description": job[2],
            "skills": job[3]
        })

    return {
        "applications": results
    }

@app.post("/apply")
async def upload_candidate_application(

    name: str = Form(...),
    job_id: int = Form(...),
    resume: UploadFile = File(...),
    user_id: int = Form(None)

):

    import uuid
    import os
    import shutil

    try:

        # Create unique filename
        unique_filename = (

            str(uuid.uuid4())
            + "_"
            + resume.filename.replace(
                " ",
                "_"
            )

        )

        file_path = os.path.join(
            "resumes",
            unique_filename
        )

        # Save uploaded resume
        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                resume.file,
                buffer
            )

        # Get job details
        job = get_job_by_id(
            job_id
        )

        if not job:

            return {

                "message":
                "Job not found"

            }

        job_description = job[2]

        # Extract text from resume
        with open(
            file_path,
            "rb"
        ) as file:

            resume_text = extract_text(
                file
            )

        # AI matching
        result = calculate_match(

            resume_text,
            job_description

        )

        print(
            "FINAL SCORE =",
            result["score"]
        )

        print(
            "MATCHED =",
            result["matched_skills"]
        )

        match_score = float(
            result["score"]
        )

        matched_skills = result[
            "matched_skills"
        ]

        # Save candidate
        save_candidate(

            name,

            ", ".join(
                matched_skills
            ),

            match_score,

            unique_filename,

            job_id

        )

        conn = get_connection()

        cur = conn.cursor()

        # Save application
        cur.execute(
            """
            INSERT INTO applications
            (
                job_id,
                user_id,
                resume_filename,
                match_score,
                status
            )
            VALUES
            (%s,%s,%s,%s,%s)
            """,
            (

                job_id,
                user_id,
                unique_filename,
                match_score,
                "Pending"

            )

        )

        conn.commit()

        cur.close()

        conn.close()

        return {

            "message":
            f"{name} applied successfully",

            "match_score":
            match_score,

            "matched_skills":
            matched_skills

        }

    except Exception as e:

        print(
            "ERROR:",
            e
        )

        return {

            "error":
            str(e)

        }

@app.get("/candidates/{job_id}")
async def view_candidates(job_id: int):

    candidates = get_candidates_by_job(
        job_id
    )

    result=[]

    for c in candidates:

        result.append({

            "id":c[0],

            "name":c[1],

            "matched_skills":c[2],

            "resume_filename":c[3],

            "created_at":str(c[4]),

            "match_score":float(c[5]),

            "status":c[6],

            "job_id":job_id

        })

    return {

        "candidates":result

    }


@app.put("/candidate-status/{candidate_id}")
async def change_candidate_status(
    candidate_id:int,
    status:str
):

    update_candidate_status(
        candidate_id,
        status
    )

    return {

        "message":"Status updated"

    }

# Serve frontend HTML pages
@app.get("/{page_name}.html")
async def serve_page(page_name: str):
    file_path = BASE_DIR / f"{page_name}.html"
    if file_path.exists():
        return FileResponse(str(file_path))
    return {"error": "Page not found"}

# Serve static assets (CSS, JS) — must be mounted LAST
app.mount(
    "/",
    StaticFiles(directory=str(BASE_DIR)),
    name="static"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)