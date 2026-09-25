from django.contrib import admin

from .models import Comment, Post, PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'nickname', 'post_type', 'category', 'created_at']
    inlines = [PostImageInline, CommentInline]


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'post']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'nickname', 'level', 'created_at']
    list_filter = ['level', 'post']
    search_fields = ['comment', 'nickname']