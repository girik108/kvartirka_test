from rest_framework import serializers
from rest_framework.settings import reload_api_settings

from .models import Post, Comment
from .serializers_raw import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'content', 'author',
                  'create_datetime', 'update_datetime')
        model = Post



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username', read_only=True)

    class Meta:
        fields = ('id', 'content', 'author',
                  'create_datetime')
        model = Comment