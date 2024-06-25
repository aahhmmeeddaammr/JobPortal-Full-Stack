from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns =[
    path('',views.JOBS.as_view(),name="aaaa"),
    path('Categories',views.Categories.as_view(),name="Categories"),
    path('Locations',views.Locations.as_view(),name="Locations"),
    path('Signup',views.signUp.as_view(),name="signUp"),
    path('Signin',views.Signin.as_view(),name="Signin"),
    path('DeleteJob/<slug:ID_slug>',views.DeleteJob.as_view(),name="DeleteJob"),
    path('details/<slug:ID_slug>',views.GETJOB.as_view(),name="details"),
    path('AddSkill/<slug:skill_slug>/<slug:ID_slug>',views.AddSkill.as_view(),name="AddSkill"),
    path('PostedJobs/<slug:ID_slug>',views.PostedJobs.as_view(),name="PostedJobs"),
    path('AppliedJobs/<slug:ID_slug>',views.AppliedJobs.as_view(),name="AppliedJobs"),
    path('Apply/<slug:ID_slug>/<slug:JID_slug>',views.Apply.as_view(),name="Apply"),
    path('RemoveApplication/<slug:Id_slug>/<slug:jid_slug>',views.RemoveApplication.as_view(),name="RemoveApplication"),
    path('DeleteSkill/<slug:jid_slug>/<slug:skill_slug>',views.DeleteSkill.as_view(),name="DeleteSkill"),
    path('AllApply/<slug:id_slug>',views.AllApply.as_view(),name="AllApply"),
    path('Search',views.Search.as_view(),name="Search"),    
    path('Postjob',views.Postjob.as_view(),name="Postjob"),
    path('Update',views.Update.as_view(),name="Update"),
    # FUNCTION
    path('GetCategories',views.GetCategories,name="GetCategories"),
    path('LoginFun',views.LoginFun,name="LoginFun"),
    path('SignUPFunc',views.SignUPFunc,name="SignUPFunc"),
    path('GetJobs',views.GetJobs,name="GetJobs"),
    path('GetJob/<slug:ID_slug>',views.GetJob,name="GetJob"),
    path('Location',views.GetLocations,name="Locations"),
]