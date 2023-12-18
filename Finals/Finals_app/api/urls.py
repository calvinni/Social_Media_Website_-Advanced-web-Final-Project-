from django.urls import path, include
from rest_framework.routers import SimpleRouter

from Finals_app.api import viewsets, views

routers = SimpleRouter()
routers.register(r'users', views.UsersView)
routers.register(r'followers', views.FollowersView)
routers.register(r'posts', views.PostView)
routers.register(r'comments', views.CommentView)
routers.register(r'likes', views.LikesView)
routers.register(r'chatroom', views.ChatRoomView)
routers.register(r'chat', views.ChatView)


urlpatterns = [
    path('ping/', views.PingView.as_view(), name='ping'),
] + routers.get_urls()
