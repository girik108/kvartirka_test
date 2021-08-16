from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, views, status, viewsets, generics
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import ReadOnly


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [ReadOnly | IsAuthenticated]


class ThreeLayerComment(views.APIView):
    permission_classes = [ReadOnly | IsAuthenticated]

    def get(self, request, post_id, comment_id):
        post = get_object_or_404(Post, pk=post_id)
        three_comment = get_object_or_404(
            Comment, pk=comment_id, post=post, depth=3)
        data = Comment.get_tree(parent=three_comment)

        return Response({'childrens': data})


class CommentListView(generics.ListAPIView):
    permission_classes = [ReadOnly | IsAuthenticated]

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        result = Comment.get_comments_tree(parent=post.root_comment, custom_depth=4)
        result =result[0]['children']

        return Response({'comments': result})


class ThreeLayerComment(views.APIView):
    permission_classes = [ReadOnly | IsAuthenticated]

    def get(self, request, post_id, comment_id):
        post = get_object_or_404(Post, pk=post_id)
        three_comment = get_object_or_404(
            Comment, pk=comment_id, post=post, depth=4)
        data = Comment.get_comments_tree(parent=three_comment)[0]

        return Response({'children': data.get('children')})

