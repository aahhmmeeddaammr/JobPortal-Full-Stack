

let JobArray=[]
let CatArray = JSON.parse(localStorage.getItem("categories"));
let myJobNode = document.getElementById('myJobList');
let myPageNatorNode = document.getElementById('pagenator');
let myCatNode = document.getElementById('Cat_ID');
let myCareerNode = document.getElementById('careersID');
let currentPage = 0;
let CurrUser=+localStorage.getItem('user_id')

async function GetAllJobsFromServer(){
    let ress =await fetch('http://127.0.0.1:8000/api/');
    let data=await ress.json();
    if (data.Jobs.length != 0) {
        currentPage = 1;
        JobArray=[...data.Jobs]
        updatePagenator()
        displayPageNator();
    } else {
        Cat_ID.innerHTML =
        `<p class="intro2" style="font-size:30px" >No<span > Jobs</span ></p> `;
    }
}
GetAllJobsFromServer();

if(localStorage.getItem("done")){
    document.querySelector(".loading").style=`display:none;`
}else{
    setTimeout(()=>{
        document.querySelector(".loading").style=`display:none;`
    },1500)
    localStorage.setItem("done",1);
}

function displayPageNator() {
    myPageNatorNode.innerHTML = "";
    myPageNatorNode.innerHTML += `<div class="pg ${(currentPage == 1) ? 'pg-disabled' : ''}" onclick="decPage()">
    <i class="fa-solid fa-arrow-left"></i>
    </div>`;
    for (let i = 0; i < JobArray.length; i += 4) {
        myPageNatorNode.innerHTML += `<div class="pg ${(currentPage == ((i / 4) + 1) ? 'pg-clicked' : '')}" onclick="CurrPage(${(i / 4) + 1})")> ${(i / 4) + 1}</div> `;
    }
    myPageNatorNode.innerHTML += `<div class="pg ${(currentPage * 4 >= JobArray.length) ? 'pg-disabled' : ''}" onclick="incPage()" ">
    <i class="fa-solid fa-arrow-right"></i>`;
}

function updatePagenator() {
    myJobNode.innerHTML = ``;
    for (let i = (currentPage - 1) * 4; i < (currentPage * 4) && i < JobArray.length; i++) {
        console.log(JobArray[1])
        myJobNode.innerHTML += `
        <div class="card2">
            <div>
                <h3 onclick="GotoDetails(${JobArray[i].job.id})" class="jt">${JobArray[i].job.name}</h3>
                <p>
                    <!--
                    <i class="fa-solid fa-building"></i>
                    <a href="https://facbook.com">Facbook.inc</a>
                    -->
                    <i class="fa-solid fa-location-dot"></i>
                    <span>${JobArray[i].job.location}</span>
                </p>
            </div>
            <a class="btn btn-main" style="text-wrap: nowrap;"  onclick="GoToApply(${JobArray[i].job.id},${JobArray[i].job.postedBy==CurrUser})" >${JobArray[i].job.postedBy==CurrUser?"View Details":"Apply Now"}</a>
        </div>
        `;
    }
}
function GoToApply(i,a){
    if(a){
         GotoDetails(i);
    }else{
         localStorage.setItem("Applyin",i);
         location.href="/Application_page"
    } 
}
function GotoDetails(index){
    localStorage.setItem("dJob",index)
    location.href="/details";
}

function incPage() {
    currentPage++;
    updatePagenator();
    displayPageNator();
}
function decPage() {
    currentPage--;
    updatePagenator();
    displayPageNator();
}

function CurrPage(index) {
    currentPage = index;
    updatePagenator();
    displayPageNator();
}

function searchJobTransfer() {
    if(document.getElementById('title-field').value){
        localStorage.setItem("title", JSON.stringify(document.getElementById('title-field').value))
    }
    if(document.getElementById('loc-field').value){
        localStorage.setItem("loc", JSON.stringify(document.getElementById('loc-field').value))
    }
    if(document.getElementById('exp-field').value){
        localStorage.setItem("exp", JSON.stringify(document.getElementById('exp-field').value))
    }

    if(document.getElementById('cat-field').value){
        localStorage.setItem("cat", JSON.stringify(document.getElementById('cat-field').value))
    }
    location.href = "/Jobs";
}

function pickCategoryTransfer(e){
    localStorage.setItem("cat", JSON.stringify(e));
    location.href = "/Jobs";
}

for (let i = 0; i < CatArray.length; i++) {
    myCareerNode.innerHTML += `
        <div class="card" onclick="pickCategoryTransfer('${CatArray[i].name}')">${CatArray[i].name}</div>
    `;
}



