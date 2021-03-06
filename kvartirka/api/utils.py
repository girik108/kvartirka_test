from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings


from api.serializers import CommentSerializer
from api.models import Comment, Post


def test(node):
    if node.get_children_count() == 0:
        return CommentSerializer(node).data


def new_comment_notification(post_id, comment_id, *args, **kwargs):
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
