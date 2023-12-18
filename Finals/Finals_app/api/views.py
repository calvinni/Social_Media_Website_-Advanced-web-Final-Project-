from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.template import loader
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from Finals_app.api.serializers import *

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from Finals_app.api.utils.constants import PostStatus
from Finals_app.models import *

from datetime import datetime, timedelta
import time
import pytz
import json

@method_decorator(name='get', decorator=swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'post_slug', openapi.IN_QUERY,
            description=("A unique string value identifying requested post"),
            type=openapi.TYPE_STRING,
            enum=[ps.value for ps in PostStatus],
            required=True
        ),
    ]
))
class PingView(APIView):
    def get(self, *args, **kwargs):
        return Response({'ping': 'pong'}, status=status.HTTP_200_OK)
    
class UsersView(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSeralizer
    
class FollowersView(viewsets.ModelViewSet):
    queryset = Users_Following.objects.all()
    serializer_class = FollowSeralizer
    
class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
class LikesView(viewsets.ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    
class ChatRoomView(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    
class ChatView(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    
def index(request):
    if 'member_id' in request.session: #Check if user is logged in
        session_id = request.session['member_id']
        postdata = Post.objects.all().select_related()
        
        paginator = Paginator(postdata, 3)
        page_number = request.GET.get('page')
        page_posts = paginator.get_page(page_number)
        
        comments = Comment.objects.values('post_id').order_by().annotate(totalcomments=Count('post_id'))
        check_comment = Comment.objects.values_list('post_id', flat=True)
        likes = Likes.objects.values('post_id').order_by().annotate(totallikes=Count('post_id'))
        check_like = Likes.objects.values_list('post_id', flat=True)
        check_liked = Likes.objects.filter(liker_id_id=session_id).values_list('post_id', flat=True)
        template = loader.get_template('index.html')
        context = {
            'page_posts': page_posts,
            'comments': comments,
            'check_comment': check_comment,
            'likes': likes,
            'check_like': check_like,
            'check_liked': check_liked,
        }
        return HttpResponse(template.render(context, request))
    else:
        postdata = Post.objects.all().select_related()
        
        paginator = Paginator(postdata, 3)
        page_number = request.GET.get('page')
        page_posts = paginator.get_page(page_number)
        
        comments = Comment.objects.values('post_id').order_by().annotate(totalcomments=Count('post_id'))
        check_comment = Comment.objects.values_list('post_id', flat=True)
        likes = Likes.objects.values('post_id').order_by().annotate(totallikes=Count('post_id'))
        check_like = Likes.objects.values_list('post_id', flat=True)
        template = loader.get_template('index.html')
        context = {
            'page_posts': page_posts,
            'comments': comments,
            'check_comment': check_comment,
            'likes': likes,
            'check_like': check_like,
        }
        return HttpResponse(template.render(context, request))
    
def myposts(request, username=None):
    if 'member_id' in request.session: #Check if user is logged in
        session_id = request.session['member_id']
        postdata = Post.objects.filter(poster_id_id=session_id).select_related()
        
        paginator = Paginator(postdata, 3)
        page_number = request.GET.get('page')
        page_posts = paginator.get_page(page_number)
        
        check_postdata = Post.objects.filter(poster_id_id=session_id).select_related().count()
        comments = Comment.objects.values('post_id').order_by().annotate(totalcomments=Count('post_id'))
        check_comment = Comment.objects.values_list('post_id', flat=True)
        likes = Likes.objects.values('post_id').order_by().annotate(totallikes=Count('post_id'))
        check_like = Likes.objects.values_list('post_id', flat=True)
        check_liked = Likes.objects.filter(liker_id_id=session_id).values_list('post_id', flat=True)
        template = loader.get_template('myposts.html')
        context = {
            'page_posts': page_posts,
            'comments': comments,
            'check_comment': check_comment,
            'likes': likes,
            'check_like': check_like,
            'check_liked': check_liked,
            'check_postdata': check_postdata,
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.error(request, 'session timed out, Please login')
        return HttpResponseRedirect(reverse('index'))

def register(request):
    return render(request, 'register.html')

def add_register(request):
    if request.method == "POST":
        U = request.POST['username']
        P = request.POST['password']
        CP = request.POST['confpw']
        G = request.POST['gender']
        DOP = request.POST['dateofbirth']
        S = request.POST['status']
        if 'profile_picture' in request.FILES:
            picture = request.FILES['profile_picture']
            extension = picture.name.split('.')[-1]
            if not extension or extension.lower() not in settings.WHITELISTED_IMAGE_TYPES.keys():
                messages.error(request, 'unrecognised file type, please use jpeg, jpg or png')
                return HttpResponseRedirect(reverse('register'))
            else:
                DP = picture
        else:
            DP = 'default.jpg'
        Userinfo = Users.objects.exclude(username=U).values()
        check_DOB = datetime.strptime(DOP, "%Y-%m-%d")
        DB_UN = Userinfo.values_list('username', flat=True)
        if CP != P: #Check the password and confirm password is the same
            messages.error(request, 'Password and Confirm Password does not match, Please try again.')
            return HttpResponseRedirect(reverse('register'))
        elif check_DOB > datetime.now():
            messages.error(request, 'Date of birth must be before today!')
            return HttpResponseRedirect(reverse('register'))
        elif U in DB_UN:
            messages.error(request, 'There is already an existing account, Please try a different username.')
            return HttpResponseRedirect(reverse('register'))
        else:
            hashedP = make_password(P)
            insertData = Users(username=U, 
                               password=hashedP,
                               gender=G,
                               date_of_birth=DOP,
                               status=S,
                               profile_img=DP)
            insertData.save()
            member = Users.objects.get(username=U)
            request.session['member_id'] = member.id
            request.session['member_name'] = member.username
            request.session['member_img'] = member.profile_img.url
            request.session['session_time_expiry'] = time.time() + 259200 # 3 days
            messages.success(request, 'account created')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('register'))

def Login(request):
    return render(request, 'login.html')

def check_login(request):
    if request.method == "POST":
        U = request.POST['username']
        P = request.POST['password']
        user = Users.objects.filter(username=U).count()
        if user == 1:
            member = Users.objects.get(username=U)
            checkP = check_password(P, member.password)
            date_expired = datetime.now() - timedelta(days=3)
            utc=pytz.UTC
            past_expiry = utc.localize(date_expired) 
            if member.is_online == True and member.last_loggin > past_expiry:
                messages.error(request, 'user is logged in on another device')
                return HttpResponseRedirect(reverse('login'))
            elif checkP == True:
                Users.objects.filter(username=U).update(is_online=True)
                Users.objects.filter(username=U).update(last_loggin=datetime.now())
                request.session['member_id'] = member.id
                request.session['member_name'] = member.username
                request.session['member_img'] = member.profile_img.url
                request.session['session_time_expiry'] = time.time() + 259200 # 3 days
                messages.success(request, f"Successfully logged in")
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.error(request, 'Invalid credential, Please try again')
                return HttpResponseRedirect(reverse('login'))
        else:
            messages.error(request, 'Invalid credential, Please try again')
            return HttpResponseRedirect(reverse('login'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('login'))

def Logout(request):
    if 'member_id' in request.session: #Check if user is logged in
        try:
            Users.objects.filter(id=request.session['member_id']).update(is_online=False)
            del request.session['member_id']
            request.session.clear_expired()
            return HttpResponseRedirect(reverse('index'))
        except KeyError:
            messages.error(request, 'Something went wrong try again')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'session timed out, Please login')
        return HttpResponseRedirect(reverse('index'))
    
def search(request):
    if 'member_id' in request.session: #Check if user is logged in
        current_user = request.GET['current_user']
        Searching = request.GET['searching']
        searchdata = Users.objects.filter(username__icontains=Searching).exclude(username=current_user)
        searchdata_count = Users.objects.filter(username__icontains=Searching).exclude(username=current_user).count()
    else:
        Searching = request.GET['searching']
        searchdata = Users.objects.filter(username__icontains=Searching)
        searchdata_count = Users.objects.filter(username__icontains=Searching).count()
    
    paginator = Paginator(searchdata, 3)
    page_number = request.GET.get('page')
    page_searches = paginator.get_page(page_number)
    
    if searchdata_count > 0:
        template = loader.get_template('search.html')
        context = {
            'page_searches': page_searches,
            'Searching': Searching,
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.error(request, 'There are no such user')
        return render(request, 'search.html')
    
def profile(request, username=None):
    if 'member_id' in request.session: #Check if user is logged in
        User = username
        session_id = request.session['member_id']
        Userinfo = Users.objects.filter(username=User).values()
        Userid = Userinfo.values_list('id', flat=True)[0]
        followed = Users_Following.objects.filter(user_id=session_id).filter(following_user_id=Userid).count()
        following = Users_Following.objects.filter(user_id=Userid).count()
        followers = Users_Following.objects.filter(following_user_id=Userid).count()
        following_list = Users_Following.objects.filter(user_id=session_id).select_related()
        
        paginator = Paginator(following_list, 3)
        page_number = request.GET.get('page')
        page_following = paginator.get_page(page_number)
        
        template = loader.get_template('profile.html')
        context = {
            'Userinfo': Userinfo,
            'followed': followed,
            'following': following,
            'followers': followers,
            'page_following': page_following,
        }
        return HttpResponse(template.render(context, request))
    else:
        User = username
        Userinfo = Users.objects.filter(username=User).values()
        Userid = Userinfo.values_list('id', flat=True)[0]
        following = Users_Following.objects.filter(user_id=Userid).count()
        followers = Users_Following.objects.filter(following_user_id=Userid).count()
        template = loader.get_template('profile.html')
        context = {
            'Userinfo': Userinfo,
            'following': following,
            'followers': followers,
        }
        return HttpResponse(template.render(context, request))

def following(request, username=None):
    if request.method == "POST":
        if 'member_id' in request.session: #Check if user is logged in
            userid = request.POST['userID']
            Followid = request.POST['followID']
            username = request.POST['profile_user']
            Users_Following.objects.create(user_id=userid,
                                           following_user_id_id=Followid)
            url = reverse('profile', kwargs={'username': username})
            return HttpResponseRedirect(url)
        else:
            messages.error(request, 'session timed out, Please login')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('index'))

def unfollow(request, username=None):
    if request.method == "POST":
        if 'member_id' in request.session: #Check if user is logged in
            userid = request.POST['userID']
            Followid = request.POST['followID']
            username = request.POST['profile_user']
            Users_Following.objects.filter(user_id=userid).filter(following_user_id=Followid).delete()
            url = reverse('profile', kwargs={'username': username})
            return HttpResponseRedirect(url)
        else:
            messages.error(request, 'session timed out, Please login')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('index'))

def edit_profile(request, username=None):
    if request.method == "POST":
        if 'member_id' in request.session: #Check if user is logged in
            User = username
            Userinfo = Users.objects.filter(username=User).values()
            
            template = loader.get_template('edit_profile.html')
            context = {
                'Userinfo': Userinfo,
            }
            return HttpResponse(template.render(context, request))
        else:
            messages.error(request, 'session timed out, Please login')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('index'))

def update_profile(request, username=None):
    if request.method == "POST":
        if 'member_id' in request.session: #Check if user is logged in
            CU = request.POST['current_user']
            ID = request.POST['userID']
            U = request.POST['username']
            P = request.POST['password']
            CP = request.POST['confpw']
            G = request.POST['gender']
            DOP = request.POST['dateofbirth']
            S = request.POST['status']
            if 'profile_picture' in request.FILES:
                picture = request.FILES['profile_picture']
                extension = picture.name.split('.')[-1]
                if not extension or extension.lower() not in settings.WHITELISTED_IMAGE_TYPES.keys():
                    messages.error(request, 'unrecognised file type, please use jpeg, jpg or png')
                    url = reverse('profile', kwargs={'username': CU})
                    return HttpResponseRedirect(url)
                else:
                    DP = picture
            else:
                DP = 'default.jpg'
            Userinfo = Users.objects.exclude(username=U).values()
            DB_UN = Userinfo.values_list('username', flat=True)
            if CP != P: #Check the password and confirm password is the same
                # print("passwords wrong")
                messages.error(request, 'Password and Confirm Password does not match, Please try again.')
                url = reverse('edit_profile', kwargs={'username': U})
                return HttpResponseRedirect(url)
            elif U in DB_UN:
                # print("User alr exsist")
                messages.error(request, 'There is already an existing account, Please try a different username.')
                url = reverse('edit_profile', kwargs={'username': U})
                return HttpResponseRedirect(url)
            else:
                hashedP = make_password(P)
                old_PP = Users.objects.get(id=ID).profile_img
                if old_PP != "default.jpg":
                    old_PP.delete(save=False)
                Users.objects.filter(id=ID).update(username=U, 
                                                password=hashedP,
                                                gender=G,
                                                date_of_birth=DOP,
                                                status=S,
                                                profile_img=DP,
                                                date_updated=datetime.now())
                if DP:
                    pic = Users.objects.all().filter(id=ID)[0]
                    pic.profile_img = DP
                    pic.save()
                request.session['member_img'] = pic.profile_img.url
                messages.success(request, 'Profile updated!')
                url = reverse('profile', kwargs={'username': U})
                return HttpResponseRedirect(url)
        else:
            messages.error(request, 'session timed out, Please login')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('index'))
    
def del_profile(request, username=None):
    if request.method == "POST":
        if 'member_id' in request.session: #Check if user is logged in
            ID = request.POST['userID']
            delete_PP = Users.objects.get(id=ID).profile_img
            if delete_PP != "default.jpg":
                delete_PP.delete(save=False)
            Users.objects.filter(id=ID).delete()
            Post.objects.filter(poster_id_id=ID).delete()
            Likes.objects.filter(liker_id_id=ID).delete()
            Comment.objects.filter(commenter_id_id=ID).delete()
            Users_Following.objects.filter(user_id=ID).delete()
            Users_Following.objects.filter(following_user_id=ID).delete()
            del request.session['member_id']
            request.session.clear_expired()
            messages.success(request, 'account deleted')
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'session timed out, Please login')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('index'))
    
