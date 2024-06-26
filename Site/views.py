from .models import Job,User,Skills,ApplayIn,Category,Location
from rest_framework import status
from rest_framework.response import Response
from APIS.serializers import Jobserializers,Userserializers,Skillserializers,ApplayInserializers,Categoryserializers,Locationserializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse

import json

#JSON Response
def GetCategories(request): #done
    categories = Category.objects.all().values()
    categories_list = list(categories)
    return JsonResponse({"categories": categories_list})

def GetLocations(Locations):
    Locations = Location.objects.all().values()
    Locations_res = list(Locations)
    return JsonResponse({"categories": Locations_res})

def LoginFun(request): #done 
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            useremail = data['email']
            userpassword = data['password']
            # Assuming you have a User model with email and password fields
            data = User.objects.get( email = useremail , password = userpassword)
            return JsonResponse({"MSG": "Login Succefuly" , "UserRole":data.role , "UserID":data.id } , status=200)
        except User.DoesNotExist:
            return JsonResponse({"MSG": "Incorrect Email or Password"}, status=400)
        except Exception as e:
            return JsonResponse({"MSG": str(e)}, status=500)
    return JsonResponse({"MSG": "Invalid request method"}, status=405)

def GetJobs( request):
        jobs=list(Job.objects.all().order_by('-postDate').values())
        res=[]
        for i in jobs:
            skill=list(Skills.objects.filter(jobID = i['id'] ).values())
            res.append({
                "job":i ,
                "skills":skill
            })
        return JsonResponse({"Jobs":res},status=200)

