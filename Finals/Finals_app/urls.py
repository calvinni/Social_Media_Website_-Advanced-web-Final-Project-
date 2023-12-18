from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .models import *
from rest_framework.routers import SimpleRouter
from rest_framework import routers

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from Finals_app.api import viewsets, views

routers = routers.DefaultRouter()
routers.register(r'users', views.UsersView)
routers.register(r'followers', views.FollowersView)
routers.register(r'posts', views.PostView)
routers.register(r'comments', views.CommentView)
routers.register(r'likes', views.LikesView)
routers.register(r'chatroom', views.ChatRoomView)
routers.register(r'chat', views.ChatView)

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Posts API",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True
)

urlpatterns = [
    #For the restframework
    path('admin/', admin.site.urls),
    path('api/', include(routers.urls)),
    #For the webpage
    path('', views.index, name='index'),
    path('myposts/<str:username>/', views.myposts, name='myposts'),
    #For register
    path('register/', views.register, name='register'),
    path('register/addregister/', views.add_register, name='add_register'),
    #For login
    path('login/', views.Login, name='login'),
    path('login/checklogin/', views.check_login, name='check_login'),
    #For logout
    path('logout/', views.Logout, name='logout'),
    #For search
    path('search/', views.search, name='search'),
    #For user following and unfollow
    path('follow/', views.following, name='following'),
    path('unfollow/', views.unfollow, name='unfollow'),
    #For profile view, edit, update and delete
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit/<str:username>/', views.edit_profile, name='edit_profile'),
    path('edit/<str:username>/updateprofile/', views.update_profile, name='update_profile'),
    path('edit/<str:username>/deleteprofile/', views.del_profile, name='del_profile'),
    #For post form, upload, edit, update and delete
    path('post/<str:username>/', views.post, name='post'),
    path('post/<str:username>/uploadpost/', views.posting, name='posting'),
    path('editpost/<str:username>/', views.edit_post, name='edit_post'),
    path('editpost/<str:username>/updatepost/', views.update_post, name='update_post'),
    path('editpost/<str:username>/deletepost/', views.del_post, name='del_post'),
    #For comment view and upload
    path('comment/<str:id>/', views.comment, name='comment'),
    path('comment/<str:id>/commenting', views.commenting, name='commenting'),
    #For post likes and dislikes
    path('like/', views.like, name='like'),
    path('dislike/', views.dislike, name='dislike'),
    #For the chat rooms
    path('chat/', views.chat, name='chat'),
    path('chat/<str:room_name>/', views.room, name='room'),
    
    #For the swagger api
    path('finalapp/', include(('Finals_app.api.urls', 'Finals_app'), namespace='Finals_app')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
]