def post(request, username=None):
    if 'member_id' in request.session: #Check if user is logged in
        User = username
        Userinfo = Users.objects.filter(username=User).values()
        
        template = loader.get_template('post.html')
        context = {
            'Userinfo': Userinfo,
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.error(request, 'session timed out, Please login')
        return HttpResponseRedirect(reverse('index'))
    
def posting(request, username=None):
    if request.method == "POST":
        if 'member_id' in request.session: #Check if user is logged in
            ID = request.POST['userID']
            U = request.POST['username']
            T = request.POST['title']
            D = request.POST['description']
            if 'post_picture' in request.FILES:
                picture = request.FILES['post_picture']
                extension = picture.name.split('.')[-1]
                if not extension or extension.lower() not in settings.WHITELISTED_IMAGE_TYPES.keys():
                    messages.error(request, 'unrecognised file type, please use jpeg, jpg or png')
                    url = reverse('post', kwargs={'username': U})
                    return HttpResponseRedirect(url)
                else:
                    PP = picture
            else:
                PP = ''
            insertData = Post(title=T, 
                              description=D, 
                              poster_id_id=ID,
                              post_img=PP)
            insertData.save()
            messages.success(request, 'Post have been submitted')
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'session timed out, Please login')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('index'))
    
def edit_post(request, username=None):
    if request.method == "POST":
        if 'member_id' in request.session: #Check if user is logged in
            post_id = request.POST['postID']
            Postinfo = Post.objects.filter(id=post_id).select_related()
            template = loader.get_template('edit_post.html')
            context = {
                'Postinfo': Postinfo,
            }
            return HttpResponse(template.render(context, request))
        else:
            messages.error(request, 'session timed out, Please login')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('index'))
    