def GetJob (request , ID_slug):
    try:
        currjob = Job.objects.get(pk=ID_slug)
        skills = list(Skills.objects.filter(jobID=ID_slug).values())
        job_data = {
            "id": currjob.id,
            "name": currjob.name,
            "salary": currjob.salary,
            "experience": currjob.experience,
            "company": currjob.company,
            "category": currjob.category.name,
            "location": currjob.location.name,
            "postedBy": currjob.postedBy.id,
            "postDate": currjob.postDate,
            "description": currjob.description,
            
        }
        res = {
            "job": job_data,
            "skills": skills
        }
        
        return JsonResponse({"JOB": res}, status=status.HTTP_200_OK)
    except Job.DoesNotExist:
        return JsonResponse({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def SignUPFunc (request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"MSG": "USER EXISTS"}, status=status.HTTP_409_CONFLICT)
            
            user = User.objects.create(
                name=data['name'],
                email=data['email'],
                password=data['password'],
                role=data['role'],
            )

            # If you have additional fields in your User model, set them here
            # e.g., user.profile.role = data['Role']
            # user.save()

            return JsonResponse({"MSG": "Done"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({"MSG": f"Invalid Data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    
    return JsonResponse({"MSG": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

def postedJobs( request,ID_slug):
    users=list(Job.objects.filter(postedBy=ID_slug).values())
    return JsonResponse({"Jobs":users},status=status.HTTP_200_OK)


def deletejob(request,ID_slug):
        data=Job.objects.get(pk=ID_slug)
        data.delete()
        return JsonResponse({"MSG":"DONEE"},status=status.HTTP_200_OK)

def addskill(request,skill_slug,ID_slug):
        if request.method == 'POST':
            data = {
                "name": skill_slug,
                "jobID": ID_slug
            }
            skill = Skill(name=data['name'], jobID=data['jobID'])
            
            try:
                skill.save()
                response_data = {
                    "id": skill.id,  # Assuming id is an auto field
                    "name": skill.name,
                    "jobID": skill.jobID
                }
                return JsonResponse(response_data, status=200)
            except Exception as e:
                response_data = {
                    "error": str(e)
                }
                return JsonResponse(response_data, status=400)
        return JsonResponse({"error": "Invalid request method"}, status=405)
def getappliedjobs( request,ID_slug):
        user=ApplayIn.objects.filter(userID=ID_slug).values()
        users=list(user)
        jobs=[]
        
        for i in user:
            job=Job.objects.get(pk=i['jobID_id'])
            job_data = {
            "id": job.id,
            "name": job.name,
            "salary": job.salary,
            "experience": job.experience,
            "company": job.company,
            "category": job.category.name,
            "location": job.location.name,
            "postedBy": job.postedBy.id,
            "postDate": job.postDate,
            "description": job.description,

        }
            jobs.append( job_data)
        return JsonResponse({
            "JOBS":jobs
        },status=status.HTTP_200_OK)

def APPLY(request,ID_slug,JID_slug):
    try:
        user = User.objects.get(pk=ID_slug)
        job = Job.objects.get(pk=JID_slug)

        if ApplayIn.objects.filter(userID=user, jobID=job).exists():
            return JsonResponse({"MSG": "ALREADY APPLIED"}, status=status.HTTP_400_BAD_REQUEST)
        
        applayIn = ApplayIn(userID=user, jobID=job)
        applayIn.save()

        return JsonResponse({"MSG": "DONE"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return JsonResponse({"MSG": "USER NOT FOUND"}, status=status.HTTP_400_BAD_REQUEST)
    except Job.DoesNotExist:
        return JsonResponse({"MSG": "JOB NOT FOUND"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"MSG": f"ERROR: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def postjob(request):
        try:
            print(data.get("description"))
            newjob={
                "name":data.get("name"),
                "salary":data.get("salary"),
                "experience":data.get("experience"),
                "company":data.get("company"),
                "category":data.get("category"),
                "location":data.get("location"),
                "description":data.get("description"),
                "postedBy":data.get("postedBy"),
            }
            newjob.save()

        skills = data.getlist('skills')  # Assuming 'skills' is a list in the request
        if not skills:
            return JsonResponse({"MSG": "Skills are required"}, status=400)

        for skill_name in skills:
            Skill.objects.create(
                name=skill_name,
                jobID=newjob
            )

        return JsonResponse({"MSG": "DONE"}, status=200)

    except Exception as e:
        return JsonResponse({"MSG": f"INVALID DATA: {str(e)}"}, status=400)
#RestFull APIs
class Categories(APIView):
    def get(self,request):
        categories=Category.objects.all()
        res=Categoryserializers(categories,many=True)
        return Response({"categories":res.data},status=status.HTTP_200_OK)

class Locations(APIView):
    def get(self,request):
        categories=Location.objects.all()
        res=Locationserializers(categories,many=True)
        return Response({"categories":res.data},status=status.HTTP_200_OK)

class JOBS(APIView):
    def get(self, request):
        jobs=list(Job.objects.all().order_by('-postDate'))
        res=[]
        for i in jobs:
            serializers=Jobserializers( i , many = False) # JSON 
            skill=list(Skills.objects.filter(jobID=i.pk)) # 1 => 1 []
            Sserializers=Skillserializers(skill,many=True) 
            res.append({
                "job":serializers.data ,
                "skills":Sserializers.data
            })
        return Response({"Jobs":res},status=status.HTTP_200_OK)
   
class GETJOB(APIView):
    def get(self, request,ID_slug):
        currjob=Job.objects.get(pk=ID_slug)
        skills=Skills.objects.filter(jobID=ID_slug)
        serializers=Jobserializers(currjob,many=False)
        Sserializers=Skillserializers(skills,many=True)
        res={
            "job":serializers.data,
            "skills":Sserializers.data
        }
        return Response({"JOB":res},status=status.HTTP_200_OK)
    
class PostedJobs(APIView):
     def get(self, request,ID_slug):
        users=list(Job.objects.filter(postedBy=ID_slug))
        serializers=Jobserializers(users,many=True)
        return Response({"Jobs":serializers.data},status=status.HTTP_200_OK)

class signUp(APIView):
    def post(self, request):
        
        try:
            user=User.objects.get(email=request.data['email'])
            res={
                "MSG":"USER IS EXIST"
            }
            return Response(res,status=status.HTTP_409_CONFLICT)   
        except:
            try:
                print(request.data['name'])
                data={
                        "role":request.data['Role'],
                        "name":request.data['name'],
                        "password":request.data['password'],
                        "email":request.data['email']
                    }
            except:
                     return Response(status=status.HTTP_400_BAD_REQUEST) 
            serializers=Userserializers(data=data)
            if serializers.is_valid():
                serializers.save()
                return Response({"MSG":serializers.data},status=status.HTTP_200_OK)
            return Response({"MSG":"INVALID DATA"},status=status.HTTP_400_BAD_REQUEST)   
    
class Signin(APIView):
    def post(self, request):
        try:
            useremail=request.data["email"]
            userpassword=request.data["password"]
            data=User.objects.filter(password=userpassword).get(email=useremail)
            serializers=Userserializers(data,many=False)
            return Response({"MSG":serializers.data},status=status.HTTP_200_OK)
        except:
            return Response({"MSG":"Incorrect Email or Password"},status=status.HTTP_401_UNAUTHORIZED)

class DeleteJob(APIView):
    def delete(self,request,ID_slug):
        data=Job.objects.get(pk=ID_slug)
        data.delete()
        serializers=Jobserializers(data,many=False)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
class AddSkill(APIView):
    def post(self,request,skill_slug,ID_slug):
        data={
            "name":skill_slug,
            "jobID":ID_slug
        }
        serializers=Skillserializers(data=data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_200_OK)
        return Response(serializers.data,status=status.HTTP_400_BAD_REQUEST)   
    
class AppliedJobs(APIView):
     def get(self, request,ID_slug):
        user=ApplayIn.objects.filter(userID=ID_slug)
        serializers=ApplayInserializers(user,many=True)
        user=serializers.data
        jobs=[]
        for i in user:
            job=Job.objects.get(pk=i['jobID'])
            jserializers=Jobserializers(job,many=False)
            jobs.append(jserializers.data)
        return Response({
            "JOBS":jobs
        },status=status.HTTP_200_OK)

class Apply(APIView):
     def post(self, request,ID_slug,JID_slug):
        try:
            user=User.objects.get(pk=ID_slug)
            job=Job.objects.get(pk=JID_slug)
            aplly={
                "userID":ID_slug,
                "jobID":JID_slug
            }
            applayInserializers=ApplayInserializers(data=aplly)
            if applayInserializers.is_valid():
                applayInserializers.save()
                return Response({"MSG":"DONE"},status=status.HTTP_200_OK)
            else:
                return Response({"MSG":"INVALID DATA"},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"MSG":"USER OR JOB IS NOT FOUND"},status=status.HTTP_400_BAD_REQUEST)

class Postjob(APIView):
    def post(self,request):
        try:
            print(request.data["description"])
            newjob={
                "name":request.data["name"],
                "salary":request.data["salary"],
                "experience":request.data["experience"],
                "company":request.data["company"],
                "category":request.data["category"],
                "location":request.data["location"],
                "description":request.data["description"],
                "postedBy":request.data["postedBy"],
            }
            skills=request.data['skills']
            # print(newjob)
            serializers=Jobserializers(data=newjob)
            if serializers.is_valid():
                serializers.save()
                currjob=Job.objects.all().order_by('-postDate')
                # print(currjob[0].pk)
                for i in skills:
                    data={
                        "name":i,
                        "jobID":currjob[0].pk
                    }
                    sserializers=Skillserializers(data=data)
                    if sserializers.is_valid():
                        sserializers.save()
                return Response({"MSG":"DONE"},status=status.HTTP_200_OK)
            else:
                return Response({"MSG":"ERRRRRRoRRRRRRRRRRRRRRRR"},status=status.HTTP_412_PRECONDITION_FAILED)
        except:
            return Response({"MSG":"INVALID DATA"},status=status.HTTP_400_BAD_REQUEST)
       
class Search(APIView):
    def post(self,request):
        title=request.data['name']
        category=request.data['category']
        location=request.data['location']
        exp=request.data['exp']
        filterdata=Job.objects.all()
        if(title):
            filterdata=filterdata.filter(name__contains=title)
        if(category):
            filterdata=filterdata.filter(category__exact=category)
        if(location):
            filterdata=filterdata.filter(location__exact=location)
        if(exp!=''):
            filterdata=filterdata.filter(experience__lte=exp)
        # serializers=Jobserializers(filterdata,many=True)
        res=[]
        for i in filterdata:
            serializers=Jobserializers(i,many=False)
            skill=list(Skills.objects.filter(jobID=i.pk))
            Sserializers=Skillserializers(skill,many=True)
            res.append({
                "job":serializers.data,
                "skills":Sserializers.data
            })
        return Response({"Jobs":res},status=status.HTTP_200_OK)

class AllApply(APIView):
    def get(self,request,id_slug):
        users=list(ApplayIn.objects.filter(jobID=id_slug))
        serializers=ApplayInserializers(users,many=True)
        # print(serializers.data)
        users=list(serializers.data)
        res=[]
        for i in users:
            # Userializers=ApplayInserializers(i,many=False)
            user=User.objects.get(pk=i['userID'])
            Userializers=Userserializers(user,many=False)
            res.append(Userializers.data)
        return Response({"Users":res},status=status.HTTP_200_OK)

class RemoveApplication(APIView):
    def get(self,request,Id_slug,jid_slug):
        apin=ApplayIn.objects.filter(userID=Id_slug).get(jobID=jid_slug)
        apin.delete()
        return Response({"DATA":"DONE"},status=status.HTTP_200_OK)

class DeleteSkill(APIView):
    def delete(self,request,jid_slug,skill_slug):
        skill=Skills.objects.get(jobID=jid_slug,name=skill_slug)
        skill.delete()
        return Response({"MSG":"DONE"},status=status.HTTP_200_OK)

class Update(APIView):  
    def put(self,request):
        try:
            job=Job.objects.get(pk=request.data['id'])
            location=Location.objects.get(pk=request.data['location'])
            category=Category.objects.get(pk=request.data['category'])
            job.name=request.data["name"]
            job.salary=request.data["salary"]
            job.experience=request.data["experience"]
            job.company=request.data["company"]
            job.category=category
            job.location=location
            job.description=request.data["description"]
            job.save()
            return Response({"MSG":"DONE"},status=status.HTTP_200_OK)
        except:
            return Response({"MSG":"INVALID DATA"},status=status.HTTP_400_BAD_REQUEST)


# Create your views here.