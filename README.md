# 🤖 AI Job Portal

An intelligent job portal powered by **AI-based resume matching**. Recruiters can post jobs, and candidates can apply by uploading their resumes. The system automatically scores and ranks resumes using **TF-IDF + Cosine Similarity** against the job description.

---

## ✨ Features

- 📋 **Job Posting** – Recruiters can post jobs with title, description, and required skills
- 📄 **Resume Upload** – Candidates upload PDF/TXT resumes when applying
- 🤖 **AI Resume Matching** – Automatically scores how well a resume matches the job (0–100%)
- 🏆 **Candidate Ranking** – Candidates ranked by AI match score per job
- ✅ **Status Management** – Recruiters can Shortlist or Reject candidates
- 👤 **Role-based Login** – Separate dashboards for Recruiters and Job Seekers

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| Database | PostgreSQL |
| AI Matching | scikit-learn (TF-IDF + Cosine Similarity) |
| PDF Parsing | pypdf |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Auth | Form-based login with localStorage |

---

## 📁 Project Structure

```
ai-job-portal/
├── backend/               # FastAPI backend
│   ├── __init__.py
│   ├── main.py            # All API routes
│   ├── database.py        # PostgreSQL connection & queries
│   ├── resume_matcher.py  # AI skill matching + TF-IDF scoring
│   ├── resume_ranker.py   # Rank resumes from folder
│   └── text_extractor.py  # Extract text from PDF/TXT files
│
├── model/                 # Test/utility scripts for AI model
│   ├── ranker.py
│   └── test_*.py
│
├── resumes/               # Uploaded resume files (git-ignored)
│   └── .gitkeep
│
├── database/              # Database scripts placeholder
│   └── .gitkeep
│
├── jobs/                  # Sample job text files
│   └── job1.txt
│
├── app/                   # Mirror of frontend (Flask-style layout)
│   ├── templates/         # HTML templates
│   └── static/            # CSS / JS assets
│
├── index.html             # Register page
├── login.html             # Login page
├── recruiter_dashboard.html
├── jobseeker_dashboard.html
├── apply.html             # Job application form
├── candidates.html        # Candidates view
├── my_applications.html   # Job seeker's applications
├── job.html               # Single job view
├── script.js              # Shared JS
├── style.css              # Shared CSS
│
├── requirements.txt       # Full pinned dependencies (generated)
├── requirements-core.txt  # Core direct dependencies (minimal)
├── .env.example           # Environment variable template
└── .gitignore
```

---

## 🚀 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Rudrabadade/ai-job-portal.git
cd ai-job-portal
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements-core.txt
```

### 4. Configure environment variables

Copy the example env file and fill in your PostgreSQL credentials:

```bash
copy .env.example .env
```

Edit `.env`:
```
DB_HOST=localhost
DB_NAME=ai_resume_ranker
DB_USER=postgres
DB_PASSWORD=your_actual_password
DB_PORT=5432
```

### 5. Set up the PostgreSQL database

Create the database and tables. You need these tables:

```sql
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    skills TEXT,
    recruiter_name VARCHAR(255),
    status VARCHAR(50) DEFAULT 'Open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE job_seekers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    skills TEXT,
    match_score NUMERIC(5,2),
    resume_filename VARCHAR(500),
    job_id INTEGER REFERENCES jobs(id),
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES jobs(id),
    user_id INTEGER REFERENCES job_seekers(id),
    resume_filename VARCHAR(500),
    match_score NUMERIC(5,2),
    status VARCHAR(50) DEFAULT 'Pending',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rankings (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(500),
    match_score NUMERIC(5,2),
    job_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6. Load environment variables and run the server

```bash
# Load .env variables (PowerShell)
Get-Content .env | ForEach-Object {
    if ($_ -match '^(.+?)=(.*)$') {
        [System.Environment]::SetEnvironmentVariable($Matches[1], $Matches[2])
    }
}

# Start the FastAPI server
uvicorn backend.main:app --reload
```

The API will be available at **http://127.0.0.1:8000**

### 7. Open the frontend

Open `index.html` (Register) or `login.html` (Login) directly in your browser.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/register` | Register a new user |
| POST | `/login` | Login and get user info |
| GET | `/jobs` | Get all jobs |
| POST | `/jobs` | Create a new job |
| POST | `/apply` | Apply to a job (upload resume) |
| GET | `/candidates/{job_id}` | Get candidates for a job |
| PUT | `/candidate-status/{candidate_id}` | Update candidate status |
| GET | `/my_applications` | Get a user's job applications |
| GET | `/rankings` | Get all resume rankings |
| GET | `/test_db` | Test database connection |

**Interactive API docs**: http://127.0.0.1:8000/docs

---

## 🧠 How AI Matching Works

The resume scoring uses a **two-part scoring system**:

1. **Skill Score (70%)** — Extracts required skills from the job description and checks how many are present in the resume. Score = `(matched_skills / required_skills) × 70`

2. **Similarity Score (30%)** — Uses TF-IDF vectorization and cosine similarity between the full resume text and job description. Score = `cosine_similarity × 30`

**Final Score** = Skill Score + Similarity Score (capped at 100%)

---

## ⚠️ Notes

- Uploaded resume files in `resumes/` are **git-ignored** to protect personal data
- Never commit your `.env` file — use `.env.example` as a template
- The `app/` directory mirrors the root-level HTML files (Flask-style layout) — root files are the active ones
- The `model/` directory contains test/utility scripts for AI model development

---

## 📄 License

This project is open source and available for educational use.
