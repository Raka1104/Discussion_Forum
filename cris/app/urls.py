from django.contrib import admin
from django.urls import path
from app import views
import urllib.parse



urlpatterns = [
    path("", views.forum, name="cris"),
    path("delete/<int:myid>/", views.delete, name="delete"),
    path("delete_reply/<int:myid>/", views.deleteReply, name="delete_reply"),
    path("delete_post/<int:myid>/", views.deletePost, name="delete_post"),
    path("edit/<int:myid>/", views.edit, name="edit"),
    path("edit_reply/<int:myid>/", views.editReply, name="edit_reply"),
    path("edit_post/<int:myid>/", views.editPost, name="edit_post"),
    path("discussion/<int:myid>/", views.discussion, name="discussion"),
    path("register/", views.userRegister, name="register"),
    path("login/", views.userLogin, name="login"),
    path("logout/", views.userLogout, name="logout"),
    path("myprofile/", views.myprofile, name="myprofile"),
    path("userprofile/<str:username>/", views.userProfile, name="userprofile"),
    path("save_post/<int:myid>/", views.savePost, name="save_post"),
    

 

]
