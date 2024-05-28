
let email = document.getElementById("mail");
let jmail = document.getElementById("jemail");
let pass = document.getElementById("pass");
let jpass = document.getElementById("jpass");
let cpass = document.getElementById("cpass");
let jcpass = document.getElementById("jcpass");
let jname = document.getElementById("name");


const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

email.addEventListener("blur", ()=> {
    if(emailRegex.test(email.value)){
        jmail.style.display = "none";
        
    } else {
        jmail.style.display = "block";
        jmail.innerHTML = `<p>Please enter a correct email.</p>`;
    }
})

pass.addEventListener("blur", ()=> {
    if(pass.value.length < 8) {
        jpass.style.display = "block";
        jpass.innerHTML = `<p>Enter a Password longer than 8 characters.</p>`
    }
    else {
        jpass.style.display = "none";
    }
})

cpass.addEventListener("blur", ()=> {
    if(cpass.value != pass.value) {
        jcpass.style.display = "block";
        jcpass.innerHTML = `<p>The passowrd is not the same.</p>`
    }
    else {
        jcpass.style.display = "none";
    }
})

let create = document.getElementById("create");

create.addEventListener("click", () => {
    let options = document.querySelector('input[name="admin"]:checked');
    if(jname.value&&pass.value&&email.value){
        SignUpWithServer(email.value,jname.value,pass.value) 
    }else{
        vaidation('ALL DATA ARE REQURIED')
    }

})

function vaidation(msg) {
    let alerts=document.querySelector(".nodata")
    alerts.style=`display:block;`
    alerts.innerHTML=`<p>${msg}</p>`;  
}

async function SignUpWithServer(email,name,password) {
    let Role='Admin'
    let user={
        Role:Role,
        email:email,
        name:name,
        password:password
    }
    let ress=await fetch('http://127.0.0.1:8000/api/Signup',{
        method:"POST",
        headers:{
            'content-type': 'application/json'
        },
        body:JSON.stringify(user)
    }).then((ress)=>ress)
    .catch((err)=>err)
    let data=await ress.json();
    if(data.MSG == 'USER IS EXIST' || data.MSG=='INVALID DATA'){
        vaidation(data.MSG)
    }else{
        location.href='../index.html'
    }
    console.log();

}


let redirect = document.getElementById("redirect");

redirect.addEventListener("click", () => {
    window.location.href = "../index.html"
})
