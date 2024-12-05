from .models import Job, User, Skills, ApplayIn, Category, Location
from rest_framework import status
from rest_framework.response import Response
from APIS.serializers import Jobserializers, Userserializers, Skillserializers, ApplayInserializers, Categoryserializers, Locationserializers
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, transaction
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
import json
import logging
# Helper function to load JSON data safely
def load_json(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None

@csrf_exempt
@require_http_methods(["GET"])
def GetCategories(request):
    categories = list(Category.objects.all().values())
    return JsonResponse({"categories": categories}, status=status.HTTP_200_OK)

@csrf_exempt
@require_http_methods(["GET"])
def GetLocations(request):
    locations = list(Location.objects.all().values())
    return JsonResponse({"locations": locations}, status=status.HTTP_200_OK)

@csrf_exempt
@require_http_methods(["POST"])
def LoginFun(request):
    data = load_json(request)
    if not data:
        return JsonResponse({"MSG": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)

    useremail = data.get('email')
    userpassword = data.get('password')

    if not useremail or not userpassword:
        return JsonResponse({"MSG": "Email and Password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=useremail)
        if check_password(userpassword, user.password):
            return JsonResponse({"MSG": "Login Successfully", "UserRole": user.role, "UserID": user.id}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"MSG": "Incorrect Password"}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return JsonResponse({"MSG": "Incorrect Email"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return JsonResponse({"MSG": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@require_http_methods(["GET"])
def GetJobs(request):
    jobs = Job.objects.all().order_by('-postDate').values()
    res = []
    for job in jobs:
        skills = list(Skills.objects.filter(jobID=job['id']).values())
        res.append({
            "job": job,
            "skills": skills
        })
    return JsonResponse({"Jobs": res}, status=status.HTTP_200_OK)

@csrf_exempt
@require_http_methods(["GET"])
def GetJob(request, ID_slug):
    try:
        job = Job.objects.get(pk=ID_slug)
        skills = list(Skills.objects.filter(jobID=ID_slug).values())
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
        return JsonResponse({"JOB": {"job": job_data, "skills": skills}}, status=status.HTTP_200_OK)
    except Job.DoesNotExist:
        return JsonResponse({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@require_http_methods(["GET"])
def postedJobs(request, ID_slug):
    jobs = list(Job.objects.filter(postedBy=ID_slug).values())
    return JsonResponse({"Jobs": jobs}, status=status.HTTP_200_OK)

@csrf_exempt
@require_http_methods(["POST"])
def SignUPFunc(request):
    data = load_json(request)
    if not data:
        return JsonResponse({"MSG": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)

    email = data.get('email')
    if not email:
        return JsonResponse({"MSG": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return JsonResponse({"MSG": "USER EXISTS"}, status=status.HTTP_409_CONFLICT)

    try:
        user = User.objects.create(
            name=data.get('name'),
            email=email,
            password=data.get('password'),  # Use Django's make_password if not using User model's default manager
            role=data.get('Role'),
        )
        return JsonResponse({"MSG": "Done"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({"MSG": f"Invalid Data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@require_http_methods(["DELETE"])
def deletejob(request, ID_slug):
    try:
        job = Job.objects.get(pk=ID_slug)
        job.delete()
        return JsonResponse({"MSG": "DONE"}, status=status.HTTP_200_OK)
    except Job.DoesNotExist:
        return JsonResponse({"MSG": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"MSG": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@require_http_methods(["POST"])
def addskill(request, skill_slug, ID_slug):
    data = {
        "name": skill_slug,
        "jobID": ID_slug
    }
    try:
        skill = Skills.objects.create(name=skill_slug, jobID=Job.objects.get(pk=ID_slug))
        return JsonResponse({"id": skill.id, "name": skill.name, "jobID": skill.jobID}, status=status.HTTP_201_CREATED)
    except Job.DoesNotExist:
        return JsonResponse({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@require_http_methods(["GET"])
def getappliedjobs(request, ID_slug):
    try:
        applied_jobs = ApplayIn.objects.filter(userID=ID_slug).select_related('jobID')
        jobs = []
        for application in applied_jobs:
            job = application.jobID
            jobs.append({
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
            })
        return JsonResponse({"JOBS": jobs}, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"MSG": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@require_http_methods(["POST"])
def APPLY(request, ID_slug, JID_slug):
    try:
        user = User.objects.get(pk=ID_slug)
        job = Job.objects.get(pk=JID_slug)

        if ApplayIn.objects.filter(userID=user, jobID=job).exists():
            return JsonResponse({"MSG": "ALREADY APPLIED"}, status=status.HTTP_400_BAD_REQUEST)

        ApplayIn.objects.create(userID=user, jobID=job)
        return JsonResponse({"MSG": "DONE"}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return JsonResponse({"MSG": "USER NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)
    except Job.DoesNotExist:
        return JsonResponse({"MSG": "JOB NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"MSG": f"ERROR: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@require_http_methods(["POST"])
def postjob(request):
    data = load_json(request)
    if not data:
        return JsonResponse({"MSG": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        newjob = Job.objects.create(
            name=data.get("name"),
            salary=data.get("salary"),
            experience=data.get("experience"),
            company=data.get("company"),
            category=Category.objects.get(pk=data.get("category")),
            location=Location.objects.get(pk=data.get("location")),
            description=data.get("description"),
            postedBy=User.objects.get(pk=data.get("postedBy")),
        )

        skills = data.get('skills', [])
        if not skills:
            return JsonResponse({"MSG": "Skills are required"}, status=status.HTTP_400_BAD_REQUEST)

        for skill_name in skills:
            Skills.objects.create(name=skill_name, jobID=newjob)

        return JsonResponse({"MSG": "DONE"}, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({"MSG": f"Related object not found: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"MSG": f"INVALID DATA: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@require_http_methods(["DELETE"])
def Deleteskill(request, skill_slug, jid_slug):
    try:
        skill = Skills.objects.get(name=skill_slug, jobID=jid_slug)
        skill.delete()
        return JsonResponse({"MSG": "DONE"}, status=status.HTTP_200_OK)
    except Skills.DoesNotExist:
        return JsonResponse({"MSG": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"MSG": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#RestFull APIs
# Setup logger
logger = logging.getLogger(__name__)

class Categories(APIView):
    def get(self, request):
        categories = Category.objects.all()
        res = Categoryserializers(categories, many=True)
        return Response({"categories": res.data}, status=status.HTTP_200_OK)

class Locations(APIView):
    def get(self, request):
        locations = Location.objects.all()
        res = Locationserializers(locations, many=True)
        return Response({"locations": res.data}, status=status.HTTP_200_OK)

class JOBS(APIView):
    def get(self, request):
        jobs = Job.objects.all().order_by('-postDate')
        res = []
        for job in jobs:
            job_serializer = Jobserializers(job)
            skills = Skills.objects.filter(jobID=job.pk)
            skill_serializer = Skillserializers(skills, many=True)
            res.append({
                "job": job_serializer.data,
                "skills": skill_serializer.data
            })
        return Response({"Jobs": res}, status=status.HTTP_200_OK)

class GETJOB(APIView):
    def get(self, request, ID_slug):
        try:
            currjob = Job.objects.get(pk=ID_slug)
            skills = Skills.objects.filter(jobID=ID_slug)
            job_serializer = Jobserializers(currjob)
            skill_serializer = Skillserializers(skills, many=True)
            res = {
                "job": job_serializer.data,
                "skills": skill_serializer.data
            }
            return Response({"JOB": res}, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            logger.warning(f"Job with ID {ID_slug} not found.")
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving job: {e}")
            return Response({"error": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostedJobs(APIView):
    def get(self, request, ID_slug):
        jobs = Job.objects.filter(postedBy=ID_slug)
        job_serializer = Jobserializers(jobs, many=True)
        return Response({"Jobs": job_serializer.data}, status=status.HTTP_200_OK)

class SignUp(APIView):
    def post(self, request):
        try:
            # Normalize email
            email = request.data.get("email", "").strip().lower()
            password = request.data.get("password", "").strip()
            name = request.data.get("name", "").strip()
            role = request.data.get("role", "").strip()

            # Validate input
            if not email or not password or not name:
                return Response({"MSG": "Email, name, and password are required."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if the user already exists
            if User.objects.filter(email=email).exists():
                return Response({"MSG": "USER EXISTS"}, status=status.HTTP_409_CONFLICT)

            # Construct data for serializer
            data = {
                "role": role,
                "name": name,
                "password": password,  
                "email": email,
            }

            serializer = Userserializers(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"MSG": "User created successfully"}, status=status.HTTP_201_CREATED)

            logger.error(f"Validation errors during sign-up: {serializer.errors}")
            return Response({"MSG": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error during sign-up: {e}")
            return Response({"MSG": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Signin(APIView):
    def post(self, request):
        try:
            # Validate input
            email = request.data.get("email", "").strip()
            password = request.data.get("password", "").strip()
            print(email)
            print(password)

            if not email or not password:
                return Response(
                    {"MSG": "Email and password are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            print("Done")
            # Retrieve user or simulate a user-like check to prevent timing attacks
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            print("Done02")
            # Perform password check
            try:
                password_valid = User.objects.get(email=email)
            except:
                return Response(
                    {"MSG": "Email Not Found"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if(password_valid.password != password): 
                return Response(
                    {"MSG": "Incorret Password"},
                    status=status.HTTP_400_BAD_REQUEST
                )       
            if password_valid:
                serializer = Userserializers(user)
                return Response(
                    {"MSG": serializer.data},
                    status=status.HTTP_200_OK
                )
            else:
                # Delay response slightly to prevent brute-force timing attacks
                check_password(password, "pbkdf2_sha256$260000$dummy$dummyhash")
                return Response(
                    {"MSG": "Incorrect email or password."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        except Exception as e:
            return Response(
                {"MSG": "An error occurred. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeleteJob(APIView):
    def delete(self, request, ID_slug):
        try:
            job = Job.objects.get(pk=ID_slug)
            job.delete()
            return Response({"MSG": "Job deleted successfully"}, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response({"MSG": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting job: {e}")
            return Response({"MSG": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddSkill(APIView):
    def post(self, request, skill_slug, ID_slug):
        data = {
            "name": skill_slug,
            "jobID": ID_slug
        }
        serializer = Skillserializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AppliedJobs(APIView):
    def get(self, request, ID_slug):
        try:
            applications = ApplayIn.objects.filter(userID=ID_slug)
            job_data = []
            for application in applications:
                job = Job.objects.get(pk=application.jobID.pk)
                job_serializer = Jobserializers(job)
                job_data.append(job_serializer.data)
            return Response({"JOBS": job_data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"MSG": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving applied jobs: {e}")
            return Response({"MSG": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Apply(APIView):
    def post(self, request, ID_slug, JID_slug):
        try:
            user = User.objects.get(pk=ID_slug)
            job = Job.objects.get(pk=JID_slug)
            apply_data = {
                "userID": ID_slug,
                "jobID": JID_slug
            }
            apply_serializer = ApplayInserializers(data=apply_data)
            if apply_serializer.is_valid():
                apply_serializer.save()
                return Response({"MSG": "Applied successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"MSG": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"MSG": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Job.DoesNotExist:
            return Response({"MSG": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error during application: {e}")
            return Response({"MSG": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Postjob(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                job_data = {
                    "name": request.data["name"],
                    "salary": request.data["salary"],
                    "experience": request.data["experience"],
                    "company": request.data["company"],
                    "category": request.data["category"],
                    "location": request.data["location"],
                    "description": request.data["description"],
                    "postedBy": request.data["postedBy"]
                }
                job_serializer = Jobserializers(data=job_data)
                if job_serializer.is_valid():
                    job = job_serializer.save()
                    skills = request.data.get('skills', [])
                    for skill_name in skills:
                        skill_data = {
                            "name": skill_name,
                            "jobID": job.pk
                        }
                        skill_serializer = Skillserializers(data=skill_data)
                        if skill_serializer.is_valid():
                            skill_serializer.save()
                        else:
                            raise IntegrityError("Invalid skill data")
                    return Response({"MSG": "Job posted successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"MSG": "Invalid job data"}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            logger.error(f"Database error during job posting: {e}")
            return Response({"MSG": "Database error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Error during job posting: {e}")
            return Response({"MSG": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Search(APIView):
    def post(self, request):
        title = request.data.get('name')
        category = request.data.get('category')
        location = request.data.get('location')
        exp = request.data.get('exp')
        filterdata = Job.objects.all()

        if title:
            filterdata = filterdata.filter(name__icontains=title)
        if category:
            filterdata = filterdata.filter(category=category)
        if location:
            filterdata = filterdata.filter(location=location)
        if exp:
            filterdata = filterdata.filter(experience__lte=exp)

        res = []
        for job in filterdata:
            job_serializer = Jobserializers(job)
            skills = Skills.objects.filter(jobID=job.pk)
            skill_serializer = Skillserializers(skills, many=True)
            res.append({
                "job": job_serializer.data,
                "skills": skill_serializer.data
            })
        return Response({"Jobs": res}, status=status.HTTP_200_OK)

class AllApply(APIView):
    def get(self, request, id_slug):
        try:
            applications = ApplayIn.objects.filter(jobID=id_slug)
            user_data = []
            for application in applications:
                user = User.objects.get(pk=application.userID.pk)
                user_serializer = Userserializers(user)
                user_data.append(user_serializer.data)
            return Response({"Users": user_data}, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response({"MSG": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving applications: {e}")
            return Response({"MSG": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RemoveApplication(APIView):
    def delete(self, request, Id_slug, jid_slug):
        try:
            application = ApplayIn.objects.filter(userID=Id_slug).get(jobID=jid_slug)
            application.delete()
            return Response({"MSG": "Application removed successfully"}, status=status.HTTP_200_OK)
        except ApplayIn.DoesNotExist:
            return Response({"MSG": "Application not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error removing application: {e}")
            return Response({"MSG": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteSkill(APIView):
    def delete(self, request, jid_slug, skill_slug):
        try:
            skill = Skills.objects.get(jobID=jid_slug, name=skill_slug)
            skill.delete()
            return Response({"MSG": "Skill deleted successfully"}, status=status.HTTP_200_OK)
        except Skills.DoesNotExist:
            return Response({"MSG": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting skill: {e}")
            return Response({"MSG": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Update(APIView):
    def put(self, request):
        try:
            job = Job.objects.get(pk=request.data['id'])
            job.name = request.data.get("name", job.name)
            job.salary = request.data.get("salary", job.salary)
            job.experience = request.data.get("experience", job.experience)
            job.company = request.data.get("company", job.company)
            job.category_id = request.data.get("category", job.category_id)
            job.location_id = request.data.get("location", job.location_id)
            job.description = request.data.get("description", job.description)
            job.save()
            return Response({"MSG": "Job updated successfully"}, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response({"MSG": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating job: {e}")
            return Response({"MSG": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)