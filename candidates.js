async function loadCandidates() {

    try {

        const response = await fetch(
            "/candidates"
        );

        const data = await response.json();

        const container =
        document.getElementById(
            "candidateContainer"
        );

        container.innerHTML = "";

        data.candidates.forEach(candidate => {

            container.innerHTML += `

            <div class="card">

            <h3>${candidate.name}</h3>

            <p>
            Skills:
            ${candidate.skills}
            </p>

            <p>
            Experience:
            ${candidate.experience}
            years
            </p>
            <p>
            Match Score:
            ${candidate.match_score.toFixed(2)}%
            </p>
            <p>

            Resume:

            <a href="/resumes/${candidate.resume_filename}"
            target="_blank">

            ${candidate.resume_filename}

            </a>

            </p>
            </div>

            `;

        });

    }

    catch(error){

        console.log(error);

    }

}

loadCandidates();