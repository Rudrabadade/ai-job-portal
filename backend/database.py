import psycopg2
import os


def get_connection():

    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "ai_resume_ranker"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", ""),
        port=os.environ.get("DB_PORT", "5432")
    )

    return conn


def init_db():
    """Create all required tables if they don't exist."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            description TEXT,
            skills TEXT,
            recruiter_name VARCHAR(255),
            status VARCHAR(50) DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_seekers (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(255),
            email VARCHAR(255) UNIQUE,
            password VARCHAR(255),
            role VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            skills TEXT,
            match_score NUMERIC(5,2),
            resume_filename VARCHAR(500),
            job_id INTEGER REFERENCES jobs(id),
            status VARCHAR(50) DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id SERIAL PRIMARY KEY,
            job_id INTEGER REFERENCES jobs(id),
            user_id INTEGER REFERENCES job_seekers(id),
            resume_filename VARCHAR(500),
            match_score NUMERIC(5,2),
            status VARCHAR(50) DEFAULT 'Pending',
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rankings (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(500),
            match_score NUMERIC(5,2),
            job_description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("Database tables initialized successfully")


def save_ranking(
    filename,
    match_score,
    job_description
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO rankings (filename, match_score, job_description)
        VALUES (%s, %s, %s)
        """,
        (
            filename,
            match_score,
            job_description
        )
    )

    conn.commit()

    cursor.close()

    conn.close()


def save_job(
    title,
    description,
    skills,
    recruiter_name
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO jobs (
            title,
            description,
            skills,
            recruiter_name
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            title,
            description,
            skills,
            recruiter_name
        )
    )

    conn.commit()

    cursor.close()

    conn.close()


def get_all_jobs():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            description,
            skills,
            recruiter_name,
            status,
            created_at
        FROM jobs
        ORDER BY created_at DESC
        """
    )

    jobs = cursor.fetchall()

    cursor.close()

    conn.close()

    return jobs


def get_job_by_id(job_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM jobs
        WHERE id = %s
        """,
        (job_id,)
    )

    job = cursor.fetchone()

    cursor.close()
    conn.close()

    return job


def register_user(
    full_name,
    email,
    password,
    role
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO job_seekers
        (
            full_name,
            email,
            password,
            role
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            full_name,
            email,
            password,
            role
        )
    )

    conn.commit()

    cursor.close()
    conn.close()


def login_user(email, password):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM job_seekers
        WHERE email=%s
        AND password=%s
        """,
        (
            email,
            password
        )
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


def apply_job(user_id, job_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO applications
        (user_id, job_id)
        VALUES (%s, %s)
        """,
        (user_id, job_id)
    )

    conn.commit()

    cursor.close()

    conn.close()


def get_user_applications(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            jobs.id,
            jobs.title,
            jobs.description,
            jobs.skills
        FROM applications
        JOIN jobs
        ON applications.job_id = jobs.id
        WHERE applications.user_id = %s
        """,
        (user_id,)
    )

    jobs = cursor.fetchall()

    cursor.close()

    conn.close()

    return jobs


def save_candidate(
    name,
    skills,
    match_score,
    resume_filename,
    job_id
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO candidates
        (
            name,
            skills,
            match_score,
            resume_filename,
            job_id
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """,
    (
        name,
        skills,
        match_score,
        resume_filename,
        job_id
    ))

    candidate_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return candidate_id


def get_candidates_by_job(job_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            skills,
            resume_filename,
            created_at,
            match_score,
            status
        FROM candidates
        WHERE job_id=%s
        ORDER BY match_score DESC
        """,
        (job_id,)
    )

    candidates = cursor.fetchall()

    cursor.close()
    conn.close()

    return candidates


def update_match_score(
    candidate_id,
    score
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE candidates
        SET match_score = %s
        WHERE id = %s
        """,
        (
            score,
            candidate_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()


def get_candidate_status(
    candidate_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status
        FROM candidates
        WHERE id=%s
        """,
        (candidate_id,)
    )

    status = cursor.fetchone()

    cursor.close()
    conn.close()

    return status


def update_candidate_status(
    candidate_id,
    status
):

    conn = get_connection()
    cursor = conn.cursor()

    # Update candidates table
    cursor.execute(
        """
        UPDATE candidates
        SET status=%s
        WHERE id=%s
        """,
        (
            status,
            candidate_id
        )
    )

    # Get resume filename of that candidate
    cursor.execute(
        """
        SELECT resume_filename
        FROM candidates
        WHERE id=%s
        """,
        (candidate_id,)
    )

    result = cursor.fetchone()

    if result:

        resume_filename = result[0]

        # Update applications table too
        cursor.execute(
            """
            UPDATE applications
            SET status=%s
            WHERE resume_filename=%s
            """,
            (
                status,
                resume_filename
            )
        )

    conn.commit()

    cursor.close()
    conn.close()

    return True