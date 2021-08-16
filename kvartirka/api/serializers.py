from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'content', 'author',
                  'create_datetime', 'update_datetime')
        model = Post



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        fields = ('id', 'content', 'author', 'post',
                  'create_datetime',)
        model = Comment