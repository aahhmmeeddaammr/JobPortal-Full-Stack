
let uemail =document.getElementById('email')
let upass=document.getElementById('password')
let btn=document.getElementById('btn')
let alert=document.querySelector(".alert")
let x=false;
btn.addEventListener('click', ()=>{
    if(uemail.value && upass.value){
        loginwithServer(uemail.value,upass.value)
    }
    else{
        vaildation()
    } 
} )

function vaildation(){
    alert.style=`display:flex`
    alert.innerHTML=`<p>Incorrect E-mail or Password</p>`
}

async function loginwithServer(email,password){
    let user={
        email:email,
        password:password
    }
    let CSRFToken=document.querySelector('[name=csrfmiddlewaretoken]').value
    let res=await fetch('http://127.0.0.1:8000/api/Signin',{
        method:"POST",
        headers:{
            'content-type': 'application/json',
            'X-CSRFToken':CSRFToken
        },
        body:JSON.stringify(user)
    }).then((ress)=>ress).catch((err)=>err)
    let data = await res.json();
    if(data.MSG=='Incorrect Email or Password'){
        vaildation();
    }else{
        localStorage.setItem('user_role',JSON.stringify(data.MSG.role))
        localStorage.setItem('user_id',JSON.stringify(data.MSG.id))
        location.href="./Home/index.html"
    }
}