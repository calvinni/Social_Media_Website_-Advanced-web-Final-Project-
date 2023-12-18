import datetime
from django.test import TestCase
from .models import *
from django.contrib.auth.hashers import make_password, check_password

# Create your tests here.
class UserInsertTest(TestCase):
    def setUp(self):
        hashedP = make_password('TESTPASSWORD')
        self.testusers = Users.objects.create(username = 'Test0001', 
                                            password = hashedP,
                                            gender = 'None',
                                            date_of_birth = '2010-02-11',
                                            status = 'Test user')
        
        self.testdata = Users.objects.get(username = 'Test0001')
        self.good_url = '/api/users/'
        self.bad_url = '/api/users/bad/'
    
    def tearDown(self):
        Users.objects.all().delete()    
    
    def test_usersReturn(self): #Test connection with users
        response = self.client.get(self.good_url, format = 'json')
        self.assertEqual(response.status_code, 200)
        
    def test_FailusersReturn(self): #Test connection with users, suppose to fail
        response = self.client.get(self.bad_url, format = 'json')
        self.assertEqual(response.status_code, 404)
        
    def test_usersInsert(self): #Test if data is inserted properly in users
        # Users data
        self.assertEqual(self.testdata.username, 'Test0001')
        PassCheck = check_password('TESTPASSWORD', self.testdata.password)
        self.assertEqual(PassCheck, True)
        self.assertEqual(self.testdata.gender, 'None')
        DOB = datetime.date(2010, 2, 11)
        self.assertEqual(self.testdata.date_of_birth, DOB)
        self.assertEqual(self.testdata.status, 'Test user')
        self.assertEqual(self.testdata.date_created, datetime.date.today())
        self.assertEqual(self.testdata.profile_img, 'default.jpg')
        
################################################################################################
        
class Users_FollowingTest(TestCase):
    def setUp(self):
        hashedP = make_password('TESTPASSWORD')
        self.testusers = Users.objects.create(username = 'Test0002', 
                                              password = hashedP,
                                              gender = 'None',
                                              date_of_birth = '2010-02-11',
                                              status = 'Test user2')
        
        self.testfollow = Users_Following.objects.create(user_id = '0002', 
                                                         following_user_id = self.testusers)
        
        self.testdata = Users_Following.objects.get(user_id = '0002')
        self.good_url = '/api/followers/'
        self.bad_url = '/api/followers/bad/'
    
    def tearDown(self):
        Users_Following.objects.all().delete()  
    
    def test_Users_FollowingReturn(self): #Test connection with Users_Following
        response = self.client.get(self.good_url, format = 'json')
        self.assertEqual(response.status_code, 200)
        
    def test_FailUsers_FollowingReturn(self): #Test connection with Users_Following, suppose to fail
        response = self.client.get(self.bad_url, format = 'json')
        self.assertEqual(response.status_code, 404)
    
    def test_Users_FollowingInsert(self): #Test if data is inserted properly in Users_Following
        # Users_Following data
        self.assertEqual(self.testdata.user_id, 2)
        # following_user_id data
        self.assertEqual(self.testdata.following_user_id.username, 'Test0002')
        PassCheck = check_password('TESTPASSWORD', self.testdata.following_user_id.password)
        self.assertEqual(PassCheck, True)
        self.assertEqual(self.testdata.following_user_id.gender, 'None')
        DOB = datetime.date(2010, 2, 11)
        self.assertEqual(self.testdata.following_user_id.date_of_birth, DOB)
        self.assertEqual(self.testdata.following_user_id.status, 'Test user2')
        
################################################################################################
        
class PostTest(TestCase):
    def setUp(self):
        hashedP = make_password('TESTPASSWORD')
        self.testusers = Users.objects.create(username = 'Test0003', 
                                              password = hashedP,
                                              gender = 'None',
                                              date_of_birth = '2010-02-11',
                                              status = 'Test user3')
        
        self.testpost = Post.objects.create(title = 'test_title3', 
                                            description = 'test_description3',
                                            poster_id = self.testusers)
        
        self.testdata = Post.objects.get(title = 'test_title3')
        self.good_url = '/api/posts/'
        self.bad_url = '/api/posts/bad/'
    
    def tearDown(self):
        Post.objects.all().delete()  
    
    def test_postReturn(self): #Test connection with Post
        response = self.client.get(self.good_url, format = 'json')
        self.assertEqual(response.status_code, 200)
        
    def test_FailpostReturn(self): #Test connection with Post, suppose to fail
        response = self.client.get(self.bad_url, format = 'json')
        self.assertEqual(response.status_code, 404)
    
    def test_postInsert(self): #Test if data is inserted properly in Post
        # Post data
        self.assertEqual(self.testdata.title, 'test_title3')
        self.assertEqual(self.testdata.description, 'test_description3')
        self.assertEqual(self.testdata.post_img, '')
        # Post poster_id data
        self.assertEqual(self.testdata.poster_id.username, 'Test0003')
        PassCheck = check_password('TESTPASSWORD', self.testdata.poster_id.password)
        self.assertEqual(PassCheck, True)
        self.assertEqual(self.testdata.poster_id.gender, 'None')
        DOB = datetime.date(2010, 2, 11)
        self.assertEqual(self.testdata.poster_id.date_of_birth, DOB)
        self.assertEqual(self.testdata.poster_id.status, 'Test user3')
        self.assertEqual(self.testdata.poster_id.date_created, datetime.date.today())
        
