from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class BaseAbstractModel(models.Model):
    create_datetime = models.DateTimeField(
        'create datetime', auto_now_add=True, db_index=True)
    update_datetime = models.DateTimeField(
        'update datetime', auto_now_add=True, db_index=True)

    class Meta:
        abstract = True


class Post(BaseAbstractModel):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts')

    class Meta:
        ordering = ['-create_datetime']


class Comment(BaseAbstractModel):
    content = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')

    class Meta:
        ordering = ['-create_datetime']
