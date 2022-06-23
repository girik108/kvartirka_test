from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.cache import cache
from django.http import HttpResponse


from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import serializers, views, mixins, viewsets, generics
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema

from drf_yasg.utils import swagger_auto_schema

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import AccessPermission
from .tasks import send_email_notifocation, add


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a post instance.

    list:
        Return all post, ordered by desc created data.

    create:
        Create a new post.

    delete:
        Remove an existing post.

    update:
        Update a post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        author = self.request.user
        post = serializer.save(author=author)
        root_comment = Comment.add_root(
            author=author, content=f'Root comment of post {post.id}', post=post)
        post.root_comment = root_comment
        post.save()


class ThreeLayerComment(views.APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(tags=['Comments'])
    def get(self, request, post_id, comment_id):
        post = get_object_or_404(Post, pk=post_id)
        three_comment = get_object_or_404(
            Comment, pk=comment_id, depth=4)
        data = Comment.get_comments_tree(parent=three_comment)[0]

        return Response({'children': data.get('children')})


class CreateDeleteComment(mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AccessPermission]

    @swagger_auto_schema(tags=['Comments'])
    def create(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        parent_comment_id = request.data.get('parent_comment')
        if parent_comment_id and isinstance(parent_comment_id, int):
            parent_comment = get_object_or_404(Comment, pk=parent_comment_id)
            new_comment = parent_comment.add_child(
                **serializer.data, author=request.user, post=post)
        else:
            new_comment = post.root_comment.add_child(
                **serializer.data, author=request.user, post=post)
            # send_email_notifocation.delay(post_id=post.id, comment_id=new_comment.id)
            send_email_notifocation.delay(post.id, new_comment.id)

        serializer = CommentSerializer(new_comment)

        return Response(serializer.data)

    @swagger_auto_schema(tags=['Comments'])
    def list(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        result = Comment.get_comments_tree(
            parent=post.root_comment, custom_depth=4)
        result = result[0].get('children')

        return Response({'comments': result})

    @swagger_auto_schema(tags=['Comments'])
    def retrieve(self, request, post_id, pk=None):
        post = get_object_or_404(Post, pk=post_id)
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['Comments'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


def send_test_email(request):
    send_mail(
        'Subject here',
        'Here is the message.',
        'from@example.com',
        ['to@example.com'],
        fail_silently=True,
    )

    last_seen = cache.get(f'seen_{request.user.username}')

    return HttpResponse(last_seen)
