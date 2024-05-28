from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, primary_key=True) 
    def __str__(self):
        return self.name
    

class Location(models.Model) : 
    name = models.CharField(max_length=100 , primary_key= True ) 
   
        
class User(models.Model) : 
    role = models.CharField(max_length=5 ,null=False)
    name = models.CharField(max_length=100  ,null=False,default="XXXXXXXXXXXXXXXx" ) 
    password = models.CharField(max_length=100  ,null=False,default="XXXXXXXXXXXXXXXx") 
    email = models.CharField(max_length=100 ,null=False,default="XXXXXXXXXXXXXXXx") 
    
class Job(models.Model) : 
    name = models.CharField(max_length=100 ) 
    salary = models.IntegerField() 
    experience = models.IntegerField() 
    company = models.CharField( max_length=100) 
    category = models.ForeignKey(Category , on_delete=models.CASCADE) 
    location = models.ForeignKey(Location , on_delete=models.CASCADE) 
    description = models.TextField( max_length=500)
    postedBy = models.ForeignKey(User , on_delete=models.CASCADE)
    postDate = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name

class Skills(models.Model):
    name=models.CharField(max_length=100)
    jobID=models.ForeignKey(Job,on_delete=models.CASCADE) 
    class Meta:
        unique_together=[['name','jobID']]

class ApplayIn(models.Model):
    userID=models.ForeignKey(User,on_delete=models.CASCADE)
    jobID=models.ForeignKey(Job,on_delete=models.CASCADE)
    class Meta:
        unique_together=[['userID','jobID']]


# Create your models here.