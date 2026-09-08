from django.contrib import admin

from .models import Post, PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'nickname', 'post_type', 'category', 'created_at']
    inlines = [PostImageInline]


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'post']