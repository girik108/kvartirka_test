from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task

from .utils import new_comment_notification
from api.models import Comment, Post


@shared_task
def send_email_notifocation(post_id, comment_id):
    '''Send new comments notification'''
    post = Post.objects.select_related(
        'author', 'root_comment').get(id=post_id)
    comment = Comment.objects.select_related('author').get(id=comment_id)

    if not post.author.is_online:
        send_mail(
            'Your post is commented',
            f'Hey, you got a new comment from user: @{comment.author.username} : {comment.content}',
            settings.EMAIL_INFORMER,
            [post.author.email, ],
            fail_silently=False,
        )
        return 'OK'
    return 'TASK END'


@shared_task
def add(x, y):
    return x + y