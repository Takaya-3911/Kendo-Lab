from rest_framework import serializers

from .models import Comment, Post, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image']


class CommentSerializer(serializers.ModelSerializer):
    level_display = serializers.CharField(source="get_level_display", read_only=True)
    video_time_seconds = serializers.IntegerField(
        required=False, allow_null=True, min_value=0
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'comment',
            'nickname',
            'level',
            'level_display',
            'video_time_seconds',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'post_type',
            'video',
            'category',
            'experience_period',
            'title',
            'nickname',
            'memo',
            'created_at',
            'images',
        ]
        read_only_fields = ['id', 'created_at']