def update_post(request, username=None):
    if request.method == "POST":
        if 'member_id' in request.session: #Check if user is logged in
            user = request.POST['post_user']
            P_ID = request.POST['postID']
            T = request.POST['title']
            D = request.POST['description']
            if 'post_picture' in request.FILES:
                picture = request.FILES['post_picture']
                extension = picture.name.split('.')[-1]
                if not extension or extension.lower() not in settings.WHITELISTED_IMAGE_TYPES.keys():
                    messages.error(request, 'unrecognised file type, please use jpeg, jpg or png')
                    url = reverse('myposts', kwargs={'username': user})
                    return HttpResponseRedirect(url)
                else:
                    PP = picture
            else:
                PP = ''
            old_PP = Post.objects.get(id=P_ID).post_img
            old_PP.delete(save=False)
            Post.objects.filter(id=P_ID).update(title=T, 
                                                description=D,
                                                post_img=PP,
                                                updated_at=datetime.now())
            if PP:
                pic = Post.objects.all().filter(id=P_ID)[0]
                pic.post_img = PP
                pic.save()
            messages.success(request, 'Post have been edited')
            url = reverse('myposts', kwargs={'username': user})
            return HttpResponseRedirect(url)
        else:
            messages.error(request, 'session timed out, Please login')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('index'))
    
