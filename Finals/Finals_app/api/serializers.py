from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from Finals_app.models import *

class UsersSeralizer(serializers.HyperlinkedModelSerializer): 
    class Meta:
        model = Users
        fields = (
            'id',
            'username', 
            'password',
            'is_online',
            'gender',
            'date_of_birth',
            'status',
            'date_created',
            'date_updated',
            'profile_img')
        
class FollowSeralizer(serializers.HyperlinkedModelSerializer): 
    following_user_id = UsersSeralizer()
    class Meta:
        model = Users_Following
        fields = ('user_id',
                  'following_user_id',
                  'started_following')
        
class PostSerializer(serializers.ModelSerializer):
    poster_id = UsersSeralizer()
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'updated_at',
            'poster_id',
        ]
        
class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    commenter_id = UsersSeralizer()
    class Meta:
        model = Comment
        fields = [
            'id',
            'message',
            'created_at',
            'updated_at',
            'post',
            'commenter_id',
        ]
        
class LikesSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    liker_id = UsersSeralizer()
    class Meta:
        model = Likes
        fields = [
            'id',
            'post',
            'liker_id',
            'created_at',
        ]
        
class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = [
            'id',
            'name',
        ]
        
class ChatSerializer(serializers.ModelSerializer):
    user_id = UsersSeralizer()
    room_id = ChatRoomSerializer()
    class Meta:
        model = Chat
        fields = [
            'id',
            'message',
            'user_id',
            'room_id',
            'timestamp',
        ]