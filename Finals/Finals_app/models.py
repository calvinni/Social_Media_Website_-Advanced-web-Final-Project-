from django.db import models
from django.core.validators import validate_image_file_extension

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_online = models.BooleanField(default=False)
    last_loggin = models.DateTimeField(auto_now_add=True,
                                       blank=True, 
                                       null=True)
    gender = models.CharField(max_length=10)
    date_of_birth = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    profile_img = models.ImageField(default='default.jpg', 
                                    upload_to='profile_pics',
                                    validators=[validate_image_file_extension],
                                    blank=True, 
                                    null=True)
    
class Users_Following(models.Model):
    user_id = models.IntegerField()
    following_user_id = models.ForeignKey(Users, 
                                          on_delete=models.CASCADE, 
                                          db_constraint=False)
    started_following = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.following_user_id

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    poster_id = models.ForeignKey(Users, 
                                  on_delete=models.CASCADE, 
                                  db_constraint=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    post_img = models.ImageField(upload_to='post_imgs',
                                 validators=[validate_image_file_extension],
                                 blank=True, 
                                 null=True)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, 
                             on_delete=models.CASCADE, 
                             db_constraint=False)
    message = models.TextField()
    commenter_id = models.ForeignKey(Users, 
                                     on_delete=models.CASCADE, 
                                     db_constraint=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.post.title
    
class Likes(models.Model):
    post = models.ForeignKey(Post, 
                             on_delete=models.CASCADE, 
                             db_constraint=False)
    liker_id = models.ForeignKey(Users, 
                                 on_delete=models.CASCADE, 
                                 db_constraint=False)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.post.title

class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    
class Chat(models.Model):
    message = models.CharField(max_length=255)
    user_id = models.ForeignKey(Users, 
                                on_delete=models.CASCADE, 
                                db_constraint=False)
    room_id = models.ForeignKey(ChatRoom, 
                                on_delete=models.CASCADE, 
                                db_constraint=False)
    timestamp = models.DateTimeField(auto_now=True)
    