let Jobtitle=document.getElementById("Jobtitle");
let currentjob=JSON.parse(localStorage.getItem("Applyin"))
let currentuser=JSON.parse(localStorage.getItem("user_id"))

document.getElementById('submitButton').addEventListener('click', function(event) {
    event.preventDefault();
    let nameInput = document.getElementById('name');
    let emailInput = document.getElementById('email');
    let salary = document.getElementById('salary_expectations');
    let candidate= document.getElementById('candidate_qualities');
    let intersts = document.getElementById('company_interest');
    let resume = document.getElementById('resume');

  if (nameInput.value.trim() === '') {
      nameInput.style.borderColor = 'red';
  }else{
      nameInput.style.borderColor = '';
  }

  if (emailInput.value.trim() === '') {
      emailInput.style.borderColor = 'red';
  }else{
      emailInput.style.borderColor = '';
  }

  let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(emailInput.value.trim())) {
      emailInput.style.borderColor = 'red';
  }else{
      emailInput.style.borderColor = '';
  }

  if (salary.value.trim() === '') {
      salary.style.borderColor = 'red';
  }else{
      salary.style.borderColor = '';
  }

  if (candidate.value.trim() === '') {
      candidate.style.borderColor = 'red';
  }else{
      candidate.style.borderColor = '';
  }

  if (intersts.value.trim() === '') {
      intersts.style.borderColor = 'red';
  }else{
      intersts.style.borderColor = '';
  }

  function validate_fileupload(input_element)
  {
      let fileName = input_element.value;
      let allowed_extensions = new Array("pdf","doc","docx");
      let file_extension = fileName.split('.').pop(); 
      for(let i = 0; i < allowed_extensions.length; i++)
      {
          if(allowed_extensions[i]==file_extension)
          {
              return true;
          }
      }
      return false;
  }
  

  if(!validate_fileupload(resume)){
      resume.style.color='red';
  }else{
      resume.style.color = '';
  }

  if(candidate.value.trim() === ''||salary.value.trim() === ''||!emailRegex.test(emailInput.value.trim())||!validate_fileupload(resume)||intersts.value.trim() === ''||emailInput.value.trim() === ''||emailInput.value.trim() === ''||nameInput.value.trim() === ''){
      return;
  }else{
        ApplyWithServer(currentuser ,currentjob)
  }
}); 

'Apply'
async function ApplyWithServer(userid,jobid){
    let res=await fetch(`http://127.0.0.1:8000/api/Apply/${userid}/${jobid}`,{
        method:"POST",
        headers:{
            'content-type': 'application/json'
        }
    }).then(()=>{
        location.href="../applied jobs/index.html"
        
    })

} 


