let alert=document.querySelector(".alert");
let message=document.getElementById("message");
let btn=document.getElementById("btn");
var Role;
function admin(){
     Role="admin"
}
function user(){
     Role="user"
}
function GoToSignUp(){
     if(Role){
          alert.classList.value="alert"
          alert.style=`
          display:flex; `
          if(Role=="user"){
               message.innerText="Hello New User";
               setTimeout(()=>{
                    location.href="../SignUpUser/index.html"
               },1000)
          }else{
               message.innerText="Hello New Admin";
               setTimeout(()=>{
                    location.href="../SignUpAdmin/index.html"
               },1000)
          }
     }else{
          message.innerText="Choose Role";
          alert.classList.value="alert-w"
          alert.style=`
               display:flex; 
          `
     }
}