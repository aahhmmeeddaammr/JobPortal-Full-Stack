let currjob =localStorage.getItem('dJob')
let CurrUser=localStorage.getItem("user_id");

async function GetDetailsFromServer(){
    console.log(currjob);
    let ress=await fetch(`http://127.0.0.1:8000/api/details/${currjob}`)
    let data=await ress.json();
    console.log(data.JOB);
    displayDetails(data.JOB)
}
GetDetailsFromServer();
function displayDetails(Job){
    let Experience_Needed=document.getElementById('Experience_Needed')
    let Career_level=document.getElementById('Career_level')
    let title=document.getElementById('title')
    let Education_level=document.getElementById('Education_level')
    let Salary=document.getElementById('Salary')
    let Job_Categories=document.getElementById('Job_Categories')
    let Description=document.getElementById('Description')
    let des_job=document.getElementById('job-des')
    let Requirements=document.getElementById('Requirements')
    let skills=document.getElementById('skills')
    let sk=Job.skills
    let newskill=""
    let Sbtn=document.getElementById('Sbtn');
    console.log(currjob==Job.job.postedBy);
    if(CurrUser==Job.job.postedBy){
        Sbtn.addEventListener('click',GoToAllApply)
        document.getElementById("t").innerText="View All Apply"
    }else{
        Sbtn.addEventListener('click',GoToApply)
        document.getElementById("t").innerText="Apply"
    }
    for (let i = 0; i < sk.length; i++) {
        newskill+=(`<p class="skill">${sk[i].name}</p>`)
    }
    skills.innerHTML=newskill;
    des_job.innerHTML=`<p class="d">Full Time</p><p class="d">On-Site</p>`;
    title.innerHTML=Job.job.name
    Experience_Needed.innerHTML=`More than ${Job.job.experience} Year(s)`
    Career_level.innerHTML=`Mid-Level`
    Education_level.innerHTML=`Bachelor Degree`
    Salary.innerHTML=Job.job.salary
    Job_Categories.innerHTML=Job.job.category
    Description.innerHTML=Job.job.description
}
function GoToApply(){
    localStorage.setItem("Applyin",currjob);
    location.href="../Application_page/Apply.html"
}
function GoToAllApply(){
    localStorage.setItem("Ajob",currjob);
    location.href="../APPLAY/index.html"
}
