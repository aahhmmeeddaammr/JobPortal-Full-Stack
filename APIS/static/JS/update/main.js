let currentJob=JSON.parse(localStorage.getItem("update"));
let JobNameinput=document.getElementById("JobName");
let JobSalaryinput=document.getElementById("JobSalary");
let JobExpinput=document.getElementById("JobExp")
let JobCompanyinput= document.getElementById("JobCompany")
let JobDescinput=document.getElementById("JobDesc");
let skillc= document.getElementById("skillc")
let jobdesc = document.getElementById("JobDesc");
let jobdescC = document.getElementById("jobdesc-c");
let jobcompany = document.getElementById("JobCompany");
let catArray = JSON.parse(localStorage.getItem("categories"));
let govArray = JSON.parse(localStorage.getItem("governments"));
let currjob=+localStorage.getItem('update')
let btnText = document.querySelector(".btn-text");
let btnTexttwo = document.querySelector(".btn-text-two");
let Skills=[];
GetDataFromServer()

async function GetDataFromServer(){
    let ress=await fetch(`http://127.0.0.1:8000/api/details/${currjob}`)
    let data=await ress.json();
    displayDetails(data.JOB)
}

async function DeleteSkill(id,skill){
     let ress=await fetch(`http://127.0.0.1:8000/api/DeleteSkill/${id}/${skill.name}`,{
          method:"DELETE",
          headers:{
               'content-type': 'application/json'
          }
     }).then(()=>{
          GetDataFromServer()
     })
}

async function UpdateJobInServer(name,location,salary,experience,company,category,description){
     let newjob={
          name:name,
          location:location,
          salary:+salary,
          experience:+experience,
          company:company,
          category:category,
          description:description,
          id:currjob
     }
     let ress=await fetch(`http://127.0.0.1:8000/api/Update`,{
          method:"put",
          headers:{
               'content-type': 'application/json'
          },body:JSON.stringify(newjob)
     }).then(()=>{
          // window.location.href='../Admin jobs/index.html'
     })
}


function displayDetails(Job){
     JobNameinput.value=Job.job.name
     JobSalaryinput.value=Job.job.salary
     JobExpinput.value=Job.job.experience
     JobCompanyinput.value=Job.job.company
     JobDescinput.value=Job.job.description
     btnTexttwo.innerText=Job.job.location
     btnText.innerText=Job.job.category
     Skills=[...Job.skills];
     displayskills(Skills)
}

function displayskills(arr) {
     let data = ``;
     skillc.style.display = "flex"
     for (let i = 0; i < arr.length; i++) {
          data += `<p class="skill"> ${arr[i].name} <i onclick="closes(${i})"  class=" close fa-solid fa-xmark fa-1x"></i></p>`
     }
     skillc.innerHTML = data;
}

function closes(i) {
     DeleteSkill(currjob,Skills[i]);
     Skills.splice(i, 1);
     if (Skills.length == 0) {
          skillc.style.display = "none"
     } else {
          displayskills(Skills)
     }
}

function displaycat() {
     let data = ``;
     for (let i = 0; i < catArray.length; i++) {
          data += `<li class="item">
                    <span class="item-text">${catArray[i].name}</span>
               </li>
          `
     }
     if (data.length) {
          document.getElementById("cat").innerHTML = data;
     }
}

function displaygov() {
     let data = ``;
     for (let i = 0; i < govArray.length; i++) {
          data += `<li class="item-two">
          <span class="item-text">${govArray[i].name}</span>
          </li>`
     }
     if (data.length) {
          document.getElementById("gov").innerHTML = data;
     }
}

displaycat();
displaygov();
const selectBtn = document.querySelector(".select-btn"),
     items = document.querySelectorAll(".item");

selectBtn.addEventListener("click", () => {
     selectBtn.classList.toggle("open");
});

items.forEach(item => {
     item.addEventListener("click", () => {
          item.classList.toggle("checked");
          let checked = document.querySelectorAll(".checked"),
               btnText = document.querySelector(".btn-text");
          if (checked.length >= 1) {
               item.classList.toggle("checked");
               btnText.innerText = checked[0].innerText;
               selectBtn.classList.toggle("open");
          } else if (checked && checked.length == 1) {
               btnText.innerText = checked[0].innerText;
               selectBtn.classList.toggle("open");
          } else {
               btnText.innerText = "Select Category";
          }
     });
})

const selectBtntwo = document.querySelector(".select-btn-two"),
     itemstwo = document.querySelectorAll(".item-two");

selectBtntwo.addEventListener("click", () => {
     selectBtntwo.classList.toggle("open");
});

itemstwo.forEach(item => {
     item.addEventListener("click", () => {
          item.classList.toggle("checkedtwo");
          let checkedtwo = document.querySelectorAll(".checkedtwo"),
               btnTexttwo = document.querySelector(".btn-text-two");
          if (checkedtwo.length >= 1) {
               item.classList.toggle("checkedtwo");
               btnTexttwo.innerText = checkedtwo[0].innerText;
               selectBtntwo.classList.toggle("open");
          } else if (checkedtwo && checkedtwo.length == 1) {
               btnTexttwo.innerText = checkedtwo[0].innerText;
               selectBtntwo.classList.toggle("open");
          } else {
               btnText.innerText = "Select Category";
          }
     });
})

let jreq = "Strong technical programming skills utilizing a variety of different coding languages and tools"
let sub = document.getElementById("submitting");
let newjob =new Object();

sub.addEventListener("click", () => {
     var name=JobNameinput.value;
     var location=btnTexttwo.innerText
     var category=btnText.innerHTML
     var salary=JobSalaryinput.value
     var company=jobcompany.value
     var desc=jobdesc.value
     var experience=JobExpinput.value
     UpdateJobInServer(name,location,salary,experience,company,category,desc)
})
