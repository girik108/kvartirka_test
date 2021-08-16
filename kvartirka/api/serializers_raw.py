from rest_framework import serializers

from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['first_name', 'last_name', 'username', 'email', 'id']
        model = User


class RawCommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = UserSerializer(read_only=True)
    content = serializers.CharField()
    create_datetime = serializers.DateTimeField()
    path = serializers.CharField()
    depth = serializers.IntegerField()
    numchild = serializers.IntegerField()
