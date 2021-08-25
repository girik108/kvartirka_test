import datetime
from django.core import serializers

from django.db import models
from django.contrib.auth import get_user_model

from treebeard.mp_tree import MP_Node, get_result_class

from .serializers_raw import RawCommentSerializer


User = get_user_model()


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    create_datetime = models.DateTimeField(
        'create datetime', auto_now_add=True, db_index=True)
    update_datetime = models.DateTimeField(
        'update datetime', auto_now_add=True, db_index=True)
    root_comment = models.ForeignKey(
        'Comment', blank=True, null=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        ordering = ['-create_datetime']


class Comment(MP_Node):
    post = models.ForeignKey('Post', on_delete=models.CASCADE,
                              related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    content = models.TextField()
    create_datetime = models.DateTimeField(
        'create datetime', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['create_datetime']


    @classmethod
    def get_comments_tree(cls, parent=None, keep_ids=True, custom_depth=None, authors=True):
        cls = get_result_class(cls)
        qset = cls._get_serializable_model().objects.all()

        if parent:
            qset = qset.filter(path__startswith=parent.path)

        if custom_depth:
            qset = qset.filter(depth__lte=custom_depth)

        if authors:
            qset = qset.select_related('author')

        ret, lnk = [], {}

        for pyobj in qset:
            newobj = RawCommentSerializer(pyobj).data
            path = newobj['path']
            depth = int(len(path) / cls.steplen)
            del newobj['depth']
            del newobj['path']
            del newobj['numchild']

            if not keep_ids:
                del newobj['id']

            if (not parent and depth == 1) or\
               (parent and len(path) == len(parent.path)):
                ret.append(newobj)
            else:
                parentpath = cls._get_basepath(path, depth - 1)
                parentobj = lnk[parentpath]
                if 'children' not in parentobj:
                    parentobj['children'] = []
                parentobj['children'].append(newobj)
            lnk[path] = newobj
        return ret