################################################################################################
        
class CommentTest(TestCase):
    def setUp(self):
        hashedP = make_password('TESTPASSWORD')
        self.testusers = Users.objects.create(username = 'Test0004', 
                                              password = hashedP,
                                              gender = 'None',
                                              date_of_birth = '2010-02-11',
                                              status = 'Test user4')
        
        self.testpost = Post.objects.create(title = 'test_title4', 
                                            description = 'test_description4',
                                            poster_id = self.testusers)
        
        self.testcomment = Comment.objects.create(post = self.testpost, 
                                                  message = 'test_message4',
                                                  commenter_id = self.testusers)
        
        self.testdata = Comment.objects.get(message = 'test_message4')
        self.good_url = '/api/posts/'
        self.bad_url = '/api/posts/bad/'
    
    def tearDown(self):
        Comment.objects.all().delete()  
    
    def test_commentReturn(self): #Test connection with Comment
        response = self.client.get(self.good_url, format = 'json')
        self.assertEqual(response.status_code, 200)
        
    def test_FailcommentReturn(self): #Test connection with Comment, suppose to fail
        response = self.client.get(self.bad_url, format = 'json')
        self.assertEqual(response.status_code, 404)
    
    def test_commentInsert(self): #Test if data is inserted properly in Comment
        # post data
        self.assertEqual(self.testdata.post.title, 'test_title4')
        self.assertEqual(self.testdata.post.description, 'test_description4')
        # post poster_id data
        self.assertEqual(self.testdata.post.poster_id.username, 'Test0004')
        PassCheck = check_password('TESTPASSWORD', self.testdata.commenter_id.password)
        self.assertEqual(PassCheck, True)
        self.assertEqual(self.testdata.post.poster_id.gender, 'None')
        DOB = datetime.date(2010, 2, 11)
        self.assertEqual(self.testdata.post.poster_id.date_of_birth, DOB)
        self.assertEqual(self.testdata.post.poster_id.status, 'Test user4')
        self.assertEqual(self.testdata.post.poster_id.date_created, datetime.date.today())
        self.assertEqual(self.testdata.post.post_img, '')
        # message data
        self.assertEqual(self.testdata.message, 'test_message4')
        # commenter_id data
        self.assertEqual(self.testdata.commenter_id.username, 'Test0004')
        PassCheck = check_password('TESTPASSWORD', self.testdata.commenter_id.password)
        self.assertEqual(PassCheck, True)
        self.assertEqual(self.testdata.commenter_id.gender, 'None')
        DOB = datetime.date(2010, 2, 11)
        self.assertEqual(self.testdata.commenter_id.date_of_birth, DOB)
        self.assertEqual(self.testdata.commenter_id.status, 'Test user4')
        self.assertEqual(self.testdata.commenter_id.date_created, datetime.date.today())
        
################################################################################################
        