def del_post(request, username=None):
    if request.method == "POST":
        if 'member_id' in request.session: #Check if user is logged in
            ID = request.POST['userID']
            P_ID = request.POST['postID']
            delete_PP = Post.objects.get(id=P_ID).post_img
            delete_PP.delete(save=False)
            Post.objects.filter(id=P_ID).delete()
            Likes.objects.filter(post_id=P_ID).delete()
            Comment.objects.filter(post_id=P_ID).delete()
            messages.success(request, 'post deleted')
            url = reverse('myposts', kwargs={'username': ID})
            return HttpResponseRedirect(url)
        else:
            messages.error(request, 'session timed out, Please login')
            return HttpResponseRedirect(reverse('index'))    
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('index'))
    
def comment(request, id=None):
    if 'member_id' in request.session: #Check if user is logged in
        post_id = id
        session_id = request.session['member_id']
        post_data = Post.objects.filter(id=post_id).select_related()
        likes = Likes.objects.values('post_id').order_by().annotate(totallikes=Count('post_id'))
        check_like = Likes.objects.values_list('post_id', flat=True)
        check_liked = Likes.objects.filter(liker_id_id=session_id).values_list('post_id', flat=True)
        comment = Comment.objects.values('post_id').order_by().annotate(totalcomments=Count('post_id'))
        comments = Comment.objects.filter(post_id=post_id).select_related()
        check_comment = Comment.objects.values_list('post_id', flat=True)
        template = loader.get_template('post_comment.html')
        context = {
            'post_data': post_data,
            'comment': comment,
            'comments': comments,
            'likes': likes,
            'check_like': check_like,
            'check_liked': check_liked,
            'check_comment': check_comment,
        }
        return HttpResponse(template.render(context, request))
    else:
        post_id = id
        post_data = Post.objects.filter(id=post_id).select_related()
        likes = Likes.objects.values('post_id').order_by().annotate(totallikes=Count('post_id'))
        check_like = Likes.objects.values_list('post_id', flat=True)
        comment = Comment.objects.values('post_id').order_by().annotate(totalcomments=Count('post_id'))
        comments = Comment.objects.filter(post_id=post_id).select_related()
        check_comment = Comment.objects.values_list('post_id', flat=True)
        template = loader.get_template('post_comment.html')
        context = {
            'post_data': post_data,
            'comment': comment,
            'comments': comments,
            'likes': likes,
            'check_like': check_like,
            'check_comment': check_comment,
        }
        return HttpResponse(template.render(context, request))

