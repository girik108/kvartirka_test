from django.contrib import admin

from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content', 'create_datetime',
                    'update_datetime', 'author')
    search_fields = ('content',)
    list_filter = ('create_datetime',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content', 'create_datetime',
                    'update_datetime', 'post', 'author')
    search_fields = ('content',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
