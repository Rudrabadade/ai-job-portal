document.getElementById("applyForm")
.addEventListener("submit", async function(event){

event.preventDefault();

const name =
document.getElementById("name").value;

const skills =
document.getElementById("skills").value;

const experience =
document.getElementById("experience").value;

const resume =
document.getElementById("resume").files[0];

const urlParams =
new URLSearchParams(window.location.search);

const jobId =
urlParams.get("job_id");

const formData = new FormData();

formData.append("name", name);
formData.append("skills", skills);
formData.append("experience", experience);
formData.append("resume", resume);
formData.append("job_id", jobId);

try{

const response = await fetch(
"http://127.0.0.1:8000/apply",
{
method:"POST",
body:formData
}
);

const data = await response.json();

alert(data.message);

}

catch(error){

console.log(error);

alert("Error while applying");

}

});