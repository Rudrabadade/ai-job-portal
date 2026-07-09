document.addEventListener("DOMContentLoaded", function () {

    const rankBtn = document.getElementById("rankBtn");

    rankBtn.addEventListener("click", async function (event) {

        event.preventDefault();



        const jobDescription =
            document.getElementById("jobDescription").value;

        const fileInput =
            document.getElementById("resumes");

        const resultsDiv =
            document.getElementById("results");

        if (jobDescription.trim() === "") {
            resultsDiv.innerHTML =
                "⚠️ Please enter a job description";
            return;
        }

        if (fileInput.files.length === 0) {
            resultsDiv.innerHTML =
                "⚠️ Please upload at least one resume";
            return;
        }

        resultsDiv.innerHTML =
            "🔍 Processing resumes...";

        const formData = new FormData();

        formData.append(
            "job_description",
            jobDescription
        );

        for (let i = 0; i < fileInput.files.length; i++) {
            formData.append(
                "files",
                fileInput.files[i]
            );
        }

        try {

            const response = await fetch(
                "/rank_uploaded_resumes",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();

           

            let output =
                "<h3>🏆 Resume Rankings</h3>";

            data.rankings.forEach(function (item) {

                output += `
                    <div>
                        <b>${item.filename}</b>
                        <br>
                        Score:
                        ${item.match_score}%
                    </div>
                    <hr>
                `;
            });

            resultsDiv.innerHTML = output;

        } catch (error) {

            console.log(error);

            resultsDiv.innerHTML =
                "❌ Error connecting to backend";
        }

    });

});
window.addEventListener("beforeunload", function () {
    console.log("PAGE IS RELOADING");
});