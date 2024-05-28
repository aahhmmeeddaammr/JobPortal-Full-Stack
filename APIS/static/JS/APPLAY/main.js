async function GetAllusersfromServer(){
    console.log(111111111111);
    let currjob=localStorage.getItem('Ajob')
    let ress=await fetch(`http://127.0.0.1:8000/api/AllApply/${currjob}`)
    let data=await ress.json();
    // console.log(data.Users);
    displayusers(data.Users)
}

function displayusers(array){
    let data=``;
    for (let i = 0; i < array.length; i++) {
        // console.log(array[i]);
       data+=`
            <div class="user">
            <div class="Name">
                <p id="uname" class="jt">${array[i].name}</p>
            </div>
            <button class="btn-sec-main btn">Accept</button>
        </div>
        
       ` 
    }
    let cont=document.getElementById('users');
    cont.innerHTML=data;
}
GetAllusersfromServer();