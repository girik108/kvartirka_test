from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content', 'create_datetime',
                    'update_datetime', 'author')
    search_fields = ('content',)
    list_filter = ('create_datetime',)
    empty_value_display = '-пусто-'


class CommentAdmin(TreeAdmin):
    form = movenodeform_factory(Comment)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)