def commenting(request, id=None):
    if request.method == "POST":
        if 'member_id' in request.session: #Check if user is logged in
            P_ID = request.POST['postID']
            U_ID = request.POST['userID']
            M = request.POST['message']
            Comment.objects.create(message=M, 
                                   commenter_id_id=U_ID, 
                                   post_id=P_ID)
            messages.success(request, 'Comment have been posted')
            url = reverse('comment', kwargs={'id': P_ID})
            return HttpResponseRedirect(url)
        else:
            messages.error(request, 'session timed out, Please login')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('index'))
    
def like(request):
    if request.method == "POST":
        if 'member_id' in request.session: #Check if user is logged in
            userid = request.POST['userID']
            post = request.POST['postID']
            Likes.objects.create(liker_id_id=userid,
                                 post_id=post)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, 'session timed out, Please login')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('index'))

def dislike(request):
    if request.method == "POST":
        if 'member_id' in request.session: #Check if user is logged in
            userid = request.POST['userID']
            post = request.POST['postID']
            Likes.objects.filter(liker_id_id=userid).filter(post_id=post).delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, 'session timed out, Please login')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('index'))
    
def chat(request):
    if 'member_id' in request.session: #Check if user is logged in
        return render(request, 'chat/chat.html')
    else:
        messages.error(request, 'session timed out, Please login')
        return HttpResponseRedirect(reverse('index'))

def room(request, room_name):
    if 'member_id' in request.session: #Check if user is logged in
        room = ChatRoom.objects.filter(name=room_name).first()
        chats = []
        if room:
            chats = Chat.objects.filter(room_id=room)
        else:
            room = ChatRoom(name=room_name)
            room.save()
        roomid = ChatRoom.objects.get(name=room_name).id
        template = loader.get_template('chat/room.html')
        context = {
            'room_name': room_name,
            'roomid': roomid,
            'chats': chats,
        }
        return HttpResponse(template.render(context, request))    
    else:
        messages.error(request, 'session timed out, Please login')
        return HttpResponseRedirect(reverse('index'))