class LikesTest(TestCase):
    def setUp(self):
        hashedP = make_password('TESTPASSWORD')
        self.testusers = Users.objects.create(username = 'Test0005', 
                                              password = hashedP,
                                              gender = 'None',
                                              date_of_birth = '2010-02-11',
                                              status = 'Test user5')
        
        self.testpost = Post.objects.create(title = 'test_title5', 
                                            description = 'test_description5',
                                            poster_id = self.testusers)
        
        self.testcomment = Likes.objects.create(id = -1,
                                                post = self.testpost, 
                                                liker_id = self.testusers)
        
        self.testdata = Likes.objects.get(id = -1)
        self.good_url = '/api/likes/'
        self.bad_url = '/api/likes/bad/'
    
    def tearDown(self):
        Likes.objects.all().delete()  
    
    def test_likesReturn(self): #Test connection with Likes
        response = self.client.get(self.good_url, format = 'json')
        self.assertEqual(response.status_code, 200)
        
    def test_FaillikesReturn(self): #Test connection with Likes, suppose to fail
        response = self.client.get(self.bad_url, format = 'json')
        self.assertEqual(response.status_code, 404)
    
    def test_likesInsert(self): #Test if data is inserted properly in Likes
        # post data
        self.assertEqual(self.testdata.post.title, 'test_title5')
        self.assertEqual(self.testdata.post.description, 'test_description5')
        # post poster_id data
        self.assertEqual(self.testdata.post.poster_id.username, 'Test0005')
        PassCheck = check_password('TESTPASSWORD', self.testdata.post.poster_id.password)
        self.assertEqual(PassCheck, True)
        self.assertEqual(self.testdata.post.poster_id.gender, 'None')
        DOB = datetime.date(2010, 2, 11)
        self.assertEqual(self.testdata.post.poster_id.date_of_birth, DOB)
        self.assertEqual(self.testdata.post.poster_id.status, 'Test user5')
        self.assertEqual(self.testdata.post.poster_id.date_created, datetime.date.today())
        self.assertEqual(self.testdata.post.post_img, '')
        # Likes data
        self.assertEqual(self.testdata.id, -1)
        # liker_id data
        self.assertEqual(self.testdata.liker_id.username, 'Test0005')
        PassCheck = check_password('TESTPASSWORD', self.testdata.liker_id.password)
        self.assertEqual(PassCheck, True)
        self.assertEqual(self.testdata.liker_id.gender, 'None')
        DOB = datetime.date(2010, 2, 11)
        self.assertEqual(self.testdata.liker_id.date_of_birth, DOB)
        self.assertEqual(self.testdata.liker_id.status, 'Test user5')
        self.assertEqual(self.testdata.liker_id.date_created, datetime.date.today())
        
################################################################################################
        
class ChatRoomTest(TestCase):
    def setUp(self):
        self.testchatroom = ChatRoom.objects.create(id = -1,
                                                   name = 'TestRoom6')
        
        self.testdata = ChatRoom.objects.get(id = -1)
        self.good_url = '/api/chatroom/'
        self.bad_url = '/api/chatroom/bad/'
    
    def tearDown(self):
        ChatRoom.objects.all().delete()  
    
    def test_chatroomReturn(self): #Test connection with ChatRoom
        response = self.client.get(self.good_url, format = 'json')
        self.assertEqual(response.status_code, 200)
        
    def test_FailchatroomReturn(self): #Test connection with ChatRoom, suppose to fail
        response = self.client.get(self.bad_url, format = 'json')
        self.assertEqual(response.status_code, 404)
    
    def test_chatroomInsert(self): #Test if data is inserted properly in ChatRoom
        # ChatRoom data
        self.assertEqual(self.testdata.id, -1)
        self.assertEqual(self.testdata.name, 'TestRoom6')
        
################################################################################################
        
class ChatTest(TestCase):
    def setUp(self):
        hashedP = make_password('TESTPASSWORD')
        self.testusers = Users.objects.create(username = 'Test0007', 
                                              password = hashedP,
                                              gender = 'None',
                                              date_of_birth = '2010-02-11',
                                              status = 'Test user7')
        
        self.testchatroom = ChatRoom.objects.create(id = -1,
                                                    name = 'TestRoom7')
        
        self.testcomment = Chat.objects.create(id = -1,
                                               message = 'Test_message7',
                                               user_id = self.testusers, 
                                               room_id = self.testchatroom)
        
        self.testdata = Chat.objects.get(id = -1)
        self.good_url = '/api/chat/'
        self.bad_url = '/api/chat/bad/'
    
    def tearDown(self):
        Chat.objects.all().delete()  
    
    def test_likesReturn(self): #Test connection with Likes
        response = self.client.get(self.good_url, format = 'json')
        self.assertEqual(response.status_code, 200)
        
    def test_FaillikesReturn(self): #Test connection with Likes, suppose to fail
        response = self.client.get(self.bad_url, format = 'json')
        self.assertEqual(response.status_code, 404)
    
    def test_likesInsert(self): #Test if data is inserted properly in Likes
        # Chat data
        self.assertEqual(self.testdata.id, -1)
        self.assertEqual(self.testdata.message, 'Test_message7')
        # user_id data
        self.assertEqual(self.testdata.user_id.username, 'Test0007')
        PassCheck = check_password('TESTPASSWORD', self.testdata.user_id.password)
        self.assertEqual(PassCheck, True)
        self.assertEqual(self.testdata.user_id.gender, 'None')
        DOB = datetime.date(2010, 2, 11)
        self.assertEqual(self.testdata.user_id.date_of_birth, DOB)
        self.assertEqual(self.testdata.user_id.status, 'Test user7')
        self.assertEqual(self.testdata.user_id.date_created, datetime.date.today())
        # room_id data
        self.assertEqual(self.testdata.room_id.id, -1)
        self.assertEqual(self.testdata.room_id.name, 'TestRoom7')
        

