document.addEventListener("DOMContentLoaded", async function () {

    const jobsContainer =
        document.getElementById("jobsContainer");

    try {

        const response = await fetch(
            "/jobs"
        );

        const data = await response.json();

        let output = "";

        data.jobs.forEach(function(job) {

           output += `
    <div class="job-card">

        <h3>${job.title}</h3>

        <p>
            <strong>Description:</strong>
            ${job.description}
        </p>

        <p>
            <strong>Skills:</strong>
            ${job.skills}
        </p>

        <p>
            <strong>Recruiter:</strong>
            ${job.recruiter_name}
        </p>

        <p>
            <strong>Status:</strong>
            ${job.status}
        </p>

        <button
            class="apply-btn"
            onclick="applyJob(${job.id})"
        >
            Apply Now
        </button>

    </div>
`;
        });

        jobsContainer.innerHTML = output;

    } catch (error) {

        console.log(error);

        jobsContainer.innerHTML =
            "Error loading jobs";
    }

});
function applyJob(jobId)
{
    localStorage.setItem(
        "selectedJobId",
        jobId
    );

    window.location.href =
        "apply.html";
}