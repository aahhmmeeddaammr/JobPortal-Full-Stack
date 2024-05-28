let OurJobs=document.getElementById("OurJobs");
let SearchByCat = document.getElementById("SearchByCat"); 
let SearchByName=document.getElementById("SearchByName");
let SearchByLocation = document.getElementById("SearchByLocation")
let SearchByYearsOfExp=document.getElementById("SearchByYearsOfExp");
let CurrUser=+localStorage.getItem('user_id')
let Searchfromhomelocation=""
let SearchfromhomeJobtitle=""
let Searchfromhomecat=""
let Searchfromhomeexp=1000000000;
let data=[]; 


search()
async function SearchFromServeer(name,cat,exp,location) {
     let CSRFToken=document.querySelector('[name=csrfmiddlewaretoken]').value
     let searchprams={
          name:name,
          category:cat,
          location:location,
          exp: exp,
     }
     console.log(searchprams);
     let ress =await fetch('http://127.0.0.1:8000/api/Search',{
          method:"POST",
          headers:{
               'content-type': 'application/json',
               'X-CSRFToken':CSRFToken
          },
          body:JSON.stringify(searchprams)
     });
     let data=await ress.json();    
     console.log(data);
     let  JobArray=[...data.Jobs]
     displayJobs(JobArray)
     console.log(CSRFToken);
}

function getdataFromLocalStorage(){
     if(localStorage.getItem("loc")){
          Searchfromhomelocation=JSON.parse(localStorage.getItem("loc"));
     }else{
          Searchfromhomelocation="";
     }
     if(localStorage.getItem("title")){
          
          SearchfromhomeJobtitle=JSON.parse(localStorage.getItem("title"));
     }else{
          SearchfromhomeJobtitle="";
     }
     if(localStorage.getItem("cat")){
         Searchfromhomecat=JSON.parse(localStorage.getItem("cat"));
     }else{
          Searchfromhomecat="";
     }
     if(localStorage.getItem("exp")){
          Searchfromhomeexp=+JSON.parse(localStorage.getItem("exp"));
     }else{
          Searchfromhomeexp="";
     }
}

function search(){
     getdataFromLocalStorage()
     SearchFromServeer(SearchfromhomeJobtitle,Searchfromhomecat,Searchfromhomeexp,Searchfromhomelocation);
     localStorage.removeItem("title")
     localStorage.removeItem("exp")
     localStorage.removeItem("loc")
     localStorage.removeItem("cat")
}


SearchByName.addEventListener("blur",()=>{
     if(SearchByName.value){
          localStorage.setItem("title",JSON.stringify(SearchByName.value))
     }else{
          if(localStorage.getItem('title')){
               localStorage.removeItem("title")
          }
     }
})

SearchByYearsOfExp.addEventListener("blur",()=>{
     if(SearchByYearsOfExp.value){
          localStorage.setItem("exp",JSON.stringify(SearchByYearsOfExp.value))
     }else{
          if(localStorage.getItem('exp')){
               localStorage.removeItem("exp")
          }
     }
})

SearchByLocation.addEventListener("blur",()=>{
     if(SearchByLocation.value){
          localStorage.setItem("loc",JSON.stringify(SearchByLocation.value))
     }else{
          if(localStorage.getItem('loc')){
               localStorage.removeItem("loc")
          }
     }
})

SearchByCat.addEventListener("blur",()=>{
     if(SearchByCat.value){
          localStorage.setItem("cat",JSON.stringify(SearchByCat.value))
     }else{
          if(localStorage.getItem('cat')){
               localStorage.removeItem("cat")
          }
     }
})

function displayJobs(Jobs){
     let data=``;
     if(Jobs.length==0){
          data=`<p class="Nodata">Not Found Jobs.</p>`
     }else{
          for(let i=0;i<Jobs.length;i++){
               data+=`
               <div class="job">
                    <div class="desc">
                         <h3 class="title"  onclick="GotoDetails(${Jobs[i].job.id})"><a  id="title" >${Jobs[i].job.name}</a></h3>
                         <div class="loc">
                              <i class="fa-solid fa-location-dot"></i>
                              <span>${Jobs[i].job.location}</span>
                         </div>
                    </div>
                    <a class="btn btn-main" style="text-wrap: nowrap;"  onclick="GoToApply(${Jobs[i].job.id},${Jobs[i].job.postedBy==CurrUser})" >${Jobs[i].job.postedBy==CurrUser?"View Details":"Apply Now"}</a>
               </div>
               `
          }
     }
     OurJobs.innerHTML=data;
}

function GoToApply(i,a){
     if(a){
          GotoDetails(i);
     }else{
          localStorage.setItem("Applyin",i);
          location.href="../Application_page/Apply.html"
     } 
}

function GotoDetails(index){
     localStorage.setItem("dJob",index)
     location.href="../details/index.html";
}