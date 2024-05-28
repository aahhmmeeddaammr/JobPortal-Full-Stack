# from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.signin,name="signin"),
    path('home',views.index,name="HOME"),
    path('About',views.About,name="About"),
    path('update',views.update,name="update"),
    path('signupuser',views.signupuser,name="signupuser"),
    path('signupadmin',views.signupadmin,name="signupadmin"),
    path('postjob',views.postjob,name="postjob"),
    path('Jobs',views.Jobs,name="Jobs"),
    path('details',views.details,name="details"),
    path('contact',views.contact,name="contact"),
    path('appliedjobs',views.appliedjobs,name="appliedjobs"),
    path('apply',views.apply,name="apply"),
    path('Adminjobs',views.Adminjobs,name="Adminjobs"),
    path('ChooseRole',views.ChooseRole,name="ChooseRole"),
    path('Applyed',views.Applyed,name="Applyed"),
]