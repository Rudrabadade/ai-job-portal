async function loadJobs(){

    try{

        const response = await fetch(
            "/jobs"
        );

        const data = await response.json();

        let html = "";

        data.jobs.forEach(job=>{

            html += `

            <div class="job-card">

                <h2>${job.title}</h2>

                <p>${job.description}</p>

                <p>
                    <b>Skills:</b>
                    ${job.skills}
                </p>

                <p>
                    <b>Recruiter:</b>
                    ${job.recruiter_name}
                </p>

                <input
                    type="file"
                    id="resume${job.id}"
                >

                <button onclick="applyJob(${job.id})">
                    Apply
                </button>

            </div>

            `;

        });

        document.getElementById(
            "jobs"
        ).innerHTML = html;

    }

    catch(error){

        console.log(error);

        alert("Error loading jobs");

    }

}

async function applyJob(jobId){

    try{

        const fileInput =
        document.getElementById(
            "resume"+jobId
        );

        if(fileInput.files.length===0){

            alert(
                "Please upload resume"
            );

            return;

        }

        const formData =
        new FormData();

        formData.append(
            "name",
            localStorage.getItem(
                "full_name"
            )
        );

        formData.append(
            "skills",
            ""
        );

        formData.append(
            "experience",
            0
        );

        formData.append(
            "job_id",
            jobId
        );

        formData.append(
            "resume",
            fileInput.files[0]
        );

        formData.append(
            "user_id",
            localStorage.getItem("user_id")
        );

        const response =
        await fetch(
            "/apply",
            {
                method:"POST",
                body:formData
            }
        );

        const data =
        await response.json();

        if(response.ok){

            alert(data.message);

        }

        else{

            alert(JSON.stringify(data));

        }

    }

    catch(error){

        console.log(error);

        alert("Application failed");

    }

}

function logout(){

    localStorage.clear();

    window.location.href =
    "login.html";

}

loadJobs();