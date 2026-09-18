from django.contrib import admin

from .models import AiAnalysis, Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at")
    list_filter = ("category",)
    search_fields = ("title", "content")


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at")
    list_filter = ("post",)
    search_fields = ("author", "body")


@admin.register(AiAnalysis)
class AiAnalysisAdmin(admin.ModelAdmin):
    list_display = ("post", "score", "created_at")
    list_filter = ("post",)
    search_fields = ("post__title", "summary")