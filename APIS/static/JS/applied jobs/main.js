let curruse= JSON.parse(localStorage.getItem('user_id'));

async function GetDataFromServer(){
    let ress=await fetch(`http://127.0.0.1:8000/api/AppliedJobs/${+curruse}`)
    let data= await ress.json();
    console.log(data.JOBS);
    displaycontent(data.JOBS);
}

function displaycontent(arr){
    let data=''
     for(let i=0; i<arr.length; i++){
        data+=`<div class="Job">
        <div class="Dsc">
            <div>
                <h3 class="jt" onclick="GotoDetails(${arr[i].id})">${arr[i].name}</h3>
                <p ><i class="fa-solid fa-location-dot"></i>
                <span>${arr[i].location}</span></p>
            </div>
            <div class="button">
                <button onclick="DeleteJob(${arr[i].id})" class="btn btn-main">Delete Applection</button>
            </div>
        </div>
    </div>`;
      }
      if(data.length){
          document.getElementById('jobs').innerHTML=data;    
     }else{
          document.getElementById('jobs').innerHTML=`<p style="text-align:center;  height:60vh; font-size:40px;">NO JOBS</p>`;    
     }
}

async function DeleteJob(index){
    let ress = await fetch(`http://127.0.0.1:8000/api/RemoveApplication/${curruse}/${index}`)
    let data=await ress.json()
    console.log(data);
    GetDataFromServer()
}

function GotoDetails(index){
    localStorage.setItem("dJob",index)
    location.href="../details/index.html";
}

GetDataFromServer()