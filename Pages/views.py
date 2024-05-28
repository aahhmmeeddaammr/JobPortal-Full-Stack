from django.shortcuts import render

def index(request):
   return render(request,"Home/index.html")

def signin(request):
   return render(request,"index.html")

def About(request):
   return render(request,"About_page/about.html")

def update(request):
   return render(request,"update/index.html")

def signupuser(request):
   return render(request,"SignUpUser/index.html")

def signupadmin(request):
   return render(request,"SignUpAdmin/index.html")

def postjob(request):
   return render(request,"Postjob/index.html")

def Jobs(request):
   return render(request,"jobs/index.html")

def details(request):
   return render(request,"details/index.html")

def contact(request):
   return render(request,"Contact/contact.html")

def appliedjobs(request):
   return render(request,"Applied jobs/index.html")

def apply(request):
   return render(request,"Application_page/Apply.html")

def Adminjobs(request):
   return render(request,"Admin jobs/index.html")

def ChooseRole(request):
   return render(request,'ChooseRole/index.html')

def Applyed(request):
   return render(request,'APPLAY/index.html')
# Create your views here.
