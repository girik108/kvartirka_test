from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated
from rest_framework import views, status, viewsets
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import ReadOnly


User = get_user_model()


class StatusOkView(views.APIView):
    permission_classes = [ReadOnly | IsAuthenticated]

    def get(self, request):
        query = request.GET.get('query')

        return Response({'status': 'OK'}, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [ReadOnly | IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [ReadOnly | IsAuthenticated]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        queryset = Comment.objects.filter(post=post)
        return queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
        return serializer
