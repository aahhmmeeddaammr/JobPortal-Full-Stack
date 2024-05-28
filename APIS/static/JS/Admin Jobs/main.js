let curruse= JSON.parse(localStorage.getItem('user_id'));
function displayjobs(array) {
    let data=``
    for(let i=0; i<array.length; i++){
        data+=`<div class="Job">
        <div class="Dsc">
            <div>
                <h3 onclick="GotoDetails(${array[i].id})" class="jt">${array[i].name}</h3>
                <span><i class="fa-solid fa-location-dot"></i> ${array[i].location}</span>
            </div>
            <div class="button">
                <button onclick="goTOUpdate(${array[i].id})" class="btn btn-sec-main">Update Job</button>
                <button onclick="DeleteJob(${array[i].id})"  class="btn btn-main delete">Delete Job</button>
            </div>
        </div>
    </div>`;
    }   
    if(data){
        document.getElementById('jobs').innerHTML=data;    
   }else{
        document.getElementById('jobs').innerHTML=`<p style="text-align:center;  height:60vh; font-size:40px;">NO JOBS</p>`;    
   }
}

async function GetDataFromServer(){
    let ress=await fetch(`http://127.0.0.1:8000/api/PostedJobs/${curruse}`);
    let data=await ress.json();
    displayjobs(data.Jobs)
}


GetDataFromServer();

function GotoDetails(index){
     localStorage.setItem("dJob",index)
     location.href="../details/index.html";
}

async function DeleteJob(id) {
    let ress=await fetch(`http://127.0.0.1:8000/api/DeleteJob/${id}`,{
        method:"delete",
        headers:{
            'content-type': 'application/json'
        }
    })
    let data=await ress.json();
    GetDataFromServer()
}

function goTOUpdate(index){
    localStorage.setItem("update",JSON.stringify(index));
    location.href="../update/index.html"
}