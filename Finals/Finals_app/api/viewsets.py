from rest_framework.viewsets import ModelViewSet

from Finals_app.models import Post, Comment
from Finals_app.api.serializers import PostSerializer, CommentSerializer

class PostViewset(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewset(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
